"""
FarmersDesk Ltd – Desktop Application  v3
Tkinter + SQLAlchemy ORM  |  SQL Server: FarmersDeskLtd

FIXES in this version:
  ✅ Create Sales: Walk-in / Credit-Customer toggle with live search
  ✅ Sales now correctly stored so Dashboard TODAY tile updates
  ✅ Transactions tab correctly shows newly created sales
  ✅ Add / Edit / Delete for Products, Customers, Suppliers
  ✅ Thermal ESC/POS receipt + QR code
  ✅ A4 PDF report generation & printing
  ✅ Automated Object-Relational Data Modeling Layer via SQLAlchemy
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import json
import os
import re
import subprocess
import tempfile
from typing import Optional, List, Dict

# Import SQLAlchemy items for the new database layer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your dynamically generated database mapping module
try:
    import farmersdeskltd_models as models
except ImportError:
    raise ImportError("Missing structural database file! Please run 'python universal_extractor.py' first.")

PRINT_OK = True

PRINTER_CFG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "printer_cfg.json")

def load_printer_cfg() -> dict:
    try:
        return json.load(open(PRINTER_CFG_FILE))
    except Exception:
        return {"connection": "USB",
                "usb_vendor": "0x04B8", "usb_product": "0x0202",
                "serial_port": "COM3",  "serial_baud": "9600",
                "net_host": "192.168.1.100", "net_port": "9100"}

def save_printer_cfg(cfg: dict):
    try:
        json.dump(cfg, open(PRINTER_CFG_FILE, "w"), indent=2)
    except Exception:
        pass

_printer_cfg: dict = load_printer_cfg()

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE CONNECTION INITIALIZATION (SQLAlchemy Edition)
# ─────────────────────────────────────────────────────────────────────────────
CONN_URL = "mssql+pyodbc://@localhost\\SQLEXPRESS01/FarmersDeskLtd?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"

try:
    # We pass the timeout inside connect_args so pyodbc handles it correctly
    engine = create_engine(
        CONN_URL, 
        pool_size=10, 
        max_overflow=20, 
        connect_args={'timeout': 5}
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    print("Database session initialized successfully.")
except Exception as conn_error:
    print(f"Engine routing failure: {conn_error}")
    session = None

# ─────────────────────────────────────────────────────────────────────────────
# UI DESIGN THEME COLOR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
CLR = {
    "bg":        "#F0F4F8",
    "header":    "#1A3C5E",
    "accent":    "#2E86AB",
    "btn":       "#2E86AB",
    "btn_hover": "#1B6CA8",
    "danger":    "#C0392B",
    "success":   "#27AE60",
    "white":     "#FFFFFF",
    "row_odd":   "#EAF2FF",
    "row_even":  "#FFFFFF",
    "text_dark": "#1A1A2E",
    "border":    "#CBD5E0",
}

FONT_H1   = ("Helvetica Neue", 18, "bold")
FONT_H2   = ("Helvetica Neue", 13, "bold")
FONT_BODY = ("Helvetica Neue", 11)
FONT_SM   = ("Helvetica Neue", 10)

# ─────────────────────────────────────────────────────────────────────────────
# COMPANY PROFILE METADATA
# ─────────────────────────────────────────────────────────────────────────────
COMPANY = {
    "name":    "FarmersDesk Ltd",
    "address": "P.O. Box 0000, Nairobi, Kenya",
    "phone":   "+254 700 000 000",
    "email":   "info@farmersdesk.co.ke",
    "pin":     "P000000000X",
}


# ═════════════════════════════════════════════════════════════════════════════
# DB LAYER (WITH AUTOMATIC EXTRACTION CAPACITY)
# ═════════════════════════════════════════════════════════════════════════════
class Database:
    def __init__(self):
        self.conn: Optional[object] = None
        
        # If explicitly assigned SQL user details fail, auto-fallback to Trusted Windows Auth
        if not c["trusted"]:
            print("SQL Auth failed. Trying Windows Authentication / Trusted Connection...")
            if self._attempt_connection(trusted=True):
                DB_CONFIG["trusted"] = True
                return True
        return False

    def _attempt_connection(self, trusted: bool) -> bool:
        try:
            c = DB_CONFIG
            if trusted:
                cs = (f"DRIVER={{{c['driver']}}};"
                      f"SERVER={c['server']};"
                      f"DATABASE={c['database']};"
                      f"Trusted_Connection=yes;")
            else:
                cs = (f"DRIVER={{{c['driver']}}};"
                      f"SERVER={c['server']};"
                      f"DATABASE={c['database']};"
                      f"UID={c['uid']};PWD={c['pwd']};")
            self.conn = pyodbc.connect(cs, timeout=5)
            return True
        except pyodbc.Error as e:
            print(f"Connection attempt failed (Trusted={trusted}): {e}")
            return False

    def cursor(self):
        if not self.conn:
            raise RuntimeError("Not connected")
        return self.conn.cursor()

    def execute(self, sql: str, params=()):
        cur = self.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    def fetchall(self, sql: str, params=()):
        cur = self.cursor()
        cur.execute(sql, params)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        return cols, [list(r) for r in rows]

    def fetchone(self, sql: str, params=()):
        cur = self.cursor()
        cur.execute(sql, params)
        return cur.fetchone()

    # ─────────────────────────────────────────────────────────────────────────
    # DYNAMIC AUTOMATIC EXTRACTION ENGINE
    # ─────────────────────────────────────────────────────────────────────────
    def extract_all_tables_data(self) -> Dict[str, Dict]:
        """Dynamically reads all schemas and active records from the DB into application memory."""
        extracted_data = {}
        try:
            find_tables_sql = """
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = 'dbo'
            """
            _, tables = self.fetchall(find_tables_sql)
            
            print(f"\nFound {len(tables)} tables. Starting dynamic map:\n" + "─"*60)
            for row in tables:
                table_name = row[0]
                try:
                    columns, rows_data = self.fetchall(f"SELECT * FROM [{table_name}]")
                    formatted_records = [dict(zip(columns, r)) for r in rows_data]
                    
                    extracted_data[table_name] = {
                        "columns": columns,
                        "records": formatted_records,
                        "total_rows": len(formatted_records)
                    }
                    print(f" ✅ [dbo].[{table_name:<15}] -> Loaded {len(formatted_records)} rows into memory.")
                except Exception as ex:
                    print(f" ❌ [dbo].[{table_name:<15}] -> Read skipped: {ex}")
            print("─"*60 + "\nAll database items dynamically compiled!")
        except Exception as e:
            print(f"Extraction error: {e}")
            
        return extracted_data

    def close(self):
        if self.conn:
            self.conn.close()


db = Database()


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def style_btn(btn: tk.Button, danger=False, success=False):
    color = CLR["danger"] if danger else (CLR["success"] if success else CLR["btn"])
    btn.config(bg=color, fg=CLR["white"], font=FONT_BODY,
               relief="flat", cursor="hand2", padx=12, pady=5, bd=0,
               activebackground=CLR["btn_hover"])

def money(v) -> str:
    try:
        return f"{float(v):,.2f}"
    except (TypeError, ValueError):
        return "0.00"

def today_str() -> str:
    return datetime.date.today().strftime("%Y-%m-%d")

def month_start() -> str:
    return datetime.date.today().replace(day=1).strftime("%Y-%m-%d")

# ─────────────────────────────────────────────────────────────────────────────
# EXAMPLE USAGE INSIDE YOUR APPLICATION
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing automatic data extraction pipeline...")
    if db.connect():
        # This single call pulls your entire database payload dynamically
        app_data_package = db.extract_all_tables_data()
        
        # Now you can easily loop through or target tables like 'dbo.Bank' or 'dbo.BCat'
        print(f"\nTotal tables imported automatically: {len(app_data_package)}")
        
        # Example safely targeting a specific table if it exists in the payload:
        if "Bank" in app_data_package:
             print(f"Bank Column headers: {app_data_package['Bank']['columns']}")
        
        db.close()
    else:
        print("Failed to establish a connection to SQLEXPRESS01.")


# ═════════════════════════════════════════════════════════════════════════════
# DATA TABLE
# ═════════════════════════════════════════════════════════════════════════════
class DataTable(ttk.Frame):
    def __init__(self, parent, columns: list, height=12, **kw):
        super().__init__(parent, **kw)
        self.columns = columns
        self.height  = height
        self._build()

    def _build(self):
        s = ttk.Style()
        s.configure("FD.Treeview", font=FONT_SM, rowheight=24,
                     background=CLR["white"], fieldbackground=CLR["white"])
        s.configure("FD.Treeview.Heading",
                     font=("Helvetica Neue", 10, "bold"),
                     background=CLR["header"], foreground=CLR["white"])
        s.map("FD.Treeview", background=[("selected", CLR["accent"])])

        self.tv = ttk.Treeview(self, columns=self.columns,
                               show="headings", style="FD.Treeview",
                               height=self.height)
        vsb = ttk.Scrollbar(self, orient="vertical",   command=self.tv.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tv.xview)
        self.tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        money_words = {"amount","balance","paid","total","bal",
                       "price","cost","kes","credit","debit"}
        for col in self.columns:
            w = 140 if len(col) > 10 else 110
            anchor = "e" if any(m in col.lower() for m in money_words) else "w"
            self.tv.heading(col, text=col, anchor=anchor)
            self.tv.column(col, width=w, anchor=anchor, minwidth=50)

        self.tv.tag_configure("odd",  background=CLR["row_odd"])
        self.tv.tag_configure("even", background=CLR["row_even"])

        self.tv.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def load(self, rows: list):
        self.tv.delete(*self.tv.get_children())
        for i, row in enumerate(rows):
            tag = "odd" if i % 2 == 0 else "even"
            self.tv.insert("", "end", values=row, tags=(tag,))

    def selected_values(self) -> list:
        sel = self.tv.selection()
        return list(self.tv.item(sel[0], "values")) if sel else []

    def bind_select(self, callback):
        self.tv.bind("<<TreeviewSelect>>", callback)

    def bind_double(self, callback):
        self.tv.bind("<Double-1>", callback)


# ═════════════════════════════════════════════════════════════════════════════
# GENERIC FORM DIALOG  (Add / Edit)
# ═════════════════════════════════════════════════════════════════════════════
class FormDialog(tk.Toplevel):
    def __init__(self, parent, title: str, fields: list, initial: dict = None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.configure(bg=CLR["bg"])
        self.grab_set()
        self.result: Optional[dict] = None
        self.fields  = fields
        self.initial = initial or {}
        self._vars   = {}
        self._build()
        h = 80 + len(fields) * 46 + 60
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"430x{h}+{(sw-430)//2}+{(sh-h)//2}")

    def _build(self):
        tk.Label(self, text=self.title(), font=FONT_H2,
                 bg=CLR["bg"], fg=CLR["text_dark"]).pack(pady=(12,6), padx=20)
        body = tk.Frame(self, bg=CLR["bg"], padx=20)
        body.pack(fill="both", expand=True)

        for label, key, wtype, opts in self.fields:
            row = tk.Frame(body, bg=CLR["bg"])
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=FONT_SM,
                     bg=CLR["bg"], width=20, anchor="w").pack(side="left")
            if wtype == "combo":
                var = tk.StringVar(value=self.initial.get(key, opts[0] if opts else ""))
                ttk.Combobox(row, textvariable=var, values=opts,
                             width=22, state="readonly").pack(side="left")
            else:
                var = tk.StringVar(value=str(self.initial.get(key, "")))
                ttk.Entry(row, textvariable=var, width=24).pack(side="left")
            self._vars[key] = var

        bf = tk.Frame(self, bg=CLR["bg"])
        bf.pack(pady=12)
        ok = tk.Button(bf, text="✔  Save", command=self._save)
        style_btn(ok, success=True)
        ok.pack(side="left", padx=6)
        tk.Button(bf, text="Cancel", command=self.destroy,
                  font=FONT_SM).pack(side="left", padx=6)

    def _save(self):
        self.result = {key: var.get().strip()
                       for key, var in self._vars.items()}
        self.destroy()


# ═════════════════════════════════════════════════════════════════════════════
# LOGIN
# ═════════════════════════════════════════════════════════════════════════════
class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.authenticated_user = None
        self.title("FarmersDesk – Login")
        self.resizable(False, False)
        self.configure(bg=CLR["bg"])
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"380x420+{(sw-380)//2}+{(sh-420)//2}")
        self.grab_set()
        self._build()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build(self):
        hdr = tk.Frame(self, bg=CLR["header"], height=80)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="🌾  FarmersDesk Ltd", font=FONT_H1,
                 bg=CLR["header"], fg=CLR["white"]).pack(expand=True)

        body = tk.Frame(self, bg=CLR["bg"], padx=40, pady=20)
        body.pack(fill="both", expand=True)
        tk.Label(body, text="Sign In", font=FONT_H2,
                 bg=CLR["bg"], fg=CLR["text_dark"]).pack(pady=(10,20))

        self.db_lbl = tk.Label(body, text="⏳ Connecting…",
                               font=FONT_SM, bg=CLR["bg"], fg="orange")
        self.db_lbl.pack(pady=(0,10))

        f1 = tk.Frame(body, bg=CLR["bg"]); f1.pack(fill="x", pady=4)
        tk.Label(f1, text="Username", font=FONT_SM,
                 bg=CLR["bg"], width=10, anchor="w").pack(side="left")
        self.user_var = tk.StringVar()
        ttk.Entry(f1, textvariable=self.user_var,
                  font=FONT_BODY, width=22).pack(side="left")

        f2 = tk.Frame(body, bg=CLR["bg"]); f2.pack(fill="x", pady=4)
        tk.Label(f2, text="Password", font=FONT_SM,
                 bg=CLR["bg"], width=10, anchor="w").pack(side="left")
        self.pass_var = tk.StringVar()
        self.pass_entry = ttk.Entry(f2, textvariable=self.pass_var,
                                    font=FONT_BODY, width=22, show="•")
        self.pass_entry.pack(side="left")
        self.pass_entry.bind("<Return>", lambda e: self._login())

        self.show_pw = tk.BooleanVar(value=False)
        ttk.Checkbutton(body, text="Show password",
                        variable=self.show_pw,
                        command=self._toggle_pw).pack(anchor="w", pady=2)

        self.err_lbl = tk.Label(body, text="", font=FONT_SM,
                                bg=CLR["bg"], fg=CLR["danger"])
        self.err_lbl.pack(pady=4)

        btn = tk.Button(body, text="  Login  ", command=self._login)
        style_btn(btn); btn.pack(pady=10)
        self.after(100, self._try_connect)

    def _toggle_pw(self):
        self.pass_entry.config(show="" if self.show_pw.get() else "•")

    def _try_connect(self):
        if db.connect():
            self.db_lbl.config(text="✅ Database connected", fg=CLR["success"])
        else:
            self.db_lbl.config(text="⚠️  Cannot reach database", fg=CLR["danger"])

    def _login(self):
        username = self.user_var.get().strip()
        password = self.pass_var.get()
        if not username:
            self.err_lbl.config(text="Username is required."); return
        if not db.conn:
            self.err_lbl.config(text="No database connection."); return
        row = db.fetchone("SELECT Username FROM dbo.Users WHERE Username=?", (username,))
        if not row:
            self.err_lbl.config(text="Invalid username or password."); return
        ok = db.fetchone(
            "SELECT Username FROM dbo.Users WHERE Username=? AND Password=?",
            (username, password))
        if not ok:
            self.err_lbl.config(text="Invalid username or password."); return
        self.authenticated_user = {"username": username, "name": username}
        self.destroy()

    def _on_close(self):
        self.parent.destroy()


# ═════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
class DashboardFrame(ttk.Frame):
    def __init__(self, parent, current_user: str):
        super().__init__(parent)
        self.current_user = current_user
        self._build()
        self.refresh()

    def _build(self):
        tk.Label(self, text="Dashboard", font=FONT_H1,
                 bg=CLR["bg"], fg=CLR["text_dark"]).pack(pady=(20,10))

        self.tiles_frame = tk.Frame(self, bg=CLR["bg"])
        self.tiles_frame.pack(pady=10)

        tile_defs = [
            ("Today's Revenue (KES)", "today_rev"),
            ("Total Credit Balance",  "credit_bal"),
            ("Items in Stock",        "total_items"),
            ("Suppliers",             "suppliers"),
        ]
        self.kpi: dict = {}
        for i, (label, key) in enumerate(tile_defs):
            frm = tk.Frame(self.tiles_frame, bg=CLR["accent"],
                           width=210, height=110, padx=16, pady=12)
            frm.grid(row=0, column=i, padx=8); frm.pack_propagate(False)
            self.kpi[key] = tk.Label(frm, text="—",
                                     font=("Helvetica Neue", 20, "bold"),
                                     bg=CLR["accent"], fg=CLR["white"])
            self.kpi[key].pack(expand=True)
            tk.Label(frm, text=label, font=FONT_SM,
                     bg=CLR["accent"], fg=CLR["white"],
                     wraplength=180, justify="center").pack()

        tk.Label(self, text="Recent Sales", font=FONT_H2,
                 bg=CLR["bg"], fg=CLR["text_dark"]).pack(
                     anchor="w", padx=20, pady=(20,4))
        cols = ["TraNo","Date","Cashier","Type","Total (KES)","Sold To"]
        self.recent_tbl = DataTable(self, cols, height=10)
        self.recent_tbl.pack(fill="both", expand=True, padx=20, pady=4)

        ref_btn = tk.Button(self, text="🔄 Refresh", command=self.refresh)
        style_btn(ref_btn); ref_btn.pack(anchor="e", padx=20, pady=8)

    def refresh(self):
        try:
            r = db.fetchone(
                "SELECT SUM(total) FROM dbo.Sale "
                "WHERE CAST(tradate AS DATE) = CAST(GETDATE() AS DATE)")
            self.kpi["today_rev"].config(
                text=f"KES {money(r[0] if r and r[0] else 0)}")

            r = db.fetchone("SELECT SUM(balance) FROM dbo.Credit_Customer")
            self.kpi["credit_bal"].config(
                text=f"KES {money(r[0] if r and r[0] else 0)}")

            r = db.fetchone("SELECT COUNT(*) FROM dbo.Stock_item")
            self.kpi["total_items"].config(text=str(r[0]) if r else "—")

            r = db.fetchone("SELECT COUNT(*) FROM dbo.Supplier")
            self.kpi["suppliers"].config(text=str(r[0]) if r else "—")

            _, rows = db.fetchall(
                "SELECT TOP 15 TraNo, tradate, cashier, tratype, "
                "total, SoldTo FROM dbo.Sale ORDER BY tradate DESC, TraNo DESC")
            self.recent_tbl.load([
                [r[0], str(r[1])[:10], r[2] or "", r[3] or "",
                 money(r[4]), r[5] or ""] for r in rows])
        except Exception as e:
            print(f"Dashboard error: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# TRANSACTIONS
# ═════════════════════════════════════════════════════════════════════════════
class TransactionsFrame(ttk.Frame):
    def __init__(self, parent, current_user: str):
        super().__init__(parent)
        self.current_user = current_user
        self._last_rows = []
        self._build()

    def _build(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=4, pady=4)

        live_tab = ttk.Frame(nb)
        nb.add(live_tab, text="  📋 Transactions  ")
        self._build_live_tab(live_tab)

        if self.current_user.lower() == "admin":
            del_tab = ttk.Frame(nb)
            nb.add(del_tab, text="  🗑 Deleted Sales  ")
            self._build_deleted_tab(del_tab)

    def _build_live_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8)
        ctrl.pack(fill="x")

        tk.Label(ctrl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.dfrom = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.dfrom.insert(0, month_start()); self.dfrom.pack(side="left", padx=2)

        tk.Label(ctrl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.dto = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.dto.insert(0, today_str()); self.dto.pack(side="left", padx=2)

        tk.Label(ctrl, text="Cashier:", font=FONT_SM,
                 bg=CLR["bg"]).pack(side="left", padx=(8,0))
        self.cashier_var = tk.StringVar()

        if self.current_user.lower() == "admin":
            ttk.Entry(ctrl, textvariable=self.cashier_var,
                      font=FONT_SM, width=14).pack(side="left", padx=2)
        else:
            self.cashier_var.set(self.current_user)
            ttk.Entry(ctrl, textvariable=self.cashier_var,
                      font=FONT_SM, width=14,
                      state="disabled").pack(side="left", padx=2)

        load = tk.Button(ctrl, text="📋 Load", command=self._load)
        style_btn(load); load.pack(side="left", padx=6)

        del_btn = tk.Button(ctrl, text="🗑 Delete Selected",
                            command=self._delete_transaction)
        style_btn(del_btn, danger=True); del_btn.pack(side="left", padx=4)

        cols = ["TraNo","Date","Time","Type",
                "Cashier","Total (KES)","VAT (KES)","Sold To"]
        self.tbl = DataTable(parent, cols)
        self.tbl.pack(fill="both", expand=True, padx=10, pady=4)

        self.status = tk.Label(parent, text="", font=FONT_SM,
                               bg=CLR["bg"], anchor="w")
        self.status.pack(fill="x", padx=10)

        pbf = tk.Frame(parent, bg=CLR["bg"])
        pbf.pack(anchor="e", padx=10, pady=2)
        for txt, cmd, kw in [
            ("💾 Save PDF",       self._save_pdf,   {}),
            ("🖨 Print A4",       self._print_a4,   {"success": True}),
            ("🧾 Reprint Receipt",self._reprint,    {}),
        ]:
            b = tk.Button(pbf, text=txt, command=cmd)
            b.config(font=FONT_SM, relief="flat", padx=10, pady=4,
                     cursor="hand2",
                     bg=CLR["success"] if kw.get("success") else CLR["btn"],
                     fg=CLR["white"])
            b.pack(side="left", padx=4)

        self._load()

    def _build_deleted_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8)
        ctrl.pack(fill="x")

        tk.Label(ctrl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.del_from = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.del_from.insert(0, month_start())
        self.del_from.pack(side="left", padx=2)

        tk.Label(ctrl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.del_to = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.del_to.insert(0, today_str())
        self.del_to.pack(side="left", padx=2)

        lb = tk.Button(ctrl, text="📋 Load", command=self._load_deleted)
        style_btn(lb); lb.pack(side="left", padx=6)

        tk.Label(ctrl, text="⚠️ Admin View – Deleted Sales",
                 font=FONT_SM, bg=CLR["bg"],
                 fg=CLR["danger"]).pack(side="left", padx=12)

        cols = ["DelId","TraNo","Sale Date","Type","Cashier",
                "Total (KES)","VAT (KES)","Sold To","Deleted At"]
        self.del_tbl = DataTable(parent, cols)
        self.del_tbl.pack(fill="both", expand=True, padx=10, pady=4)

        self.del_status = tk.Label(parent, text="", font=FONT_SM,
                                   bg=CLR["bg"], anchor="w")
        self.del_status.pack(fill="x", padx=10)

        self._del_rows = []
        pbf = tk.Frame(parent, bg=CLR["bg"])
        pbf.pack(anchor="e", padx=10, pady=2)
        for txt, col, cmd in [
            ("💾 Save PDF", CLR["btn"],
             lambda: save_pdf("Deleted Sales", cols, self._del_rows,
                              parent_window=self.winfo_toplevel())),
            ("🖨 Print A4", CLR["success"],
             lambda: direct_print_pdf("Deleted Sales", cols, self._del_rows,
                                      parent_window=self.winfo_toplevel())),
        ]:
            tk.Button(pbf, text=txt, command=cmd,
                      bg=col, fg=CLR["white"], font=FONT_SM,
                      relief="flat", padx=10, pady=4,
                      cursor="hand2").pack(side="left", padx=4)

        self._load_deleted()

    def _load_deleted(self):
        try:
            d1 = datetime.datetime.strptime(self.del_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.del_to.get(),   "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Dates must be YYYY-MM-DD.")
            return
        try:
            _, rows = db.fetchall(
                "SELECT DelId, TraNo, tradate, tratype, cashier, "
                "total, vat, SoldTo, DeletedAt "
                "FROM dbo.Sale_Deleted "
                "WHERE CAST(tradate AS DATE) BETWEEN ? AND ? "
                "ORDER BY DeletedAt DESC",
                (d1.date(), d2.date()))
            fmt = [[r[0], r[1], str(r[2])[:10], r[3] or "",
                    r[4] or "", money(r[5]), money(r[6]),
                    r[7] or "", str(r[8])[:19]] for r in rows]
            self._del_rows = fmt
            self.del_tbl.load(fmt)
            total = sum(float(r[5]) for r in rows if r[5])
            self.del_status.config(
                text=f"{len(rows)} deleted sales | "
                     f"Total Value: KES {money(total)}")
        except Exception as e:
            self.del_status.config(text=f"Error: {str(e)[:100]}")

    def _load(self):
        self._last_rows = []
        try:
            d1 = datetime.datetime.strptime(self.dfrom.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.dto.get(),   "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Dates must be YYYY-MM-DD.")
            return

        is_admin = self.current_user.lower() == "admin"
        cashier  = f"%{self.cashier_var.get().strip()}%" if is_admin \
                   else self.current_user
        try:
            if is_admin:
                _, rows = db.fetchall(
                    "SELECT TOP 1000 TraNo, tradate, SaleTime, tratype, "
                    "cashier, total, vat, SoldTo "
                    "FROM dbo.Sale "
                    "WHERE CAST(tradate AS DATE) BETWEEN ? AND ? "
                    "  AND cashier LIKE ? "
                    "ORDER BY tradate DESC, TraNo DESC",
                    (d1.date(), d2.date(), cashier))
            else:
                _, rows = db.fetchall(
                    "SELECT TOP 1000 TraNo, tradate, SaleTime, tratype, "
                    "cashier, total, vat, SoldTo "
                    "FROM dbo.Sale "
                    "WHERE CAST(tradate AS DATE) BETWEEN ? AND ? "
                    "  AND cashier = ? "
                    "ORDER BY tradate DESC, TraNo DESC",
                    (d1.date(), d2.date(), cashier))

            fmt = [[r[0], str(r[1])[:10],
                    str(r[2])[11:19] if r[2] and len(str(r[2])) > 10 else
                    (str(r[2])[:8] if r[2] else ""),
                    r[3] or "", r[4] or "",
                    money(r[5]), money(r[6]), r[7] or ""] for r in rows]
            self._last_rows = fmt
            self.tbl.load(fmt)
            total = sum(float(r[5]) for r in rows if r[5])
            self.status.config(
                text=f"{len(rows)} transactions  |  Total: KES {money(total)}")
        except Exception as e:
            self.status.config(text=f"Error: {str(e)[:100]}")

    def _delete_transaction(self):
        vals = self.tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a transaction to delete.")
            return
        trano = vals[0]
        if not messagebox.askyesno("Confirm Delete",
                f"Delete transaction #{trano}?\n"
                "Sale items will be removed and stock restored."):
            return
        try:
            _, items = db.fetchall(
                "SELECT ItemCode, qty FROM dbo.Sale_Item WHERE trano=?", (trano,))
            for item in items:
                db.execute(
                    "UPDATE dbo.Stock_item SET qtystock = qtystock + ? "
                    "WHERE pcode=?", (item[1] or 0, item[0]))
            db.execute("DELETE FROM dbo.Sale_Item WHERE trano=?", (trano,))
            db.execute("DELETE FROM dbo.Sale WHERE TraNo=?", (trano,))
            messagebox.showinfo("Deleted", f"Transaction #{trano} deleted.")
            self._load()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _save_pdf(self):
        save_pdf("Transactions Report",
                 ["TraNo","Date","Time","Type","Cashier",
                  "Total (KES)","VAT (KES)","Sold To"],
                 self._last_rows, parent_window=self.winfo_toplevel())

    def _print_a4(self):
        direct_print_pdf("Transactions Report",
                         ["TraNo","Date","Time","Type","Cashier",
                          "Total (KES)","VAT (KES)","Sold To"],
                         self._last_rows, parent_window=self.winfo_toplevel())

    def _reprint(self):
        vals = self.tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a transaction row first.")
            return
        trano = vals[0]
        try:
            row = db.fetchone(
                "SELECT TraNo, tradate, cashier, SoldTo, "
                "cash, change, vat, total "
                "FROM dbo.Sale WHERE TraNo=?", (trano,))
            if not row:
                messagebox.showwarning("Not Found", f"Sale {trano} not found.")
                return
            sale = {"trano": row[0], "date": str(row[1])[:19],
                    "cashier": row[2] or "", "customer": row[3] or "",
                    "cash": row[4] or 0, "change": row[5] or 0,
                    "vat": row[6] or 0, "total": row[7] or 0, "invno": ""}
            _, irows = db.fetchall(
                "SELECT ItemCode, ItemName, qty, "
                "CASE WHEN qty>0 THEN total/qty ELSE 0 END, total, vat "
                "FROM dbo.Sale_Item WHERE trano=?", (trano,))
            items = [{"code": r[0], "name": r[1] or "",
                      "qty": r[2] or 1, "price": r[3] or 0,
                      "total": r[4] or 0, "vat": r[5] or 0} for r in irows]
            print_sale_receipt(_printer_cfg, sale, items)
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ═════════════════════════════════════════════════════════════════════════════
# ITEMS TAB
# ═════════════════════════════════════════════════════════════════════════════
class ItemsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build(); self._load()

    def _build(self):
        ctrl = tk.Frame(self, bg=CLR["bg"], padx=10, pady=8); ctrl.pack(fill="x")
        tk.Label(ctrl, text="Search:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.q = tk.StringVar()
        e = ttk.Entry(ctrl, textvariable=self.q, font=FONT_BODY, width=26)
        e.pack(side="left", padx=4); e.bind("<Return>", lambda _: self._load())
        lb = tk.Button(ctrl, text="🔍 Search", command=self._load)
        style_btn(lb); lb.pack(side="left", padx=2)

        cols = ["ItemId","Product Code","Qty","Price (KES)","SubTotal (KES)"]
        self.tbl = DataTable(self, cols)
        self.tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.status = tk.Label(self, text="", font=FONT_SM,
                               bg=CLR["bg"], anchor="w")
        self.status.pack(fill="x", padx=10)

    def _load(self):
        q = f"%{self.q.get().strip()}%"
        try:
            _, rows = db.fetchall(
                "SELECT ItemId, PCode, Qty, Price, SubTotal "
                "FROM dbo.CItem WHERE CAST(PCode AS VARCHAR) LIKE ? "
                "ORDER BY ItemId", (q,))
            self.tbl.load([[r[0], r[1] or "", r[2] or "0",
                            money(r[3]), money(r[4])] for r in rows])
            self.status.config(text=f"{len(rows)} items found")
        except Exception as e:
            self.status.config(text=f"Error: {str(e)[:60]}")


# ═════════════════════════════════════════════════════════════════════════════
# CREATE SALES  ── FIXED VERSION
# Key fixes:
#   1. Walk-in / Credit-Customer radio toggle shown prominently
#   2. Credit customer shown in scrollable listbox with live search
#   3. tradate stored as a proper Python datetime.date (not a string)
#      so CAST(tradate AS DATE) = GETDATE() works on dashboard
#   4. After saving, dashboard notified via callback
# ═════════════════════════════════════════════════════════════════════════════
class CreateSalesFrame(ttk.Frame):
    def __init__(self, parent, username: str, on_sale_saved=None):
        super().__init__(parent)
        self.current_user   = username
        self.on_sale_saved  = on_sale_saved   # callable → refreshes dashboard
        self.cart           = []
        self._items_list    = []
        self._customers_raw = []   # [{"id":, "name":, "phone":}]
        self._build()
        self._load_customers()
        self._load_items()

    # ─────────────────────────────────────────────────────────────────────
    def _build(self):
        hdr = tk.Frame(self, bg=CLR["header"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="🛒  Create Sale", font=FONT_H2,
                 bg=CLR["header"], fg=CLR["white"]).pack(side="left",
                                                          padx=20, pady=10)

        main = tk.Frame(self, bg=CLR["bg"])
        main.pack(fill="both", expand=True, padx=10, pady=10)
        main.columnconfigure(0, weight=2)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=1)
        main.rowconfigure(0, weight=1)

        # ── LEFT: Items ───────────────────────────────────────────────────
        left = tk.LabelFrame(main, text="Available Items",
                              font=FONT_SM, bg=CLR["bg"], fg=CLR["header"])
        left.grid(row=0, column=0, sticky="nsew", padx=4)

        sf = tk.Frame(left, bg=CLR["bg"]); sf.pack(fill="x", padx=8, pady=4)
        tk.Label(sf, text="Search:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.item_search = ttk.Entry(sf, width=25)
        self.item_search.pack(side="left", padx=4, fill="x", expand=True)
        self.item_search.bind("<KeyRelease>", lambda _: self._search_items())

        item_cols = ["Code","Name","Stock","Price (KES)"]
        self.item_tbl = DataTable(left, item_cols, height=10)
        self.item_tbl.pack(fill="both", expand=True, padx=8, pady=4)
        self.item_tbl.bind_double(self._add_to_cart)

        qf = tk.Frame(left, bg=CLR["bg"]); qf.pack(fill="x", padx=8, pady=4)
        tk.Label(qf, text="Qty:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.quick_qty = ttk.Entry(qf, width=8)
        self.quick_qty.insert(0, "1"); self.quick_qty.pack(side="left", padx=4)
        tk.Button(qf, text="➕ Add Selected",
                  command=self._add_selected_item,
                  bg=CLR["btn"], fg=CLR["white"],
                  font=FONT_SM, relief="flat", padx=10, pady=4,
                  cursor="hand2").pack(side="left", padx=4)

        # ── MIDDLE: Cart ──────────────────────────────────────────────────
        mid = tk.LabelFrame(main, text="Shopping Cart",
                             font=FONT_SM, bg=CLR["bg"], fg=CLR["header"])
        mid.grid(row=0, column=1, sticky="nsew", padx=4)

        cart_cols = ["Code","Name","Qty","Price (KES)","Total (KES)"]
        self.cart_tbl = DataTable(mid, cart_cols, height=10)
        self.cart_tbl.pack(fill="both", expand=True, padx=8, pady=4)

        cf = tk.Frame(mid, bg=CLR["bg"]); cf.pack(fill="x", padx=8, pady=4)
        for txt, cmd, col in [
            ("🗑 Remove",   self._remove_from_cart, CLR["danger"]),
            ("📝 Edit Qty", self._edit_qty,          CLR["btn"]),
            ("❌ Clear",    self._clear_cart,         "#555"),
        ]:
            tk.Button(cf, text=txt, command=cmd,
                      bg=col, fg=CLR["white"], font=FONT_SM,
                      relief="flat", padx=8, pady=3,
                      cursor="hand2").pack(side="left", padx=2)

        # ── RIGHT: Summary & Payment ──────────────────────────────────────
        right = tk.LabelFrame(main, text="Sale Summary",
                               font=FONT_SM, bg=CLR["bg"], fg=CLR["header"])
        right.grid(row=0, column=2, sticky="nsew", padx=4)

        # ══════════════════════════════════════════════════════════════════
        # CUSTOMER SELECTION  ──  THE KEY FIX
        # ══════════════════════════════════════════════════════════════════
        cust_outer = tk.LabelFrame(right, text="Customer",
                                    font=FONT_SM, bg=CLR["bg"],
                                    fg=CLR["header"])
        cust_outer.pack(fill="x", padx=8, pady=6)

        # Walk-in / Credit radio buttons (big, clear)
        radio_row = tk.Frame(cust_outer, bg=CLR["bg"])
        radio_row.pack(fill="x", padx=4, pady=(4,2))

        self.cust_type = tk.StringVar(value="walkin")
        tk.Radiobutton(radio_row, text="🚶 Walk-in",
                       variable=self.cust_type, value="walkin",
                       command=self._on_cust_type_change,
                       bg=CLR["bg"], font=FONT_BODY,
                       fg=CLR["text_dark"],
                       activebackground=CLR["bg"]).pack(side="left", padx=6)
        tk.Radiobutton(radio_row, text="👤 Credit Customer",
                       variable=self.cust_type, value="credit",
                       command=self._on_cust_type_change,
                       bg=CLR["bg"], font=FONT_BODY,
                       fg=CLR["text_dark"],
                       activebackground=CLR["bg"]).pack(side="left", padx=6)

        # Credit customer panel (hidden when Walk-in selected)
        self.credit_panel = tk.Frame(cust_outer, bg=CLR["bg"])
        self.credit_panel.pack(fill="x", padx=4, pady=(2,4))

        # Search box
        csf = tk.Frame(self.credit_panel, bg=CLR["bg"]); csf.pack(fill="x")
        tk.Label(csf, text="Search:", font=FONT_SM,
                 bg=CLR["bg"]).pack(side="left")
        self.cust_search_var = tk.StringVar()
        cse = ttk.Entry(csf, textvariable=self.cust_search_var, width=16)
        cse.pack(side="left", padx=4)
        cse.bind("<KeyRelease>", self._filter_customers)
        tk.Button(csf, text="🔄", command=self._load_customers,
                  bg=CLR["accent"], fg=CLR["white"],
                  font=FONT_SM, relief="flat", padx=4, pady=2,
                  cursor="hand2").pack(side="left")

        # Customer listbox + scrollbar
        lb_frame = tk.Frame(self.credit_panel, bg=CLR["bg"])
        lb_frame.pack(fill="x", pady=2)
        self.cust_listbox = tk.Listbox(lb_frame, height=5,
                                        font=FONT_SM,
                                        selectmode=tk.SINGLE,
                                        bg=CLR["white"],
                                        selectbackground=CLR["accent"],
                                        selectforeground=CLR["white"],
                                        relief="flat", bd=1,
                                        highlightthickness=1,
                                        highlightcolor=CLR["border"])
        cust_vsb = ttk.Scrollbar(lb_frame, orient="vertical",
                                   command=self.cust_listbox.yview)
        self.cust_listbox.configure(yscrollcommand=cust_vsb.set)
        self.cust_listbox.pack(side="left", fill="x", expand=True)
        cust_vsb.pack(side="left", fill="y")
        self.cust_listbox.bind("<<ListboxSelect>>", self._on_cust_select)

        self.selected_cust_lbl = tk.Label(self.credit_panel,
                                           text="No customer selected",
                                           font=FONT_SM, bg=CLR["bg"],
                                           fg=CLR["accent"], wraplength=190)
        self.selected_cust_lbl.pack(anchor="w", pady=2)

        # Start with credit panel hidden
        self._selected_customer = {"id": None, "name": "Walk-in"}
        self._on_cust_type_change()

        # ── Totals ────────────────────────────────────────────────────────
        self.lbl_items = tk.Label(right, text="Items: 0",
                                   font=FONT_SM, bg=CLR["bg"])
        self.lbl_items.pack(fill="x", padx=8, pady=2)

        tk.Frame(right, height=2, bg=CLR["border"]).pack(fill="x", padx=8, pady=4)

        self.lbl_subtotal = tk.Label(right, text="Subtotal: KES 0.00",
                                      font=FONT_SM, bg=CLR["bg"])
        self.lbl_subtotal.pack(fill="x", padx=8, pady=1)

        self.lbl_vat = tk.Label(right, text="VAT (16%): KES 0.00",
                                 font=FONT_SM, bg=CLR["bg"],
                                 fg=CLR["accent"])
        self.lbl_vat.pack(fill="x", padx=8, pady=1)

        tk.Frame(right, height=2, bg=CLR["border"]).pack(fill="x", padx=8, pady=4)

        self.lbl_total = tk.Label(right, text="TOTAL: KES 0.00",
                                   font=("Helvetica", 14, "bold"),
                                   bg=CLR["bg"], fg=CLR["header"])
        self.lbl_total.pack(fill="x", padx=8, pady=4)

        # ── Payment ───────────────────────────────────────────────────────
        tk.Label(right, text="Payment Mode:", font=FONT_SM,
                 bg=CLR["bg"]).pack(fill="x", padx=8, pady=(8,2))
        self.payment_mode = tk.StringVar(value="CASH")
        for mode in ["CASH","CREDIT","CHEQUE","MPESA","BANK TRANSFER"]:
            ttk.Radiobutton(right, text=mode,
                            variable=self.payment_mode, value=mode,
                            command=self._on_payment_mode_change).pack(
                                anchor="w", padx=20, pady=1)

        self.cash_frame = tk.Frame(right, bg=CLR["bg"])
        self.cash_frame.pack(fill="x", padx=8, pady=4)
        tk.Label(self.cash_frame, text="Cash Received:",
                 font=FONT_SM, bg=CLR["bg"]).pack()
        self.cash_entry = ttk.Entry(self.cash_frame, width=15)
        self.cash_entry.pack(fill="x", pady=2)
        self.cash_entry.bind("<KeyRelease>", lambda _: self._calc_change())

        self.lbl_change = tk.Label(right, text="Change: KES 0.00",
                                    font=FONT_SM, bg=CLR["bg"],
                                    fg=CLR["success"])
        self.lbl_change.pack(fill="x", padx=8, pady=2)

        tk.Frame(right, height=2, bg=CLR["border"]).pack(fill="x", padx=8, pady=4)

        bf = tk.Frame(right, bg=CLR["bg"]); bf.pack(fill="x", padx=8, pady=4)
        tk.Button(bf, text="💾 Save Sale",
                  command=self._save_sale,
                  bg=CLR["success"], fg=CLR["white"],
                  font=FONT_SM, relief="flat", padx=8, pady=6,
                  cursor="hand2").pack(fill="x", pady=2)
        tk.Button(bf, text="🧾 Print Receipt",
                  command=self._print_receipt_preview,
                  bg=CLR["accent"], fg=CLR["white"],
                  font=FONT_SM, relief="flat", padx=8, pady=6,
                  cursor="hand2").pack(fill="x", pady=2)

        self._on_payment_mode_change()

    # ── Customer helpers ──────────────────────────────────────────────────
    def _on_cust_type_change(self):
        if self.cust_type.get() == "walkin":
            self.credit_panel.pack_forget()
            self._selected_customer = {"id": None, "name": "Walk-in"}
        else:
            self.credit_panel.pack(fill="x", padx=4, pady=(2,4))
            self._load_customers()

    def _load_customers(self):
        try:
            _, rows = db.fetchall(
                "SELECT id, name, phone FROM dbo.Credit_Customer ORDER BY name")
            self._customers_raw = [{"id": r[0], "name": r[1] or "",
                                    "phone": r[2] or ""} for r in rows]
            self._populate_listbox(self._customers_raw)
        except Exception as e:
            print(f"Load customers error: {e}")

    def _populate_listbox(self, customers):
        self.cust_listbox.delete(0, tk.END)
        self._listbox_data = customers
        for c in customers:
            phone = f"  ({c['phone']})" if c["phone"] else ""
            self.cust_listbox.insert(tk.END, f"{c['name']}{phone}")

    def _filter_customers(self, *_):
        term = self.cust_search_var.get().lower()
        filtered = ([c for c in self._customers_raw
                     if term in c["name"].lower() or term in c["phone"].lower()]
                    if term else self._customers_raw)
        self._populate_listbox(filtered)

    def _on_cust_select(self, *_):
        sel = self.cust_listbox.curselection()
        if not sel:
            return
        c = self._listbox_data[sel[0]]
        self._selected_customer = {"id": c["id"], "name": c["name"]}
        self.selected_cust_lbl.config(
            text=f"✔ {c['name']}  [{c['phone']}]")

    # ── Item helpers ──────────────────────────────────────────────────────
    def _load_items(self):
        try:
            _, rows = db.fetchall(
                "SELECT pcode, name, spw, qtystock FROM dbo.Stock_item ORDER BY name")
            self._items_list = [{"code": str(r[0]), "name": r[1] or "",
                                 "price": r[2] or 0,
                                 "qty_stock": int(r[3]) if r[3] else 0}
                               for r in rows]
            self._display_items(self._items_list)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load items: {e}")

    def _search_items(self):
        term = self.item_search.get().lower()
        filtered = ([i for i in self._items_list
                     if term in i["code"].lower() or term in i["name"].lower()]
                    if term else self._items_list)
        self._display_items(filtered)

    def _display_items(self, items):
        self.item_tbl.load([[str(i["code"]), i["name"],
                             str(int(i["qty_stock"])), money(i["price"])]
                            for i in items])

    def _add_to_cart(self, *_):
        self._add_selected_item()

    def _add_selected_item(self):
        vals = self.item_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Item", "Select an item first.")
            return
        try:
            qty = float(self.quick_qty.get())
            if qty <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Qty", "Enter a valid quantity.")
            return

        code, name, stock, price_str = vals
        price     = float(price_str.replace(",", ""))
        qty_stock = float(stock)

        if qty > qty_stock:
            messagebox.showwarning("Out of Stock",
                f"{name}: only {qty_stock} available.")
            return

        for item in self.cart:
            if item["code"] == code:
                item["qty"]   += qty
                item["total"]  = item["qty"] * item["price"]
                self._update_cart_display()
                return

        self.cart.append({"code": code, "name": name,
                           "qty": qty, "price": price, "total": qty * price})
        self.quick_qty.delete(0, "end")
        self.quick_qty.insert(0, "1")
        self._update_cart_display()

    def _update_cart_display(self):
        self.cart_tbl.load([[i["code"], i["name"][:15], str(i["qty"]),
                             money(i["price"]), money(i["total"])]
                            for i in self.cart])
        subtotal = sum(i["total"] for i in self.cart)
        vat      = subtotal * 0.16
        total    = subtotal + vat
        self.lbl_items.config(text=f"Items: {len(self.cart)}")
        self.lbl_subtotal.config(text=f"Subtotal: KES {money(subtotal)}")
        self.lbl_vat.config(text=f"VAT (16%): KES {money(vat)}")
        self.lbl_total.config(text=f"TOTAL: KES {money(total)}")
        if self.payment_mode.get() == "CASH":
            self._calc_change()

    def _remove_from_cart(self):
        vals = self.cart_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Item", "Select a cart item to remove.")
            return
        self.cart = [i for i in self.cart if i["code"] != vals[0]]
        self._update_cart_display()

    def _edit_qty(self):
        vals = self.cart_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Item", "Select a cart item."); return
        code = vals[0]
        dlg = tk.Toplevel(self); dlg.title("Edit Quantity")
        dlg.resizable(False, False); dlg.configure(bg=CLR["bg"]); dlg.grab_set()
        tk.Label(dlg, text=f"{code}: New Quantity",
                 font=FONT_SM, bg=CLR["bg"]).pack(padx=10, pady=8)
        entry = ttk.Entry(dlg, width=15)
        entry.insert(0, vals[2]); entry.pack(padx=10, pady=4); entry.focus()
        def _save():
            try:
                new_qty = float(entry.get())
                if new_qty <= 0: raise ValueError
                for i in self.cart:
                    if i["code"] == code:
                        i["qty"] = new_qty; i["total"] = new_qty * i["price"]
                dlg.destroy(); self._update_cart_display()
            except ValueError:
                messagebox.showerror("Invalid", "Enter a valid quantity.")
        tk.Button(dlg, text="Save", command=_save,
                  bg=CLR["success"], fg=CLR["white"],
                  relief="flat", padx=10, pady=4,
                  cursor="hand2").pack(padx=10, pady=4)

    def _clear_cart(self):
        if self.cart and messagebox.askyesno("Clear Cart", "Clear all items?"):
            self.cart = []; self._update_cart_display()

    def _on_payment_mode_change(self):
        if self.payment_mode.get() == "CASH":
            self.cash_frame.pack(fill="x", padx=8, pady=4)
            self.lbl_change.pack(fill="x", padx=8, pady=2)
        else:
            self.cash_frame.pack_forget()
            self.lbl_change.pack_forget()

    def _calc_change(self):
        try:
            subtotal = sum(i["total"] for i in self.cart)
            total    = subtotal * 1.16
            cash     = float(self.cash_entry.get() or 0)
            change   = cash - total
            self.lbl_change.config(
                text=f"Change: KES {money(change)}",
                fg=CLR["success"] if change >= 0 else CLR["danger"])
        except ValueError:
            self.lbl_change.config(text="Change: —")

    # ── SAVE SALE  ── THE MAIN FIX ────────────────────────────────────────
    def _save_sale(self):
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Add items to cart first.")
            return

        # Validate customer for credit mode
        mode = self.payment_mode.get()
        sold_to = self._selected_customer["name"]
        if self.cust_type.get() == "credit":
            if self._selected_customer["id"] is None:
                messagebox.showwarning("No Customer",
                    "Please select a credit customer from the list.")
                return
            if mode not in ("CREDIT", "CASH", "MPESA", "CHEQUE", "BANK TRANSFER"):
                pass  # any mode valid for credit customers

        try:
            subtotal = sum(i["total"] for i in self.cart)
            vat      = subtotal * 0.16
            total    = subtotal + vat

            cash = 0.0; change = 0.0
            if mode == "CASH":
                try:
                    cash   = float(self.cash_entry.get() or 0)
                    change = cash - total
                    if change < 0:
                        messagebox.showerror("Payment Error",
                                             "Insufficient cash received.")
                        return
                except ValueError:
                    messagebox.showerror("Invalid Input",
                                         "Enter a valid cash amount.")
                    return

            # ── Generate TraNo ─────────────────────────────────────────
            last = db.fetchone("SELECT MAX(CAST(TraNo AS INT)) FROM dbo.Sale")
            trano = str((last[0] or 0) + 1) if last and last[0] else "1"

            now        = datetime.datetime.now()
            # ── FIX: store tradate as a real date, not a string ────────
            # This makes CAST(tradate AS DATE) = CAST(GETDATE() AS DATE)
            # work correctly on the Dashboard and Transactions tab
            sale_date  = now.date()          # Python date object → SQL DATE
            sale_time  = now               # full datetime for SaleTime column

            db.execute(
                "INSERT INTO dbo.Sale "
                "(TraNo, tradate, tratype, cashier, SoldTo, "
                " cash, change, vat, total, SaleTime) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (trano, sale_date, mode, self.current_user,
                 sold_to, cash, change, vat, total, sale_time))

            for item in self.cart:
                item_vat = item["total"] * 0.16
                db.execute(
                    "INSERT INTO dbo.Sale_Item "
                    "(trano, TraDate, ItemCode, ItemName, qty, total, vat) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (trano, sale_date, item["code"], item["name"],
                     item["qty"], item["total"], item_vat))
                db.execute(
                    "UPDATE dbo.Stock_item SET qtystock = qtystock - ? "
                    "WHERE pcode=?", (item["qty"], item["code"]))

            # If credit customer, update their balance
            if (self.cust_type.get() == "credit"
                    and self._selected_customer["id"] is not None
                    and mode == "CREDIT"):
                db.execute(
                    "UPDATE dbo.Credit_Customer "
                    "SET balance = balance + ? WHERE id=?",
                    (total, self._selected_customer["id"]))

            messagebox.showinfo("Sale Saved",
                f"✅ Sale #{trano} saved successfully!\n"
                f"Customer: {sold_to}\n"
                f"Total:    KES {money(total)}")

            # ── Notify dashboard ───────────────────────────────────────
            if self.on_sale_saved:
                try:
                    self.on_sale_saved()
                except Exception:
                    pass

            if messagebox.askyesno("Print Receipt", "Print thermal receipt?"):
                self._do_print_receipt(trano, sold_to, cash, change, vat, total)

            # Reset
            self.cart = []
            self._update_cart_display()
            self._load_items()
            # Reset customer to walk-in
            self.cust_type.set("walkin")
            self._on_cust_type_change()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def _print_receipt_preview(self):
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Add items first.")
            return
        subtotal = sum(i["total"] for i in self.cart)
        vat = subtotal * 0.16; total = subtotal + vat
        self._do_print_receipt("PREVIEW",
                               self._selected_customer["name"],
                               0, 0, vat, total)

    def _do_print_receipt(self, trano, sold_to, cash, change, vat, total):
        if not PRINT_OK:
            return
        sale_data = {"trano": trano,
                     "date":  datetime.datetime.now().isoformat(),
                     "cashier":  self.current_user,
                     "customer": sold_to,
                     "cash": cash, "change": change,
                     "vat":  vat,  "total":  total,
                     "invno": ""}
        print_sale_receipt(_printer_cfg, sale_data, self.cart)


# ═════════════════════════════════════════════════════════════════════════════
# CREDIT CUSTOMERS  (Add / Edit / Delete)
# ═════════════════════════════════════════════════════════════════════════════
class CreditCustomersFrame(ttk.Frame):
    def __init__(self, parent, current_user: str):
        super().__init__(parent)
        self.current_user = current_user
        self.selected_customer_id   = None
        self.selected_customer_name = ""
        self._build(); self._load_customers()

    _FIELDS = [
        ("Name *",          "name",    "entry", []),
        ("Phone",           "phone",   "entry", []),
        ("Route",           "route",   "entry", []),
        ("Credit Period",   "cperiod", "entry", []),
        ("Date Due",        "datedue", "entry", []),
        ("Balance (KES)",   "balance", "entry", []),
    ]

    def _build(self):
        top = tk.LabelFrame(self, text="Credit Customers",
                            font=FONT_H2, bg=CLR["bg"],
                            fg=CLR["text_dark"], padx=6, pady=6)
        top.pack(fill="x", padx=10, pady=(10,4))

        ctrl = tk.Frame(top, bg=CLR["bg"]); ctrl.pack(fill="x", pady=(0,4))
        tk.Label(ctrl, text="Search:", font=FONT_SM,
                 bg=CLR["bg"]).pack(side="left")
        self.search_var = tk.StringVar()
        e = ttk.Entry(ctrl, textvariable=self.search_var,
                      font=FONT_BODY, width=24)
        e.pack(side="left", padx=4)
        e.bind("<Return>", lambda _: self._load_customers())

        for txt, cmd, kw in [
            ("🔍 Search", self._load_customers,  {}),
            ("🔄 Refresh",self._load_customers,  {}),
            ("➕ Add",    self._add,             {"success": True}),
            ("✏️ Edit",   self._edit,            {}),
            ("🗑 Delete", self._delete,          {"danger": True}),
        ]:
            btn = tk.Button(ctrl, text=txt, command=cmd)
            style_btn(btn, **kw); btn.pack(side="left", padx=2)

        cust_cols = ["ID","Name","Phone","Route",
                     "Balance (KES)","Credit Period","Date Due"]
        self.cust_tbl = DataTable(top, cust_cols, height=6)
        self.cust_tbl.pack(fill="x")
        self.cust_tbl.bind_select(self._on_select)
        self.cust_status = tk.Label(top, text="", font=FONT_SM,
                                    bg=CLR["bg"], anchor="w")
        self.cust_status.pack(fill="x")

        bottom = tk.Frame(self, bg=CLR["bg"])
        bottom.pack(fill="both", expand=True, padx=10, pady=4)
        bottom.columnconfigure(0, weight=3); bottom.columnconfigure(1, weight=1)
        bottom.rowconfigure(0, weight=1)

        inv_frame = tk.LabelFrame(bottom, text="Invoices / Ledger",
                                  font=FONT_H2, bg=CLR["bg"],
                                  fg=CLR["text_dark"], padx=6, pady=6)
        inv_frame.grid(row=0, column=0, sticky="nsew", padx=(0,4))
        inv_frame.rowconfigure(1, weight=1); inv_frame.columnconfigure(0, weight=1)

        ictl = tk.Frame(inv_frame, bg=CLR["bg"])
        ictl.grid(row=0, column=0, sticky="w", pady=(0,4))
        tk.Label(ictl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.inv_from = ttk.Entry(ictl, font=FONT_SM, width=12)
        self.inv_from.insert(0, month_start()); self.inv_from.pack(side="left", padx=2)
        tk.Label(ictl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.inv_to = ttk.Entry(ictl, font=FONT_SM, width=12)
        self.inv_to.insert(0, today_str()); self.inv_to.pack(side="left", padx=2)
        lb = tk.Button(ictl, text="📋 Load", command=self._load_invoices)
        style_btn(lb); lb.pack(side="left", padx=4)

        inv_cols = ["RecId","Date","Ref No","Detail",
                    "Amount (KES)","Paid (KES)","Balance (KES)"]
        self.inv_tbl = DataTable(inv_frame, inv_cols)
        self.inv_tbl.grid(row=1, column=0, sticky="nsew")
        self.inv_status = tk.Label(inv_frame, text="← Select a customer",
                                   font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.inv_status.grid(row=2, column=0, sticky="w")

        pay_frame = tk.LabelFrame(bottom, text="Record Payment",
                                  font=FONT_H2, bg=CLR["bg"],
                                  fg=CLR["text_dark"], padx=10, pady=10)
        pay_frame.grid(row=0, column=1, sticky="nsew")

        self.pay_cust_lbl = tk.Label(pay_frame, text="No customer selected",
                                     font=FONT_SM, bg=CLR["bg"],
                                     fg=CLR["accent"], wraplength=200)
        self.pay_cust_lbl.pack(anchor="w", pady=(0,8))

        fields = [("Amount (KES):","pay_amount"),("Payment Mode:","pay_mode"),
                  ("Cheque No:","pay_chequeno"),("Bank:","pay_bank"),
                  ("Reference:","pay_ref")]
        self.pay_vars = {}
        for label, key in fields:
            tk.Label(pay_frame, text=label, font=FONT_SM,
                     bg=CLR["bg"], anchor="w").pack(fill="x")
            if key == "pay_mode":
                var = tk.StringVar(value="CASH")
                ttk.Combobox(pay_frame, textvariable=var, font=FONT_SM, width=22,
                             values=["CASH","CHEQUE","MPESA",
                                     "BANK TRANSFER","OTHER"]
                             ).pack(fill="x", pady=(0,6))
            else:
                var = tk.StringVar()
                ttk.Entry(pay_frame, textvariable=var,
                          font=FONT_SM).pack(fill="x", pady=(0,6))
            self.pay_vars[key] = var

        self.pay_bal_lbl = tk.Label(pay_frame, text="",
                                    font=("Helvetica Neue",10,"bold"),
                                    bg=CLR["bg"], fg=CLR["danger"])
        self.pay_bal_lbl.pack(anchor="w", pady=4)

        pay_btn = tk.Button(pay_frame, text="💳  Save Payment",
                            command=self._save_payment)
        style_btn(pay_btn, success=True); pay_btn.pack(fill="x", pady=(8,2))
        clr_btn = tk.Button(pay_frame, text="✖  Clear",
                            command=self._clear_payment_form)
        style_btn(clr_btn, danger=True); clr_btn.pack(fill="x")

    def _load_customers(self):
        q = f"%{self.search_var.get().strip()}%"
        try:
            _, rows = db.fetchall(
                "SELECT id, name, phone, Route, balance, cperiod, datedue "
                "FROM dbo.Credit_Customer "
                "WHERE name LIKE ? OR phone LIKE ? OR Route LIKE ? ORDER BY name",
                (q,q,q))
            self.cust_tbl.load([[r[0], r[1] or "", r[2] or "", r[3] or "",
                                  money(r[4]), r[5] or "", r[6] or ""]
                                 for r in rows])
            total_bal = sum(float(r[4]) for r in rows if r[4])
            self.cust_status.config(
                text=f"{len(rows)} customers  |  "
                     f"Total Outstanding: KES {money(total_bal)}")
        except Exception as e:
            self.cust_status.config(text=f"Error: {str(e)[:80]}")

    def _add(self):
        dlg = FormDialog(self.winfo_toplevel(), "Add Credit Customer",
                         self._FIELDS)
        self.wait_window(dlg)
        if not dlg.result or not dlg.result.get("name"):
            return
        d = dlg.result
        try:
            db.execute(
                "INSERT INTO dbo.Credit_Customer "
                "(name,phone,Route,cperiod,datedue,balance) VALUES (?,?,?,?,?,?)",
                (d["name"],d["phone"],d["route"],
                 d["cperiod"] or None, d["datedue"] or None,
                 float(d["balance"] or 0)))
            messagebox.showinfo("Added", f"Customer '{d['name']}' added.")
            self._load_customers()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _edit(self):
        vals = self.cust_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a customer to edit.")
            return
        initial = {"name": vals[1], "phone": vals[2], "route": vals[3],
                   "balance": vals[4].replace(",",""),
                   "cperiod": vals[5], "datedue": vals[6]}
        dlg = FormDialog(self.winfo_toplevel(), "Edit Customer",
                         self._FIELDS, initial)
        self.wait_window(dlg)
        if not dlg.result:
            return
        d = dlg.result
        try:
            db.execute(
                "UPDATE dbo.Credit_Customer SET name=?,phone=?,Route=?,"
                "cperiod=?,datedue=?,balance=? WHERE id=?",
                (d["name"],d["phone"],d["route"],
                 d["cperiod"] or None, d["datedue"] or None,
                 float(d["balance"] or 0), vals[0]))
            messagebox.showinfo("Updated", "Customer updated.")
            self._load_customers()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        vals = self.cust_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a customer to delete.")
            return
        if not messagebox.askyesno("Confirm Delete",
                f"Delete '{vals[1]}'?\n"
                "Invoices and payment history are NOT removed."):
            return
        try:
            db.execute("DELETE FROM dbo.Credit_Customer WHERE id=?", (vals[0],))
            messagebox.showinfo("Deleted", f"'{vals[1]}' deleted.")
            self.selected_customer_id = None
            self._load_customers()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_select(self, _=None):
        vals = self.cust_tbl.selected_values()
        if not vals: return
        self.selected_customer_id   = vals[0]
        self.selected_customer_name = vals[1]
        self.pay_cust_lbl.config(
            text=f"{self.selected_customer_name}\n(ID: {self.selected_customer_id})")
        self.pay_bal_lbl.config(text=f"Current Balance: KES {vals[4]}")
        self._load_invoices()

    def _load_invoices(self):
        if not self.selected_customer_id: return
        try:
            d1 = datetime.datetime.strptime(self.inv_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.inv_to.get(),   "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, rows = db.fetchall(
                "SELECT RecId, TraDate, CRefNo, Detail, Amount, Paid, Balance "
                "FROM dbo.DInv WHERE Idno=? AND TraDate BETWEEN ? AND ? "
                "ORDER BY TraDate DESC",
                (self.selected_customer_id, d1, d2))
            self.inv_tbl.load([[r[0], str(r[1])[:10], r[2] or "", r[3] or "",
                                 money(r[4]), money(r[5]), money(r[6])]
                                for r in rows])
            ta=sum(float(r[4]) for r in rows if r[4])
            tp=sum(float(r[5]) for r in rows if r[5])
            tb=sum(float(r[6]) for r in rows if r[6])
            self.inv_status.config(
                text=f"{len(rows)} invoices | "
                     f"Total: {money(ta)}  Paid: {money(tp)}  Bal: {money(tb)}")
        except Exception as e:
            self.inv_status.config(text=f"Error: {str(e)[:80]}")

    def _save_payment(self):
        if not self.selected_customer_id:
            messagebox.showwarning("No Customer", "Please select a customer first.")
            return
        amt_str = self.pay_vars["pay_amount"].get().strip()
        if not amt_str:
            messagebox.showwarning("Missing Amount", "Enter a payment amount.")
            return
        try:
            amount = float(amt_str.replace(",", ""))
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Amount", "Amount must be a positive number.")
            return
        mode     = self.pay_vars["pay_mode"].get().strip() or "CASH"
        chequeno = self.pay_vars["pay_chequeno"].get().strip() or None
        bank     = self.pay_vars["pay_bank"].get().strip() or None
        ref      = self.pay_vars["pay_ref"].get().strip() or None
        now      = datetime.datetime.now()
        if not messagebox.askyesno("Confirm Payment",
                f"Record KES {money(amount)} for "
                f"{self.selected_customer_name} via {mode}?"):
            return
        try:
            row = db.fetchone(
                "SELECT balance FROM dbo.Credit_Customer WHERE id=?",
                (self.selected_customer_id,))
            current_bal = float(row[0]) if row and row[0] else 0.0
            new_bal = current_bal - amount
            db.execute(
                "INSERT INTO dbo.Payment "
                "(trano,Sid,paydate,amount,bal,paymode,chequeno,dbank,ddocno,DoneBy) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (ref, self.selected_customer_id, now, amount, new_bal,
                 mode, chequeno, bank, ref, self.current_user))
            db.execute(
                "UPDATE dbo.Credit_Customer SET balance=? WHERE id=?",
                (new_bal, self.selected_customer_id))
            messagebox.showinfo("Payment Saved",
                f"✅ KES {money(amount)} recorded.\n"
                f"New Balance: KES {money(new_bal)}")
            if PRINT_OK and messagebox.askyesno("Print",
                    "Print payment receipt?"):
                print_payment_receipt(_printer_cfg, {
                    "payno":    "—", "date":     str(now)[:19],
                    "customer": self.selected_customer_name,
                    "amount":   amount, "mode":     mode,
                    "chequeno": chequeno or "", "balance":  new_bal,
                    "doneby":   self.current_user, "trano":    ref or ""})
            self._clear_payment_form()
            self._load_customers(); self._load_invoices()
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def _clear_payment_form(self):
        for key, var in self.pay_vars.items():
            var.set("CASH" if key == "pay_mode" else "")


# ═════════════════════════════════════════════════════════════════════════════
# SUPPLIERS  (Add / Edit / Delete)
# ═════════════════════════════════════════════════════════════════════════════
class SuppliersFrame(ttk.Frame):
    def __init__(self, parent, current_user: str):
        super().__init__(parent)
        self.current_user = current_user
        self.selected_supplier_id   = None
        self.selected_supplier_name = ""
        self._build(); self._load_suppliers()

    _FIELDS = [
        ("Name *",         "name",     "entry", []),
        ("Tel / Phone",    "telno",    "entry", []),
        ("Town",           "town",     "entry", []),
        ("Contact Person", "cperson",  "entry", []),
        ("PIN",            "pin",      "entry", []),
        ("Amount Owing",   "amtowing", "entry", []),
    ]

    def _build(self):
        top = tk.LabelFrame(self, text="Suppliers",
                            font=FONT_H2, bg=CLR["bg"],
                            fg=CLR["text_dark"], padx=6, pady=6)
        top.pack(fill="x", padx=10, pady=(10,4))

        ctrl = tk.Frame(top, bg=CLR["bg"]); ctrl.pack(fill="x", pady=(0,4))
        tk.Label(ctrl, text="Search:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.s_search = tk.StringVar()
        e = ttk.Entry(ctrl, textvariable=self.s_search, font=FONT_BODY, width=24)
        e.pack(side="left", padx=4)
        e.bind("<Return>", lambda _: self._load_suppliers())
        for txt, cmd, kw in [
            ("🔍 Search", self._load_suppliers, {}),
            ("➕ Add",    self._add,            {"success": True}),
            ("✏️ Edit",   self._edit,           {}),
            ("🗑 Delete", self._delete,         {"danger": True}),
        ]:
            btn = tk.Button(ctrl, text=txt, command=cmd)
            style_btn(btn, **kw); btn.pack(side="left", padx=2)

        sup_cols = ["ID","Name","Tel","Town",
                    "Contact Person","Amount Owing (KES)","PIN"]
        self.sup_tbl = DataTable(top, sup_cols, height=6)
        self.sup_tbl.pack(fill="x")
        self.sup_tbl.bind_select(self._on_select)
        self.sup_status = tk.Label(top, text="", font=FONT_SM,
                                   bg=CLR["bg"], anchor="w")
        self.sup_status.pack(fill="x")

        bottom = tk.Frame(self, bg=CLR["bg"])
        bottom.pack(fill="both", expand=True, padx=10, pady=4)
        bottom.columnconfigure(0, weight=1); bottom.columnconfigure(1, weight=1)
        bottom.rowconfigure(0, weight=1)

        inv_frame = tk.LabelFrame(bottom, text="Supplier Invoices",
                                  font=FONT_H2, bg=CLR["bg"],
                                  fg=CLR["text_dark"], padx=6, pady=6)
        inv_frame.grid(row=0, column=0, sticky="nsew", padx=(0,4))
        inv_frame.rowconfigure(1, weight=1); inv_frame.columnconfigure(0, weight=1)

        ictl = tk.Frame(inv_frame, bg=CLR["bg"])
        ictl.grid(row=0, column=0, sticky="w", pady=(0,4))
        tk.Label(ictl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.sinv_from = ttk.Entry(ictl, font=FONT_SM, width=12)
        self.sinv_from.insert(0, month_start()); self.sinv_from.pack(side="left", padx=2)
        tk.Label(ictl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.sinv_to = ttk.Entry(ictl, font=FONT_SM, width=12)
        self.sinv_to.insert(0, today_str()); self.sinv_to.pack(side="left", padx=2)
        lb = tk.Button(ictl, text="📋 Load", command=self._load_sinv)
        style_btn(lb); lb.pack(side="left", padx=4)

        sinv_cols = ["RecId","Inv Date","TraNo","Detail",
                     "Inv Amount (KES)","Paid (KES)","Balance (KES)"]
        self.sinv_tbl = DataTable(inv_frame, sinv_cols)
        self.sinv_tbl.grid(row=1, column=0, sticky="nsew")
        self.sinv_status = tk.Label(inv_frame, text="← Select a supplier",
                                    font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.sinv_status.grid(row=2, column=0, sticky="w")

        rep_frame = tk.LabelFrame(bottom, text="Stock Replenishments",
                                  font=FONT_H2, bg=CLR["bg"],
                                  fg=CLR["text_dark"], padx=6, pady=6)
        rep_frame.grid(row=0, column=1, sticky="nsew")
        rep_frame.rowconfigure(1, weight=1); rep_frame.columnconfigure(0, weight=1)

        rctl = tk.Frame(rep_frame, bg=CLR["bg"])
        rctl.grid(row=0, column=0, sticky="w", pady=(0,4))
        tk.Label(rctl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.rep_from = ttk.Entry(rctl, font=FONT_SM, width=12)
        self.rep_from.insert(0, month_start()); self.rep_from.pack(side="left", padx=2)
        tk.Label(rctl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.rep_to = ttk.Entry(rctl, font=FONT_SM, width=12)
        self.rep_to.insert(0, today_str()); self.rep_to.pack(side="left", padx=2)
        rlb = tk.Button(rctl, text="📋 Load", command=self._load_replenishments)
        style_btn(rlb); rlb.pack(side="left", padx=4)

        rep_cols = ["TraNo","Issue Date","Due Date","Doc No",
                    "Amount (KES)","VAT (KES)","Mode"]
        self.rep_tbl = DataTable(rep_frame, rep_cols)
        self.rep_tbl.grid(row=1, column=0, sticky="nsew")
        self.rep_status = tk.Label(rep_frame, text="← Select a supplier",
                                   font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.rep_status.grid(row=2, column=0, sticky="w")

    def _load_suppliers(self):
        q = f"%{self.s_search.get().strip()}%"
        try:
            _, rows = db.fetchall(
                "SELECT supplierid, name, telno, town, cperson, AmountOwing, pin "
                "FROM dbo.Supplier WHERE name LIKE ? OR town LIKE ? OR cperson LIKE ? "
                "ORDER BY name", (q,q,q))
            self.sup_tbl.load([[r[0], r[1] or "", r[2] or "", r[3] or "",
                                 r[4] or "", money(r[5]), r[6] or ""]
                                for r in rows])
            total_owe = sum(float(r[5]) for r in rows if r[5])
            self.sup_status.config(
                text=f"{len(rows)} suppliers | Total Owing: KES {money(total_owe)}")
        except Exception as e:
            self.sup_status.config(text=f"Error: {str(e)[:80]}")

    def _add(self):
        dlg = FormDialog(self.winfo_toplevel(), "Add Supplier", self._FIELDS)
        self.wait_window(dlg)
        if not dlg.result or not dlg.result.get("name"): return
        d = dlg.result
        try:
            db.execute(
                "INSERT INTO dbo.Supplier "
                "(name,telno,town,cperson,pin,AmountOwing) VALUES (?,?,?,?,?,?)",
                (d["name"],d["telno"],d["town"],d["cperson"],
                 d["pin"], float(d["amtowing"] or 0)))
            messagebox.showinfo("Added", f"Supplier '{d['name']}' added.")
            self._load_suppliers()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _edit(self):
        vals = self.sup_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a supplier to edit.")
            return
        initial = {"name": vals[1], "telno": vals[2], "town": vals[3],
                   "cperson": vals[4], "amtowing": vals[5].replace(",",""),
                   "pin": vals[6]}
        dlg = FormDialog(self.winfo_toplevel(), "Edit Supplier",
                         self._FIELDS, initial)
        self.wait_window(dlg)
        if not dlg.result: return
        d = dlg.result
        try:
            db.execute(
                "UPDATE dbo.Supplier SET name=?,telno=?,town=?,cperson=?,"
                "pin=?,AmountOwing=? WHERE supplierid=?",
                (d["name"],d["telno"],d["town"],d["cperson"],
                 d["pin"], float(d["amtowing"] or 0), vals[0]))
            messagebox.showinfo("Updated", "Supplier updated.")
            self._load_suppliers()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        vals = self.sup_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a supplier to delete.")
            return
        if not messagebox.askyesno("Confirm Delete",
                f"Delete supplier '{vals[1]}'?"):
            return
        try:
            db.execute("DELETE FROM dbo.Supplier WHERE supplierid=?", (vals[0],))
            messagebox.showinfo("Deleted", f"Supplier '{vals[1]}' deleted.")
            self.selected_supplier_id = None
            self._load_suppliers()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_select(self, _=None):
        vals = self.sup_tbl.selected_values()
        if not vals: return
        self.selected_supplier_id   = vals[0]
        self.selected_supplier_name = vals[1]
        self._load_sinv(); self._load_replenishments()

    def _load_sinv(self):
        if not self.selected_supplier_id: return
        try:
            d1 = datetime.datetime.strptime(self.sinv_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.sinv_to.get(),   "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, rows = db.fetchall(
                "SELECT RecId, InvDate, TraNo, Detail, InvAmount, Paid, Balance "
                "FROM dbo.SInv WHERE SId=? AND InvDate BETWEEN ? AND ? "
                "ORDER BY InvDate DESC",
                (self.selected_supplier_id, d1, d2))
            self.sinv_tbl.load([[r[0], str(r[1])[:10], r[2] or "", r[3] or "",
                                  money(r[4]), money(r[5]), money(r[6])]
                                 for r in rows])
            total = sum(float(r[6]) for r in rows if r[6])
            self.sinv_status.config(
                text=f"{len(rows)} invoices | Outstanding: KES {money(total)}")
        except Exception as e:
            self.sinv_status.config(text=f"Error: {str(e)[:80]}")

    def _load_replenishments(self):
        if not self.selected_supplier_id: return
        try:
            d1 = datetime.datetime.strptime(self.rep_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.rep_to.get(),   "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, rows = db.fetchall(
                "SELECT trano, issuedate, datedue, docno, amount, vatamount, dmode "
                "FROM dbo.Stock_Replenish WHERE sid=? AND issuedate BETWEEN ? AND ? "
                "ORDER BY issuedate DESC",
                (self.selected_supplier_id, d1, d2))
            self.rep_tbl.load([[r[0], str(r[1])[:10],
                                 str(r[2])[:10] if r[2] else "",
                                 r[3] or "", money(r[4]), money(r[5]),
                                 r[6] or ""] for r in rows])
            total = sum(float(r[4]) for r in rows if r[4])
            self.rep_status.config(
                text=f"{len(rows)} replenishments | Total: KES {money(total)}")
        except Exception as e:
            self.rep_status.config(text=f"Error: {str(e)[:80]}")


# ═════════════════════════════════════════════════════════════════════════════
# INVENTORY  (Add / Edit / Delete products)
# ═════════════════════════════════════════════════════════════════════════════
class InventoryFrame(ttk.Frame):
    def __init__(self, parent, current_user: str):
        super().__init__(parent)
        self.current_user = current_user
        self._build(); self._load_stock()

    _PROD_FIELDS = [
        ("Product Code *",   "pcode",    "entry", []),
        ("Name *",           "name",     "entry", []),
        ("Category",         "category", "entry", []),
        ("Buy Price (KES)",  "bpw",      "entry", []),
        ("Sale Price (KES)", "spw",      "entry", []),
        ("Wholesale Price",  "spr",      "entry", []),
        ("Opening Qty",      "qtystock", "entry", []),
        ("Re-Order Level",   "rlevel",   "entry", []),
        ("VAT Code",         "vat",      "combo", ["","A","B","C","EXEMPT"]),
    ]

    def _build(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=4, pady=4)

        stock_tab = ttk.Frame(nb)
        nb.add(stock_tab, text="  📦 Stock Items  ")
        self._build_stock_tab(stock_tab)

        scard_tab = ttk.Frame(nb)
        nb.add(scard_tab, text="  📋 Stock Card  ")
        self._build_scard_tab(scard_tab)

        dmg_tab = ttk.Frame(nb)
        nb.add(dmg_tab, text="  ⚠️ Damaged Stock  ")
        self._build_damaged_tab(dmg_tab)

        exp_tab = ttk.Frame(nb)
        nb.add(exp_tab, text="  🗓️ Expiry  ")
        self._build_expiry_tab(exp_tab)

    def _build_stock_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8); ctrl.pack(fill="x")
        tk.Label(ctrl, text="Search:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.stock_q = tk.StringVar()
        e = ttk.Entry(ctrl, textvariable=self.stock_q, font=FONT_BODY, width=22)
        e.pack(side="left", padx=4); e.bind("<Return>", lambda _: self._load_stock())

        tk.Label(ctrl, text="Category:", font=FONT_SM,
                 bg=CLR["bg"]).pack(side="left", padx=(6,0))
        self.stock_cat = tk.StringVar()
        ttk.Entry(ctrl, textvariable=self.stock_cat, font=FONT_SM, width=12).pack(
            side="left", padx=2)

        for txt, cmd, kw in [
            ("🔍 Search", self._load_stock,    {}),
            ("➕ Add",    self._add_product,   {"success": True}),
            ("✏️ Edit",   self._edit_product,  {}),
            ("🗑 Delete", self._delete_product,{"danger": True}),
        ]:
            btn = tk.Button(ctrl, text=txt, command=cmd)
            style_btn(btn, **kw); btn.pack(side="left", padx=2)

        self.low_stock_var = tk.BooleanVar()
        ttk.Checkbutton(ctrl, text="Low Stock Only",
                        variable=self.low_stock_var,
                        command=self._load_stock).pack(side="left", padx=4)

        cols = ["PCode","Name","Category","Qty Stock","Re-Order",
                "Buy Price (KES)","Sale Price (KES)","Wholesale (KES)","VAT"]
        self.stock_tbl = DataTable(parent, cols)
        self.stock_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.stock_status = tk.Label(parent, text="", font=FONT_SM,
                                     bg=CLR["bg"], anchor="w")
        self.stock_status.pack(fill="x", padx=10)

    def _load_stock(self):
        q   = f"%{self.stock_q.get().strip()}%"
        cat = f"%{self.stock_cat.get().strip()}%"
        low = self.low_stock_var.get()
        extra = "AND qtystock <= RLevel" if low else ""
        try:
            _, rows = db.fetchall(
                f"SELECT pcode, name, PCategory, qtystock, RLevel, "
                f"bpw, spw, spr, vat FROM dbo.Stock_item "
                f"WHERE (name LIKE ? OR CAST(pcode AS VARCHAR) LIKE ?) "
                f"AND PCategory LIKE ? {extra} ORDER BY name", (q,q,cat))
            self.stock_tbl.load([[r[0], r[1] or "", r[2] or "",
                                   r[3] or 0, r[4] or 0,
                                   money(r[5]), money(r[6]), money(r[7]),
                                   r[8] or ""] for r in rows])
            self.stock_status.config(
                text=f"{len(rows)} items"
                     + ("  ⚠️ Low stock filter ON" if low else ""))
        except Exception as e:
            self.stock_status.config(text=f"Error: {str(e)[:80]}")

    def _add_product(self):
        dlg = FormDialog(self.winfo_toplevel(), "Add New Product",
                         self._PROD_FIELDS)
        self.wait_window(dlg)
        if not dlg.result: return
        d = dlg.result
        if not d.get("pcode") or not d.get("name"):
            messagebox.showwarning("Required",
                                   "Product Code and Name are required.")
            return
        if db.fetchone("SELECT pcode FROM dbo.Stock_item WHERE pcode=?",
                       (d["pcode"],)):
            messagebox.showwarning("Duplicate",
                f"Product code '{d['pcode']}' already exists.")
            return
        try:
            db.execute(
                "INSERT INTO dbo.Stock_item "
                "(pcode,name,PCategory,bpw,spw,spr,qtystock,RLevel,vat) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (d["pcode"], d["name"], d["category"],
                 float(d["bpw"] or 0), float(d["spw"] or 0),
                 float(d["spr"] or 0), float(d["qtystock"] or 0),
                 float(d["rlevel"] or 0), d["vat"]))
            messagebox.showinfo("Added",
                f"Product '{d['name']}' (code: {d['pcode']}) added.")
            self._load_stock()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _edit_product(self):
        vals = self.stock_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a product to edit.")
            return
        initial = {
            "pcode": vals[0], "name": vals[1], "category": vals[2],
            "qtystock": str(vals[3]), "rlevel": str(vals[4]),
            "bpw": vals[5].replace(",",""),
            "spw": vals[6].replace(",",""),
            "spr": vals[7].replace(",",""),
            "vat": vals[8],
        }
        fields = [f for f in self._PROD_FIELDS if f[1] != "pcode"]
        dlg = FormDialog(self.winfo_toplevel(),
                         f"Edit Product – {vals[0]}", fields, initial)
        self.wait_window(dlg)
        if not dlg.result: return
        d = dlg.result
        try:
            db.execute(
                "UPDATE dbo.Stock_item SET name=?,PCategory=?,"
                "bpw=?,spw=?,spr=?,qtystock=?,RLevel=?,vat=? WHERE pcode=?",
                (d["name"], d["category"],
                 float(d["bpw"] or 0), float(d["spw"] or 0),
                 float(d["spr"] or 0), float(d["qtystock"] or 0),
                 float(d["rlevel"] or 0), d["vat"], vals[0]))
            messagebox.showinfo("Updated", f"Product '{d['name']}' updated.")
            self._load_stock()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete_product(self):
        vals = self.stock_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a product to delete.")
            return
        if not messagebox.askyesno("Confirm Delete",
                f"Delete '{vals[1]}' (code: {vals[0]})?\n"
                "Sales history is NOT removed."):
            return
        try:
            db.execute("DELETE FROM dbo.Stock_item WHERE pcode=?", (vals[0],))
            messagebox.showinfo("Deleted", f"Product '{vals[1]}' deleted.")
            self._load_stock()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _build_scard_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8); ctrl.pack(fill="x")
        tk.Label(ctrl, text="Product Code:", font=FONT_SM,
                 bg=CLR["bg"]).pack(side="left")
        self.sc_pcode = tk.StringVar()
        ttk.Entry(ctrl, textvariable=self.sc_pcode,
                  font=FONT_SM, width=14).pack(side="left", padx=4)
        tk.Label(ctrl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.sc_from = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.sc_from.insert(0, month_start()); self.sc_from.pack(side="left", padx=2)
        tk.Label(ctrl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.sc_to = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.sc_to.insert(0, today_str()); self.sc_to.pack(side="left", padx=2)
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_scard)
        style_btn(lb); lb.pack(side="left", padx=4)

        cols = ["RecId","Date","Narration","Category",
                "Qty In","Qty Out","New Qty","Done By"]
        self.sc_tbl = DataTable(parent, cols)
        self.sc_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.sc_status = tk.Label(parent, text="", font=FONT_SM,
                                  bg=CLR["bg"], anchor="w")
        self.sc_status.pack(fill="x", padx=10)

    def _load_scard(self):
        pcode = self.sc_pcode.get().strip()
        if not pcode:
            messagebox.showwarning("Missing", "Enter a product code.")
            return
        try:
            d1 = datetime.datetime.strptime(self.sc_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.sc_to.get(),   "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, rows = db.fetchall(
                "SELECT RecId, MDate, Narration, Category, "
                "QIn, QOut, NewQty, DBy FROM dbo.SCard "
                "WHERE PCode=? AND MDate BETWEEN ? AND ? ORDER BY MDate DESC",
                (pcode, d1, d2))
            self.sc_tbl.load([[r[0], str(r[1])[:10], r[2] or "", r[3] or "",
                                r[4] or 0, r[5] or 0, r[6] or 0, r[7] or ""]
                               for r in rows])
            self.sc_status.config(text=f"{len(rows)} movements")
        except Exception as e:
            self.sc_status.config(text=f"Error: {str(e)[:80]}")

    def _build_damaged_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8); ctrl.pack(fill="x")
        tk.Label(ctrl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.dmg_from = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.dmg_from.insert(0, month_start()); self.dmg_from.pack(side="left", padx=2)
        tk.Label(ctrl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.dmg_to = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.dmg_to.insert(0, today_str()); self.dmg_to.pack(side="left", padx=2)
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_damaged)
        style_btn(lb); lb.pack(side="left", padx=4)

        cols = ["RecNo","Item Code","Item Name","Qty",
                "Date","Buy Price (KES)","Narration","Entered By"]
        self.dmg_tbl = DataTable(parent, cols)
        self.dmg_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.dmg_status = tk.Label(parent, text="", font=FONT_SM,
                                   bg=CLR["bg"], anchor="w")
        self.dmg_status.pack(fill="x", padx=10)
        self._load_damaged()

    def _load_damaged(self):
        try:
            d1 = datetime.datetime.strptime(self.dmg_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.dmg_to.get(),   "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, rows = db.fetchall(
                "SELECT RecNo, ItemCode, ItemName, Qty, DDate, BP, Narration, EnteredBy "
                "FROM dbo.DamagedStock WHERE DDate BETWEEN ? AND ? ORDER BY DDate DESC",
                (d1, d2))
            self.dmg_tbl.load([[r[0], r[1], r[2] or "", r[3] or 0,
                                  str(r[4])[:10], money(r[5]), r[6] or "",
                                  r[7] or ""] for r in rows])
            total_loss = sum(float(r[3])*float(r[5]) for r in rows if r[3] and r[5])
            self.dmg_status.config(
                text=f"{len(rows)} records | Est. Loss: KES {money(total_loss)}")
        except Exception as e:
            self.dmg_status.config(text=f"Error: {str(e)[:80]}")

    def _build_expiry_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8); ctrl.pack(fill="x")
        tk.Label(ctrl, text="Expiry Before:", font=FONT_SM,
                 bg=CLR["bg"]).pack(side="left")
        self.exp_before = ttk.Entry(ctrl, font=FONT_SM, width=12)
        ahead = (datetime.date.today()+datetime.timedelta(days=90)).strftime("%Y-%m-%d")
        self.exp_before.insert(0, ahead); self.exp_before.pack(side="left", padx=4)
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_expiry)
        style_btn(lb); lb.pack(side="left", padx=4)

        cols = ["RecId","Batch No","PCode","Mfg Date",
                "Expiry Date","Qty","Done By","TraNo"]
        self.exp_tbl = DataTable(parent, cols)
        self.exp_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.exp_status = tk.Label(parent, text="", font=FONT_SM,
                                   bg=CLR["bg"], anchor="w")
        self.exp_status.pack(fill="x", padx=10)
        self._load_expiry()

    def _load_expiry(self):
        try:
            d = datetime.datetime.strptime(self.exp_before.get(), "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, rows = db.fetchall(
                "SELECT RecId, BatchNo, PCode, MDate, EDate, Qty, DoneBy, TraNo "
                "FROM dbo.Expiry WHERE EDate<=? ORDER BY EDate ASC", (d,))
            self.exp_tbl.load([[r[0], r[1] or "", r[2],
                                  str(r[3])[:10] if r[3] else "",
                                  str(r[4])[:10] if r[4] else "",
                                  r[5] or 0, r[6] or "", r[7] or ""]
                                 for r in rows])
            self.exp_status.config(
                text=f"{len(rows)} items expiring before {self.exp_before.get()}")
        except Exception as e:
            self.exp_status.config(text=f"Error: {str(e)[:80]}")


# ═════════════════════════════════════════════════════════════════════════════
# PAYMENTS & RECEIPTS
# ═════════════════════════════════════════════════════════════════════════════
class PaymentsFrame(ttk.Frame):
    def __init__(self, parent, current_user: str):
        super().__init__(parent)
        self.current_user = current_user
        self._build()

    def _build(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=4, pady=4)

        cust_tab = ttk.Frame(nb)
        nb.add(cust_tab, text="  💰 Customer Payments  ")
        self._build_cust_payments(cust_tab)

        sup_tab = ttk.Frame(nb)
        nb.add(sup_tab, text="  🏦 Supplier Payments  ")
        self._build_sup_payments(sup_tab)

        cb_tab = ttk.Frame(nb)
        nb.add(cb_tab, text="  📒 Cash Book  ")
        self._build_cashbook(cb_tab)

    def _date_ctrl(self, parent, attr_from, attr_to):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8); ctrl.pack(fill="x")
        tk.Label(ctrl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        e1 = ttk.Entry(ctrl, font=FONT_SM, width=12)
        e1.insert(0, month_start()); e1.pack(side="left", padx=2)
        tk.Label(ctrl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        e2 = ttk.Entry(ctrl, font=FONT_SM, width=12)
        e2.insert(0, today_str()); e2.pack(side="left", padx=2)
        setattr(self, attr_from, e1); setattr(self, attr_to, e2)
        return ctrl

    def _build_cust_payments(self, parent):
        ctrl = self._date_ctrl(parent, "cp_from", "cp_to")
        tk.Label(ctrl, text="Mode:", font=FONT_SM,
                 bg=CLR["bg"]).pack(side="left", padx=(8,0))
        self.cp_mode = tk.StringVar()
        ttk.Combobox(ctrl, textvariable=self.cp_mode, font=FONT_SM, width=12,
                     values=["","CASH","CHEQUE","MPESA",
                             "BANK TRANSFER","OTHER"]).pack(side="left", padx=2)
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_cust_payments)
        style_btn(lb); lb.pack(side="left", padx=6)
        del_btn = tk.Button(ctrl, text="🗑 Delete", command=self._delete_payment)
        style_btn(del_btn, danger=True); del_btn.pack(side="left", padx=4)

        cols = ["PayNo","Date","Cust ID","Amount (KES)","Balance (KES)",
                "Mode","Cheque No","Bank","Done By"]
        self.cp_tbl = DataTable(parent, cols)
        self.cp_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.cp_status = tk.Label(parent, text="", font=FONT_SM,
                                  bg=CLR["bg"], anchor="w")
        self.cp_status.pack(fill="x", padx=10)
        self._cp_rows = []

        pbf = tk.Frame(parent, bg=CLR["bg"]); pbf.pack(anchor="e", padx=10, pady=2)
        CP_COLS = ["PayNo","Date","Cust ID","Amount (KES)","Balance (KES)",
                   "Mode","Cheque No","Bank","Done By"]
        for txt, cmd, col in [
            ("💾 Save PDF",   lambda: save_pdf("Customer Payments", CP_COLS,
                                               self._cp_rows,
                                               parent_window=parent.winfo_toplevel()),
             CLR["btn"]),
            ("🖨 Print A4",   lambda: direct_print_pdf("Customer Payments", CP_COLS,
                                                        self._cp_rows,
                                                        parent_window=parent.winfo_toplevel()),
             CLR["success"]),
            ("🧾 Reprint",    self._reprint_payment, CLR["accent"]),
        ]:
            tk.Button(pbf, text=txt, command=cmd,
                      bg=col, fg=CLR["white"], font=FONT_SM,
                      relief="flat", padx=10, pady=4,
                      cursor="hand2").pack(side="left", padx=4)
        self._load_cust_payments()

    def _delete_payment(self):
        vals = self.cp_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a payment to delete.")
            return
        if not messagebox.askyesno("Confirm Delete",
                f"Delete payment #{vals[0]}?\n"
                "Customer balance will NOT be auto-restored."):
            return
        try:
            db.execute("DELETE FROM dbo.Payment WHERE payno=?", (vals[0],))
            messagebox.showinfo("Deleted", f"Payment #{vals[0]} deleted.")
            self._load_cust_payments()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _reprint_payment(self):
        vals = self.cp_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a payment row first.")
            return
        print_payment_receipt(_printer_cfg, {
            "payno": vals[0], "date": vals[1],
            "customer": f"ID {vals[2]}",
            "amount": vals[3].replace(",",""),
            "mode": vals[5], "chequeno": vals[6],
            "balance": vals[4].replace(",",""),
            "doneby": vals[8], "trano": ""})

    def _load_cust_payments(self):
        try:
            d1 = datetime.datetime.strptime(self.cp_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.cp_to.get(),   "%Y-%m-%d")
        except ValueError:
            return
        mode  = self.cp_mode.get().strip()
        extra = "AND paymode=?" if mode else ""
        params = (d1, d2, mode) if mode else (d1, d2)
        try:
            _, rows = db.fetchall(
                f"SELECT payno, paydate, Sid, amount, bal, paymode, "
                f"chequeno, dbank, DoneBy FROM dbo.Payment "
                f"WHERE paydate BETWEEN ? AND ? {extra} ORDER BY paydate DESC",
                params)
            fmt = [[r[0], str(r[1])[:10], r[2], money(r[3]), money(r[4]),
                    r[5] or "", r[6] or "", r[7] or "", r[8] or ""]
                   for r in rows]
            self._cp_rows = fmt; self.cp_tbl.load(fmt)
            total = sum(float(r[3]) for r in rows if r[3])
            self.cp_status.config(
                text=f"{len(rows)} payments | Total Received: KES {money(total)}")
        except Exception as e:
            self.cp_status.config(text=f"Error: {str(e)[:80]}")

    def _build_sup_payments(self, parent):
        ctrl = self._date_ctrl(parent, "sp_from", "sp_to")
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_sup_payments)
        style_btn(lb); lb.pack(side="left", padx=6)

        cols = ["PayNo","Date","Supplier ID","Amount (KES)",
                "Mode","Cheque No","Bank Acc","Done By"]
        self.sp_tbl = DataTable(parent, cols)
        self.sp_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.sp_status = tk.Label(parent, text="", font=FONT_SM,
                                  bg=CLR["bg"], anchor="w")
        self.sp_status.pack(fill="x", padx=10)
        self._load_sup_payments()

    def _load_sup_payments(self):
        try:
            d1 = datetime.datetime.strptime(self.sp_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.sp_to.get(),   "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, rows = db.fetchall(
                "SELECT PayNo, PDATE, SID, AMT, PMODE, CQNO, TBANK, DBY "
                "FROM dbo.SPay WHERE PDATE BETWEEN ? AND ? ORDER BY PDATE DESC",
                (d1, d2))
            self.sp_tbl.load([[r[0], str(r[1])[:10], r[2], money(r[3]),
                                r[4] or "", r[5] or "", r[6] or "",
                                r[7] or ""] for r in rows])
            total = sum(float(r[3]) for r in rows if r[3])
            self.sp_status.config(
                text=f"{len(rows)} payments | Total Paid Out: KES {money(total)}")
        except Exception as e:
            self.sp_status.config(text=f"Error: {str(e)[:80]}")

    def _build_cashbook(self, parent):
        ctrl = self._date_ctrl(parent, "cb_from", "cb_to")
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_cashbook)
        style_btn(lb); lb.pack(side="left", padx=6)

        cols = ["RecId","Date","Time","Category","Category2",
                "Cash In (KES)","Cash Out (KES)","Bank In (KES)",
                "Bank Out (KES)","Done By"]
        self.cb_tbl = DataTable(parent, cols)
        self.cb_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.cb_status = tk.Label(parent, text="", font=FONT_SM,
                                  bg=CLR["bg"], anchor="w")
        self.cb_status.pack(fill="x", padx=10)
        self._load_cashbook()

    def _load_cashbook(self):
        try:
            d1 = datetime.datetime.strptime(self.cb_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.cb_to.get(),   "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, rows = db.fetchall(
                "SELECT recid, Dt, Tm, MCat, MCat2, cin, cout, bin, bout, dby "
                "FROM dbo.CB WHERE Dt BETWEEN ? AND ? ORDER BY Dt DESC, Tm DESC",
                (d1, d2))
            self.cb_tbl.load([[r[0], str(r[1])[:10],
                                str(r[2])[11:19] if r[2] and len(str(r[2]))>10 else "",
                                r[3] or "", r[4] or "",
                                money(r[5]), money(r[6]), money(r[7]), money(r[8]),
                                r[9] or ""] for r in rows])
            ti = sum(float(r[5]) for r in rows if r[5])
            to_ = sum(float(r[6]) for r in rows if r[6])
            self.cb_status.config(
                text=f"{len(rows)} entries | "
                     f"Cash In: KES {money(ti)}  Cash Out: KES {money(to_)}")
        except Exception as e:
            self.cb_status.config(text=f"Error: {str(e)[:80]}")


# ═════════════════════════════════════════════════════════════════════════════
# REPORTS
# ═════════════════════════════════════════════════════════════════════════════
class ReportsFrame(ttk.Frame):
    def __init__(self, parent, current_user: str):
        super().__init__(parent)
        self.current_user = current_user
        self._build()

    def _build(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=4, pady=4)

        for label, builder in [
            ("  📊 Sales Summary  ",   self._build_sales_summary),
            ("  📈 Trading Account  ", self._build_trading),
            ("  🔁 Reconcile  ",       self._build_reconcile),
            ("  👥 Debtor Ageing  ",   self._build_ageing),
            ("  🗒️ Vote Transactions  ",self._build_vote),
        ]:
            tab = ttk.Frame(nb)
            nb.add(tab, text=label)
            builder(tab)

    def _date_ctrl(self, parent, attr_from, attr_to, cmd):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8); ctrl.pack(fill="x")
        tk.Label(ctrl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        e1 = ttk.Entry(ctrl, font=FONT_SM, width=12)
        e1.insert(0, month_start()); e1.pack(side="left", padx=2)
        tk.Label(ctrl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        e2 = ttk.Entry(ctrl, font=FONT_SM, width=12)
        e2.insert(0, today_str()); e2.pack(side="left", padx=2)
        setattr(self, attr_from, e1); setattr(self, attr_to, e2)
        lb = tk.Button(ctrl, text="📋 Load", command=cmd)
        style_btn(lb); lb.pack(side="left", padx=6)
        return ctrl

    def _print_bar(self, parent, title, get_cols, get_rows, get_sub=None):
        pbf = tk.Frame(parent, bg=CLR["bg"]); pbf.pack(anchor="e", padx=10, pady=2)
        for txt, fn, col in [
            ("💾 Save PDF", save_pdf,        CLR["btn"]),
            ("🖨 Print A4", direct_print_pdf, CLR["success"]),
        ]:
            def make_cmd(f=fn):
                def cmd():
                    f(title, get_cols(), get_rows(),
                      subtitle=get_sub() if get_sub else "",
                      parent_window=parent.winfo_toplevel())
                return cmd
            tk.Button(pbf, text=txt, command=make_cmd(),
                      bg=col, fg=CLR["white"], font=FONT_SM,
                      relief="flat", padx=10, pady=4,
                      cursor="hand2").pack(side="left", padx=4)

    def _build_sales_summary(self, parent):
        ctrl = self._date_ctrl(parent, "ss_from", "ss_to",
                               self._load_sales_summary)
        ctrl.config()

        is_admin = self.current_user.lower() == "admin"
        who = "All Cashiers (Admin View)" if is_admin else self.current_user
        tk.Label(parent, text=f"📋 Showing sales for: {who}",
                 font=FONT_SM, bg=CLR["bg"],
                 fg=CLR["accent"]).pack(anchor="w", padx=12, pady=(2,0))

        kpi_frame = tk.Frame(parent, bg=CLR["bg"])
        kpi_frame.pack(fill="x", padx=10, pady=4)
        self.ss_kpi_labels = {}
        for i, (key, label) in enumerate([
            ("total_sales",  "Total Sales (KES)"),
            ("total_vat",    "Total VAT (KES)"),
            ("num_sales",    "No. of Sales"),
            ("credit_sales", "Credit Sales (KES)"),
        ]):
            f = tk.Frame(kpi_frame, bg=CLR["accent"],
                         width=200, height=70, padx=10, pady=6)
            f.grid(row=0, column=i, padx=6)
            f.pack_propagate(False)
            lbl = tk.Label(f, text="—",
                           font=("Helvetica Neue", 16, "bold"),
                           bg=CLR["accent"], fg=CLR["white"])
            lbl.pack(expand=True)
            tk.Label(f, text=label, font=FONT_SM,
                     bg=CLR["accent"], fg=CLR["white"]).pack()
            self.ss_kpi_labels[key] = lbl

        self._ss_rows = []
        cols = ["Date", "TraNo", "Type", "Cashier",
                "Total (KES)", "VAT (KES)", "Sold To"]
        self.ss_tbl = DataTable(parent, cols)
        self.ss_tbl.pack(fill="both", expand=True, padx=10, pady=4)

        self.ss_status = tk.Label(parent, text="", font=FONT_SM,
                                  bg=CLR["bg"], anchor="w")
        self.ss_status.pack(fill="x", padx=10)

        self._print_bar(parent, "Sales Summary Report",
                        lambda: cols,
                        lambda: self._ss_rows,
                        lambda: f"Cashier: {who}  |  "
                                f"{self.ss_from.get()} to {self.ss_to.get()}")

    def _load_sales_summary(self):
        try:
            d1 = datetime.datetime.strptime(self.ss_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.ss_to.get(),   "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Dates must be YYYY-MM-DD.")
            return
        try:
            is_admin = self.current_user.lower() == "admin"
            if is_admin:
                _, rows = db.fetchall(
                    "SELECT tradate, TraNo, tratype, cashier, total, vat, SoldTo "
                    "FROM dbo.Sale "
                    "WHERE CAST(tradate AS DATE) BETWEEN ? AND ? "
                    "ORDER BY tradate DESC",
                    (d1.date(), d2.date()))
            else:
                _, rows = db.fetchall(
                    "SELECT tradate, TraNo, tratype, cashier, total, vat, SoldTo "
                    "FROM dbo.Sale "
                    "WHERE CAST(tradate AS DATE) BETWEEN ? AND ? "
                    "AND cashier = ? "
                    "ORDER BY tradate DESC",
                    (d1.date(), d2.date(), self.current_user))

            fmt = [[str(r[0])[:10], r[1], r[2] or "", r[3] or "",
                    money(r[4]), money(r[5]), r[6] or ""] for r in rows]
            self._ss_rows = fmt
            self.ss_tbl.load(fmt)
            ts = sum(float(r[4]) for r in rows if r[4])
            tv = sum(float(r[5]) for r in rows if r[5])
            cs = sum(float(r[4]) for r in rows
                     if r[4] and r[2] and "credit" in str(r[2]).lower())
            self.ss_kpi_labels["total_sales"].config(text=f"KES {money(ts)}")
            self.ss_kpi_labels["total_vat"].config(text=f"KES {money(tv)}")
            self.ss_kpi_labels["num_sales"].config(text=str(len(rows)))
            self.ss_kpi_labels["credit_sales"].config(text=f"KES {money(cs)}")
            label = "All Cashiers" if is_admin else self.current_user
            self.ss_status.config(
                text=f"{len(rows)} sales for {label} | Total: KES {money(ts)}")
        except Exception as e:
            self.ss_status.config(text=f"Error: {str(e)[:80]}")

    def _build_trading(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8); ctrl.pack(fill="x")
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_trading)
        style_btn(lb); lb.pack(side="left")
        cols = ["Start Date","End Date","Sales (KES)","Purchases (KES)",
                "Cost of Goods (KES)","Gross Profit (KES)",
                "Opening Stock (KES)","Closing Stock (KES)"]
        self.tr_tbl = DataTable(parent, cols)
        self.tr_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.tr_status = tk.Label(parent, text="", font=FONT_SM,
                                  bg=CLR["bg"], anchor="w")
        self.tr_status.pack(fill="x", padx=10)
        self._load_trading()

    def _load_trading(self):
        try:
            _, rows = db.fetchall(
                "SELECT StartDate, EndDate, Sales, Purchases, CostOfGoods, "
                "GrossProfit, OpeningStock, ClosingStock "
                "FROM dbo.Trading ORDER BY StartDate DESC")
            self.tr_tbl.load([[str(r[0])[:10], str(r[1])[:10],
                                money(r[2]), money(r[3]), money(r[4]),
                                money(r[5]), money(r[6]), money(r[7])]
                               for r in rows])
            self.tr_status.config(text=f"{len(rows)} period(s) found")
        except Exception as e:
            self.tr_status.config(text=f"Error: {str(e)[:80]}")

    def _build_reconcile(self, parent):
        self._date_ctrl(parent, "rc_from", "rc_to", self._load_reconcile)
        cols = ["Date","Cash Sales (KES)","Credit Sales (KES)","Invoices (KES)",
                "Expenses (KES)","Net Cash (KES)","Banked (KES)",
                "Surplus/Deficit (KES)","Comment"]
        self._rc_rows = []
        self.rc_tbl = DataTable(parent, cols)
        self.rc_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.rc_status = tk.Label(parent, text="", font=FONT_SM,
                                  bg=CLR["bg"], anchor="w")
        self.rc_status.pack(fill="x", padx=10)
        self._print_bar(parent, "Reconciliation Report",
                        lambda: cols, lambda: self._rc_rows)
        self._load_reconcile()

    def _load_reconcile(self):
        try:
            d1 = datetime.datetime.strptime(self.rc_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.rc_to.get(),   "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, col_rows = db.fetchall(
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_NAME = 'Reconcile' AND TABLE_SCHEMA = 'dbo'")
            existing = {r[0].lower() for r in col_rows}
            if not existing:
                self.rc_status.config(
                    text="Table dbo.Reconcile does not exist. Run the SQL fix script.")
                return
            col_map = {
                "TraDate":    "TraDate",
                "CashSale":   "CashSale",
                "CreditSale": "CreditSale",
                "Invoices":   "Invoices",
                "Expenses":   "Expenses",
                "NetCash":    "NetCash",
                "Banked":     "Banked",
                "DefSurp":    "DefSurp",
                "Comment":    "Comment",
            }
            missing = [c for c in col_map if c.lower() not in existing]
            if missing:
                self.rc_status.config(
                    text=f"Missing columns: {', '.join(missing)}. Run SQL fix script.")
                return
            _, rows = db.fetchall(
                "SELECT TraDate, CashSale, CreditSale, Invoices, Expenses, "
                "NetCash, Banked, DefSurp, Comment FROM dbo.Reconcile "
                "WHERE TraDate BETWEEN ? AND ? ORDER BY TraDate DESC", (d1, d2))
            fmt = [[str(r[0])[:10], money(r[1]), money(r[2]), money(r[3]),
                    money(r[4]), money(r[5]), money(r[6]), money(r[7]),
                    r[8] or ""] for r in rows]
            self._rc_rows = fmt
            self.rc_tbl.load(fmt)
            self.rc_status.config(text=f"{len(rows)} reconciliation records")
        except Exception as e:
            self.rc_status.config(text=f"Error: {str(e)[:120]}")

    def _build_ageing(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8); ctrl.pack(fill="x")
        lb = tk.Button(ctrl, text="📋 Load Debtor Ageing", command=self._load_ageing)
        style_btn(lb); lb.pack(side="left")
        cols = ["Cust ID","0-30 Days (KES)","31-60 Days (KES)","61-90 Days (KES)",
                "91-120 Days (KES)","Over 120 (KES)","Total (KES)","Unallocated (KES)"]
        self._age_rows = []
        self.age_tbl = DataTable(parent, cols)
        self.age_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.age_status = tk.Label(parent, text="", font=FONT_SM,
                                   bg=CLR["bg"], anchor="w")
        self.age_status.pack(fill="x", padx=10)
        self._print_bar(parent, "Debtor Ageing Report",
                        lambda: cols, lambda: self._age_rows)
        self._load_ageing()

    def _load_ageing(self):
        try:
            _, rows = db.fetchall(
                "SELECT sid, a30, a60, a90, a120, aover, atotal, UB "
                "FROM dbo.SDAS ORDER BY atotal DESC")
            fmt = [[r[0], money(r[1]), money(r[2]), money(r[3]),
                    money(r[4]), money(r[5]), money(r[6]), money(r[7])]
                   for r in rows]
            self._age_rows = fmt; self.age_tbl.load(fmt)
            grand = sum(float(r[6]) for r in rows if r[6])
            self.age_status.config(
                text=f"{len(rows)} debtors | Grand Total: KES {money(grand)}")
        except Exception as e:
            self.age_status.config(text=f"Error: {str(e)[:80]}")

    def _build_vote(self, parent):
        ctrl = self._date_ctrl(parent, "vt_from", "vt_to", self._load_vote)
        tk.Label(ctrl, text="Votehead:", font=FONT_SM,
                 bg=CLR["bg"]).pack(side="left", padx=(8,0))
        self.vt_vh = tk.StringVar()
        ttk.Entry(ctrl, textvariable=self.vt_vh,
                  font=FONT_SM, width=16).pack(side="left", padx=2)

        cols = ["RecNo","Date","Votehead","Narration","CR (KES)","DR (KES)","Type"]
        self._vt_rows = []
        self.vt_tbl = DataTable(parent, cols)
        self.vt_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.vt_status = tk.Label(parent, text="", font=FONT_SM,
                                  bg=CLR["bg"], anchor="w")
        self.vt_status.pack(fill="x", padx=10)
        self._print_bar(parent, "Vote Transactions",
                        lambda: cols, lambda: self._vt_rows)

    def _load_vote(self):
        try:
            d1 = datetime.datetime.strptime(self.vt_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.vt_to.get(),   "%Y-%m-%d")
        except ValueError:
            return
        vh = f"%{self.vt_vh.get().strip()}%"
        try:
            _, rows = db.fetchall(
                "SELECT TOP 1000 RecNo, TraDate, Votehead, Narration, CR, DR, PT "
                "FROM dbo.VoteT WHERE TraDate BETWEEN ? AND ? AND Votehead LIKE ? "
                "ORDER BY TraDate DESC", (d1, d2, vh))
            fmt = [[r[0], str(r[1])[:10], r[2] or "", r[3] or "",
                    money(r[4]), money(r[5]), r[6] or ""] for r in rows]
            self._vt_rows = fmt; self.vt_tbl.load(fmt)
            tc=sum(float(r[4]) for r in rows if r[4])
            td=sum(float(r[5]) for r in rows if r[5])
            self.vt_status.config(
                text=f"{len(rows)} entries | CR: {money(tc)}  DR: {money(td)}")
        except Exception as e:
            self.vt_status.config(text=f"Error: {str(e)[:80]}")


# ═════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title("FarmersDesk Ltd – Desktop Application")
        self.configure(bg=CLR["bg"])
        self.geometry("1280x780")
        self.minsize(1000, 650)

        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame",      background=CLR["bg"])
        s.configure("TNotebook",   background=CLR["bg"])
        s.configure("TNotebook.Tab", font=FONT_SM, padding=[12,5],
                    background=CLR["border"], foreground=CLR["text_dark"])
        s.map("TNotebook.Tab",
              background=[("selected", CLR["accent"])],
              foreground=[("selected", CLR["white"])])

        self._show_login()

    def _show_login(self):
        login = LoginWindow(self)
        self.wait_window(login)
        if not login.authenticated_user:
            self.destroy(); return
        self.current_user = login.authenticated_user
        self._build_main()
        self.deiconify()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"1280x780+{(sw-1280)//2}+{(sh-780)//2}")

    def _build_main(self):
        uname = self.current_user["name"]

        # Header
        hdr = tk.Frame(self, bg=CLR["header"], height=56)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="🌾  FarmersDesk Ltd", font=FONT_H1,
                 bg=CLR["header"], fg=CLR["white"]).pack(side="left", padx=20)
        tk.Label(hdr, text=f"👤  {uname}   |   "
                            f"{datetime.date.today().strftime('%d %b %Y')}",
                 font=FONT_SM, bg=CLR["header"],
                 fg=CLR["white"]).pack(side="right", padx=20)
        cfg_btn = tk.Button(hdr, text="🖨 Printer",
                            command=self._open_printer_cfg,
                            font=FONT_SM, bg=CLR["accent"],
                            fg=CLR["white"], relief="flat",
                            padx=10, pady=4, cursor="hand2")
        cfg_btn.pack(side="right", padx=8)

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=4, pady=4)

        # Create dashboard first so we can pass its refresh to CreateSales
        self._dashboard = DashboardFrame(nb, uname)
        self._dashboard.configure(style="TFrame")
        nb.add(self._dashboard, text="  🏠 Dashboard  ")

        # CreateSales gets a callback to refresh dashboard after saving
        sales_frame = CreateSalesFrame(nb, uname,
                                       on_sale_saved=self._dashboard.refresh)
        sales_frame.configure(style="TFrame")
        nb.add(sales_frame, text="  🛒 Create Sales  ")

        for label, FrameClass, args in [
            ("💳 Transactions",     TransactionsFrame,    (uname,)),
            ("📦 Items",            ItemsFrame,           ()),
            ("👥 Credit Customers", CreditCustomersFrame, (uname,)),
            ("🏭 Suppliers",        SuppliersFrame,       (uname,)),
            ("🗄️ Inventory",        InventoryFrame,       (uname,)),
            ("💰 Payments",         PaymentsFrame,        (uname,)),
            ("📊 Reports",          ReportsFrame,         (uname,)),
        ]:
            frame = FrameClass(nb, *args)
            frame.configure(style="TFrame")
            nb.add(frame, text=f"  {label}  ")

        # Status bar
        sb = tk.Frame(self, bg=CLR["border"], height=22)
        sb.pack(fill="x", side="bottom"); sb.pack_propagate(False)
        tk.Label(sb,
                 text=(f"  {DB_CONFIG['server']} / {DB_CONFIG['database']}"
                       f"   |   User: {uname}"),
                 font=FONT_SM, bg=CLR["border"],
                 fg=CLR["text_dark"]).pack(side="left")

    def _open_printer_cfg(self):
        global _printer_cfg
        dlg = PrinterConfigDialog(self, _printer_cfg)
        self.wait_window(dlg)
        if dlg.result:
            _printer_cfg = dlg.result
            save_printer_cfg(_printer_cfg)

    def on_close(self):
        db.close(); self.destroy()


# ═════════════════════════════════════════════════════════════════════════════
# PRINTING ENGINE
# ═════════════════════════════════════════════════════════════════════════════
try:
    from escpos.printer import Usb, Serial, Network
    ESCPOS_OK = True
except ImportError:
    ESCPOS_OK = False

try:
    import qrcode
    QR_OK = True
except ImportError:
    QR_OK = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                    Paragraph, Spacer, HRFlowable)
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    RL_OK = True
except ImportError:
    RL_OK = False


class PrinterConfigDialog(tk.Toplevel):
    DEFAULTS = {"connection": "USB", "usb_vendor": "0x04B8",
                "usb_product": "0x0202", "serial_port": "COM3",
                "serial_baud": "9600", "net_host": "192.168.1.100",
                "net_port": "9100"}

    def __init__(self, parent, config: dict):
        super().__init__(parent)
        self.title("Thermal Printer Settings")
        self.resizable(False, False)
        self.configure(bg=CLR["bg"])
        self.grab_set()
        self.result = None
        self.cfg = {**self.DEFAULTS, **config}
        self._build()

    def _build(self):
        tk.Label(self, text="Thermal Printer Settings",
                 font=FONT_H2, bg=CLR["bg"],
                 fg=CLR["text_dark"]).pack(pady=(12,6), padx=20)

        f = tk.Frame(self, bg=CLR["bg"], padx=20, pady=8)
        f.pack(fill="both")

        tk.Label(f, text="Connection:", font=FONT_SM,
                 bg=CLR["bg"]).grid(row=0, column=0, sticky="e", pady=4)
        self.conn_var = tk.StringVar(value=self.cfg["connection"])
        cb = ttk.Combobox(f, textvariable=self.conn_var, width=16,
                          values=["USB","Serial","Network"], state="readonly")
        cb.grid(row=0, column=1, sticky="w", padx=8, pady=4)
        cb.bind("<<ComboboxSelected>>", lambda _: self._toggle())

        def make_lf(text, row):
            lf = tk.LabelFrame(f, text=text, bg=CLR["bg"], font=FONT_SM)
            lf.grid(row=row, column=0, columnspan=2, sticky="ew", pady=4)
            return lf

        usb = make_lf("USB Settings", 1)
        self.usb_frame = usb
        for i, (lbl, attr, val) in enumerate([
            ("Vendor ID (hex):", "usb_vendor",  self.cfg["usb_vendor"]),
            ("Product ID (hex):","usb_product", self.cfg["usb_product"]),
        ]):
            tk.Label(usb, text=lbl, font=FONT_SM, bg=CLR["bg"]).grid(
                row=i, column=0, sticky="e", padx=4, pady=3)
            e = ttk.Entry(usb, width=12); e.insert(0, val)
            e.grid(row=i, column=1, sticky="w", padx=4, pady=3)
            setattr(self, attr.replace(".","_"), e)

        ser = make_lf("Serial Settings", 2)
        self.ser_frame = ser
        for i, (lbl, attr, val) in enumerate([
            ("COM Port:", "ser_port", self.cfg["serial_port"]),
            ("Baud Rate:", "ser_baud", self.cfg["serial_baud"]),
        ]):
            tk.Label(ser, text=lbl, font=FONT_SM, bg=CLR["bg"]).grid(
                row=i, column=0, sticky="e", padx=4, pady=3)
            e = ttk.Entry(ser, width=12); e.insert(0, val)
            e.grid(row=i, column=1, sticky="w", padx=4, pady=3)
            setattr(self, attr, e)

        net = make_lf("Network Settings", 3)
        self.net_frame = net
        for i, (lbl, attr, val) in enumerate([
            ("IP Address:", "net_host", self.cfg["net_host"]),
            ("Port:",       "net_port", self.cfg["net_port"]),
        ]):
            tk.Label(net, text=lbl, font=FONT_SM, bg=CLR["bg"]).grid(
                row=i, column=0, sticky="e", padx=4, pady=3)
            e = ttk.Entry(net, width=16); e.insert(0, val)
            e.grid(row=i, column=1, sticky="w", padx=4, pady=3)
            setattr(self, attr, e)

        btn_row = tk.Frame(f, bg=CLR["bg"])
        btn_row.grid(row=4, column=0, columnspan=2, pady=10)
        test = tk.Button(btn_row, text="🖨 Test Print", command=self._test)
        style_btn(test); test.pack(side="left", padx=4)
        save = tk.Button(btn_row, text="💾 Save", command=self._save)
        style_btn(save, success=True); save.pack(side="left", padx=4)
        tk.Button(btn_row, text="Cancel", command=self.destroy,
                  font=FONT_SM).pack(side="left", padx=4)
        self._toggle()

    def _toggle(self):
        conn = self.conn_var.get()
        for frame, show in [
            (self.usb_frame, conn=="USB"),
            (self.ser_frame, conn=="Serial"),
            (self.net_frame, conn=="Network"),
        ]:
            frame.grid() if show else frame.grid_remove()

    def _save(self):
        self.result = {
            "connection":  self.conn_var.get(),
            "usb_vendor":  self.usb_vendor.get().strip(),
            "usb_product": self.usb_product.get().strip(),
            "serial_port": self.ser_port.get().strip(),
            "serial_baud": self.ser_baud.get().strip(),
            "net_host":    self.net_host.get().strip(),
            "net_port":    self.net_port.get().strip(),
        }
        self.destroy()

    def _test(self):
        self._save()
        p = _open_printer(self.result) if self.result else None
        if p:
            try:
                p.set(align="center", bold=True)
                p.text("FarmersDesk Ltd\n")
                p.set(align="center", bold=False)
                p.text("*** TEST PRINT OK ***\n\n")
                p.cut()
                messagebox.showinfo("Test", "Test print sent.")
            except Exception as e:
                messagebox.showerror("Print Error", str(e))
            finally:
                try: p.close()
                except Exception: pass
        else:
            messagebox.showerror("Failed", "Could not connect to printer.")


def _open_printer(cfg: dict):
    if not ESCPOS_OK:
        messagebox.showerror("Missing",
                             "python-escpos not installed.\n"
                             "pip install python-escpos")
        return None
    try:
        conn = cfg.get("connection","USB")
        if conn == "USB":
            return Usb(int(cfg.get("usb_vendor","0x04B8"),16),
                       int(cfg.get("usb_product","0x0202"),16))
        elif conn == "Serial":
            return Serial(cfg.get("serial_port","COM3"),
                          baudrate=int(cfg.get("serial_baud",9600)))
        else:
            return Network(cfg.get("net_host","192.168.1.100"),
                           port=int(cfg.get("net_port",9100)))
    except Exception as e:
        messagebox.showerror("Printer Error", f"Cannot open printer:\n{e}")
        return None


def _make_qr_image(data: str):
    if not QR_OK:
        return None
    try:
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_M,
                           box_size=4, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black",
                             back_color="white").convert("RGB")
    except Exception:
        return None


W = 48

def _line(ch="-") -> str:
    return ch * W + "\n"

def _two_col(left: str, right: str, width=W) -> str:
    gap = max(1, width - len(left) - len(right))
    return left + " " * gap + right + "\n"


def print_sale_receipt(cfg: dict, sale: dict, items: List[Dict]):
    p = _open_printer(cfg)
    if not p:
        return
    try:
        p.set(align="center", bold=True, double_height=True, double_width=True)
        p.text(COMPANY["name"] + "\n")
        p.set(align="center", bold=False, double_height=False, double_width=False)
        p.text(COMPANY["address"] + "\n")
        p.text(f"Tel: {COMPANY['phone']}\n")
        p.text(f"PIN: {COMPANY['pin']}\n")
        p.text(_line("="))
        p.set(align="left")
        p.text(_two_col("Receipt No:", str(sale.get("trano",""))))
        p.text(_two_col("Date:",       str(sale.get("date",""))[:19]))
        p.text(_two_col("Cashier:",    str(sale.get("cashier",""))))
        cust = sale.get("customer","")
        if cust and cust != "Walk-in":
            p.text(_two_col("Customer:", str(cust)))
        p.text(_line())
        p.set(bold=True); p.text(_two_col("ITEM","TOTAL")); p.set(bold=False)
        p.text(_line())

        subtotal = 0.0; total_vat = 0.0
        qr_parts = [f"FDL|{sale.get('trano','')}"]
        for it in items:
            name  = str(it.get("name",""))[:22]
            qty   = it.get("qty",1)
            price = float(it.get("price",0))
            tot   = float(it.get("total", price*float(qty)))
            vat   = float(it.get("vat",0))
            subtotal += tot; total_vat += vat
            p.text(f"  {name}\n")
            p.text(_two_col(f"  {qty} x {money(price)}", f"KES {money(tot)}"))
            qr_parts.append(f"{it.get('code','')}:{name}:{qty}:{price}")

        p.text(_line())
        p.text(_two_col("Subtotal (excl VAT):", f"KES {money(subtotal-total_vat)}"))
        p.text(_two_col("VAT (16%):",           f"KES {money(total_vat)}"))
        p.set(bold=True)
        p.text(_two_col("TOTAL:", f"KES {money(subtotal)}"))
        p.set(bold=False); p.text(_line())

        cash = float(sale.get("cash",0))
        change = float(sale.get("change",0))
        if cash:
            p.text(_two_col("Cash Tendered:", f"KES {money(cash)}"))
            p.text(_two_col("Change:",        f"KES {money(change)}"))
            p.text(_line())

        qr_parts.append(f"TOTAL:{money(subtotal)}")
        qr_img = _make_qr_image("|".join(qr_parts))
        if qr_img:
            p.set(align="center")
            p.image(qr_img)
            p.text("Scan to verify prices\n")

        p.set(align="center")
        p.text(_line("="))
        p.text("Thank you for your business!\n")
        p.text(f"{COMPANY['email']}\n")
        p.text(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
        p.text("\n\n\n"); p.cut()
    except Exception as e:
        messagebox.showerror("Print Error", str(e))
    finally:
        try: p.close()
        except Exception: pass


def print_payment_receipt(cfg: dict, payment: dict):
    p = _open_printer(cfg)
    if not p:
        return
    try:
        p.set(align="center", bold=True, double_height=True, double_width=True)
        p.text(COMPANY["name"] + "\n")
        p.set(align="center", bold=False, double_height=False, double_width=False)
        p.text(COMPANY["address"] + "\n")
        p.text(_line("="))
        p.set(align="center", bold=True); p.text("PAYMENT RECEIPT\n")
        p.set(align="left", bold=False); p.text(_line())
        p.text(_two_col("Receipt No:", str(payment.get("payno",""))))
        p.text(_two_col("Date:",       str(payment.get("date",""))[:19]))
        p.text(_two_col("Customer:",   str(payment.get("customer",""))))
        p.text(_line())
        p.set(bold=True)
        p.text(_two_col("Amount Paid:", f"KES {money(payment.get('amount',0))}"))
        p.set(bold=False)
        p.text(_two_col("Mode:", str(payment.get("mode","CASH"))))
        cq = payment.get("chequeno","")
        if cq:
            p.text(_two_col("Cheque No:", str(cq)))
        p.text(_two_col("New Balance:", f"KES {money(payment.get('balance',0))}"))
        p.text(_line())

        qr_data = (f"FDL-PAY|{payment.get('payno','')}|"
                   f"{payment.get('customer','')}|"
                   f"AMT:{money(payment.get('amount',0))}|"
                   f"BAL:{money(payment.get('balance',0))}")
        qr_img = _make_qr_image(qr_data)
        if qr_img:
            p.set(align="center"); p.image(qr_img)
            p.text("Scan to verify payment\n")

        p.set(align="center")
        p.text(_line("="))
        p.text("Thank you!\n")
        p.text(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
        p.text("\n\n\n"); p.cut()
    except Exception as e:
        messagebox.showerror("Print Error", str(e))
    finally:
        try: p.close()
        except Exception: pass


def _rl_color(h: str):
    h = h.lstrip("#")
    return colors.Color(int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255)


def _build_pdf(filepath: str, title: str, columns: List[str],
               rows: List[List], subtitle: str = "",
               summary_rows=None) -> bool:
    if not RL_OK:
        messagebox.showerror("Missing", "pip install reportlab")
        return False

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            leftMargin=15*mm, rightMargin=15*mm,
                            topMargin=15*mm, bottomMargin=15*mm)
    accent = _rl_color("#1A3C5E"); light = _rl_color("#EAF2FF")
    white  = colors.white;         dark  = _rl_color("#1A1A2E")

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Normal"], fontSize=16,
                         textColor=accent, fontName="Helvetica-Bold",
                         alignment=TA_CENTER, spaceAfter=2)
    h2 = ParagraphStyle("h2", parent=styles["Normal"], fontSize=10,
                         textColor=dark, fontName="Helvetica",
                         alignment=TA_CENTER, spaceAfter=2)

    story = [
        Paragraph(COMPANY["name"], h1),
        Paragraph(f"{COMPANY['address']}  |  {COMPANY['phone']}  |  "
                  f"{COMPANY['email']}", h2),
        HRFlowable(width="100%", thickness=2, color=accent, spaceAfter=6),
        Paragraph(title, ParagraphStyle("t", parent=styles["Normal"],
                  fontSize=13, fontName="Helvetica-Bold", textColor=accent,
                  alignment=TA_CENTER, spaceAfter=2)),
    ]
    if subtitle:
        story.append(Paragraph(subtitle, h2))
    story.append(Paragraph(
        f"Generated: {datetime.datetime.now().strftime('%d %b %Y  %H:%M')}",
        ParagraphStyle("g", parent=styles["Normal"], fontSize=8,
                       textColor=colors.grey, alignment=TA_CENTER)))
    story.append(Spacer(1, 5*mm))

    usable_w = A4[0] - 30*mm
    col_w    = [usable_w / max(len(columns),1)] * len(columns)

    hdr_row = [Paragraph(f"<b>{c}</b>",
                         ParagraphStyle("th", parent=styles["Normal"],
                                        fontSize=8, textColor=white,
                                        fontName="Helvetica-Bold",
                                        alignment=TA_CENTER))
               for c in columns]
    tdata = [hdr_row] + [
        [Paragraph(str(cell) if cell is not None else "",
                   ParagraphStyle("td", parent=styles["Normal"],
                                  fontSize=7, textColor=dark,
                                  fontName="Helvetica"))
         for cell in r] for r in rows]

    tbl = Table(tdata, colWidths=col_w, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  accent),
        ("TEXTCOLOR",     (0,0), (-1,0),  white),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [white, light]),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.lightgrey),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    story.append(tbl)

    if summary_rows:
        story += [Spacer(1, 5*mm),
                  HRFlowable(width="100%", thickness=1, color=accent, spaceAfter=4)]
        for label, value in summary_rows:
            story.append(Paragraph(f"<b>{label}</b>  {value}",
                                   ParagraphStyle("sum", parent=styles["Normal"],
                                                  fontSize=9, fontName="Helvetica",
                                                  alignment=TA_RIGHT)))

    story += [Spacer(1, 8*mm),
              HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey),
              Paragraph(f"{COMPANY['name']}  –  Confidential",
                        ParagraphStyle("ft", parent=styles["Normal"],
                                       fontSize=7, textColor=colors.grey,
                                       alignment=TA_CENTER))]
    doc.build(story)
    return True


def save_pdf(title: str, columns: List[str], rows: List[List],
             subtitle: str = "", summary_rows=None, parent_window=None):
    filepath = filedialog.asksaveasfilename(
        parent=parent_window, title="Save Report as PDF",
        defaultextension=".pdf",
        filetypes=[("PDF files","*.pdf"),("All files","*.*")],
        initialfile=re.sub(r"[^\w]","_",title) + ".pdf")
    if not filepath:
        return
    if _build_pdf(filepath, title, columns, rows, subtitle, summary_rows):
        messagebox.showinfo("Saved", f"PDF saved:\n{filepath}")
        try:
            os.startfile(filepath)
        except Exception:
            try:
                subprocess.Popen(["xdg-open", filepath])
            except Exception:
                pass


def direct_print_pdf(title: str, columns: List[str], rows: List[List],
                     subtitle: str = "", summary_rows=None, parent_window=None):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as fh:
        filepath = fh.name
    if not _build_pdf(filepath, title, columns, rows, subtitle, summary_rows):
        return
    try:
        import win32api
        win32api.ShellExecute(0, "print", filepath, None, ".", 0)
        messagebox.showinfo("Printing", "Report sent to default A4 printer.")
    except ImportError:
        try:
            subprocess.run(["lp", filepath], check=True)
            messagebox.showinfo("Printing", "Report sent to printer.")
        except Exception as e:
            messagebox.showerror("Print Error",
                f"Could not print.\n{e}\nTry 'Save PDF' instead.")
    except Exception as e:
        messagebox.showerror("Print Error", str(e))


# ─────────────────────────────────────────────────────────────────────────────
# APPLICATION ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Initialize your main Tkinter window dashboard
    root = tk.Tk()
    
    # Run the application interface loop
    # (Assuming your main layout class or function is named main() or similar)
    # app = FarmersDeskApp(root) 
    
    root.mainloop()
