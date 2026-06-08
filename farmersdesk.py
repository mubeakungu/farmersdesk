"""
FarmersDesk Ltd – Desktop Application  v4
Tkinter + pyodbc  |  SQL Server: FarmersDeskLtd

FIXES in v4 (aligned to live DB schema from diagnostic):
  FIX1  Sale_Item INSERT now includes itemcost (was crashing all new sales)
  FIX2  Sale_Deleted SELECT column order corrected (SoldTo/total were swapped)
  FIX3  SaleTime/CB Tm parsed correctly (stored as 1899-12-30 HH:MM:SS datetime)
  FIX4  CItem query updated (CNoteNo column added to display)
  FIX5  DamagedStock column order fixed (BP is last col, not 6th)
  FIX6  Credit sales filter fixed (tratype == 'CREDIT' exact match)
  FIX7  Reconcile uses actual live column names
  FIX8  SPay/Expiry/Reconcile show "(empty)" note since they have 0 rows
  FIX9  Stock_item vat values are YES/NO/EXEMPT not A/B/C
  FIX10 SCard uses DBy not DoneBy
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyodbc
import datetime
import json
import os
import re
import subprocess
import tempfile
from typing import Optional, List, Dict

PRINT_OK = True

PRINTER_CFG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "printer_cfg.json")

def load_printer_cfg() -> dict:
    try:
        return json.load(open(PRINTER_CFG_FILE))
    except Exception:
        return {"connection": "USB", "usb_vendor": "0x04B8",
                "usb_product": "0x0202", "serial_port": "COM3",
                "serial_baud": "9600", "net_host": "192.168.1.232",
                "net_port": "9100"}

def save_printer_cfg(cfg: dict):
    try:
        json.dump(cfg, open(PRINTER_CFG_FILE, "w"), indent=2)
    except Exception:
        pass

_printer_cfg: dict = load_printer_cfg()

DB_CONFIG = {
    "driver":   "ODBC Driver 17 for SQL Server",
    "server":   "192.168.1.254\\FARMERSDESKLTD",
    "database": "FarmersDeskLtd",
    "trusted":  False,
    "uid":      "pos",
    "pwd":      "PosApp@2026",
}


CLR = {
    "bg": "#F0F4F8", "header": "#1A3C5E", "accent": "#2E86AB",
    "btn": "#2E86AB", "btn_hover": "#1B6CA8", "danger": "#C0392B",
    "success": "#27AE60", "white": "#FFFFFF", "row_odd": "#EAF2FF",
    "row_even": "#FFFFFF", "text_dark": "#1A1A2E", "border": "#CBD5E0",
}

FONT_H1   = ("Helvetica Neue", 18, "bold")
FONT_H2   = ("Helvetica Neue", 13, "bold")
FONT_BODY = ("Helvetica Neue", 11)
FONT_SM   = ("Helvetica Neue", 10)

COMPANY = {
    "name":    "FarmersDesk Ltd",
    "address": "P.O. Box 26719-00504, Nairobi, Kenya",
    "phone":   "+254 740129670",
    "email":   "info@farmersdesk.co.ke",
    "pin":     "P051513622V",
}


class Database:
    def __init__(self):
        self.conn: Optional[object] = None

    def connect(self) -> bool:
        try:
            c = DB_CONFIG
            cs = (f"DRIVER={{{c['driver']}}};SERVER={c['server']};"
                  f"DATABASE={c['database']};UID={c['uid']};PWD={c['pwd']};")
            self.conn = pyodbc.connect(cs, timeout=10)
            return True
        except pyodbc.Error as e:
            print(f"Connection error: {e}")
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
        return cols, [list(r) for r in cur.fetchall()]

    def fetchone(self, sql: str, params=()):
        cur = self.cursor()
        cur.execute(sql, params)
        return cur.fetchone()

    def close(self):
        if self.conn:
            self.conn.close()


db = Database()


def style_btn(btn: tk.Button, danger=False, success=False, **kwargs):
    # Safely extract 'accent' if passed, defaulting to False if not present
    accent = kwargs.pop('accent', False)
    
    # Determine background color based on flags
    if danger:
        color = CLR["danger"]
    elif success:
        color = CLR["success"]
    elif accent:
        color = CLR["btn"]  # Or map this to an explicit CLR["accent"] if defined
    else:
        color = CLR["btn"]
        
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

def extract_time(val) -> str:
    """
    FIX3: SaleTime/Tm stored as datetime with 1899-12-30 base.
    E.g. '1899-12-30 15:08:21' -> '15:08:21'
    """
    if val is None:
        return ""
    m = re.search(r'(\d{1,2}:\d{2}:\d{2})', str(val))
    return m.group(1) if m else ""


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
        self.rowconfigure(0, weight=1); self.columnconfigure(0, weight=1)

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


class FormDialog(tk.Toplevel):
    def __init__(self, parent, title: str, fields: list, initial: dict = None):
        super().__init__(parent)
        self.title(title); self.resizable(False, False)
        self.configure(bg=CLR["bg"]); self.grab_set()
        self.result: Optional[dict] = None
        self.fields = fields; self.initial = initial or {}; self._vars = {}
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
            row = tk.Frame(body, bg=CLR["bg"]); row.pack(fill="x", pady=3)
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
        bf = tk.Frame(self, bg=CLR["bg"]); bf.pack(pady=12)
        ok = tk.Button(bf, text="✔  Save", command=self._save)
        style_btn(ok, success=True); ok.pack(side="left", padx=6)
        tk.Button(bf, text="Cancel", command=self.destroy,
                  font=FONT_SM).pack(side="left", padx=6)

    def _save(self):
        self.result = {k: v.get().strip() for k, v in self._vars.items()}
        self.destroy()


# ═════════════════════════════════════════════════════════════════════════════
# LOGIN
# ═════════════════════════════════════════════════════════════════════════════
class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent; self.authenticated_user = None
        self.title("FarmersDesk – Login"); self.resizable(False, False)
        self.configure(bg=CLR["bg"])
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"380x420+{(sw-380)//2}+{(sh-420)//2}")
        self.grab_set(); self._build()
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
        ttk.Checkbutton(body, text="Show password", variable=self.show_pw,
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
        self._build(); self.refresh()

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
        self._del_rows = []
        self._build()

    def _build(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=4, pady=4)
        
        live_tab = ttk.Frame(nb)
        nb.add(live_tab, text="   📋 Live Transactions   ")
        self._build_live_tab(live_tab)
        
        if self.current_user.lower() == "admin":
            del_tab = ttk.Frame(nb)
            nb.add(del_tab, text="   🗑 Deleted Sales Logs   ")
            self._build_deleted_tab(del_tab)

    def _build_live_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8)
        ctrl.pack(fill="x")
        
        tk.Label(ctrl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.dfrom = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.dfrom.insert(0, month_start())
        self.dfrom.pack(side="left", padx=2)
        
        tk.Label(ctrl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.dto = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.dto.insert(0, today_str())
        self.dto.pack(side="left", padx=2)
        
        tk.Label(ctrl, text="Cashier:", font=FONT_SM, bg=CLR["bg"]).pack(side="left", padx=(8,0))
        self.cashier_var = tk.StringVar()
        
        if self.current_user.lower() == "admin":
            ttk.Entry(ctrl, textvariable=self.cashier_var, font=FONT_SM, width=14).pack(side="left", padx=2)
        else:
            self.cashier_var.set(self.current_user)
            ttk.Entry(ctrl, textvariable=self.cashier_var, font=FONT_SM, width=14, state="disabled").pack(side="left", padx=2)
            
        load = tk.Button(ctrl, text="📋 Load Ledger", command=self._load)
        style_btn(load)
        load.pack(side="left", padx=6)
        
        del_btn = tk.Button(ctrl, text="🗑 Delete Selected", command=self._delete_transaction)
        style_btn(del_btn, danger=True)
        del_btn.pack(side="left", padx=4)
        
        cols = ["TraNo", "Date", "Time", "Type", "Cashier", "Total (KES)", "Sold To"]
        self.tbl = DataTable(parent, cols)
        self.tbl.pack(fill="both", expand=True, padx=10, pady=4)
        
        self.status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.status.pack(fill="x", padx=10)
        
        pbf = tk.Frame(parent, bg=CLR["bg"])
        pbf.pack(anchor="e", padx=10, pady=4)
        
        for txt, cmd, kw in [
            ("💾 Save PDF", self._save_pdf, {}),
            ("🖨 Print A4", self._print_a4, {"success": True}),
            ("🧾 Reprint Receipt", self._reprint, {}),
        ]:
            b = tk.Button(pbf, text=txt, command=cmd)
            b.config(font=FONT_SM, relief="flat", padx=12, pady=5, cursor="hand2",
                     bg=CLR["success"] if kw.get("success") else CLR["btn"], fg=CLR["white"])
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
        
        lb = tk.Button(ctrl, text="📋 Load Archives", command=self._load_deleted)
        style_btn(lb)
        lb.pack(side="left", padx=6)
        
        tk.Label(ctrl, text="⚠️ Admin Forensic Audit – Deleted Records", font=FONT_SM, bg=CLR["bg"], fg=CLR["danger"]).pack(side="left", padx=12)
        
        cols = ["DelId", "TraNo", "Sale Date", "Type", "Cashier", "Total (KES)", "Sold To", "Deleted At"]
        self.del_tbl = DataTable(parent, cols)
        self.del_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        
        self.del_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.del_status.pack(fill="x", padx=10)
        
        pbf = tk.Frame(parent, bg=CLR["bg"])
        pbf.pack(anchor="e", padx=10, pady=4)
        
        for txt, col, cmd in [
            ("💾 Save PDF", CLR["btn"], lambda: save_pdf("Deleted Sales", cols, self._del_rows, parent_window=self.winfo_toplevel())),
            ("🖨 Print A4", CLR["success"], lambda: direct_print_pdf("Deleted Sales", cols, self._del_rows, parent_window=self.winfo_toplevel())),
        ]:
            tk.Button(pbf, text=txt, command=cmd, bg=col, fg=CLR["white"], font=FONT_SM, relief="flat", padx=12, pady=5, cursor="hand2").pack(side="left", padx=4)
            
        self._load_deleted()

    def _load(self):
        self._last_rows = []
        try:
            d1 = datetime.datetime.strptime(self.dfrom.get().strip(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.dto.get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Dates must conform to YYYY-MM-DD pattern."); return
            
        is_admin = self.current_user.lower() == "admin"
        cashier_filter = f"%{self.cashier_var.get().strip()}%" if is_admin else self.current_user
        
        try:
            if is_admin:
                _, rows = db.fetchall(
                    "SELECT TOP 1000 TraNo, tradate, SaleTime, tratype, cashier, total, SoldTo "
                    "FROM dbo.Sale WHERE CAST(tradate AS DATE) BETWEEN ? AND ? "
                    "AND cashier LIKE ? ORDER BY tradate DESC, TraNo DESC",
                    (d1.date(), d2.date(), cashier_filter))
            else:
                _, rows = db.fetchall(
                    "SELECT TOP 1000 TraNo, tradate, SaleTime, tratype, cashier, total, SoldTo "
                    "FROM dbo.Sale WHERE CAST(tradate AS DATE) BETWEEN ? AND ? "
                    "AND cashier = ? ORDER BY tradate DESC, TraNo DESC",
                    (d1.date(), d2.date(), cashier_filter))
                    
            fmt = [[r[0], str(r[1])[:10], extract_time(r[2]), r[3] or "", r[4] or "", money(r[5]), r[6] or ""] for r in rows]
            self._last_rows = fmt
            self.tbl.load(fmt)
            
            total = sum(float(r[5]) for r in rows if r[5])
            self.status.config(text=f"Total Records: {len(rows)} Transactions | Combined Aggregation: KES {money(total)}")
        except Exception as e:
            self.status.config(text=f"Database Read Exception: {str(e)[:100]}")

    def _load_deleted(self):
        self._del_rows = []
        try:
            d1 = datetime.datetime.strptime(self.del_from.get().strip(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.del_to.get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Dates must conform to YYYY-MM-DD pattern."); return
            
        try:
            _, rows = db.fetchall(
                "SELECT DelId, TraNo, tradate, tratype, cashier, total, SoldTo, DeletedAt "
                "FROM dbo.Sale_Deleted WHERE CAST(tradate AS DATE) BETWEEN ? AND ? "
                "ORDER BY DeletedAt DESC", (d1.date(), d2.date()))
                
            fmt = [[r[0], r[1], str(r[2])[:10], r[3] or "", r[4] or "", money(r[5]), r[6] or "", str(r[7])[:19]] for r in rows]
            self._del_rows = fmt
            self.del_tbl.load(fmt)
            
            total = sum(float(r[5]) for r in rows if r[5])
            self.del_status.config(text=f"Archived Data Points: {len(rows)} Records | Cumulative Purged Value: KES {money(total)}")
        except Exception as e:
            self.del_status.config(text=f"Database Read Exception: {str(e)[:100]}")

    def _delete_transaction(self):
        vals = self.tbl.selected_values()
        if not vals:
            messagebox.showinfo("Selection Conflict", "Identify and select an active ledger record from the data grid."); return
            
        trano = vals[0]
        if not messagebox.askyesno("Critical Operation Confirm", f"Are you sure you want to permanently delete transaction #{trano}?\nThis action rolls back physical store quantities."): 
            return
            
        try:
            # Step 1: Secure a local deep-copy profile of the target transaction metadata for audit trailing
            sale = db.fetchone("SELECT TraNo, tradate, tratype, cashier, SoldTo, total, vat, cash FROM dbo.Sale WHERE TraNo=?", (trano,))
            if not sale:
                messagebox.showerror("Fault", "Transaction context could not be resolved inside current workspace registry."); return
                
            # Step 2: Route critical metrics into the secure backup log matrix
            db.execute(
                "INSERT INTO dbo.Sale_Deleted (TraNo, tradate, tratype, cashier, SoldTo, total, vat, cash, DeletedAt) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (sale[0], sale[1], sale[2], sale[3], sale[4], sale[5], sale[6], sale[7], datetime.datetime.now())
            )
            
            # Step 3: Parse child components, loop inventory elements, and reverse physical store tracking counts
            _, items = db.fetchall("SELECT ItemCode, qty FROM dbo.Sale_Item WHERE trano=?", (trano,))
            for item in items:
                db.execute("UPDATE dbo.Stock_item SET qtystock = qtystock + ? WHERE pcode=?", (item[1] or 0, item[0]))
                
            # Step 4: Safely wipe database relationships
            db.execute("DELETE FROM dbo.Sale_Item WHERE trano=?", (trano,))
            db.execute("DELETE FROM dbo.Sale WHERE TraNo=?", (trano,))
            
            messagebox.showinfo("Operation Terminated", f"Transaction #{trano} successfully wiped and shifted to forensics archive.")
            self._load()
            if self.current_user.lower() == "admin":
                self._load_deleted()
        except Exception as e:
            messagebox.showerror("Execution Fault", f"Transaction wipe trace aborted: {str(e)}")

    def _save_pdf(self):
        if not self._last_rows:
            messagebox.showwarning("Empty Report", "No transaction metrics loaded in the current dataset views."); return
        save_pdf("Transactions Report", ["TraNo", "Date", "Time", "Type", "Cashier", "Total (KES)", "Sold To"], self._last_rows, parent_window=self.winfo_toplevel())

    def _print_a4(self):
        if not self._last_rows:
            messagebox.showwarning("Empty Report", "No transaction metrics loaded in the current dataset views."); return
        direct_print_pdf("Transactions Report", ["TraNo", "Date", "Time", "Type", "Cashier", "Total (KES)", "Sold To"], self._last_rows, parent_window=self.winfo_toplevel())

    def _reprint(self):
        vals = self.tbl.selected_values()
        if not vals:
            messagebox.showinfo("Selection Conflict", "Select a valid historical row to send data back to receipt buffer spool."); return
        trano = vals[0]
        try:
            row = db.fetchone("SELECT TraNo, tradate, cashier, SoldTo, cash, change, total FROM dbo.Sale WHERE TraNo=?", (trano,))
            if not row:
                messagebox.showwarning("Reference Fault", f"Transaction record identity #{trano} does not exist."); return
                
            sale = {"trano": row[0], "date": str(row[1])[:19], "cashier": row[2] or "", "customer": row[3] or "", "cash": row[4] or 0, "change": row[5] or 0, "total": row[6] or 0, "invno": ""}
            
            _, irows = db.fetchall("SELECT ItemCode, ItemName, qty, CASE WHEN qty>0 THEN total/qty ELSE 0 END, total FROM dbo.Sale_Item WHERE trano=?", (trano,))
            items = [{"code": r[0], "name": r[1] or "", "qty": r[2] or 1, "price": r[3] or 0, "total": r[4] or 0} for r in irows]
            
            print_sale_receipt(_printer_cfg, sale, items)
        except Exception as e:
            messagebox.showerror("Spooler Error", f"Receipt print operation crashed: {str(e)}")


# ═════════════════════════════════════════════════════════════════════════════
# ITEMS TAB  (CItem)
# ═════════════════════════════════════════════════════════════════════════════
class ItemsFrame(ttk.Frame):
    # Modified signature: username now has a default fallback to prevent 'missing positional argument' crashes
    def __init__(self, parent, username: str = "Admin", on_catalog_changed=None):
        super().__init__(parent)
        self.current_user = username
        self.on_catalog_changed = on_catalog_changed
        self._items_list = []
        self._build()
        self._load_items()

    def _build(self):
        # Header UI setup
        hdr = tk.Frame(self, bg=CLR["header"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="📦  Items Master Registry", font=FONT_H2,
                 bg=CLR["header"], fg=CLR["white"]).pack(side="left", padx=20, pady=10)
        
        main = tk.Frame(self, bg=CLR["bg"])
        main.pack(fill="both", expand=True, padx=10, pady=10)
        main.columnconfigure(0, weight=2)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=1)
        main.rowconfigure(0, weight=1)

        # --- LEFT PANEL: Product Grid Matrix ---
        left = tk.LabelFrame(main, text="Item Registry Matrix", font=FONT_SM, bg=CLR["bg"], fg=CLR["header"])
        left.grid(row=0, column=0, sticky="nsew", padx=4)
        
        sf = tk.Frame(left, bg=CLR["bg"])
        sf.pack(fill="x", padx=8, pady=4)
        tk.Label(sf, text="Search Name/Code:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.item_search = ttk.Entry(sf, width=25)
        self.item_search.pack(side="left", padx=4, fill="x", expand=True)
        self.item_search.bind("<KeyRelease>", lambda _: self._search_items())

        # Grid view matching the rest of your sales management workflow
        item_cols = ["Code", "Item Name", "Stock Level", "Retail (KES)", "Wholesale (KES)"]
        self.item_tbl = DataTable(left, item_cols, height=12)
        self.item_tbl.pack(fill="both", expand=True, padx=8, pady=4)
        self.item_tbl.bind_double(self._on_row_double_click)
        
        # --- MODIFIED: Bind Selection Click for instant item previews without needing to double click ---
        if hasattr(self.item_tbl, "tree"):
            self.item_tbl.tree.bind("<<TreeviewSelect>>", self._on_row_selected)
        elif hasattr(self.item_tbl, "view"):
            self.item_tbl.view.bind("<<TreeviewSelect>>", self._on_row_selected)

        # --- MIDDLE PANEL: Inline Modification Controls ---
        mid = tk.LabelFrame(main, text="Item Operations Profile", font=FONT_SM, bg=CLR["bg"], fg=CLR["header"])
        mid.grid(row=0, column=1, sticky="nsew", padx=4)
        
        self.form_vars = {}
        fields = [
            ("pcode", "Product Code *"), ("name", "Product Name *"), 
            ("category", "Category Group"), ("bp", "Acquisition Cost (Buying Price)"),
            ("spr", "Standard Retail Sale Price"), ("spw", "Wholesale Tier Price"),
            ("qtystock", "Current Store Physical Stock"), ("rlevel", "Safety Re-Order Point")
        ]
        
        form_container = tk.Frame(mid, bg=CLR["bg"])
        form_container.pack(fill="both", expand=True, padx=8, pady=6)
        
        for key, label in fields:
            lbl = tk.Label(form_container, text=label, font=FONT_SM, bg=CLR["bg"], anchor="w")
            lbl.pack(fill="x", padx=4, pady=(4, 0))
            v = tk.StringVar()
            self.form_vars[key] = v
            ent = ttk.Entry(form_container, textvariable=v)
            ent.pack(fill="x", padx=4, pady=2)
            
        tk.Label(form_container, text="VAT Strategy Status:", font=FONT_SM, bg=CLR["bg"], anchor="w").pack(fill="x", padx=4, pady=(4,0))
        self.vat_var = tk.StringVar(value="YES")
        self.vat_combo = ttk.Combobox(form_container, textvariable=self.vat_var, values=["", "YES", "NO", "EXEMPT"], state="readonly")
        self.vat_combo.pack(fill="x", padx=4, pady=2)

        # Button Dashboard Operations
        btn_f = tk.Frame(mid, bg=CLR["bg"])
        btn_f.pack(fill="x", padx=8, pady=8)
        tk.Button(btn_f, text="➕ Create Item", command=self._save_new, bg=CLR["success"], fg=CLR["white"], font=FONT_SM, relief="flat", padx=6, pady=4, cursor="hand2").pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(btn_f, text="✏️ Update Item", command=self._save_update, bg=CLR["btn"], fg=CLR["white"], font=FONT_SM, relief="flat", padx=6, pady=4, cursor="hand2").pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(btn_f, text="🗑 Delete", command=self._delete_item, bg=CLR["danger"], fg=CLR["white"], font=FONT_SM, relief="flat", padx=6, pady=4, cursor="hand2").pack(side="left", padx=2)

        # --- RIGHT PANEL: Catalog Summary Metrics ---
        right = tk.LabelFrame(main, text="Catalog Summary Metrics", font=FONT_SM, bg=CLR["bg"], fg=CLR["header"])
        right.grid(row=0, column=2, sticky="nsew", padx=4)

        self.lbl_count = tk.Label(right, text="Total Profiles: 0 Items", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.lbl_count.pack(fill="x", padx=8, pady=4)
        self.lbl_valuation = tk.Label(right, text="Stock Valuation: KES 0.00", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.lbl_valuation.pack(fill="x", padx=8, pady=4)

        tk.Frame(right, height=2, bg=CLR["border"]).pack(fill="x", padx=8, pady=6)
        
        # --- MODIFIED: Added a Product Inspection Display box inside the right metrics rail ---
        tk.Label(right, text="🔍 Selected Product Inspector:", font=FONT_SM, bg=CLR["bg"], fg=CLR["header"], anchor="w").pack(fill="x", padx=8, pady=(2, 0))
        self.product_inspect_box = tk.Text(right, font=FONT_SM, bg=CLR["bg"], height=5, relief="flat", wrap="word")
        self.product_inspect_box.pack(fill="x", padx=8, pady=(0, 6))
        self.product_inspect_box.insert(tk.END, "No product selected.\nClick any row to view breakdown details.")
        self.product_inspect_box.config(state="disabled")

        tk.Frame(right, height=2, bg=CLR["border"]).pack(fill="x", padx=8, pady=4)
        tk.Label(right, text="Category Groups Distribution:", font=FONT_SM, bg=CLR["bg"], fg=CLR["header"], anchor="w").pack(fill="x", padx=8, pady=2)
        
        self.cat_listbox = tk.Listbox(right, font=FONT_SM, bg=CLR["white"], relief="flat", bd=1, height=8)
        self.cat_listbox.pack(fill="both", expand=True, padx=8, pady=4)

    def _load_items(self):
        try:
            _, rows = db.fetchall("SELECT pcode, name, spr, spw, bp, qtystock, PCategory, RLevel, vat FROM dbo.Stock_item ORDER BY name")
            self._items_list = [{
                "code": str(r[0]), "name": r[1] or "",
                "price_retail": float(r[2]) if r[2] else 0.0,
                "price_wholesale": float(r[3]) if r[3] else 0.0,
                "price_buying": float(r[4]) if r[4] else 0.0,
                "qty_stock": float(r[5]) if r[5] else 0.0,
                "category": r[6] or "", "rlevel": float(r[7]) if r[7] else 0.0, "vat": r[8] or ""
            } for r in rows]
            self._search_items()
            self._update_metrics()
        except Exception as e:
            messagebox.showerror("Data Query Fault", f"Failed to pull active catalog metrics: {e}")

    def _search_items(self):
        term = self.item_search.get().lower()
        filtered = [i for i in self._items_list if term in i["code"].lower() or term in i["name"].lower()] if term else self._items_list
        self.item_tbl.load([[i["code"], i["name"], str(int(i["qty_stock"])), money(i["price_retail"]), money(i["price_wholesale"])] for i in filtered])

    def _on_row_selected(self, event):
        """MODIFIED: Updates the inspector pane instantly when a product row is selected."""
        try:
            table_widget = event.widget
            selected_item = table_widget.selection()
            if not selected_item: return
            
            row_values = table_widget.item(selected_item[0], "values")
            if not row_values: return
            
            item = next((i for i in self._items_list if i["code"] == row_values[0]), None)
            if not item: return

            # Construct display inspector breakdown string
            inspect_text = (
                f"🏷️ Code: {item['code']}\n"
                f"📦 Product: {item['name']}\n"
                f"🗂️ Category: {item['category'] or 'N/A'}\n"
                f"💸 Costs: Retail KES {money(item['price_retail'])} | Wholesale KES {money(item['price_wholesale'])}\n"
                f"📈 Margin Baseline: Buying Price KES {money(item['price_buying'])}"
            )
            
            self.product_inspect_box.config(state="normal")
            self.product_inspect_box.delete("1.0", tk.END)
            self.product_inspect_box.insert(tk.END, inspect_text)
            self.product_inspect_box.config(state="disabled")
        except Exception:
            pass

    def _on_row_double_click(self, *_):
        vals = self.item_tbl.selected_values()
        if not vals: return
        item = next((i for i in self._items_list if i["code"] == vals[0]), None)
        if not item: return
        
        self.form_vars["pcode"].set(item["code"])
        self.form_vars["name"].set(item["name"])
        self.form_vars["category"].set(item["category"])
        self.form_vars["bp"].set(str(item["price_buying"]))
        self.form_vars["spr"].set(str(item["price_retail"]))
        self.form_vars["spw"].set(str(item["price_wholesale"]))
        self.form_vars["qtystock"].set(str(item["qty_stock"]))
        self.form_vars["rlevel"].set(str(item["rlevel"]))
        self.vat_var.set(item["vat"])

    def _update_metrics(self):
        self.lbl_count.config(text=f"Total Profiles: {len(self._items_list)} Items")
        total_value = sum(i["qty_stock"] * i["price_buying"] for i in self._items_list)
        self.lbl_valuation.config(text=f"Asset Valuation: KES {money(total_value)}")
        
        cats = {}
        for i in self._items_list:
            c = i["category"] or "Uncategorized"
            cats[c] = cats.get(c, 0) + 1
        self.cat_listbox.delete(0, tk.END)
        for c, count in sorted(cats.items()):
            self.cat_listbox.insert(tk.END, f"   📁 {c} ({count} items)")

    def _clear_form(self):
        for var in self.form_vars.values(): var.set("")
        self.vat_var.set("YES")
        
        # Clear inspector box safely
        self.product_inspect_box.config(state="normal")
        self.product_inspect_box.delete("1.0", tk.END)
        self.product_inspect_box.insert(tk.END, "No product selected.\nClick any row to view breakdown details.")
        self.product_inspect_box.config(state="disabled")

    def _save_new(self):
        d = {k: v.get().strip() for k, v in self.form_vars.items()}
        d["vat"] = self.vat_var.get()
        if not d["pcode"] or not d["name"]:
            messagebox.showwarning("Validation Error", "Product Code and Name are mandatory configuration tracks."); return
        if any(i["code"] == d["pcode"] for i in self._items_list):
            messagebox.showerror("Conflict", "Product Code key structure already exists inside registry."); return
        try:
            db.execute("INSERT INTO dbo.Stock_item (pcode, name, PCategory, bp, spr, spw, qtystock, RLevel, vat) VALUES (?,?,?,?,?,?,?,?,?)",
                       (d["pcode"], d["name"], d["category"], float(d["bp"] or 0), float(d["spr"] or 0), float(d["spw"] or 0), float(d["qtystock"] or 0), float(d["rlevel"] or 0), d["vat"]))
            messagebox.showinfo("Success", "Product registry entry built successfully.")
            self._load_items(); self._clear_form()
            if self.on_catalog_changed: self.on_catalog_changed()
        except Exception as e: messagebox.showerror("Execution Fault", str(e))

    def _save_update(self):
        d = {k: v.get().strip() for k, v in self.form_vars.items()}
        d["vat"] = self.vat_var.get()
        if not d["pcode"]:
            messagebox.showwarning("Selection Required", "Double-click an item row trace from the registry matrix grid."); return
        try:
            db.execute("UPDATE dbo.Stock_item SET name=?, PCategory=?, bp=?, spr=?, spw=?, qtystock=?, RLevel=?, vat=? WHERE pcode=?",
                       (d["name"], d["category"], float(d["bp"] or 0), float(d["spr"] or 0), float(d["spw"] or 0), float(d["qtystock"] or 0), float(d["rlevel"] or 0), d["vat"], d["pcode"]))
            messagebox.showinfo("Modified", "Product entry settings adjusted.")
            self._load_items(); self._clear_form()
            if self.on_catalog_changed: self.on_catalog_changed()
        except Exception as e: messagebox.showerror("Execution Fault", str(e))

    def _delete_item(self):
        pcode = self.form_vars["pcode"].get().strip()
        name = self.form_vars["name"].get().strip()
        if not pcode:
            messagebox.showinfo("Selection Required", "Select an active item entity."); return
        if not messagebox.askyesno("Confirm Drop Action", f"Completely purge tracking logic for item '{name}'?"): return
        try:
            db.execute("DELETE FROM dbo.Stock_item WHERE pcode=?", (pcode,))
            messagebox.showinfo("Dropped", "Record dropped from inventory metrics tracking.")
            self._load_items(); self._clear_form()
            if self.on_catalog_changed: self.on_catalog_changed()
        except Exception as e: messagebox.showerror("Execution Fault", str(e))
# ═════════════════════════════════════════════════════════════════════════════
# CREATE SALES
# ═════════════════════════════════════════════════════════════════════════════

class CreateSalesFrame(ttk.Frame):
    def __init__(self, parent, username: str, on_sale_saved=None):
        super().__init__(parent)
        self.current_user = username
        self.on_sale_saved = on_sale_saved
        self.cart = []
        self._items_list = []
        self._customers_raw = []
        self._build()
        self._load_customers()
        self._load_items()

    def _build(self):
        # --- HEADER ---
        hdr = tk.Frame(self, bg=CLR["header"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="🛒  Create Sale", font=FONT_H2,
                 bg=CLR["header"], fg=CLR["white"]).pack(side="left", padx=20, pady=10)
        
        # --- MAIN PANEL CONTAINER ---
        main = tk.Frame(self, bg=CLR["bg"])
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Grid Configuration: We let columns 0 and 1 scale, but give Column 2 a fixed-minimum structure
        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=3)
        main.columnconfigure(2, weight=0, minsize=280) # FORCES Sale Summary to never shrink below 280 pixels
        main.rowconfigure(0, weight=1)

        # =====================================================================
        # --- LEFT PANEL: Available Items Selection Matrix ---
        # =====================================================================
        left = tk.LabelFrame(main, text="Available Items", font=FONT_SM,
                             bg=CLR["bg"], fg=CLR["header"])
        left.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        
        sf = tk.Frame(left, bg=CLR["bg"])
        sf.pack(fill="x", padx=8, pady=4)
        
        tk.Label(sf, text="Search:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.item_search = ttk.Entry(sf, width=15)
        self.item_search.pack(side="left", padx=4, fill="x", expand=True)
        self.item_search.bind("<KeyRelease>", lambda _: self._search_items())
        
        tk.Label(sf, text="Sell As:", font=FONT_SM, bg=CLR["bg"]).pack(side="left", padx=(10, 2))
        self.quick_tier = tk.StringVar(value="Retail")
        tier_combo = ttk.Combobox(sf, textvariable=self.quick_tier, values=["Retail", "Wholesale"], width=10, state="readonly")
        tier_combo.pack(side="left", padx=4)
        
        item_cols = ["Code", "Name", "Stock", "Retail (KES)", "Wholesale (KES)"]
        self.item_tbl = DataTable(left, item_cols, height=10)
        self.item_tbl.pack(fill="both", expand=True, padx=8, pady=4)
        self.item_tbl.bind_double(self._add_to_cart)
        
        qf = tk.Frame(left, bg=CLR["bg"])
        qf.pack(fill="x", padx=8, pady=4)
        
        tk.Label(qf, text="Qty to Add:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.quick_qty = ttk.Entry(qf, width=6)
        self.quick_qty.insert(0, "1")
        self.quick_qty.pack(side="left", padx=4)
        
        tk.Button(qf, text="➕ Add Selected Item", command=self._add_selected_item,
                  bg=CLR["btn"], fg=CLR["white"], font=FONT_SM, relief="flat",
                  padx=12, pady=4, cursor="hand2").pack(side="left", padx=4)

        # =====================================================================
        # --- MIDDLE PANEL: Shopping Cart View Grid ---
        # =====================================================================
        mid = tk.LabelFrame(main, text="Shopping Cart", font=FONT_SM,
                            bg=CLR["bg"], fg=CLR["header"])
        mid.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)
        
        cart_cols = ["Code", "Item Name", "Mode", "Qty", "Unit Price", "Total (KES)", "BP (KES)"]
        self.cart_tbl = DataTable(mid, cart_cols, height=10)
        self.cart_tbl.pack(fill="both", expand=True, padx=8, pady=4)
        
        cf = tk.Frame(mid, bg=CLR["bg"])
        cf.pack(fill="x", padx=8, pady=4)
        
        for txt, cmd, col in [
            ("🗑 Remove", self._remove_from_cart, CLR["danger"]),
            ("📝 Edit", self._edit_qty, CLR["btn"]),
            ("🔄 Switch Tier", self._toggle_cart_item_tier, CLR["accent"]),
            ("❌ Clear", self._clear_cart, "#555"),
        ]:
            tk.Button(cf, text=txt, command=cmd, bg=col, fg=CLR["white"],
                      font=FONT_SM, relief="flat", padx=6, pady=3,
                      cursor="hand2").pack(side="left", padx=2)

        # =====================================================================
        # --- RIGHT PANEL: Account Ledger & Checkout Settlements ---
        # =====================================================================
        right = tk.LabelFrame(main, text="Sale Summary", font=FONT_SM,
                             bg=CLR["bg"], fg=CLR["header"])
        right.grid(row=0, column=2, sticky="nsew", padx=4, pady=4)
        
        # --- CUSTOMER SECTION ---
        cust_outer = tk.LabelFrame(right, text="Customer Type", font=FONT_SM,
                                    bg=CLR["bg"], fg=CLR["header"])
        cust_outer.pack(fill="x", padx=8, pady=6)
        
        radio_row = tk.Frame(cust_outer, bg=CLR["bg"])
        radio_row.pack(fill="x", padx=6, pady=4)
        
        self.cust_type = tk.StringVar(value="walkin")
        tk.Radiobutton(radio_row, text="🚶 Walk-in", variable=self.cust_type,
                       value="walkin", command=self._on_cust_type_change,
                       bg=CLR["bg"], font=FONT_BODY, fg=CLR["text_dark"],
                       activebackground=CLR["bg"]).pack(side="left", padx=10)
        tk.Radiobutton(radio_row, text="👤 Credit Customer", variable=self.cust_type,
                       value="credit", command=self._on_cust_type_change,
                       bg=CLR["bg"], font=FONT_BODY, fg=CLR["text_dark"],
                       activebackground=CLR["bg"]).pack(side="left", padx=10)
        
        # Internal panel container for searching credit customers
        self.credit_panel = tk.Frame(cust_outer, bg=CLR["bg"])
        
        csf = tk.Frame(self.credit_panel, bg=CLR["bg"])
        csf.pack(fill="x", padx=4, pady=2)
        tk.Label(csf, text="Search:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        
        self.cust_search_var = tk.StringVar()
        cse = ttk.Entry(csf, textvariable=self.cust_search_var, width=14)
        cse.pack(side="left", padx=4, fill="x", expand=True)
        cse.bind("<KeyRelease>", self._filter_customers)
        
        tk.Button(csf, text="🔄", command=self._load_customers,
                  bg=CLR["accent"], fg=CLR["white"], font=FONT_SM,
                  relief="flat", padx=6, pady=2, cursor="hand2").pack(side="right")
                  
        lb_frame = tk.Frame(self.credit_panel, bg=CLR["bg"])
        lb_frame.pack(fill="x", padx=4, pady=4)
        
        # Set explicitly to 4 lines high to ensure it fits comfortably within low-height displays
        self.cust_listbox = tk.Listbox(lb_frame, height=4, font=FONT_SM,
                                       selectmode=tk.SINGLE, bg=CLR["white"],
                                       selectbackground=CLR["accent"],
                                       selectforeground=CLR["white"],
                                       relief="solid", bd=1)
        cust_vsb = ttk.Scrollbar(lb_frame, orient="vertical", command=self.cust_listbox.yview)
        self.cust_listbox.configure(yscrollcommand=cust_vsb.set)
        self.cust_listbox.pack(side="left", fill="x", expand=True)
        cust_vsb.pack(side="right", fill="y")
        self.cust_listbox.bind("<<ListboxSelect>>", self._on_cust_select)
        
        self.selected_cust_lbl = tk.Label(self.credit_panel, text="No customer selected",
                                           font=FONT_SM, bg=CLR["bg"], fg=CLR["accent"],
                                           wraplength=240, justify="left")
        self.selected_cust_lbl.pack(anchor="w", padx=4, pady=2)
        
        self._selected_customer = {"id": None, "name": "Walk-in"}
        self._on_cust_type_change()

        # --- FINANCIAL SUMMARY BREAKDOWN ---
        self.lbl_items = tk.Label(right, text="Items: 0", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.lbl_items.pack(fill="x", padx=12, pady=2)
        
        tk.Frame(right, height=1, bg=CLR["border"]).pack(fill="x", padx=12, pady=4)
        
        self.lbl_total = tk.Label(right, text="TOTAL: KES 0.00",
                                   font=("Helvetica", 13, "bold"),
                                   bg=CLR["bg"], fg=CLR["header"], anchor="w")
        self.lbl_total.pack(fill="x", padx=12, pady=4)
        
        tk.Label(right, text="Payment Mode:", font=FONT_SM, bg=CLR["bg"], anchor="w").pack(fill="x", padx=12, pady=(4,2))
        self.payment_mode = tk.StringVar(value="CASH")
        
        pm_frame = tk.Frame(right, bg=CLR["bg"])
        pm_frame.pack(fill="x", padx=12)
        for mode in ["CASH", "CREDIT", "CHEQUE", "MPESA", "BANK TRANSFER"]:
            ttk.Radiobutton(pm_frame, text=mode, variable=self.payment_mode, value=mode,
                            command=self._on_payment_mode_change).pack(anchor="w", pady=1)
                            
        self.cash_frame = tk.Frame(right, bg=CLR["bg"])
        self.cash_frame.pack(fill="x", padx=12, pady=4)
        tk.Label(self.cash_frame, text="Cash Received:", font=FONT_SM, bg=CLR["bg"], anchor="w").pack(fill="x")
        self.cash_entry = ttk.Entry(self.cash_frame, font=FONT_BODY)
        self.cash_entry.pack(fill="x", pady=2)
        self.cash_entry.bind("<KeyRelease>", lambda _: self._calc_change())
        
        self.lbl_change = tk.Label(right, text="Change: KES 0.00",
                                    font=FONT_SM, bg=CLR["bg"], fg=CLR["success"], anchor="w")
        self.lbl_change.pack(fill="x", padx=12, pady=2)
        
        tk.Frame(right, height=1, bg=CLR["border"]).pack(fill="x", padx=12, pady=4)
        
        bf = tk.Frame(right, bg=CLR["bg"])
        bf.pack(fill="x", padx=12, pady=4)
        
        tk.Button(bf, text="💾 Save Sale", command=self._save_sale,
                  bg=CLR["success"], fg=CLR["white"], font=FONT_SM,
                  relief="flat", padx=8, pady=5, cursor="hand2").pack(fill="x", pady=2)
        tk.Button(bf, text="🧾 Print Receipt", command=self._print_receipt_preview,
                  bg=CLR["accent"], fg=CLR["white"], font=FONT_SM,
                  relief="flat", padx=8, pady=5, cursor="hand2").pack(fill="x", pady=2)
                  
        self._on_payment_mode_change()

    def _on_cust_type_change(self):
        if self.cust_type.get() == "walkin":
            self.credit_panel.pack_forget()
            self._selected_customer = {"id": None, "name": "Walk-in"}
        else:
            self.credit_panel.pack(fill="x", padx=4, pady=(2,4))
            self._load_customers()

    def _load_customers(self):
        try:
            _, rows = db.fetchall("SELECT id, name, phone FROM dbo.Credit_Customer ORDER BY name")
            self._customers_raw = [{"id": r[0], "name": r[1] or "", "phone": r[2] or ""} for r in rows]
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
        if not sel: return
        c = self._listbox_data[sel[0]]
        self._selected_customer = {"id": c["id"], "name": c["name"]}
        self.selected_cust_lbl.config(text=f"✔ {c['name']}  [{c['phone']}]")

    def _load_items(self):
        try:
            # Querying pcode, name, spr, spw, bp, qtystock explicitly
            _, rows = db.fetchall("SELECT pcode, name, spr, spw, bp, qtystock FROM dbo.Stock_item ORDER BY name")
            self._items_list = [{
                "code": str(r[0]), 
                "name": r[1] or "",
                "price_retail": float(r[2]) if r[2] else 0.0,
                "price_wholesale": float(r[3]) if r[3] else 0.0,
                "price_buying": float(r[4]) if r[4] else 0.0, # Capturing bp safely
                "qty_stock": float(r[5]) if r[5] else 0.0
            } for r in rows]
            self._search_items()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load product matrices: {e}")

    def _search_items(self):
        term = self.item_search.get().lower()
        filtered = ([i for i in self._items_list
                     if term in i["code"].lower() or term in i["name"].lower()]
                    if term else self._items_list)
        self._display_items(filtered)

    def _display_items(self, items):
        self.item_tbl.load([[
            str(i["code"]), 
            i["name"],
            str(int(i["qty_stock"])), 
            money(i["price_retail"]), 
            money(i["price_wholesale"])
        ] for i in items])

    def _add_to_cart(self, *_): 
        self._add_selected_item()

    def _add_selected_item(self):
        vals = self.item_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Item", "Select an item from the matrix grid first."); return
        try:
            qty = float(self.quick_qty.get())
            if qty <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Qty", "Enter a valid product quantity."); return

        code = vals[0]
        db_item = next((i for i in self._items_list if i["code"] == code), None)
        if not db_item: return

        if qty > db_item["qty_stock"]:
            messagebox.showwarning("Out of Stock", f"{db_item['name']}: only {db_item['qty_stock']} available.")
            return

        tier = self.quick_tier.get() 
        selected_price = db_item["price_retail"] if tier == "Retail" else db_item["price_wholesale"]

        for item in self.cart:
            if item["code"] == code and item["tier"] == tier:
                item["qty"] += qty
                item["total"] = item["qty"] * item["price"]
                self._update_cart_display()
                return

        self.cart.append({
            "code": code,
            "name": db_item["name"],
            "tier": tier,
            "qty": qty,
            "price": selected_price,
            "price_buying": db_item["price_buying"],
            "price_retail_base": db_item["price_retail"],
            "price_wholesale_base": db_item["price_wholesale"],
            "total": qty * selected_price
        })
        self.quick_qty.delete(0, "end")
        self.quick_qty.insert(0, "1")
        self._update_cart_display()

    def _update_cart_display(self):
        # FIXED: Re-mapped the array structure so BP is passed at index [6] matching cart_cols layout
        self.cart_tbl.load([[
            i["code"], 
            i["name"][:15], 
            i["tier"], 
            str(i["qty"]),
            money(i["price"]), 
            money(i["total"]),
            money(i["price_buying"]) # BP placed explicitly as the last item
        ] for i in self.cart])
        
        total = sum(i["total"] for i in self.cart)
        self.lbl_items.config(text=f"Items: {len(self.cart)}")
        self.lbl_total.config(text=f"TOTAL: KES {money(total)}")
        if self.payment_mode.get() == "CASH": 
            self._calc_change()

    def _toggle_cart_item_tier(self):
        vals = self.cart_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Item", "Select an item inside the shopping cart first."); return
        
        code, current_tier = vals[0], vals[2]
        cart_item = next((i for i in self.cart if i["code"] == code and i["tier"] == current_tier), None)
        if not cart_item: return

        new_tier = "Wholesale" if current_tier == "Retail" else "Retail"
        new_price = cart_item["price_wholesale_base"] if new_tier == "Wholesale" else cart_item["price_retail_base"]
        
        existing_target = next((i for i in self.cart if i["code"] == code and i["tier"] == new_tier), None)
        if existing_target:
            existing_target["qty"] += cart_item["qty"]
            existing_target["total"] = existing_target["qty"] * existing_target["price"]
            self.cart.remove(cart_item)
        else:
            cart_item["tier"] = new_tier
            cart_item["price"] = new_price
            cart_item["total"] = cart_item["qty"] * new_price
            
        self._update_cart_display()

    def _remove_from_cart(self):
        vals = self.cart_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Item", "Select a cart line component to isolate."); return
        self.cart = [i for i in self.cart if not (i["code"] == vals[0] and i["tier"] == vals[2])]
        self._update_cart_display()

    def _edit_qty(self):
        vals = self.cart_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Item", "Select an active row item within the checkout cart layout."); return
        
        code, _, tier = vals[0], vals[1], vals[2]
        cart_item = next((i for i in self.cart if i["code"] == code and i["tier"] == tier), None)
        if not cart_item: return

        db_item = next((i for i in self._items_list if i["code"] == code), None)
        qty_stock = db_item["qty_stock"] if db_item else cart_item["qty"]

        dlg = tk.Toplevel(self)
        dlg.title("Modify System Allocation Metrics")
        dlg.resizable(False, False)
        dlg.configure(bg=CLR["bg"])
        dlg.grab_set()
        
        tk.Label(dlg, text=f"Product: {cart_item['name']} ({tier})", font=FONT_SM, bg=CLR["bg"]).pack(padx=10, pady=4)
        
        margin_frame = tk.LabelFrame(dlg, text="📊 Live Margin Reference", font=FONT_SM, bg=CLR["bg"], fg=CLR["accent"])
        margin_frame.pack(fill="x", padx=10, pady=4)
        
        tk.Label(margin_frame, text=f"Cost (Buying Price): KES {money(cart_item['price_buying'])}", font=FONT_SM, bg=CLR["bg"], anchor="w").pack(fill="x", padx=6, pady=1)
        tk.Label(margin_frame, text=f"Base Selling Price ({tier}): KES {money(cart_item['price'])}", font=FONT_SM, bg=CLR["bg"], anchor="w").pack(fill="x", padx=6, pady=1)

        tk.Label(dlg, text="Adjust Quantity:", font=FONT_SM, bg=CLR["bg"]).pack(padx=10, pady=2)
        qty_entry = ttk.Entry(dlg, width=15)
        qty_entry.insert(0, str(cart_item["qty"]))
        qty_entry.pack(padx=10, pady=4)
        
        tk.Label(dlg, text="Override Unit Selling Price:", font=FONT_SM, bg=CLR["bg"]).pack(padx=10, pady=2)
        price_entry = ttk.Entry(dlg, width=15)
        price_entry.insert(0, str(cart_item["price"]))
        price_entry.pack(padx=10, pady=4)
        
        qty_entry.focus()

        def _save():
            try:
                new_qty = float(qty_entry.get())
                new_price = float(price_entry.get().replace(",", ""))
                
                if new_qty <= 0 or new_price <= 0: 
                    raise ValueError
                
                if new_price < cart_item["price_buying"]:
                    if not messagebox.askyesno("Margin Warning", "Warning: The entered selling price is lower than the acquisition cost. Proceed anyway?"):
                        return
                
                if new_qty > qty_stock:
                    messagebox.showwarning("Out of Stock", f"Requested allocation exceeds current stock of {qty_stock} units.")
                    return

                cart_item["qty"] = new_qty
                cart_item["price"] = new_price
                cart_item["total"] = new_qty * new_price
                
                dlg.destroy()
                self._update_cart_display()
                
            except ValueError:
                messagebox.showerror("Invalid Input", "Provide numeric entries for both quantities and price overrides.")

        tk.Button(dlg, text="💾 Update Ledger Row", command=_save, bg=CLR["success"], fg=CLR["white"],
                  relief="flat", padx=10, pady=4, cursor="hand2").pack(padx=10, pady=10)

    def _clear_cart(self):
        if self.cart and messagebox.askyesno("Clear Cart", "Clear all items from the current cart session?"):
            self.cart = []
            self._update_cart_display()

    def _on_payment_mode_change(self):
        if self.payment_mode.get() == "CASH":
            self.cash_frame.pack(fill="x", padx=8, pady=4)
            self.lbl_change.pack(fill="x", padx=8, pady=2)
        else:
            self.cash_frame.pack_forget()
            self.lbl_change.pack_forget()

    def _calc_change(self):
        try:
            total = sum(i["total"] for i in self.cart)
            cash = float(self.cash_entry.get() or 0)
            change = cash - total
            self.lbl_change.config(
                text=f"Change: KES {money(change)}",
                fg=CLR["success"] if change >= 0 else CLR["danger"])
        except ValueError:
            self.lbl_change.config(text="Change: —")

    def _save_sale(self):
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Add items to cart first."); return
        
        mode = self.payment_mode.get()
        sold_to = self._selected_customer["name"]
        if self.cust_type.get() == "credit" and self._selected_customer["id"] is None:
            messagebox.showwarning("No Customer", "Please select a credit customer account line item."); return
            
        # --- FIXED: RETAIL PRICE RESTRICTION SCANNER ---
        below_retail_items = []
        for item in self.cart:
            # Checking if final negotiated unit price is lower than database base retail price
            if item["price"] < item["price_retail_base"]:
                diff = item["price_retail_base"] - item["price"]
                below_retail_items.append(
                    f"• {item['name']}: Price KES {money(item['price'])} | "
                    f"Min Retail: KES {money(item['price_retail_base'])} | "
                    f"Variance: -KES {money(diff)}"
                )

        explanation_text = ""
        if below_retail_items:
            # Block the save thread until an explanation window provides confirmation
            explanation_text = self._prompt_retail_explanation(below_retail_items)
            if not explanation_text:
                # Cancel clicked or validation failed
                return
        # -----------------------------------------------

        try:
            total = sum(i["total"] for i in self.cart)
            cash = 0.0
            change = 0.0
            if mode == "CASH":
                try:
                    cash = float(self.cash_entry.get() or 0)
                    change = cash - total
                    if change < 0:
                        messagebox.showerror("Payment Error", "Insufficient cash received."); return
                except ValueError:
                    messagebox.showerror("Invalid Input", "Enter a valid cash amount entry."); return

            last = db.fetchone("SELECT MAX(CAST(TraNo AS INT)) FROM dbo.Sale")
            trano = str((last[0] or 0) + 1) if last and last[0] else "1"
            now = datetime.datetime.now()
            sale_date = now.date()
            sale_time = now

            db.execute(
                "INSERT INTO dbo.Sale "
                "(TraNo, tradate, tratype, cashier, SoldTo, cash, change, vat, total, SaleTime) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (trano, sale_date, mode, self.current_user, sold_to, cash, change, 0, total, sale_time)
            )

            for item in self.cart:
                item_name_final = f"{item['name']} ({item['tier']})"
                # Audit log tracking directly into the line description field
                if item["price"] < item["price_retail_base"] and explanation_text:
                    item_name_final += f" [BELOW RETAIL: {explanation_text}]"

                db.execute(
                    "INSERT INTO dbo.Sale_Item "
                    "(trano, TraDate, ItemCode, ItemName, qty, total, itemcost, vat) "
                    "VALUES (?,?,?,?,?,?,?,?)",
                    (trano, sale_date, item["code"], item_name_final,
                     item["qty"], item["total"], item["price_buying"], 0)
                )
                db.execute(
                    "UPDATE dbo.Stock_item SET qtystock = qtystock - ? WHERE pcode=?",
                    (item["qty"], item["code"])
                )

            if self.cust_type.get() == "credit" and self._selected_customer["id"] is not None and mode == "CREDIT":
                db.execute("UPDATE dbo.Credit_Customer SET balance = balance + ? WHERE id=?",
                           (total, self._selected_customer["id"]))

            messagebox.showinfo("Sale Saved", f"✅ Sale #{trano} saved!\nCustomer: {sold_to}\nTotal: KES {money(total)}")
            
            if self.on_sale_saved:
                try: self.on_sale_saved()
                except Exception: pass
                
            if messagebox.askyesno("Print Receipt", "Print thermal checkout confirmation receipt?"):
                self._do_print_receipt(trano, sold_to, cash, change, total)

            self.cart = []
            self._update_cart_display()
            self._load_items()
            self.cust_type.set("walkin")
            self._on_cust_type_change()
            
        except Exception as e:
            messagebox.showerror("Database Transaction Error", str(e))

    def _prompt_retail_explanation(self, items_list):
        """
        Creates a modal prompt block forcing user compliance when product metrics
        drop beneath baseline standard retail numbers.
        """
        result = {"text": ""}
        
        dialog = tk.Toplevel(self)
        dialog.title("⚠️ Price Below Retail Baseline Authorization")
        dialog.geometry("460x390")
        dialog.resizable(False, False)
        dialog.configure(bg=CLR["bg"])
        dialog.grab_set() 
        
        hdr = tk.Frame(dialog, bg=CLR["accent"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="Price Below Retail Limit Detected", font=("Helvetica", 11, "bold"), 
                 bg=CLR["accent"], fg=CLR["white"]).pack(pady=6)
                 
        body = tk.Frame(dialog, bg=CLR["bg"])
        body.pack(fill="both", expand=True, padx=15, pady=10)
        
        tk.Label(body, text="The items listed below are set lower than standard retail pricing:", 
                 font=FONT_SM, bg=CLR["bg"], fg=CLR["text_dark"], anchor="w").pack(fill="x", pady=(0,5))
                 
        items_box = tk.Text(body, height=5, font=FONT_SM, bg="#F0F4F8", fg=CLR["header"], relief="solid", bd=1)
        items_box.pack(fill="x", pady=2)
        items_box.insert("1.0", "\n".join(items_list))
        items_box.config(state="disabled")
        
        tk.Label(body, text="Provide Explanation/Justification for this Discount:", 
                 font=FONT_SM, bg=CLR["bg"], fg=CLR["header"], anchor="w").pack(fill="x", pady=(10,2))
                 
        reason_entry = tk.Text(body, height=4, font=FONT_BODY, wrap="word", relief="solid", bd=1)
        reason_entry.pack(fill="x", pady=2)
        reason_entry.focus()
        
        def _confirm_auth():
            text_input = reason_entry.get("1.0", "end-1c").strip()
            if len(text_input) < 5:
                messagebox.showwarning("Input Validation Failure", "You must provide a clear reason (min 5 characters) before proceeding.", parent=dialog)
                return
            result["text"] = text_input
            dialog.destroy()
            
        def _cancel_auth():
            dialog.destroy()

        btn_frame = tk.Frame(body, bg=CLR["bg"])
        btn_frame.pack(fill="x", pady=15)
        
        tk.Button(btn_frame, text="❌ Cancel Sale", command=_cancel_auth,
                  bg="#555", fg=CLR["white"], font=FONT_SM, relief="flat",
                  padx=14, pady=6, cursor="hand2").pack(side="left")
                  
        tk.Button(btn_frame, text="🔓 Approve & Complete Sale", command=_confirm_auth,
                  bg=CLR["success"], fg=CLR["white"], font=FONT_SM, relief="flat",
                  padx=14, pady=6, cursor="hand2").pack(side="right")
                  
        self.wait_window(dialog)
        return result["text"]

    def _print_receipt_preview(self):
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Add items first."); return
        total = sum(i["total"] for i in self.cart)
        self._do_print_receipt("PREVIEW", self._selected_customer["name"], 0, 0, total)

    def _do_print_receipt(self, trano, sold_to, cash, change, total):
        sale_data = {
            "trano": trano, "date": datetime.datetime.now().isoformat(),
            "cashier": self.current_user, "customer": sold_to,
            "cash": cash, "change": change, "total": total, "invno": ""
        }
        print_sale_receipt(_printer_cfg, sale_data, self.cart)
# ═════════════════════════════════════════════════════════════════════════════
# CREDIT CUSTOMERS
# ═════════════════════════════════════════════════════════════════════════════
class CreditCustomersFrame(ttk.Frame):
    def __init__(self, parent, current_user: str):
        super().__init__(parent)
        self.current_user = current_user
        self.selected_customer_id = None
        self.selected_customer_name = ""
        self._build()
        self._load_customers()

    _FIELDS = [
        ("Name *",        "name",    "entry", []),
        ("Phone",         "phone",   "entry", []),
        ("Route",         "route",   "entry", []),
        ("Credit Period", "cperiod", "entry", []),
        ("Date Due",      "datedue", "entry", []),
        ("Balance (KES)", "balance", "entry", []),
    ]

    def _build(self):
        top = tk.LabelFrame(self, text="Credit Customers", font=FONT_H2,
                            bg=CLR["bg"], fg=CLR["text_dark"], padx=6, pady=6)
        top.pack(fill="x", padx=10, pady=(10, 4))

        ctrl = tk.Frame(top, bg=CLR["bg"])
        ctrl.pack(fill="x", pady=(0, 4))

        tk.Label(ctrl, text="Search:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.search_var = tk.StringVar()
        e = ttk.Entry(ctrl, textvariable=self.search_var, font=FONT_BODY, width=24)
        e.pack(side="left", padx=4)
        e.bind("<Return>", lambda _: self._load_customers())

        for txt, cmd, kw in [
            ("🔍 Search",  self._load_customers, {}),
            ("🔄 Refresh", self._load_customers, {}),
            ("➕ Add",      self._add,            {"success": True}),
            ("✏️ Edit",     self._edit,           {}),
            ("🗑 Delete",   self._delete,         {"danger": True}),
        ]:
            btn = tk.Button(ctrl, text=txt, command=cmd)
            style_btn(btn, **kw)
            btn.pack(side="left", padx=2)

        cust_cols = ["ID", "Name", "Phone", "Route", "Balance (KES)", "Credit Period", "Date Due"]
        self.cust_tbl = DataTable(top, cust_cols, height=6)
        self.cust_tbl.pack(fill="x")
        self.cust_tbl.bind_select(self._on_select)

        self.cust_status = tk.Label(top, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.cust_status.pack(fill="x")

        # --- BOTTOM SECTION ---
        bottom = tk.Frame(self, bg=CLR["bg"])
        bottom.pack(fill="both", expand=True, padx=10, pady=4)
        bottom.columnconfigure(0, weight=3)
        bottom.columnconfigure(1, weight=1)
        bottom.rowconfigure(0, weight=1)

        # Left: Invoices / Ledger
        inv_frame = tk.LabelFrame(bottom, text="Invoices / Ledger", font=FONT_H2,
                                  bg=CLR["bg"], fg=CLR["text_dark"], padx=6, pady=6)
        inv_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        inv_frame.rowconfigure(1, weight=1)
        inv_frame.columnconfigure(0, weight=1)

        ictl = tk.Frame(inv_frame, bg=CLR["bg"])
        ictl.grid(row=0, column=0, sticky="w", pady=(0, 4))

        tk.Label(ictl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.inv_from = ttk.Entry(ictl, font=FONT_SM, width=12)
        self.inv_from.insert(0, month_start())
        self.inv_from.pack(side="left", padx=2)

        tk.Label(ictl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.inv_to = ttk.Entry(ictl, font=FONT_SM, width=12)
        self.inv_to.insert(0, today_str())
        self.inv_to.pack(side="left", padx=2)

        lb = tk.Button(ictl, text="📋 Load", command=self._load_invoices)
        style_btn(lb)
        lb.pack(side="left", padx=2)

        rep_b = tk.Button(ictl, text="📊 Full Statement",
                          command=self._generate_credit_report)
        style_btn(rep_b, accent=True)
        rep_b.pack(side="left", padx=2)

        inv_cols = ["RecId", "Date", "Ref No", "Detail",
                    "Amount (KES)", "Paid (KES)", "Balance (KES)"]
        self.inv_tbl = DataTable(inv_frame, inv_cols)
        self.inv_tbl.grid(row=1, column=0, sticky="nsew")

        self.inv_status = tk.Label(inv_frame, text="← Select a customer",
                                   font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.inv_status.grid(row=2, column=0, sticky="w")

        # Right: Record Payment
        pay_frame = tk.LabelFrame(bottom, text="Record Payment", font=FONT_H2,
                                  bg=CLR["bg"], fg=CLR["text_dark"], padx=10, pady=10)
        pay_frame.grid(row=0, column=1, sticky="nsew")

        self.pay_cust_lbl = tk.Label(pay_frame, text="No customer selected",
                                     font=FONT_SM, bg=CLR["bg"], fg=CLR["accent"],
                                     wraplength=200)
        self.pay_cust_lbl.pack(anchor="w", pady=(0, 8))

        self.pay_vars = {}
        for label, key in [
            ("Amount (KES):", "pay_amount"),
            ("Payment Mode:", "pay_mode"),
            ("Cheque No:",    "pay_chequeno"),
            ("Bank:",         "pay_bank"),
            ("Reference:",    "pay_ref"),
        ]:
            tk.Label(pay_frame, text=label, font=FONT_SM,
                     bg=CLR["bg"], anchor="w").pack(fill="x")
            if key == "pay_mode":
                var = tk.StringVar(value="CASH")
                ttk.Combobox(pay_frame, textvariable=var, font=FONT_SM, width=22,
                             values=["CASH", "CHEQUE", "MPESA",
                                     "BANK TRANSFER", "OTHER"],
                             state="readonly").pack(fill="x", pady=(0, 6))
            else:
                var = tk.StringVar()
                ttk.Entry(pay_frame, textvariable=var,
                          font=FONT_SM).pack(fill="x", pady=(0, 6))
            self.pay_vars[key] = var

        self.pay_bal_lbl = tk.Label(pay_frame, text="",
                                    font=("Helvetica Neue", 10, "bold"),
                                    bg=CLR["bg"], fg=CLR["danger"])
        self.pay_bal_lbl.pack(anchor="w", pady=4)

        pay_btn = tk.Button(pay_frame, text="💳  Save Payment",
                            command=self._save_payment)
        style_btn(pay_btn, success=True)
        pay_btn.pack(fill="x", pady=(8, 2))

        clr_btn = tk.Button(pay_frame, text="✖  Clear",
                            command=self._clear_payment_form)
        style_btn(clr_btn, danger=True)
        clr_btn.pack(fill="x")

    # ── Customer loaders ──────────────────────────────────────────────────────
    def _load_customers(self):
        q = f"%{self.search_var.get().strip()}%"
        try:
            _, rows = db.fetchall(
                "SELECT id, name, phone, Route, balance, cperiod, datedue "
                "FROM dbo.Credit_Customer "
                "WHERE name LIKE ? OR phone LIKE ? OR Route LIKE ? "
                "ORDER BY name", (q, q, q))
            self.cust_tbl.load([[r[0], r[1] or "", r[2] or "", r[3] or "",
                                  money(r[4]), r[5] or "", r[6] or ""] for r in rows])
            total_bal = sum(float(r[4]) for r in rows if r[4])
            self.cust_status.config(
                text=f"{len(rows)} customers  |  "
                     f"Total Outstanding: KES {money(total_bal)}")
        except Exception as e:
            self.cust_status.config(text=f"Error: {str(e)[:80]}")

    def _add(self):
        dlg = FormDialog(self.winfo_toplevel(), "Add Credit Customer", self._FIELDS)
        self.wait_window(dlg)
        if not dlg.result or not dlg.result.get("name"):
            return
        d = dlg.result
        try:
            db.execute(
                "INSERT INTO dbo.Credit_Customer "
                "(name,phone,Route,cperiod,datedue,balance) VALUES (?,?,?,?,?,?)",
                (d["name"], d["phone"], d["route"],
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
                   "balance": vals[4].replace(",", ""),
                   "cperiod": vals[5], "datedue": vals[6]}
        dlg = FormDialog(self.winfo_toplevel(), "Edit Customer", self._FIELDS, initial)
        self.wait_window(dlg)
        if not dlg.result:
            return
        d = dlg.result
        try:
            db.execute(
                "UPDATE dbo.Credit_Customer "
                "SET name=?,phone=?,Route=?,cperiod=?,datedue=?,balance=? "
                "WHERE id=?",
                (d["name"], d["phone"], d["route"],
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
                f"Delete '{vals[1]}'?\nInvoices are NOT removed."):
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
        if not vals:
            return
        self.selected_customer_id   = vals[0]
        self.selected_customer_name = vals[1]
        self.pay_cust_lbl.config(
            text=f"{self.selected_customer_name}\n(ID: {self.selected_customer_id})")
        self.pay_bal_lbl.config(text=f"Current Balance: KES {vals[4]}")
        self._load_invoices()

    def _load_invoices(self):
        if not self.selected_customer_id:
            return
        try:
            d1 = datetime.datetime.strptime(self.inv_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.inv_to.get(), "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, rows = db.fetchall(
                "SELECT RecId, TraDate, CRefNo, Detail, Amount, Paid, Balance "
                "FROM dbo.DInv WHERE Idno=? AND TraDate BETWEEN ? AND ? "
                "ORDER BY TraDate DESC",
                (self.selected_customer_id, d1, d2))
            self.inv_tbl.load([[r[0], str(r[1])[:10], r[2] or "", r[3] or "",
                                  money(r[4]), money(r[5]), money(r[6])] for r in rows])
            ta = sum(float(r[4]) for r in rows if r[4])
            tp = sum(float(r[5]) for r in rows if r[5])
            tb = sum(float(r[6]) for r in rows if r[6])
            self.inv_status.config(
                text=f"{len(rows)} invoices | "
                     f"Total: {money(ta)}  Paid: {money(tp)}  Bal: {money(tb)}")
        except Exception as e:
            self.inv_status.config(text=f"Error: {str(e)[:80]}")

    # ── Full itemized credit statement ────────────────────────────────────────
    def _generate_credit_report(self):
        """
        Builds a rich itemized statement per invoice showing:
        - Transaction date and exact time
        - Every product sold, unit price, quantity, and line total
        - Running balance after each transaction
        - Payment receipts clearly separated
        - Grand totals and current outstanding balance
        """
        if not self.selected_customer_id:
            messagebox.showwarning(
                "Select Customer",
                "Please select a customer from the grid first.")
            return

        try:
            d1 = datetime.datetime.strptime(self.inv_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.inv_to.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date",
                "Dates must be in YYYY-MM-DD format.")
            return

        try:
            # 1. Customer master details
            cust = db.fetchone(
                "SELECT phone, Route, balance, cperiod, datedue "
                "FROM dbo.Credit_Customer WHERE id=?",
                (self.selected_customer_id,))
            phone        = (cust[0] or "N/A") if cust else "N/A"
            route        = (cust[1] or "N/A") if cust else "N/A"
            curr_balance = float(cust[2]) if cust and cust[2] else 0.0
            cperiod      = (cust[3] or "N/A") if cust else "N/A"
            datedue      = str(cust[4])[:10] if cust and cust[4] else "N/A"

            # 2. All invoices (sales debits) in range — include full datetime
            _, inv_rows = db.fetchall(
                "SELECT TraDate, CRefNo, Detail, Amount, Paid, Balance "
                "FROM dbo.DInv "
                "WHERE Idno=? AND TraDate BETWEEN ? AND ? "
                "ORDER BY TraDate ASC",
                (self.selected_customer_id, d1, d2))

            # 3. All payments in range from Payment table
            _, pay_rows = db.fetchall(
                "SELECT paydate, amount, paymode, ddocno, bal "
                "FROM dbo.Payment "
                "WHERE Sid=? AND paydate BETWEEN ? AND ? "
                "ORDER BY paydate ASC",
                (self.selected_customer_id, d1, d2))

            # 4. Build merged timeline: tag each entry as INVOICE or PAYMENT
            #    so we can sort everything by datetime
            timeline = []
            for r in inv_rows:
                timeline.append({
                    "type":    "INVOICE",
                    "dt":      r[0],                        # datetime object
                    "ref":     str(r[1] or "").strip(),
                    "detail":  str(r[2] or "").strip(),
                    "debit":   float(r[3]) if r[3] else 0.0,
                    "paid":    float(r[4]) if r[4] else 0.0,
                    "balance": float(r[5]) if r[5] else 0.0,
                })
            for r in pay_rows:
                timeline.append({
                    "type":    "PAYMENT",
                    "dt":      r[0],
                    "ref":     str(r[3] or "").strip(),
                    "detail":  f"Payment via {r[2] or 'CASH'}",
                    "debit":   0.0,
                    "paid":    float(r[1]) if r[1] else 0.0,
                    "balance": float(r[4]) if r[4] else 0.0,
                })

            # Sort merged timeline by datetime ascending
            timeline.sort(key=lambda x: x["dt"] if x["dt"] else datetime.datetime.min)

            # ── Build the statement text ──────────────────────────────────────
            W = 62   # total line width
            SEP  = "=" * W
            DASH = "-" * W

            lines = []

            def pad(text, width):
                """Left-pad a string to a fixed width, truncating if needed."""
                return str(text)[:width].ljust(width)

            lines.append(SEP)
            lines.append("       CREDIT ACCOUNT STATEMENT — ITEMIZED        ")
            lines.append(SEP)
            lines.append(f"  Customer  : {self.selected_customer_name}")
            lines.append(f"  Account # : {self.selected_customer_id}")
            lines.append(f"  Phone     : {phone}")
            lines.append(f"  Route     : {route}")
            lines.append(f"  Cr Period : {cperiod} days")
            lines.append(f"  Due Date  : {datedue}")
            lines.append(f"  Statement : {self.inv_from.get()}  to  {self.inv_to.get()}")
            lines.append(DASH)
            lines.append(f"  Current Outstanding Balance: KES {money(curr_balance)}")
            lines.append(SEP)

            tot_debits   = 0.0
            tot_payments = 0.0

            for entry in timeline:
                # Format datetime: show date + time if available
                try:
                    dt_obj = entry["dt"]
                    if isinstance(dt_obj, datetime.datetime):
                        dt_str = dt_obj.strftime("%Y-%m-%d  %H:%M:%S")
                    elif isinstance(dt_obj, datetime.date):
                        dt_str = str(dt_obj)[:10] + "  (time N/A)"
                    else:
                        dt_str = str(dt_obj)[:19]
                except Exception:
                    dt_str = str(entry["dt"])[:19]

                if entry["type"] == "INVOICE":
                    tot_debits += entry["debit"]
                    lines.append("")
                    lines.append(f"  ┌─ SALE  {dt_str}")
                    lines.append(f"  │  Ref   : {entry['ref'] or '(no ref)'}")
                    lines.append(f"  │  Detail: {entry['detail'] or '—'}")
                    lines.append(f"  │  Amount: KES {money(entry['debit'])}")
                    lines.append(f"  │  Paid  : KES {money(entry['paid'])}")
                    lines.append(f"  │  Bal   : KES {money(entry['balance'])}")

                    # ── Fetch product line items for this invoice ─────────────
                    item_lines = []

                    # Primary: TransSub by TraNo (your existing table)
                    if entry["ref"]:
                        try:
                            _, sub_items = db.fetchall(
                                "SELECT Description, Qty, Price, Amount "
                                "FROM dbo.TransSub WHERE TraNo = ?",
                                (entry["ref"],))
                            for it in sub_items:
                                item_lines.append({
                                    "name":  str(it[0] or "Unknown")[:30],
                                    "qty":   it[1] if it[1] else 0,
                                    "price": float(it[2]) if it[2] else 0.0,
                                    "total": float(it[3]) if it[3] else 0.0,
                                })
                        except Exception:
                            pass

                    # Fallback: SaleItem table if TransSub is empty
                    if not item_lines and entry["ref"]:
                        try:
                            _, sale_items = db.fetchall(
                                "SELECT description, qty, price, total "
                                "FROM dbo.SaleItem WHERE TraNo = ?",
                                (entry["ref"],))
                            for it in sale_items:
                                item_lines.append({
                                    "name":  str(it[0] or "Unknown")[:30],
                                    "qty":   it[1] if it[1] else 0,
                                    "price": float(it[2]) if it[2] else 0.0,
                                    "total": float(it[3]) if it[3] else 0.0,
                                })
                        except Exception:
                            pass

                    if item_lines:
                        lines.append(f"  │  {'─'*55}")
                        lines.append(
                            f"  │  {'PRODUCT':<30} {'QTY':>4}  "
                            f"{'PRICE':>10}  {'TOTAL':>10}")
                        lines.append(f"  │  {'─'*55}")
                        for it in item_lines:
                            lines.append(
                                f"  │  {pad(it['name'], 30)} "
                                f"{str(it['qty']):>4}  "
                                f"KES {money(it['price']):>8}  "
                                f"KES {money(it['total']):>8}")
                        lines.append(f"  │  {'─'*55}")
                    else:
                        lines.append(f"  │  (no product detail available for this invoice)")

                    lines.append(f"  └─{'─'*W}")

                else:
                    # PAYMENT row
                    tot_payments += entry["paid"]
                    lines.append("")
                    lines.append(f"  ┌─ PAYMENT  {dt_str}")
                    lines.append(f"  │  Mode    : {entry['detail']}")
                    lines.append(f"  │  Ref     : {entry['ref'] or '(no ref)'}")
                    lines.append(f"  │  Amount  : KES {money(entry['paid'])}")
                    lines.append(f"  │  Bal After: KES {money(entry['balance'])}")
                    lines.append(f"  └─{'─'*W}")

            # ── Grand summary ─────────────────────────────────────────────────
            lines.append("")
            lines.append(SEP)
            lines.append(f"  TOTAL SALES (DEBITS)   : KES {money(tot_debits)}")
            lines.append(f"  TOTAL PAYMENTS         : KES {money(tot_payments)}")
            lines.append(f"  NET OUTSTANDING        : KES {money(tot_debits - tot_payments)}")
            lines.append(DASH)
            lines.append(f"  CURRENT SYSTEM BALANCE : KES {money(curr_balance)}")
            lines.append(SEP)
            lines.append(f"  Printed by : {self.current_user}")
            lines.append(
                f"  Timestamp  : "
                f"{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
            lines.append(SEP)

            report_text = "\n".join(lines)

            # ── Preview dialog ────────────────────────────────────────────────
            dlg = tk.Toplevel(self)
            dlg.title(
                f"Statement — {self.selected_customer_name}  "
                f"({self.inv_from.get()} to {self.inv_to.get()})")
            dlg.geometry("700x680")
            dlg.configure(bg=CLR["bg"])
            dlg.grab_set()

            # Header KPI strip inside dialog
            kpi_bar = tk.Frame(dlg, bg=CLR["accent"], pady=6)
            kpi_bar.pack(fill="x")
            for label, value in [
                ("Sales",    f"KES {money(tot_debits)}"),
                ("Payments", f"KES {money(tot_payments)}"),
                ("Balance",  f"KES {money(curr_balance)}"),
            ]:
                cell = tk.Frame(kpi_bar, bg=CLR["accent"], padx=20)
                cell.pack(side="left")
                tk.Label(cell, text=value,
                         font=("Helvetica Neue", 13, "bold"),
                         bg=CLR["accent"], fg=CLR["white"]).pack()
                tk.Label(cell, text=label,
                         font=FONT_SM,
                         bg=CLR["accent"], fg=CLR["white"]).pack()

            # Scrollable text display
            txt_frame = tk.Frame(dlg, bg=CLR["bg"])
            txt_frame.pack(fill="both", expand=True, padx=8, pady=6)

            scrollbar = tk.Scrollbar(txt_frame)
            scrollbar.pack(side="right", fill="y")

            h_scrollbar = tk.Scrollbar(txt_frame, orient="horizontal")
            h_scrollbar.pack(side="bottom", fill="x")

            text_area = tk.Text(
                txt_frame,
                font=("Courier New", 10),
                bg="#FFFFFF", fg="#1a1a1a",
                relief="flat",
                wrap="none",                    # no wrap so columns align
                yscrollcommand=scrollbar.set,
                xscrollcommand=h_scrollbar.set,
                padx=10, pady=8)
            text_area.pack(fill="both", expand=True)
            scrollbar.config(command=text_area.yview)
            h_scrollbar.config(command=text_area.xview)

            # Color-code SALE and PAYMENT lines using text tags
            text_area.tag_config("sale",    foreground="#1a5276", font=("Courier New", 10, "bold"))
            text_area.tag_config("payment", foreground="#1e8449", font=("Courier New", 10, "bold"))
            text_area.tag_config("product", foreground="#5d4037")
            text_area.tag_config("summary", foreground="#7b241c", font=("Courier New", 10, "bold"))
            text_area.tag_config("header",  foreground="#212121", font=("Courier New", 10, "bold"))

            for line in lines:
                stripped = line.strip()
                if stripped.startswith("┌─ SALE"):
                    text_area.insert("end", line + "\n", "sale")
                elif stripped.startswith("┌─ PAYMENT"):
                    text_area.insert("end", line + "\n", "payment")
                elif stripped.startswith("│  PRODUCT") or "KES" in line and "│" in line and "↳" not in line:
                    text_area.insert("end", line + "\n", "product")
                elif "TOTAL" in line or "OUTSTANDING" in line or "BALANCE" in line:
                    text_area.insert("end", line + "\n", "summary")
                elif line.startswith("=") or line.startswith("  Customer") or line.startswith("  Account"):
                    text_area.insert("end", line + "\n", "header")
                else:
                    text_area.insert("end", line + "\n")

            text_area.config(state="disabled")

            # Footer buttons
            btn_f = tk.Frame(dlg, bg=CLR["bg"])
            btn_f.pack(fill="x", pady=(0, 10))

            def _do_print():
                if not PRINT_OK:
                    messagebox.showwarning(
                        "Printer Unavailable",
                        "Printing services are currently disabled.", parent=dlg)
                    return
                try:
                    print_sale_receipt(
                        _printer_cfg,
                        {"raw_text": report_text},
                        [])
                    messagebox.showinfo(
                        "Sent to Printer",
                        "Statement sent to thermal printer.", parent=dlg)
                except Exception as e:
                    messagebox.showerror("Print Error", str(e), parent=dlg)

            def _save_txt():
                """Save the statement as a plain text file."""
                import tkinter.filedialog as fd
                path = fd.asksaveasfilename(
                    parent=dlg,
                    defaultextension=".txt",
                    filetypes=[("Text file", "*.txt"), ("All files", "*.*")],
                    initialfile=f"Statement_{self.selected_customer_name}_{self.inv_from.get()}.txt")
                if not path:
                    return
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(report_text)
                    messagebox.showinfo("Saved", f"Statement saved to:\n{path}", parent=dlg)
                except Exception as e:
                    messagebox.showerror("Save Error", str(e), parent=dlg)

            tk.Button(btn_f, text="❌ Close",
                      command=dlg.destroy,
                      bg="#555", fg=CLR["white"],
                      font=FONT_SM, relief="flat",
                      padx=10, pady=5).pack(side="left", padx=12)

            tk.Button(btn_f, text="💾 Save as .txt",
                      command=_save_txt,
                      bg=CLR["btn"], fg=CLR["white"],
                      font=FONT_SM, relief="flat",
                      padx=10, pady=5).pack(side="left", padx=4)

            tk.Button(btn_f, text="🖨️ Print Statement",
                      command=_do_print,
                      bg=CLR["success"], fg=CLR["white"],
                      font=FONT_SM, relief="flat",
                      padx=10, pady=5).pack(side="right", padx=12)

        except Exception as e:
            messagebox.showerror("Statement Error",
                f"Could not build statement:\n{e}")

    # ── Payment saving ────────────────────────────────────────────────────────
    def _save_payment(self):
        if not self.selected_customer_id:
            messagebox.showwarning("No Customer", "Select a customer first.")
            return
        amt_str = self.pay_vars["pay_amount"].get().strip()
        if not amt_str:
            messagebox.showwarning("Missing Amount", "Enter a payment amount.")
            return
        try:
            amount = float(amt_str.replace(",", ""))
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Amount",
                "Amount must be a positive number.")
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
            new_bal     = current_bal - amount

            db.execute(
                "INSERT INTO dbo.Payment "
                "(trano,Sid,paydate,amount,bal,paymode,chequeno,dbank,ddocno,DoneBy) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (ref, self.selected_customer_id, now, amount,
                 new_bal, mode, chequeno, bank, ref, self.current_user))

            db.execute(
                "UPDATE dbo.Credit_Customer SET balance=? WHERE id=?",
                (new_bal, self.selected_customer_id))

            messagebox.showinfo(
                "Payment Saved",
                f"✅ KES {money(amount)} recorded.\n"
                f"New Balance: KES {money(new_bal)}")

            if PRINT_OK and messagebox.askyesno("Print", "Print payment receipt?"):
                print_payment_receipt(_printer_cfg, {
                    "payno":    "—",
                    "date":     str(now)[:19],
                    "customer": self.selected_customer_name,
                    "amount":   amount,
                    "mode":     mode,
                    "chequeno": chequeno or "",
                    "balance":  new_bal,
                    "doneby":   self.current_user,
                    "trano":    ref or "",
                })

            self._clear_payment_form()
            self._load_customers()
            self._load_invoices()

        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def _clear_payment_form(self):
        for key, var in self.pay_vars.items():
            var.set("CASH" if key == "pay_mode" else "")

# ═════════════════════════════════════════════════════════════════════════════
# SUPPLIERS
# ═════════════════════════════════════════════════════════════════════════════
# =============================================================================
#  SuppliersFrame — FarmersDesk POS
#  Requires: dbo.Stock_Replenish_Lines (run migration_Stock_Replenish_Lines.sql)
#
#  Fixes applied vs previous version:
#    1. _next_trano  — cast changed from INT → NUMERIC(10,0) to match schema
#    2. _do_pay      — PayMode now written to SInv.PayMode (add column below)
#    3. _reprint_grn — LineAmt column alias fixed (was "Amount", now computed)
#    4. All date filter widgets default correctly on every panel reload
#
#  Pre-requisite SQL (run once):
#    ALTER TABLE dbo.SInv ADD PayMode VARCHAR(20) NULL;
# =============================================================================

COMPANY = {
    "name":    "FarmersDesk Ltd",
    "address": "P.O. Box 26719-00504, Nairobi, Kenya",
    "phone":   "+254 740129670",
    "email":   "info@farmersdesk.co.ke",
    "pin":     "P051513622V",
}


class SuppliersFrame(ttk.Frame):
    def __init__(self, parent, current_user: str):
        super().__init__(parent)
        self.current_user = current_user
        self.selected_supplier_id   = None
        self.selected_supplier_name = ""
        self._build()
        self._load_suppliers()

    _FIELDS = [
        ("Name *",         "name",     "entry", []),
        ("Tel / Phone",    "telno",    "entry", []),
        ("Town",           "town",     "entry", []),
        ("Contact Person", "cperson",  "entry", []),
        ("PIN",            "pin",      "entry", []),
        ("Amount Owing",   "amtowing", "entry", []),
    ]

    # =========================================================================
    #  DATABASE HELPERS
    # =========================================================================

    def _fetch_product_names(self):
        """Return all product names from Stock_item, sorted."""
        try:
            _, rows = db.fetchall(
                "SELECT name FROM dbo.Stock_item "
                "WHERE name IS NOT NULL ORDER BY name", ())
            return [r[0] for r in rows if r[0]]
        except Exception as e:
            print(f"[_fetch_product_names] {e}")
            return []

    def _fetch_last_price(self, product_name: str, supplier_id=None) -> tuple:
        """
        Returns (unit_rate, date_str) for the most recent GRN line containing
        this product from dbo.Stock_Replenish_Lines.
        Falls back to Stock_item.costprice, then (None, None).
        supplier_id scopes the search to that supplier only if provided.
        """
        try:
            if supplier_id:
                _, row = db.fetchone(
                    """
                    SELECT TOP 1 srl.UnitRate, sr.issuedate
                    FROM dbo.Stock_Replenish_Lines srl
                    INNER JOIN dbo.Stock_Replenish sr ON sr.trano = srl.TraNo
                    WHERE srl.ItemName = ?
                      AND sr.sid = ?
                      AND srl.UnitRate > 0
                    ORDER BY sr.issuedate DESC
                    """,
                    (product_name, supplier_id))
            else:
                _, row = db.fetchone(
                    """
                    SELECT TOP 1 srl.UnitRate, sr.issuedate
                    FROM dbo.Stock_Replenish_Lines srl
                    INNER JOIN dbo.Stock_Replenish sr ON sr.trano = srl.TraNo
                    WHERE srl.ItemName = ?
                      AND srl.UnitRate > 0
                    ORDER BY sr.issuedate DESC
                    """,
                    (product_name,))

            if row and row[0]:
                return (round(float(row[0]), 2), str(row[1])[:10])
        except Exception as e:
            print(f"[_fetch_last_price] lines lookup: {e}")

        try:
            _, row = db.fetchone(
                "SELECT TOP 1 costprice FROM dbo.Stock_item WHERE name = ?",
                (product_name,))
            if row and row[0]:
                return (round(float(row[0]), 2), "stock cost price")
        except Exception as e:
            print(f"[_fetch_last_price] costprice fallback: {e}")

        return (None, None)

    def _next_trano(self) -> str:
        """
        Safe TraNo sequence — uses NUMERIC(10,0) cast to match actual column type.
        Non-numeric rows (old journal entries) are ignored via TRY_CAST.
        """
        try:
            _, row = db.fetchone(
                "SELECT ISNULL(MAX(TRY_CAST(trano AS NUMERIC(10,0))), 0) "
                "FROM dbo.Stock_Replenish", ())
            return str(int((row[0] if row else 0) + 1))
        except Exception:
            return "1"

    def _validate_dates(self, from_entry, to_entry, status_label):
        """
        Parse two date Entry widgets (YYYY-MM-DD).
        Returns (d1, d2) on success or sets status label and returns (None, None).
        """
        try:
            d1 = datetime.datetime.strptime(from_entry.get().strip(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(to_entry.get().strip(),   "%Y-%m-%d")
            if d1 > d2:
                raise ValueError("From date is after To date")
            return d1, d2
        except ValueError as e:
            status_label.config(
                text=f"⚠️  Invalid date: {e}  (use YYYY-MM-DD)",
                fg="#c0392b")
            return None, None

    # =========================================================================
    #  BUILD UI
    # =========================================================================

    def _build(self):
        # ── TOP: supplier master table ────────────────────────────────────────
        top = tk.LabelFrame(self, text="Suppliers Profile & Accounts Ledger",
                            font=FONT_H2, bg=CLR["bg"], fg=CLR["text_dark"],
                            padx=6, pady=6)
        top.pack(fill="x", padx=10, pady=(10, 4))

        ctrl = tk.Frame(top, bg=CLR["bg"])
        ctrl.pack(fill="x", pady=(0, 4))

        tk.Label(ctrl, text="Search:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.s_search = tk.StringVar()
        e = ttk.Entry(ctrl, textvariable=self.s_search, font=FONT_BODY, width=18)
        e.pack(side="left", padx=4)
        e.bind("<Return>",     lambda _: self._load_suppliers())
        e.bind("<KeyRelease>", self._on_search_keyup)

        for txt, cmd, kw in [
            ("🔍 Search",                      self._load_suppliers,                            {}),
            ("➕ Add",                          self._add,                                       {"success": True}),
            ("✏️ Edit",                         self._edit,                                      {}),
            ("🗑 Delete",                       self._delete,                                    {"danger": True}),
            ("📥 Incoming Invoice (Stock In)",  lambda: self._open_invoice_wizard("INCOMING"),   {"success": True}),
            ("📤 Outgoing Invoice (Stock Out)", lambda: self._open_invoice_wizard("OUTGOING"),   {"accent": True}),
        ]:
            btn = tk.Button(ctrl, text=txt, command=cmd)
            style_btn(btn, **kw)
            btn.pack(side="left", padx=2)

        sup_cols = ["ID", "Name", "Tel", "Town", "Contact Person",
                    "Amount Owing (KES)", "PIN"]
        self.sup_tbl = DataTable(top, sup_cols, height=6)
        self.sup_tbl.pack(fill="x")
        self.sup_tbl.bind_select(self._on_select)

        self.sup_status = tk.Label(top, text="", font=FONT_SM,
                                   bg=CLR["bg"], anchor="w")
        self.sup_status.pack(fill="x")

        # ── BOTTOM: three sub-ledger panels ───────────────────────────────────
        bottom = tk.Frame(self, bg=CLR["bg"])
        bottom.pack(fill="both", expand=True, padx=10, pady=4)
        for col in range(2):
            bottom.columnconfigure(col, weight=1)
        bottom.rowconfigure(0, weight=1)

        # ── Left: Supplier Ledger Invoices ────────────────────────────────────
        inv_frame = tk.LabelFrame(bottom, text="Supplier Ledger Invoices",
                                  font=FONT_H2, bg=CLR["bg"],
                                  fg=CLR["text_dark"], padx=6, pady=6)
        inv_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        inv_frame.rowconfigure(1, weight=1)
        inv_frame.columnconfigure(0, weight=1)

        ictl = tk.Frame(inv_frame, bg=CLR["bg"])
        ictl.grid(row=0, column=0, sticky="w", pady=(0, 4))

        tk.Label(ictl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.sinv_from = ttk.Entry(ictl, font=FONT_SM, width=12)
        self.sinv_from.insert(0, month_start())
        self.sinv_from.pack(side="left", padx=2)

        tk.Label(ictl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.sinv_to = ttk.Entry(ictl, font=FONT_SM, width=12)
        self.sinv_to.insert(0, today_str())
        self.sinv_to.pack(side="left", padx=2)

        lb = tk.Button(ictl, text="📋 Load", command=self._load_sinv)
        style_btn(lb)
        lb.pack(side="left", padx=4)

        pay_btn = tk.Button(ictl, text="💳 Record Payment",
                            command=self._record_payment)
        style_btn(pay_btn, success=True)
        pay_btn.pack(side="left", padx=4)

        del_inv_btn = tk.Button(ictl, text="🗑 Delete Invoice",
                                command=self._delete_invoice)
        style_btn(del_inv_btn, danger=True)
        del_inv_btn.pack(side="left", padx=4)

        sinv_cols = ["RecId", "Inv Date", "TraNo", "Detail",
                     "Inv Amount (KES)", "Paid (KES)", "Balance (KES)", "Pay Mode"]
        self.sinv_tbl = DataTable(inv_frame, sinv_cols)
        self.sinv_tbl.grid(row=1, column=0, sticky="nsew")

        self.sinv_status = tk.Label(inv_frame, text="← Select a supplier",
                                    font=FONT_SM, bg=CLR["bg"],
                                    fg=CLR["text_dark"], anchor="w")
        self.sinv_status.grid(row=2, column=0, sticky="w")

        # ── Centre: Stock Document Ledger ─────────────────────────────────────
        rep_frame = tk.LabelFrame(bottom, text="Stock Document Ledger",
                                  font=FONT_H2, bg=CLR["bg"],
                                  fg=CLR["text_dark"], padx=6, pady=6)
        rep_frame.grid(row=0, column=1, sticky="nsew", padx=2)
        rep_frame.rowconfigure(1, weight=1)
        rep_frame.columnconfigure(0, weight=1)

        rctl = tk.Frame(rep_frame, bg=CLR["bg"])
        rctl.grid(row=0, column=0, sticky="w", pady=(0, 4))

        tk.Label(rctl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.rep_from = ttk.Entry(rctl, font=FONT_SM, width=12)
        self.rep_from.insert(0, month_start())
        self.rep_from.pack(side="left", padx=2)

        tk.Label(rctl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.rep_to = ttk.Entry(rctl, font=FONT_SM, width=12)
        self.rep_to.insert(0, today_str())
        self.rep_to.pack(side="left", padx=2)

        rlb = tk.Button(rctl, text="📋 Load", command=self._load_replenishments)
        style_btn(rlb)
        rlb.pack(side="left", padx=4)

        rprint_btn = tk.Button(rctl, text="🖨 Reprint GRN",
                               command=self._reprint_grn)
        style_btn(rprint_btn)
        rprint_btn.pack(side="left", padx=4)

        rep_cols = ["TraNo", "Issue Date", "Due Date", "Doc No",
                    "Amount (KES)", "VAT (KES)", "Mode"]
        self.rep_tbl = DataTable(rep_frame, rep_cols)
        self.rep_tbl.grid(row=1, column=0, sticky="nsew")

        self.rep_status = tk.Label(rep_frame, text="← Select a supplier",
                                   font=FONT_SM, bg=CLR["bg"],
                                   fg=CLR["text_dark"], anchor="w")
        self.rep_status.grid(row=2, column=0, sticky="w")


    # =========================================================================
    #  SUPPLIER TABLE — LOAD / ADD / EDIT / DELETE
    # =========================================================================

    def _on_search_keyup(self, event=None):
        if hasattr(self, "_search_after_id"):
            self.after_cancel(self._search_after_id)
        self._search_after_id = self.after(220, self._load_suppliers)

    def _load_suppliers(self):
        q = f"%{self.s_search.get().strip()}%"
        try:
            _, rows = db.fetchall(
                "SELECT supplierid, name, telno, town, cperson, AmountOwing, pin "
                "FROM dbo.Supplier "
                "WHERE name LIKE ? OR town LIKE ? OR cperson LIKE ? "
                "ORDER BY name", (q, q, q))
            self.sup_tbl.load([
                [r[0], r[1] or "", r[2] or "", r[3] or "",
                 r[4] or "", money(r[5]), r[6] or ""]
                for r in rows])
            total_owe = sum(float(r[5]) for r in rows if r[5])
            self.sup_status.config(
                text=f"{len(rows)} suppliers  |  Total Owing: KES {money(total_owe)}",
                fg=CLR["text_dark"])
        except Exception as e:
            self.sup_status.config(text=f"Error: {str(e)[:80]}", fg="#c0392b")

    def _add(self):
        dlg = FormDialog(self.winfo_toplevel(), "Add Supplier", self._FIELDS)
        self.wait_window(dlg)
        if not dlg.result or not dlg.result.get("name"):
            return
        d = dlg.result
        try:
            db.execute(
                "INSERT INTO dbo.Supplier (name,telno,town,cperson,pin,AmountOwing) "
                "VALUES (?,?,?,?,?,?)",
                (d["name"], d["telno"], d["town"], d["cperson"],
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
        initial = {
            "name":     vals[1], "telno":    vals[2],
            "town":     vals[3], "cperson":  vals[4],
            "amtowing": vals[5].replace(",", ""), "pin": vals[6],
        }
        dlg = FormDialog(self.winfo_toplevel(), "Edit Supplier",
                         self._FIELDS, initial)
        self.wait_window(dlg)
        if not dlg.result:
            return
        d = dlg.result
        try:
            db.execute(
                "UPDATE dbo.Supplier "
                "SET name=?,telno=?,town=?,cperson=?,pin=?,AmountOwing=? "
                "WHERE supplierid=?",
                (d["name"], d["telno"], d["town"], d["cperson"],
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
        if not vals:
            return
        self.selected_supplier_id   = vals[0]
        self.selected_supplier_name = vals[1]
        self._load_sinv()
        self._load_replenishments()

    # =========================================================================
    #  SUB-LEDGER LOADERS
    # =========================================================================

    def _load_sinv(self):
        if not self.selected_supplier_id:
            return
        d1, d2 = self._validate_dates(
            self.sinv_from, self.sinv_to, self.sinv_status)
        if d1 is None:
            return
        try:
            _, rows = db.fetchall(
                "SELECT RecId, InvDate, TraNo, Detail, InvAmount, Paid, Balance, "
                "       ISNULL(PayMode, '') "
                "FROM dbo.SInv "
                "WHERE SId=? AND InvDate BETWEEN ? AND ? "
                "ORDER BY InvDate DESC",
                (self.selected_supplier_id, d1, d2))
            self.sinv_tbl.load([
                [r[0], str(r[1])[:10], r[2] or "", r[3] or "",
                 money(r[4]), money(r[5]), money(r[6]), r[7]]
                for r in rows])
            outstanding = sum(float(r[6]) for r in rows if r[6])
            self.sinv_status.config(
                text=f"{len(rows)} invoices  |  Outstanding: KES {money(outstanding)}",
                fg=CLR["text_dark"])
        except Exception as e:
            self.sinv_status.config(text=f"Error: {str(e)[:80]}", fg="#c0392b")

    def _load_replenishments(self):
        if not self.selected_supplier_id:
            return
        d1, d2 = self._validate_dates(
            self.rep_from, self.rep_to, self.rep_status)
        if d1 is None:
            return
        try:
            _, rows = db.fetchall(
                "SELECT trano, issuedate, datedue, docno, amount, vatamount, dmode "
                "FROM dbo.Stock_Replenish "
                "WHERE sid=? AND issuedate BETWEEN ? AND ? "
                "ORDER BY issuedate DESC",
                (self.selected_supplier_id, d1, d2))
            self.rep_tbl.load([
                [r[0], str(r[1])[:10],
                 str(r[2])[:10] if r[2] else "",
                 r[3] or "", money(r[4]), money(r[5]), r[6] or ""]
                for r in rows])
            total = sum(float(r[4]) for r in rows if r[4])
            self.rep_status.config(
                text=f"{len(rows)} documents  |  Total: KES {money(total)}",
                fg=CLR["text_dark"])
        except Exception as e:
            self.rep_status.config(text=f"Error: {str(e)[:80]}", fg="#c0392b")

    def _delete_invoice(self):
        vals = self.sinv_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Invoice",
                                "Select an invoice row to delete.")
            return

        rec_id     = vals[0]
        trano      = vals[2]
        detail     = vals[3]
        inv_amount = vals[4]
        balance    = vals[6]

        if not messagebox.askyesno(
                "Confirm Delete Invoice",
                f"Delete invoice #{trano}?\n\n"
                f"Detail : {detail}\n"
                f"Amount : KES {inv_amount}\n"
                f"Balance: KES {balance}\n\n"
                f"⚠️  This will also reduce the supplier's\n"
                f"   AmountOwing by the outstanding balance.\n\n"
                f"This cannot be undone."):
            return

        try:
            # Reduce supplier AmountOwing by the remaining balance
            bal_float = float(str(balance).replace(",", "") or 0)
            if bal_float > 0:
                db.execute(
                    "UPDATE dbo.Supplier "
                    "SET AmountOwing = CASE "
                    "  WHEN AmountOwing >= ? THEN AmountOwing - ? "
                    "  ELSE 0 END "
                    "WHERE supplierid = ?",
                    (bal_float, bal_float, self.selected_supplier_id))

            # Delete the invoice record
            db.execute("DELETE FROM dbo.SInv WHERE RecId=?", (rec_id,))

            messagebox.showinfo(
                "Deleted",
                f"✅ Invoice #{trano} deleted.\n"
                f"Supplier balance reduced by KES {balance}.")

            self._load_sinv()
            self._load_suppliers()

        except Exception as e:
            messagebox.showerror("Delete Error", str(e))

    def _record_payment(self):
        vals = self.sinv_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Invoice",
                                "Select an invoice row to record a payment against.")
            return

        rec_id       = vals[0]
        trano        = vals[2]
        inv_amount   = float(str(vals[4]).replace(",", "") or 0)
        already_paid = float(str(vals[5]).replace(",", "") or 0)
        balance      = float(str(vals[6]).replace(",", "") or 0)

        if balance <= 0:
            messagebox.showinfo("Fully Paid",
                                f"Invoice #{trano} is already fully paid.")
            return

        win = tk.Toplevel(self)
        win.title(f"💳 Record Payment — Invoice #{trano}")
        win.geometry("400x280")
        win.configure(bg=CLR["bg"])
        win.grab_set()
        win.resizable(False, False)

        tk.Label(win, text=f"Invoice #{trano}", font=FONT_H2,
                 bg=CLR["bg"], fg=CLR["header"]).pack(pady=(12, 2))

        info_f = tk.Frame(win, bg=CLR["bg"])
        info_f.pack(fill="x", padx=20, pady=4)

        for label, value in [
            ("Invoice Amount:", f"KES {money(inv_amount)}"),
            ("Already Paid:",   f"KES {money(already_paid)}"),
            ("Outstanding:",    f"KES {money(balance)}"),
        ]:
            row = tk.Frame(info_f, bg=CLR["bg"])
            row.pack(fill="x", pady=1)
            tk.Label(row, text=label, font=FONT_SM, bg=CLR["bg"],
                     width=18, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Helvetica", 10, "bold"),
                     bg=CLR["bg"]).pack(side="left")

        form_f = tk.Frame(win, bg=CLR["bg"])
        form_f.pack(fill="x", padx=20, pady=8)

        tk.Label(form_f, text="Amount Paying (KES):", font=FONT_SM,
                 bg=CLR["bg"]).grid(row=0, column=0, sticky="w")
        v_pay = tk.StringVar(value=f"{balance:.2f}")
        e_pay = ttk.Entry(form_f, textvariable=v_pay, font=FONT_BODY, width=16)
        e_pay.grid(row=0, column=1, padx=8, pady=4)
        e_pay.select_range(0, "end")
        e_pay.focus()

        tk.Label(form_f, text="Payment Mode:", font=FONT_SM,
                 bg=CLR["bg"]).grid(row=1, column=0, sticky="w")
        v_pmode = tk.StringVar(value="CASH")
        ttk.Combobox(form_f, textvariable=v_pmode,
                     values=["CASH", "MPESA", "BANK TRANSFER", "CHEQUE"],
                     font=FONT_BODY, state="readonly", width=14
                     ).grid(row=1, column=1, padx=8, pady=4)

        tk.Label(form_f, text="Reference / Notes:", font=FONT_SM,
                 bg=CLR["bg"]).grid(row=2, column=0, sticky="w")
        v_ref = tk.StringVar()
        ttk.Entry(form_f, textvariable=v_ref, font=FONT_BODY, width=22
                  ).grid(row=2, column=1, padx=8, pady=4)

        def _do_pay():
            try:
                paying = float(v_pay.get().strip())
                if paying <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Invalid", "Enter a valid positive amount.",
                                       parent=win)
                return

            paying      = min(paying, balance)
            new_paid    = already_paid + paying
            new_balance = max(inv_amount - new_paid, 0)
            pmode       = v_pmode.get()

            try:
                db.execute(
                    "UPDATE dbo.SInv SET Paid=?, Balance=?, PayMode=? "
                    "WHERE RecId=?",
                    (new_paid, new_balance, pmode, rec_id))

                db.execute(
                    "UPDATE dbo.Supplier "
                    "SET AmountOwing = CASE "
                    "  WHEN AmountOwing >= ? THEN AmountOwing - ? "
                    "  ELSE 0 END "
                    "WHERE supplierid = ?",
                    (paying, paying, self.selected_supplier_id))

                messagebox.showinfo(
                    "Payment Recorded",
                    f"✅ KES {money(paying)} recorded via {pmode}.\n"
                    f"Remaining balance: KES {money(new_balance)}",
                    parent=win)
                win.destroy()
                self._load_sinv()
                self._load_suppliers()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=win)

        btn_f = tk.Frame(win, bg=CLR["bg"])
        btn_f.pack(side="bottom", fill="x", padx=20, pady=10)

        tk.Button(btn_f, text="✖ Cancel", command=win.destroy,
                  bg="#555", fg=CLR["white"], font=FONT_SM,
                  relief="flat", padx=12, pady=5).pack(side="left")

        pay_ok = tk.Button(btn_f, text="💳 Confirm Payment", command=_do_pay)
        style_btn(pay_ok, success=True)
        pay_ok.pack(side="right")

        self.wait_window(win)

    # =========================================================================
    #  REPRINT past GRN from the Stock Document Ledger panel
    # =========================================================================

    def _reprint_grn(self):
        vals = self.rep_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row",
                                "Select a GRN row from the Stock Document Ledger to reprint.")
            return

        trano  = vals[0]
        doc_no = vals[3]

        try:
            # TRY_CAST guards the join: SInv.TraNo is NVARCHAR,
            # Stock_Replenish.trano is NUMERIC(10,0) — implicit cast fails
            # on the old journal/adjustment rows that contain text values.
            _, hdr = db.fetchone(
                "SELECT sr.amount, sr.vatamount, sr.dmode, si.Detail "
                "FROM dbo.Stock_Replenish sr "
                "LEFT JOIN dbo.SInv si "
                "  ON TRY_CAST(si.TraNo AS NUMERIC(10,0)) = sr.trano "
                "WHERE sr.trano = ?", (trano,))
            if not hdr:
                messagebox.showerror("Not Found", f"GRN #{trano} not found.")
                return

            # Fetch line items — LineAmt is a computed column (Qty * UnitRate)
            _, line_rows = db.fetchall(
                "SELECT ItemName, Qty, UnitRate, LineAmt "
                "FROM dbo.Stock_Replenish_Lines "
                "WHERE TraNo = ? ORDER BY LineId",
                (trano,))

            if line_rows:
                items = [
                    {"name":   r[0],
                     "qty":    float(r[1]),
                     "rate":   float(r[2]),
                     "amount": float(r[3]) if r[3] is not None else float(r[1]) * float(r[2])}
                    for r in line_rows
                ]
            else:
                detail = hdr[3] or ""
                items  = self._parse_detail_items(detail)

            detail_raw = hdr[3] or ""
            direction  = "OUTGOING" if detail_raw.startswith("RTN:") else "INCOMING"

            self._print_grn_document(
                doc_no        = doc_no,
                supplier_name = self.selected_supplier_name,
                items         = items,
                vat_amount    = float(hdr[1] or 0),
                mode          = hdr[2] or "",
                direction     = direction,
                issued_by     = self.current_user,
            )
        except Exception as e:
            messagebox.showerror("Reprint Error", str(e))

    def _parse_detail_items(self, detail: str) -> list:
        """
        Fall-back parser: extract items from the legacy Detail string
        e.g. 'GRN: Sugar x10, Salt x5'
        Returns list of dicts with name/qty/rate/amount (rate=0 for legacy rows).
        """
        import re
        clean = detail.replace("GRN: ", "").replace("RTN: ", "")
        items = []
        for part in clean.split(","):
            part = part.strip()
            m = re.match(r"^(.+?)\s+x([\d.]+)$", part)
            if m:
                items.append({
                    "name":   m.group(1).strip(),
                    "qty":    float(m.group(2)),
                    "rate":   0.0,
                    "amount": 0.0,
                })
        return items

    # =========================================================================
    #  REVERSE / UNDO GRN
    # =========================================================================

    # =========================================================================
    #  INVOICE WIZARD  (INCOMING / OUTGOING)
    # =========================================================================

    def _open_invoice_wizard(self, direction: str):
        if not self.selected_supplier_id:
            messagebox.showinfo("Select Supplier",
                                "Please select a supplier from the table first.")
            return

        is_incoming = (direction == "INCOMING")
        win_title   = (
            f"📥 Incoming Invoice — Stock In  |  {self.selected_supplier_name}"
            if is_incoming else
            f"📤 Outgoing Invoice — Stock Out  |  {self.selected_supplier_name}"
        )
        hint_color = (CLR.get("success", "#27ae60") if is_incoming
                      else CLR.get("accent",  "#e67e22"))

        win = tk.Toplevel(self)
        win.title(win_title)
        win.minsize(900, 700)
        win.configure(bg=CLR["bg"])
        win.grab_set()

        # ── Direction banner ──────────────────────────────────────────────────
        banner_text = (
            "📥  INCOMING  —  Stock will be ADDED to inventory. "
            "Supplier balance increases on credit."
            if is_incoming else
            "📤  OUTGOING  —  Stock will be DEDUCTED from inventory. "
            "Supplier balance decreases."
        )
        tk.Label(win, text=banner_text, font=FONT_SM,
                 bg=hint_color, fg=CLR["white"],
                 anchor="w", padx=10, pady=5).pack(fill="x")

        # ── Live invoice number bar ───────────────────────────────────────────
        inv_bar = tk.Frame(win, bg=CLR.get("header", "#1a5276"), pady=4)
        inv_bar.pack(fill="x")

        tk.Label(inv_bar, text="Invoice No:", font=FONT_SM,
                 bg=CLR.get("header", "#1a5276"), fg=CLR["white"],
                 padx=10).pack(side="left")
        lbl_inv_no = tk.Label(inv_bar, text="— not entered yet —",
                              font=("Helvetica", 11, "bold"),
                              bg=CLR.get("header", "#1a5276"), fg="#f9ca24")
        lbl_inv_no.pack(side="left")
        tk.Label(inv_bar,
                 text=f"  |  Supplier: {self.selected_supplier_name}",
                 font=FONT_SM,
                 bg=CLR.get("header", "#1a5276"), fg=CLR["white"]
                 ).pack(side="left")

        # ── Invoice header fields ─────────────────────────────────────────────
        meta_f = tk.LabelFrame(win, text="Invoice Information",
                               bg=CLR["bg"], font=FONT_SM, fg=CLR["header"])
        meta_f.pack(fill="x", padx=10, pady=5)

        for i, lbl in enumerate(["Invoice / Doc No *", "Payment Mode",
                                  "VAT Amount (KES)", "Invoice Type"]):
            meta_f.columnconfigure(i, weight=1)
            tk.Label(meta_f, text=lbl, font=FONT_SM,
                     bg=CLR["bg"]).grid(row=0, column=i, sticky="w",
                                        padx=5, pady=(4, 0))

        v_doc = tk.StringVar()
        e_doc = ttk.Entry(meta_f, textvariable=v_doc, font=FONT_BODY)
        e_doc.grid(row=1, column=0, sticky="ew", padx=5, pady=3)
        e_doc.focus()

        def _on_doc_change(*_):
            val = v_doc.get().strip()
            lbl_inv_no.config(text=val if val else "— not entered yet —")
        v_doc.trace_add("write", _on_doc_change)

        v_mode = tk.StringVar(value="CREDIT" if is_incoming else "CASH")
        ttk.Combobox(meta_f, textvariable=v_mode,
                     values=["CREDIT", "CASH", "MPESA", "BANK TRANSFER"],
                     font=FONT_BODY, state="readonly"
                     ).grid(row=1, column=1, sticky="ew", padx=5, pady=3)

        v_vat = tk.StringVar(value="0.0")
        ttk.Entry(meta_f, textvariable=v_vat, font=FONT_BODY
                  ).grid(row=1, column=2, sticky="ew", padx=5, pady=3)

        inv_type_display = "RECEIVING (GRN)" if is_incoming else "RETURN / CREDIT NOTE"
        tk.Label(meta_f, text=inv_type_display, font=FONT_BODY,
                 bg=hint_color, fg=CLR["white"],
                 relief="flat", padx=8, pady=4
                 ).grid(row=1, column=3, sticky="ew", padx=5, pady=3)

        # ── Line item entry row ───────────────────────────────────────────────
        line_f = tk.LabelFrame(win, text="Add Line Item",
                               bg=CLR["bg"], font=FONT_SM, fg=CLR["header"])
        line_f.pack(fill="x", padx=10, pady=5)

        for i, lbl in enumerate(["Product *", "Qty *", "Rate (KES) *"]):
            line_f.columnconfigure(i, weight=2 if i == 0 else 1)
            tk.Label(line_f, text=lbl, font=FONT_SM,
                     bg=CLR["bg"]).grid(row=0, column=i, sticky="w", padx=5)

        # ── Product autocomplete ──────────────────────────────────────────────
        product_names = self._fetch_product_names()
        v_pname = tk.StringVar()

        ac_frame = tk.Frame(line_f, bg=CLR["bg"])
        ac_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=3)
        ac_frame.columnconfigure(0, weight=1)

        e_pname = ttk.Entry(ac_frame, textvariable=v_pname, font=FONT_BODY)
        e_pname.grid(row=0, column=0, sticky="ew")

        ac_lb = tk.Listbox(ac_frame, font=FONT_BODY, height=6,
                           selectmode="browse", relief="solid", bd=1,
                           exportselection=False)

        def _ac_show(matches):
            if not matches:
                ac_lb.grid_remove(); return
            ac_lb.delete(0, "end")
            for m in matches:
                ac_lb.insert("end", m)
            ac_lb.grid(row=1, column=0, sticky="ew")
            ac_lb.lift()

        def _ac_hide(_=None):
            ac_lb.grid_remove()

        def _ac_type(*_):
            typed = v_pname.get().strip().lower()
            if not typed:
                _ac_hide(); return
            _ac_show([p for p in product_names
                      if typed in p.lower()][:12])

        def _on_product_selected(name: str):
            name = name.strip()
            if not name:
                lbl_last_price.config(text=""); return

            rate, date = self._fetch_last_price(
                name, supplier_id=self.selected_supplier_id)
            if rate is None:
                rate, date = self._fetch_last_price(name)

            if rate is not None:
                scope = ("this supplier" if date and date != "stock cost price"
                         else "stock cost price")
                lbl_last_price.config(
                    text=f"📦 Last received @ KES {rate:,.2f}  ({date})  [{scope}]",
                    fg=CLR.get("accent", "#e67e22"))
                if not v_rate.get().strip():
                    v_rate.set(f"{rate:.2f}")
            else:
                lbl_last_price.config(
                    text="No previous receipt found for this product",
                    fg=CLR.get("text_dark", "#555"))

        def _ac_pick(event=None):
            if not ac_lb.curselection():
                return
            chosen = ac_lb.get(ac_lb.curselection()[0])
            v_pname.set(chosen)
            _ac_hide()
            _on_product_selected(chosen)
            e_qty.focus()

        def _ac_arrow(event):
            if not ac_lb.winfo_ismapped():
                return
            cur  = ac_lb.curselection()
            size = ac_lb.size()
            if not size:
                return
            if cur:
                new = cur[0] + (1 if event.keysym == "Down" else -1)
            else:
                new = 0 if event.keysym == "Down" else size - 1
            new = max(0, min(new, size - 1))
            ac_lb.selection_clear(0, "end")
            ac_lb.selection_set(new)
            ac_lb.see(new)

        def _ac_return(event):
            if ac_lb.winfo_ismapped() and ac_lb.curselection():
                _ac_pick(); return "break"

        v_pname.trace_add("write", _ac_type)
        ac_lb.bind("<<ListboxSelect>>", _ac_pick)
        e_pname.bind("<Down>",     _ac_arrow)
        e_pname.bind("<Up>",       _ac_arrow)
        e_pname.bind("<Return>",   _ac_return)
        e_pname.bind("<Escape>",   _ac_hide)
        e_pname.bind("<FocusOut>", lambda e: ac_frame.after(
            150, lambda: (_ac_hide(),
                          _on_product_selected(v_pname.get()))))

        hint_txt = (f"({len(product_names)} products loaded)"
                    if product_names else "⚠️ No products found in Stock_item")
        tk.Label(line_f, text=hint_txt, font=FONT_SM, bg=CLR["bg"],
                 fg=CLR["accent"] if product_names else "red"
                 ).grid(row=2, column=0, sticky="w", padx=5)

        # ── Qty / Rate ────────────────────────────────────────────────────────
        v_qty  = tk.StringVar()
        v_rate = tk.StringVar()
        e_qty  = ttk.Entry(line_f, textvariable=v_qty,  font=FONT_BODY)
        e_rate = ttk.Entry(line_f, textvariable=v_rate, font=FONT_BODY)
        e_qty.grid( row=1, column=1, sticky="ew", padx=5, pady=3)
        e_rate.grid(row=1, column=2, sticky="ew", padx=5, pady=3)

        # Live line total hint
        lbl_line_total = tk.Label(line_f, text="", font=FONT_SM,
                                  bg=CLR["bg"], fg=CLR.get("header", "#1a5276"))
        lbl_line_total.grid(row=2, column=2, sticky="e", padx=5)

        def _update_line_total(*_):
            try:
                q = float(v_qty.get().strip() or 0)
                r = float(v_rate.get().strip() or 0)
                lbl_line_total.config(text=f"Line Total: KES {money(q * r)}")
            except ValueError:
                lbl_line_total.config(text="")

        v_qty.trace_add("write",  _update_line_total)
        v_rate.trace_add("write", _update_line_total)

        lbl_last_price = tk.Label(line_f, text="", font=FONT_SM,
                                  bg=CLR["bg"],
                                  fg=CLR.get("accent", "#e67e22"))
        lbl_last_price.grid(row=2, column=1, columnspan=2,
                            sticky="w", padx=5)

        # ── Session items list ────────────────────────────────────────────────
        invoice_items = []

        item_cols = ["Product Description", "Qty", "Rate (KES)", "Total (KES)"]
        tbl_frame = tk.Frame(win, bg=CLR["bg"])
        tbl_frame.pack(fill="both", expand=True, padx=10, pady=5)
        items_tbl = DataTable(tbl_frame, item_cols, height=8)
        items_tbl.pack(fill="both", expand=True)

        lbl_summary = tk.Label(
            win,
            text="Sub-Total: KES 0.00  |  VAT: KES 0.00  |  Gross Total: KES 0.00",
            font=("Helvetica", 11, "bold"),
            bg=CLR["bg"], fg=hint_color)
        lbl_summary.pack(pady=4)

        def _recalc():
            sub = sum(i["amount"] for i in invoice_items)
            try:
                vat = float(v_vat.get().strip() or 0)
            except ValueError:
                vat = 0.0
            lbl_summary.config(
                text=(f"Sub-Total: KES {money(sub)}  |  "
                      f"VAT: KES {money(vat)}  |  "
                      f"Gross Total: KES {money(sub + vat)}"))

        def _add_line():
            name = v_pname.get().strip()
            if not name:
                messagebox.showwarning("Required",
                    "Please select or type a product name.", parent=win)
                return
            try:
                qty  = float(v_qty.get().strip())
                rate = float(v_rate.get().strip())
                if qty <= 0 or rate <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Invalid Input",
                    "Quantity and Rate must be positive numbers.", parent=win)
                return
            invoice_items.append({
                "name": name, "qty": qty,
                "rate": rate, "amount": qty * rate,
            })
            items_tbl.load([
                [i["name"], i["qty"], money(i["rate"]), money(i["amount"])]
                for i in invoice_items])
            _recalc()
            v_pname.set(""); v_qty.set(""); v_rate.set("")
            lbl_last_price.config(text="")
            lbl_line_total.config(text="")
            e_pname.focus()

        def _remove_line():
            sel = items_tbl.selected_values()
            if not sel:
                messagebox.showinfo("Select Row",
                    "Select a line to remove.", parent=win)
                return
            for idx, item in enumerate(invoice_items):
                if item["name"] == sel[0] and money(item["rate"]) == sel[2]:
                    invoice_items.pop(idx); break
            items_tbl.load([
                [i["name"], i["qty"], money(i["rate"]), money(i["amount"])]
                for i in invoice_items])
            _recalc()

        def _edit_line():
            """Allow editing qty/rate of a selected line in-place."""
            sel = items_tbl.selected_values()
            if not sel:
                messagebox.showinfo("Select Row",
                    "Select a line to edit.", parent=win)
                return
            for idx, item in enumerate(invoice_items):
                if item["name"] == sel[0] and money(item["rate"]) == sel[2]:
                    # Pre-fill entry fields for re-entry
                    v_pname.set(item["name"])
                    v_qty.set(str(item["qty"]))
                    v_rate.set(str(item["rate"]))
                    invoice_items.pop(idx)
                    items_tbl.load([
                        [i["name"], i["qty"], money(i["rate"]), money(i["amount"])]
                        for i in invoice_items])
                    _recalc()
                    e_qty.focus()
                    break

        btn_add = tk.Button(line_f, text="➕ Add Line", command=_add_line)
        style_btn(btn_add, success=True)
        btn_add.grid(row=1, column=3, padx=5, pady=3)

        btn_rem = tk.Button(line_f, text="🗑 Remove", command=_remove_line)
        style_btn(btn_rem, danger=True)
        btn_rem.grid(row=1, column=4, padx=5, pady=3)

        btn_edit = tk.Button(line_f, text="✏️ Edit Line", command=_edit_line)
        style_btn(btn_edit)
        btn_edit.grid(row=1, column=5, padx=5, pady=3)

        # Bind Enter on qty/rate to add line
        e_qty.bind("<Return>",  lambda _: e_rate.focus())
        e_rate.bind("<Return>", lambda _: _add_line())

        # ── Print GRN (draft) ─────────────────────────────────────────────────
        def _print_grn():
            doc_no = v_doc.get().strip() or "DRAFT"
            if not invoice_items:
                messagebox.showwarning("Empty",
                    "Add at least one line item first.", parent=win)
                return
            try:
                vat = float(v_vat.get().strip() or 0)
            except ValueError:
                vat = 0.0
            self._print_grn_document(
                doc_no        = doc_no,
                supplier_name = self.selected_supplier_name,
                items         = invoice_items,
                vat_amount    = vat,
                mode          = v_mode.get(),
                direction     = direction,
                issued_by     = self.current_user,
            )

        # ── Commit ────────────────────────────────────────────────────────────
        def _commit():
            doc_no = v_doc.get().strip()
            if not doc_no:
                messagebox.showwarning("Required",
                    "Invoice / Doc No is required.", parent=win)
                return
            if not invoice_items:
                messagebox.showwarning("Required",
                    "Add at least one line item before saving.", parent=win)
                return
            try:
                sub_total   = sum(i["amount"] for i in invoice_items)
                vat_amount  = float(v_vat.get().strip() or 0)
                gross_total = sub_total + vat_amount
                mode        = v_mode.get().strip()

                if is_incoming:
                    paid_amount    = gross_total if mode != "CREDIT" else 0.0
                    balance_amount = gross_total - paid_amount
                else:
                    paid_amount    = 0.0
                    balance_amount = -gross_total

                detail = ("GRN: " if is_incoming else "RTN: ") + ", ".join(
                    f"{i['name']} x{i['qty']}" for i in invoice_items)
                if len(detail) > 500:
                    detail = detail[:497] + "..."

                today = datetime.datetime.now().date()
                trano = self._next_trano()

                # ── Header records ────────────────────────────────────────────
                db.execute(
                    "INSERT INTO dbo.Stock_Replenish "
                    "(trano,sid,issuedate,datedue,docno,amount,vatamount,dmode) "
                    "VALUES (?,?,?,?,?,?,?,?)",
                    (trano, self.selected_supplier_id, today, today,
                     doc_no, gross_total, vat_amount, mode))

                db.execute(
                    "INSERT INTO dbo.SInv "
                    "(SId,InvDate,TraNo,Detail,InvAmount,Paid,Balance,PayMode) "
                    "VALUES (?,?,?,?,?,?,?,?)",
                    (self.selected_supplier_id, today, trano,
                     detail, gross_total, paid_amount, abs(balance_amount),
                     mode if mode != "CREDIT" else None))

                # ── Line items ────────────────────────────────────────────────
                for item in invoice_items:
                    db.execute(
                        "INSERT INTO dbo.Stock_Replenish_Lines "
                        "(TraNo,ItemName,Qty,UnitRate) VALUES (?,?,?,?)",
                        (trano, item["name"], item["qty"], item["rate"]))

                    if is_incoming:
                        db.execute(
                            "UPDATE dbo.Stock_item "
                            "SET qtystock = qtystock + ?, costprice = ? "
                            "WHERE name = ?",
                            (item["qty"], item["rate"], item["name"]))
                    else:
                        db.execute(
                            "UPDATE dbo.Stock_item "
                            "SET qtystock = CASE "
                            "  WHEN qtystock >= ? THEN qtystock - ? "
                            "  ELSE 0 END WHERE name = ?",
                            (item["qty"], item["qty"], item["name"]))

                # ── Supplier balance ──────────────────────────────────────────
                if is_incoming and balance_amount > 0:
                    db.execute(
                        "UPDATE dbo.Supplier "
                        "SET AmountOwing = AmountOwing + ? "
                        "WHERE supplierid = ?",
                        (balance_amount, self.selected_supplier_id))
                elif not is_incoming:
                    db.execute(
                        "UPDATE dbo.Supplier "
                        "SET AmountOwing = CASE "
                        "  WHEN AmountOwing >= ? THEN AmountOwing - ? "
                        "  ELSE 0 END WHERE supplierid = ?",
                        (gross_total, gross_total, self.selected_supplier_id))

                label = "Incoming GRN" if is_incoming else "Outgoing Return"
                messagebox.showinfo(
                    "Saved",
                    f"✅ {label} #{doc_no} saved as GRN #{trano}.\n"
                    f"Lines saved: {len(invoice_items)}")
                win.destroy()

                self._load_suppliers()
                self._load_sinv()
                self._load_replenishments()

                if messagebox.askyesno(
                        "Print",
                        f"Print GRN document for {label} #{trano}?"):
                    self._print_itemized_stock_receipt(
                        trano, doc_no, invoice_items,
                        gross_total, paid_amount, abs(balance_amount))

            except ValueError:
                messagebox.showerror("Format Error",
                    "VAT must be a valid number.", parent=win)
            except Exception as e:
                messagebox.showerror("Database Error",
                    f"Failed to save invoice:\n{e}", parent=win)

        # ── Footer buttons ────────────────────────────────────────────────────
        btn_f = tk.Frame(win, bg=CLR["bg"])
        btn_f.pack(fill="x", side="bottom", pady=10)

        tk.Button(btn_f, text="✖ Cancel", command=win.destroy,
                  bg="#555", fg=CLR["white"], font=FONT_SM,
                  relief="flat", padx=15, pady=6).pack(side="left", padx=15)

        grn_btn = tk.Button(btn_f, text="🖨 Print GRN (Draft)",
                            command=_print_grn)
        style_btn(grn_btn)
        grn_btn.pack(side="left", padx=6)

        save_btn = tk.Button(
            btn_f,
            text=("💾 Save Incoming Invoice & Update Stock"
                  if is_incoming else
                  "💾 Save Outgoing Return & Adjust Stock"),
            command=_commit)
        style_btn(save_btn, success=True)
        save_btn.pack(side="right", padx=15)

        v_vat.trace_add("write", lambda *_: _recalc())
        self.wait_window(win)

    # =========================================================================
    #  PDF GRN DOCUMENT GENERATOR
    # =========================================================================

    def _print_grn_document(self, doc_no, supplier_name, items,
                             vat_amount, mode, direction, issued_by):
        """
        Generate an A4 GRN / Stock Return PDF, save to Desktop\GRNs,
        confirm saved, then open for printing.
        Requires: pip install reportlab
        """
        import os, tempfile, subprocess, sys

        # ── Import reportlab — install if missing ─────────────────────────────
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.units import mm
            from reportlab.platypus import (SimpleDocTemplate, Table,
                                            TableStyle, Paragraph, Spacer)
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER, TA_RIGHT
        except ImportError:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "reportlab"],
                               check=True)
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors
                from reportlab.lib.units import mm
                from reportlab.platypus import (SimpleDocTemplate, Table,
                                                TableStyle, Paragraph, Spacer)
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.enums import TA_CENTER, TA_RIGHT
            except Exception as ie:
                messagebox.showerror("Missing Library",
                    f"reportlab could not be installed:\n{ie}\n\n"
                    "Run:  pip install reportlab")
                return

        # ── Determine save path ───────────────────────────────────────────────
        def _grn_folder():
            home = os.path.expanduser("~")
            for candidate in [
                os.path.join(home, "Desktop", "GRNs"),
                os.path.join(home, "Documents", "GRNs"),
                os.path.join(tempfile.gettempdir(), "GRNs"),
            ]:
                try:
                    os.makedirs(candidate, exist_ok=True)
                    return candidate
                except Exception:
                    continue
            return tempfile.gettempdir()

        save_dir = _grn_folder()
        safe_doc = "".join(c for c in str(doc_no) if c.isalnum() or c in "-_")
        tmp_path = os.path.join(
            save_dir,
            f"GRN_{safe_doc}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

        # ── Build PDF ─────────────────────────────────────────────────────────
        C = COMPANY

        styles  = getSampleStyleSheet()
        bold    = ParagraphStyle("bold",   parent=styles["Normal"],
                                 fontName="Helvetica-Bold",  fontSize=10)
        normal  = ParagraphStyle("normal", parent=styles["Normal"],
                                 fontName="Helvetica",        fontSize=9)
        heading = ParagraphStyle("h1",     parent=styles["Normal"],
                                 fontName="Helvetica-Bold",  fontSize=15,
                                 alignment=TA_CENTER, spaceAfter=2)
        sub_h   = ParagraphStyle("sub",    parent=styles["Normal"],
                                 fontName="Helvetica",        fontSize=9,
                                 alignment=TA_CENTER, spaceAfter=3)
        pin_sty = ParagraphStyle("pin",    parent=styles["Normal"],
                                 fontName="Helvetica",        fontSize=8,
                                 alignment=TA_CENTER, spaceAfter=5,
                                 textColor=colors.HexColor("#555555"))
        right_p = ParagraphStyle("right",  parent=styles["Normal"],
                                 fontName="Helvetica-Bold",  fontSize=9,
                                 alignment=TA_RIGHT)

        doc = SimpleDocTemplate(
            tmp_path, pagesize=A4,
            leftMargin=28*mm, rightMargin=28*mm,
            topMargin=25*mm,  bottomMargin=25*mm)

        today    = datetime.datetime.now().strftime("%d %b %Y  %H:%M")
        grn_type = ("GOODS RECEIVED NOTE (GRN)"
                    if direction == "INCOMING" else "STOCK RETURN NOTE")
        story    = []

        # Letterhead
        story.append(Paragraph(C["name"].upper(), heading))
        story.append(Paragraph(
            f"{C['address']}  |  Tel: {C['phone']}  |  {C['email']}", sub_h))
        story.append(Paragraph(f"PIN: {C['pin']}", pin_sty))
        story.append(Table([[""]],
            colWidths=[120*mm],
            style=TableStyle([
                ("LINEBELOW",     (0, 0), (-1, 0), 1.2,
                 colors.HexColor("#1a5276")),
                ("TOPPADDING",    (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ])))
        story.append(Spacer(1, 3*mm))

        story.append(Paragraph(grn_type, ParagraphStyle(
            "gtype", parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1a5276"), spaceAfter=8)))

        # Meta block
        meta = [
            [Paragraph("<b>GRN / Doc No:</b>",   normal),
             Paragraph(str(doc_no),               bold),
             Paragraph("<b>Date &amp; Time:</b>", normal),
             Paragraph(today,                     bold)],
            [Paragraph("<b>Our PIN:</b>",         normal),
             Paragraph(C["pin"],                  bold),
             Paragraph("<b>Payment Mode:</b>",    normal),
             Paragraph(mode,                      bold)],
            [Paragraph("<b>Supplier:</b>",        normal),
             Paragraph(supplier_name,             bold),
             Paragraph("<b>Type:</b>",            normal),
             Paragraph("INCOMING — GRN" if direction == "INCOMING"
                       else "OUTGOING — RETURN",  bold)],
            [Paragraph("<b>Received by:</b>",     normal),
             Paragraph(issued_by,                 bold),
             Paragraph("<b>Company:</b>",         normal),
             Paragraph(C["name"],                 bold)],
        ]
        meta_tbl = Table(meta, colWidths=[32*mm, 56*mm, 32*mm, 36*mm])
        meta_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#eaf4fb")),
            ("BOX",           (0, 0), (-1, -1), 0.5, colors.grey),
            ("INNERGRID",     (0, 0), (-1, -1), 0.3, colors.lightgrey),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ]))
        story.append(meta_tbl)
        story.append(Spacer(1, 8*mm))

        # Line items table
        hdr_row = [Paragraph(f"<b>{t}</b>", bold) for t in
                   ["#", "Product Description", "Qty",
                    "Unit Rate (KES)", "Amount (KES)"]]
        rows = [hdr_row]
        for n, item in enumerate(items, 1):
            rows.append([
                Paragraph(str(n),                  normal),
                Paragraph(str(item["name"]),        normal),
                Paragraph(str(item["qty"]),         normal),
                Paragraph(f"{item['rate']:,.2f}",   normal),
                Paragraph(f"{item['amount']:,.2f}", normal),
            ])

        sub_total   = sum(i["amount"] for i in items)
        gross_total = sub_total + vat_amount
        n_items     = len(items)

        rows += [
            ["", "", "",
             Paragraph("<b>Sub-Total:</b>",   right_p),
             Paragraph(f"{sub_total:,.2f}",   bold)],
            ["", "", "",
             Paragraph("<b>VAT:</b>",         right_p),
             Paragraph(f"{vat_amount:,.2f}",  bold)],
            ["", "", "",
             Paragraph("<b>TOTAL (KES):</b>", right_p),
             Paragraph(f"{gross_total:,.2f}",
                       ParagraphStyle("tot", parent=styles["Normal"],
                                      fontName="Helvetica-Bold",
                                      fontSize=11))],
        ]

        items_tbl = Table(rows,
                          colWidths=[8*mm, 56*mm, 16*mm, 32*mm, 32*mm],
                          repeatRows=1)
        items_tbl.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0),  (-1, 0),        colors.HexColor("#1a5276")),
            ("TEXTCOLOR",      (0, 0),  (-1, 0),        colors.white),
            ("BOX",            (0, 0),  (-1, n_items),  0.5, colors.grey),
            ("INNERGRID",      (0, 0),  (-1, n_items),  0.3, colors.lightgrey),
            ("ROWBACKGROUNDS", (0, 1),  (-1, n_items),
             [colors.white, colors.HexColor("#f5f9fd")]),
            ("ALIGN",          (2, 1),  (-1, -1),       "RIGHT"),
            ("TOPPADDING",     (0, 0),  (-1, -1),       4),
            ("BOTTOMPADDING",  (0, 0),  (-1, -1),       4),
            ("LEFTPADDING",    (0, 0),  (-1, -1),       4),
            ("LINEABOVE",      (3, n_items + 1),
             (-1, n_items + 1), 0.8, colors.grey),
            ("LINEABOVE",      (3, n_items + 3),
             (-1, n_items + 3), 1.2, colors.HexColor("#1a5276")),
        ]))
        story.append(items_tbl)
        story.append(Spacer(1, 12*mm))

        # Signature block
        sig = [
            [Paragraph("Received / Verified by", normal),
             Paragraph("Approved by",             normal),
             Paragraph("Supplier Representative", normal)],
            [Paragraph("<br/><br/>_____________________", normal),
             Paragraph("<br/><br/>_____________________", normal),
             Paragraph("<br/><br/>_____________________", normal)],
            [Paragraph(f"Name: {issued_by}",          normal),
             Paragraph("Name: _______________",        normal),
             Paragraph(f"Supplier: {supplier_name}",   normal)],
            [Paragraph(f"Date: {today}",               normal),
             Paragraph("Date: _______________",        normal),
             Paragraph("Date: _______________",        normal)],
        ]
        sig_tbl = Table(sig, colWidths=[45*mm, 45*mm, 45*mm])
        sig_tbl.setStyle(TableStyle([
            ("BOX",           (0, 0), (-1, -1), 0.4, colors.grey),
            ("INNERGRID",     (0, 0), (-1, -1), 0.3, colors.lightgrey),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ]))
        story.append(sig_tbl)
        story.append(Spacer(1, 6*mm))

        story.append(Paragraph(
            f"This document is a Goods Received Note issued by {C['name']}. "
            f"PIN: {C['pin']}  |  {C['email']}  |  {C['phone']}. "
            "Computer-generated and valid without a physical signature "
            "unless otherwise specified.",
            ParagraphStyle("footer", parent=styles["Normal"],
                           fontName="Helvetica-Oblique", fontSize=7,
                           textColor=colors.grey, alignment=TA_CENTER)))

        # ── Save PDF ──────────────────────────────────────────────────────────
        try:
            doc.build(story)
        except Exception as build_err:
            messagebox.showerror(
                "PDF Build Error",
                f"Failed to generate PDF:\n{build_err}\n\n"
                f"Save path:\n{tmp_path}")
            return

        # ── Confirm saved, then open ──────────────────────────────────────────
        messagebox.showinfo(
            "GRN Saved",
            f"\u2705 PDF saved to:\n{tmp_path}\n\nOpening for print...")

        try:
            if sys.platform == "win32":
                os.startfile(tmp_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", tmp_path])
            else:
                subprocess.Popen(["xdg-open", tmp_path])
        except Exception as e:
            messagebox.showwarning(
                "Could Not Open",
                f"PDF saved but could not open automatically:\n{e}\n\n"
                f"Open manually from:\n{tmp_path}")


    # =========================================================================
    #  THERMAL RECEIPT PRINTER
    # =========================================================================

    def _print_itemized_stock_receipt(self, trano, docno, items,
                                       total, paid, balance):
        receipt_payload = {
            "trano":    f"GRN-{trano}",
            "date":     datetime.datetime.now().isoformat(),
            "cashier":  self.current_user,
            "customer": f"SUPPLIER: {self.selected_supplier_name}",
            "cash":     paid,
            "change":   0.0,
            "total":    total,
            "invno":    f"DOC-{docno}",
        }
        virtual_items = [{
            "code":  "GRN-LN",
            "name":  i["name"][:15],
            "qty":   i["qty"],
            "price": i["rate"],
            "total": i["amount"],
        } for i in items]
        try:
            print_sale_receipt(_printer_cfg, receipt_payload, virtual_items)
        except Exception as e:
            messagebox.showerror("Print Error",
                f"Could not send to printer:\n{e}")
# ═════════════════════════════════════════════════════════════════════════════
# INVENTORY
# ═════════════════════════════════════════════════════════════════════════════
class InventoryFrame(ttk.Frame):
    def __init__(self, parent, current_user: str):
        super().__init__(parent)
        self.current_user = current_user
        self._build()
        self._load_stock()

    # FIXED: Realigned fields to perfectly match the database keys utilized by CreateSalesFrame
    _PROD_FIELDS = [
        ("Product Code *",   "pcode",    "entry", []),
        ("Name *",           "name",     "entry", []),
        ("Category",         "category", "entry", []),
        ("Buying Price",     "bp",       "entry", []), 
        ("Retail Price",     "spr",      "entry", []), 
        ("Wholesale Price",  "spw",      "entry", []), 
        ("Opening Qty",      "qtystock", "entry", []),
        ("Re-Order Level",   "rlevel",   "entry", []),
        ("VAT",              "vat",      "combo", ["", "YES", "NO", "EXEMPT"]),
    ]

    def _build(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=4, pady=4)
        
        stock_tab = ttk.Frame(nb)
        nb.add(stock_tab, text=" 📦 Stock Items ")
        self._build_stock_tab(stock_tab)
        
        scard_tab = ttk.Frame(nb)
        nb.add(scard_tab, text=" 📋 Stock Card ")
        self._build_scard_tab(scard_tab)
        
        dmg_tab = ttk.Frame(nb)
        nb.add(dmg_tab, text=" ⚠️ Damaged Stock ")
        self._build_damaged_tab(dmg_tab)
        
        exp_tab = ttk.Frame(nb)
        nb.add(exp_tab, text=" 🗓️ Expiry ")
        self._build_expiry_tab(exp_tab)

    def _build_stock_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8)
        ctrl.pack(fill="x")
        
        tk.Label(ctrl, text="Search:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.stock_q = tk.StringVar()
        e = ttk.Entry(ctrl, textvariable=self.stock_q, font=FONT_BODY, width=22)
        e.pack(side="left", padx=4)
        e.bind("<Return>", lambda _: self._load_stock())
        
        tk.Label(ctrl, text="Category:", font=FONT_SM, bg=CLR["bg"]).pack(side="left", padx=(6,0))
        self.stock_cat = tk.StringVar()
        ttk.Entry(ctrl, textvariable=self.stock_cat, font=FONT_SM, width=12).pack(side="left", padx=2)
        
        for txt, cmd, kw in [
            ("🔍 Search", self._load_stock, {}),
            ("➕ Add", self._add_product, {"success": True}),
            ("✏️ Edit", self._edit_product, {}),
            ("🗑 Delete", self._delete_product, {"danger": True}),
        ]:
            btn = tk.Button(ctrl, text=txt, command=cmd)
            style_btn(btn, **kw)
            btn.pack(side="left", padx=2)
            
        self.low_stock_var = tk.BooleanVar()
        ttk.Checkbutton(ctrl, text="Low Stock Only", variable=self.low_stock_var,
                        command=self._load_stock).pack(side="left", padx=4)
                            
        cols = ["PCode", "Name", "Category", "Qty Stock", "Re-Order",
                "Buying Price (KES)", "Retail Price (KES)", "Wholesale (KES)", "VAT"]
        self.stock_tbl = DataTable(parent, cols)
        self.stock_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        
        self.stock_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.stock_status.pack(fill="x", padx=10)

    def _load_stock(self):
        """Fetches and displays inventory items while safely handling NULL values."""
        q = f"%{self.stock_q.get().strip()}%"
        cat = f"%{self.stock_cat.get().strip()}%"
        low = self.low_stock_var.get()
        
        # Enforce safety against missing fallback properties
        extra = "AND ISNULL(qtystock, 0) <= ISNULL(RLevel, 0)" if low else ""
        try:
            # FIXED: Added ISNULL updates on string targets so items with missing fields display cleanly
            query = (
                f"SELECT pcode, name, PCategory, qtystock, RLevel, bp, spr, spw, vat "
                f"FROM dbo.Stock_item "
                f"WHERE (ISNULL(name, '') LIKE ? OR CAST(pcode AS VARCHAR) LIKE ?) "
                f"AND ISNULL(PCategory, '') LIKE ? {extra} "
                f"ORDER BY name"
            )
            
            _, rows = db.fetchall(query, (q, q, cat))
                
            self.stock_tbl.load([[
                r[0], 
                r[1] or "[Unnamed Item]", 
                r[2] or "Unassigned", 
                r[3] or 0, 
                r[4] or 0,
                money(r[5] or 0), 
                money(r[6] or 0), 
                money(r[7] or 0), 
                r[8] or "NO"
            ] for r in rows])
            
            self.stock_status.config(
                text=f"{len(rows)} items total" + (" ⚠️ Low stock filter ACTIVE" if low else ""))
        except Exception as e:
            self.stock_status.config(text=f"Error Loading Stock: {str(e)[:80]}")

    def _add_product(self):
        dlg = FormDialog(self.winfo_toplevel(), "Add New Product", self._PROD_FIELDS)
        self.wait_window(dlg)
        if not dlg.result: return
        d = dlg.result
        
        if not d.get("pcode") or not d.get("name"):
            messagebox.showwarning("Required", "Product Code and Name are required."); return
        if db.fetchone("SELECT pcode FROM dbo.Stock_item WHERE pcode=?", (d["pcode"],)):
            messagebox.showwarning("Duplicate", f"Product code '{d['pcode']}' already exists."); return
            
        try:
            db.execute(
                "INSERT INTO dbo.Stock_item (pcode, name, PCategory, bp, spr, spw, qtystock, RLevel, vat) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (d["pcode"], d["name"], d["category"], float(d["bp"] or 0), float(d["spr"] or 0),
                 float(d["spw"] or 0), float(d["qtystock"] or 0), float(d["rlevel"] or 0), d["vat"]))
                 
            messagebox.showinfo("Added", f"Product '{d['name']}' added.")
            self._load_stock()
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def _edit_product(self):
        vals = self.stock_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a product to edit."); return
            
        initial = {
            "pcode": vals[0], 
            "name": vals[1], 
            "category": "" if vals[2] == "Unassigned" else vals[2],
            "qtystock": str(vals[3]), 
            "rlevel": str(vals[4]),
            "bp": vals[5].replace(",", ""),   
            "spr": vals[6].replace(",", ""),  
            "spw": vals[7].replace(",", ""),  
            "vat": vals[8]
        }
        
        fields = [f for f in self._PROD_FIELDS if f[1] != "pcode"]
        dlg = FormDialog(self.winfo_toplevel(), f"Edit Product – {vals[0]}", fields, initial)
        self.wait_window(dlg)
        if not dlg.result: return
        d = dlg.result
        
        try:
            db.execute(
                "UPDATE dbo.Stock_item SET name=?, PCategory=?, bp=?, spr=?, spw=?, qtystock=?, RLevel=?, vat=? WHERE pcode=?",
                (d["name"], d["category"], float(d["bp"] or 0), float(d["spr"] or 0),
                 float(d["spw"] or 0), float(d["qtystock"] or 0), float(d["rlevel"] or 0), d["vat"], vals[0]))
                 
            messagebox.showinfo("Updated", f"Product '{d['name']}' updated.")
            self._load_stock()
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def _delete_product(self):
        vals = self.stock_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a product to delete."); return
        if not messagebox.askyesno("Confirm Delete", f"Delete '{vals[1]}' (code: {vals[0]})?"):
            return
        try:
            db.execute("DELETE FROM dbo.Stock_item WHERE pcode=?", (vals[0],))
            messagebox.showinfo("Deleted", f"Product '{vals[1]}' deleted.")
            self._load_stock()
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def _build_scard_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8)
        ctrl.pack(fill="x")
        tk.Label(ctrl, text="Product Code:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.sc_pcode = tk.StringVar()
        ttk.Entry(ctrl, textvariable=self.sc_pcode, font=FONT_SM, width=14).pack(side="left", padx=4)
        tk.Label(ctrl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.sc_from = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.sc_from.insert(0, month_start())
        self.sc_from.pack(side="left", padx=2)
        tk.Label(ctrl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.sc_to = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.sc_to.insert(0, today_str())
        self.sc_to.pack(side="left", padx=2)
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_scard)
        style_btn(lb)
        lb.pack(side="left", padx=4)
        
        cols = ["RecId", "Date", "Narration", "Category", "Qty Item In", "Qty Out", "New Qty", "Done By"]
        self.sc_tbl = DataTable(parent, cols)
        self.sc_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.sc_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.sc_status.pack(fill="x", padx=10)

    def _load_scard(self):
        pcode = self.sc_pcode.get().strip()
        if not pcode:
            messagebox.showwarning("Missing", "Enter a product code."); return
        try:
            d1 = datetime.datetime.strptime(self.sc_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.sc_to.get(), "%Y-%m-%d")
        except ValueError: return
        try:
            _, rows = db.fetchall(
                "SELECT RecId, MDate, Narration, Category, QIn, QOut, NewQty, DBy "
                "FROM dbo.SCard WHERE PCode=? AND MDate BETWEEN ? AND ? ORDER BY MDate DESC",
                (pcode, d1, d2))
            self.sc_tbl.load([[r[0], str(r[1])[:10], r[2] or "", r[3] or "",
                                r[4] or 0, r[5] or 0, r[6] or 0, r[7] or ""] for r in rows])
            self.sc_status.config(text=f"{len(rows)} movements")
        except Exception as e:
            self.sc_status.config(text=f"Error: {str(e)[:80]}")

    def _build_damaged_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8)
        ctrl.pack(fill="x")
        tk.Label(ctrl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.dmg_from = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.dmg_from.insert(0, month_start())
        self.dmg_from.pack(side="left", padx=2)
        tk.Label(ctrl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.dmg_to = ttk.Entry(ctrl, font=FONT_SM, width=12)
        self.dmg_to.insert(0, today_str())
        self.dmg_to.pack(side="left", padx=2)
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_damaged)
        style_btn(lb)
        lb.pack(side="left", padx=4)
        
        cols = ["RecNo", "Item Code", "Item Name", "Qty", "Date", "Buy Price (KES)", "Narration", "Entered By"]
        self.dmg_tbl = DataTable(parent, cols)
        self.dmg_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.dmg_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.dmg_status.pack(fill="x", padx=10)
        self._load_damaged()

    def _load_damaged(self):
        try:
            d1 = datetime.datetime.strptime(self.dmg_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.dmg_to.get(), "%Y-%m-%d")
        except ValueError: return
        try:
            _, rows = db.fetchall(
                "SELECT RecNo, ItemCode, ItemName, Qty, DDate, BP, Narration, EnteredBy "
                "FROM dbo.DamagedStock WHERE DDate BETWEEN ? AND ? ORDER BY DDate DESC", (d1, d2))
            self.dmg_tbl.load([[r[0], r[1], r[2] or "", r[3] or 0,
                                 str(r[4])[:10], money(r[5] or 0), r[6] or "", r[7] or ""] for r in rows])
            total_loss = sum(float(r[3])*float(r[5]) for r in rows if r[3] and r[5])
            self.dmg_status.config(
                text=f"{len(rows)} records | Est. Loss: KES {money(total_loss)}")
        except Exception as e:
            self.dmg_status.config(text=f"Error: {str(e)[:80]}")

    def _build_expiry_tab(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8)
        ctrl.pack(fill="x")
        tk.Label(ctrl, text="Expiry Before:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        self.exp_before = ttk.Entry(ctrl, font=FONT_SM, width=12)
        ahead = (datetime.date.today()+datetime.timedelta(days=90)).strftime("%Y-%m-%d")
        self.exp_before.insert(0, ahead)
        self.exp_before.pack(side="left", padx=4)
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_expiry)
        style_btn(lb)
        lb.pack(side="left", padx=4)
        
        cols = ["RecId", "Batch No", "PCode", "Mfg Date", "Expiry Date", "Qty", "Done By", "TraNo"]
        self.exp_tbl = DataTable(parent, cols)
        self.exp_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.exp_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.exp_status.pack(fill="x", padx=10)
        self._load_expiry()

    def _load_expiry(self):
        try:
            d = datetime.datetime.strptime(self.exp_before.get(), "%Y-%m-%d")
        except ValueError: return
        try:
            _, rows = db.fetchall(
                "SELECT RecId, BatchNo, PCode, MDate, EDate, Qty, DoneBy, TraNo "
                "FROM dbo.Expiry WHERE EDate<=? ORDER BY EDate ASC", (d,))
            self.exp_tbl.load([[r[0], r[1] or "", r[2],
                                 str(r[3])[:10] if r[3] else "",
                                 str(r[4])[:10] if r[4] else "",
                                 r[5] or 0, r[6] or "", r[7] or ""] for r in rows])
            note = " (table currently empty)" if not rows else ""
            self.exp_status.config(
                text=f"{len(rows)} items expiring before {self.exp_before.get()}{note}")
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
        nb = ttk.Notebook(self); nb.pack(fill="both", expand=True, padx=4, pady=4)
        cust_tab = ttk.Frame(nb); nb.add(cust_tab, text="  💰 Customer Payments  ")
        self._build_cust_payments(cust_tab)
        sup_tab = ttk.Frame(nb); nb.add(sup_tab, text="  🏦 Supplier Payments  ")
        self._build_sup_payments(sup_tab)
        cb_tab = ttk.Frame(nb); nb.add(cb_tab, text="  📒 Cash Book  ")
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
        tk.Label(ctrl, text="Mode:", font=FONT_SM, bg=CLR["bg"]).pack(side="left", padx=(8,0))
        self.cp_mode = tk.StringVar()
        ttk.Combobox(ctrl, textvariable=self.cp_mode, font=FONT_SM, width=12,
                     values=["","CASH","CHEQUE","MPESA","BANK TRANSFER","OTHER"]
                     ).pack(side="left", padx=2)
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_cust_payments)
        style_btn(lb); lb.pack(side="left", padx=6)
        del_btn = tk.Button(ctrl, text="🗑 Delete", command=self._delete_payment)
        style_btn(del_btn, danger=True); del_btn.pack(side="left", padx=4)
        cols = ["PayNo","Date","Cust ID","Amount (KES)","Balance (KES)",
                "Mode","Cheque No","Bank","Done By"]
        self.cp_tbl = DataTable(parent, cols)
        self.cp_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.cp_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.cp_status.pack(fill="x", padx=10)
        self._cp_rows = []
        pbf = tk.Frame(parent, bg=CLR["bg"]); pbf.pack(anchor="e", padx=10, pady=2)
        CP_COLS = cols[:]
        for txt, cmd, col in [
            ("💾 Save PDF",
             lambda: save_pdf("Customer Payments", CP_COLS, self._cp_rows,
                              parent_window=parent.winfo_toplevel()),
             CLR["btn"]),
            ("🖨 Print A4",
             lambda: direct_print_pdf("Customer Payments", CP_COLS, self._cp_rows,
                                      parent_window=parent.winfo_toplevel()),
             CLR["success"]),
            ("🧾 Reprint", self._reprint_payment, CLR["accent"]),
        ]:
            tk.Button(pbf, text=txt, command=cmd, bg=col, fg=CLR["white"],
                      font=FONT_SM, relief="flat", padx=10, pady=4,
                      cursor="hand2").pack(side="left", padx=4)
        self._load_cust_payments()

    def _delete_payment(self):
        vals = self.cp_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a payment to delete."); return
        if not messagebox.askyesno("Confirm Delete",
                f"Delete payment #{vals[0]}?\nCustomer balance will NOT be auto-restored."): return
        try:
            db.execute("DELETE FROM dbo.Payment WHERE payno=?", (vals[0],))
            messagebox.showinfo("Deleted", f"Payment #{vals[0]} deleted.")
            self._load_cust_payments()
        except Exception as e: messagebox.showerror("Error", str(e))

    def _reprint_payment(self):
        vals = self.cp_tbl.selected_values()
        if not vals:
            messagebox.showinfo("Select Row", "Select a payment row first."); return
        print_payment_receipt(_printer_cfg, {
            "payno": vals[0], "date": vals[1], "customer": f"ID {vals[2]}",
            "amount": vals[3].replace(",",""), "mode": vals[5],
            "chequeno": vals[6], "balance": vals[4].replace(",",""),
            "doneby": vals[8], "trano": ""})

    def _load_cust_payments(self):
        try:
            d1 = datetime.datetime.strptime(self.cp_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.cp_to.get(), "%Y-%m-%d")
        except ValueError: return
        mode = self.cp_mode.get().strip()
        extra = "AND paymode=?" if mode else ""
        params = (d1, d2, mode) if mode else (d1, d2)
        try:
            _, rows = db.fetchall(
                f"SELECT payno, paydate, Sid, amount, bal, paymode, chequeno, dbank, DoneBy "
                f"FROM dbo.Payment WHERE paydate BETWEEN ? AND ? {extra} ORDER BY paydate DESC",
                params)
            fmt = [[r[0], str(r[1])[:10], r[2], money(r[3]), money(r[4]),
                    r[5] or "", r[6] or "", r[7] or "", r[8] or ""] for r in rows]
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
        tk.Label(ctrl, text="ℹ️ SPay table is currently empty",
                 font=FONT_SM, bg=CLR["bg"], fg="grey").pack(side="left", padx=8)
        cols = ["PayNo","Date","Supplier ID","Amount (KES)","Mode","Cheque No","Bank Acc","Done By"]
        self.sp_tbl = DataTable(parent, cols)
        self.sp_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.sp_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.sp_status.pack(fill="x", padx=10)
        self._load_sup_payments()

    def _load_sup_payments(self):
        try:
            d1 = datetime.datetime.strptime(self.sp_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.sp_to.get(), "%Y-%m-%d")
        except ValueError: return
        try:
            # SPay actual cols: PayNo,AMT,SID,PDATE,PTIME,PMODE,CQNO,TRDATE,TFROM,ACCNO,TTO,TBANK,DBY
            _, rows = db.fetchall(
                "SELECT PayNo, PDATE, SID, AMT, PMODE, CQNO, TBANK, DBY "
                "FROM dbo.SPay WHERE PDATE BETWEEN ? AND ? ORDER BY PDATE DESC", (d1, d2))
            self.sp_tbl.load([[r[0], str(r[1])[:10], r[2], money(r[3]),
                                r[4] or "", r[5] or "", r[6] or "", r[7] or ""] for r in rows])
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
                "Cash In (KES)","Cash Out (KES)","Bank In (KES)","Bank Out (KES)","Done By"]
        self.cb_tbl = DataTable(parent, cols)
        self.cb_tbl.pack(fill="both", expand=True, padx=10, pady=4)
        self.cb_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.cb_status.pack(fill="x", padx=10)
        self._load_cashbook()

    def _load_cashbook(self):
        try:
            d1 = datetime.datetime.strptime(self.cb_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.cb_to.get(), "%Y-%m-%d")
        except ValueError: return
        try:
            # CB actual cols: recid,Dt,Tm,MCat,MCat2,cin,cout,bin,bout,accno,dby,MCat3,GRP
            _, rows = db.fetchall(
                "SELECT recid, Dt, Tm, MCat, MCat2, cin, cout, bin, bout, dby "
                "FROM dbo.CB WHERE Dt BETWEEN ? AND ? ORDER BY Dt DESC, Tm DESC", (d1, d2))
            # FIX3: extract time from 1899-base datetime in Tm column
            fmt = [[r[0], str(r[1])[:10], extract_time(r[2]),
                    r[3] or "", r[4] or "",
                    money(r[5]), money(r[6]), money(r[7]), money(r[8]),
                    r[9] or ""] for r in rows]
            self.cb_tbl.load(fmt)
            ti  = sum(float(r[5]) for r in rows if r[5])
            to_ = sum(float(r[6]) for r in rows if r[6])
            self.cb_status.config(
                text=f"{len(rows)} entries | Cash In: KES {money(ti)}  Cash Out: KES {money(to_)}")
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

    # ── Shared helper: fetch product lines for a given TraNo ──────────────────
    def _fetch_items_for_trano(self, trano, table="dbo.SaleItem",
                                trano_col="TraNo",
                                cols="itemcode, description, qty, price, total"):
        """
        Returns a list of formatted sub-row strings for a transaction.
        Falls back gracefully if the items table does not exist or has no rows.
        """
        try:
            _, rows = db.fetchall(
                f"SELECT {cols} FROM {table} WHERE {trano_col} = ?", (trano,))
            if not rows:
                return []
            return [
                f"  ↳ {r[1] or r[0]}  |  Qty: {r[2]}  |  "
                f"Rate: KES {money(r[3])}  |  Total: KES {money(r[4])}"
                for r in rows
            ]
        except Exception:
            return []

    def _build(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=4, pady=4)
        for label, builder in [
            ("  📊 Sales Summary  ",    self._build_sales_summary),
            ("  📈 Trading Account  ",  self._build_trading),
            ("  🔁 Reconcile  ",        self._build_reconcile),
            ("  👥 Debtor Ageing  ",    self._build_ageing),
            ("  🗒️ Vote Transactions  ", self._build_vote),
        ]:
            tab = ttk.Frame(nb)
            nb.add(tab, text=label)
            builder(tab)

    def _date_ctrl(self, parent, attr_from, attr_to, cmd):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8)
        ctrl.pack(fill="x")
        tk.Label(ctrl, text="From:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        e1 = ttk.Entry(ctrl, font=FONT_SM, width=12)
        e1.insert(0, month_start())
        e1.pack(side="left", padx=2)
        tk.Label(ctrl, text="To:", font=FONT_SM, bg=CLR["bg"]).pack(side="left")
        e2 = ttk.Entry(ctrl, font=FONT_SM, width=12)
        e2.insert(0, today_str())
        e2.pack(side="left", padx=2)
        setattr(self, attr_from, e1)
        setattr(self, attr_to, e2)
        lb = tk.Button(ctrl, text="📋 Load", command=cmd)
        style_btn(lb)
        lb.pack(side="left", padx=6)
        return ctrl

    def _print_bar(self, parent, title, get_cols, get_rows, get_sub=None):
        pbf = tk.Frame(parent, bg=CLR["bg"])
        pbf.pack(anchor="e", padx=10, pady=2)
        for txt, fn, col in [
            ("💾 Save PDF",  save_pdf,          CLR["btn"]),
            ("🖨 Print A4",  direct_print_pdf,  CLR["success"]),
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

    # ── Generic sub-row expander attached to any DataTable ───────────────────
    def _bind_expander(self, tbl, parent_win,
                       trano_col_index,
                       fetch_fn,
                       title="Product Details"):
        """
        Binds a double-click on `tbl` that opens a small Toplevel showing
        product sub-rows for the selected transaction's TraNo.

        trano_col_index : column index in the table row that holds TraNo/RecNo
        fetch_fn        : callable(trano) -> list[str] of formatted product lines
        """
        def on_double_click(_event=None):
            vals = tbl.selected_values()
            if not vals:
                return
            trano = vals[trano_col_index]
            if not trano:
                return

            lines = fetch_fn(str(trano).strip())

            # Build popup
            popup = tk.Toplevel(parent_win)
            popup.title(f"{title}  —  Ref: {trano}")
            popup.geometry("640x320")
            popup.configure(bg=CLR["bg"])
            popup.grab_set()

            tk.Label(popup,
                     text=f"📦 Products / Line Items for Transaction: {trano}",
                     font=FONT_H2, bg=CLR["bg"], fg=CLR["text_dark"],
                     anchor="w").pack(fill="x", padx=10, pady=(10, 2))

            if not lines:
                tk.Label(popup,
                         text="ℹ️  No item detail records found for this transaction.",
                         font=FONT_SM, bg=CLR["bg"], fg="grey").pack(
                             pady=20)
            else:
                # Scrollable text area
                frame = tk.Frame(popup, bg=CLR["bg"])
                frame.pack(fill="both", expand=True, padx=10, pady=6)

                scrollbar = tk.Scrollbar(frame)
                scrollbar.pack(side="right", fill="y")

                txt = tk.Text(frame, font=FONT_SM, bg=CLR["card"],
                              fg=CLR["text_dark"], relief="flat",
                              yscrollcommand=scrollbar.set,
                              wrap="word", padx=8, pady=6)
                txt.pack(fill="both", expand=True)
                scrollbar.config(command=txt.yview)

                for line in lines:
                    txt.insert("end", line + "\n")
                txt.config(state="disabled")

                # Summary count
                tk.Label(popup,
                         text=f"✅  {len(lines)} line item(s) found.",
                         font=FONT_SM, bg=CLR["bg"],
                         fg=CLR["accent"]).pack(anchor="w", padx=10)

            tk.Button(popup, text="✖ Close", command=popup.destroy,
                      bg="#555", fg=CLR["white"], font=FONT_SM,
                      relief="flat", padx=12, pady=5).pack(pady=8)

        # Bind double-click on the treeview inside DataTable
        tbl.bind("<Double-1>", on_double_click)
        # Also show hint label below the table
        tk.Label(parent_win,
                 text="💡 Double-click any row to view product line items.",
                 font=FONT_SM, bg=CLR["bg"], fg="grey",
                 anchor="w").pack(fill="x", padx=12, pady=(0, 2))

    # =========================================================================
    # SALES SUMMARY
    # =========================================================================
    def _build_sales_summary(self, parent):
        self._date_ctrl(parent, "ss_from", "ss_to", self._load_sales_summary)
        is_admin = self.current_user.lower() == "admin"
        who = "All Cashiers (Admin View)" if is_admin else self.current_user
        tk.Label(parent, text=f"📋 Showing: {who}", font=FONT_SM,
                 bg=CLR["bg"], fg=CLR["accent"]).pack(anchor="w", padx=12, pady=(2, 0))

        kpi_frame = tk.Frame(parent, bg=CLR["bg"])
        kpi_frame.pack(fill="x", padx=10, pady=4)
        self.ss_kpi_labels = {}
        for i, (key, label) in enumerate([
            ("total_sales",  "Total Sales (KES)"),
            ("num_sales",    "No. of Sales"),
            ("credit_sales", "Credit Sales (KES)"),
        ]):
            f = tk.Frame(kpi_frame, bg=CLR["accent"], width=200, height=70, padx=10, pady=6)
            f.grid(row=0, column=i, padx=6)
            f.pack_propagate(False)
            lbl = tk.Label(f, text="—", font=("Helvetica Neue", 16, "bold"),
                           bg=CLR["accent"], fg=CLR["white"])
            lbl.pack(expand=True)
            tk.Label(f, text=label, font=FONT_SM,
                     bg=CLR["accent"], fg=CLR["white"]).pack()
            self.ss_kpi_labels[key] = lbl

        self._ss_rows = []
        cols = ["Date", "TraNo", "Type", "Cashier", "Total (KES)", "Sold To"]
        self.ss_tbl = DataTable(parent, cols)
        self.ss_tbl.pack(fill="both", expand=True, padx=10, pady=4)

        self.ss_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.ss_status.pack(fill="x", padx=10)

        self._print_bar(parent, "Sales Summary Report",
                        lambda: cols, lambda: self._ss_rows,
                        lambda: f"Cashier: {who}  |  {self.ss_from.get()} to {self.ss_to.get()}")

        # Expander: TraNo is column index 1 in Sales Summary
        # Fetches from dbo.SaleItem joined by TraNo
        self._bind_expander(
            self.ss_tbl, parent,
            trano_col_index=1,
            fetch_fn=lambda trano: self._fetch_items_for_trano(
                trano,
                table="dbo.SaleItem",
                trano_col="TraNo",
                cols="itemcode, description, qty, price, total"
            ),
            title="Sale Line Items"
        )

    def _load_sales_summary(self):
        try:
            d1 = datetime.datetime.strptime(self.ss_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.ss_to.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Dates must be YYYY-MM-DD.")
            return
        try:
            is_admin = self.current_user.lower() == "admin"
            if is_admin:
                _, rows = db.fetchall(
                    "SELECT tradate, TraNo, tratype, cashier, total, SoldTo "
                    "FROM dbo.Sale WHERE CAST(tradate AS DATE) BETWEEN ? AND ? "
                    "ORDER BY tradate DESC", (d1.date(), d2.date()))
            else:
                _, rows = db.fetchall(
                    "SELECT tradate, TraNo, tratype, cashier, total, SoldTo "
                    "FROM dbo.Sale WHERE CAST(tradate AS DATE) BETWEEN ? AND ? "
                    "AND cashier = ? ORDER BY tradate DESC",
                    (d1.date(), d2.date(), self.current_user))
            fmt = [[str(r[0])[:10], r[1], r[2] or "", r[3] or "",
                    money(r[4]), r[5] or ""] for r in rows]
            self._ss_rows = fmt
            self.ss_tbl.load(fmt)
            ts = sum(float(r[4]) for r in rows if r[4])
            cs = sum(float(r[4]) for r in rows
                     if r[4] and r[2] and str(r[2]).upper() == "CREDIT")
            self.ss_kpi_labels["total_sales"].config(text=f"KES {money(ts)}")
            self.ss_kpi_labels["num_sales"].config(text=str(len(rows)))
            self.ss_kpi_labels["credit_sales"].config(text=f"KES {money(cs)}")
            lbl = "All Cashiers" if is_admin else self.current_user
            self.ss_status.config(
                text=f"{len(rows)} sales for {lbl} | Total: KES {money(ts)}")
        except Exception as e:
            self.ss_status.config(text=f"Error: {str(e)[:80]}")

    # =========================================================================
    # TRADING ACCOUNT
    # =========================================================================
    def _build_trading(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8)
        ctrl.pack(fill="x")
        lb = tk.Button(ctrl, text="📋 Load", command=self._load_trading)
        style_btn(lb)
        lb.pack(side="left")

        cols = ["Start Date", "End Date", "Sales (KES)", "Purchases (KES)",
                "Cost of Goods (KES)", "Gross Profit (KES)",
                "Opening Stock (KES)", "Closing Stock (KES)"]
        self.tr_tbl = DataTable(parent, cols)
        self.tr_tbl.pack(fill="both", expand=True, padx=10, pady=4)

        self.tr_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.tr_status.pack(fill="x", padx=10)

        # Expander: Trading has no single TraNo — show top purchased products
        # within the period defined by StartDate/EndDate (cols 0 and 1)
        def _trading_fetch(start_date):
            """
            For a Trading period row, fetch top products purchased (Stock_Replenish items)
            within that period's start date as a reference lookup.
            """
            try:
                _, rows = db.fetchall(
                    "SELECT si.description, SUM(sr_item.qty) AS total_qty, "
                    "SUM(sr_item.total) AS total_val "
                    "FROM dbo.Stock_Replenish sr "
                    "JOIN dbo.Stock_Replenish_Item sr_item ON sr.trano = sr_item.trano "
                    "JOIN dbo.Stock_item si ON sr_item.item_name = si.description "
                    "WHERE CAST(sr.issuedate AS DATE) >= ? "
                    "GROUP BY si.description ORDER BY total_val DESC",
                    (start_date,))
                if not rows:
                    return []
                return [
                    f"  ↳ {r[0]}  |  Total Qty: {r[1]}  |  Total Value: KES {money(r[2])}"
                    for r in rows
                ]
            except Exception:
                # Fallback: show top-selling products from Sale items in the period
                try:
                    _, rows = db.fetchall(
                        "SELECT si.description, SUM(si.qty) AS total_qty, "
                        "SUM(si.total) AS total_val "
                        "FROM dbo.SaleItem si "
                        "GROUP BY si.description ORDER BY total_val DESC",
                        ())
                    return [
                        f"  ↳ {r[0]}  |  Total Qty: {r[1]}  |  "
                        f"Total Value: KES {money(r[2])}"
                        for r in rows
                    ]
                except Exception:
                    return []

        self._bind_expander(
            self.tr_tbl, parent,
            trano_col_index=0,   # StartDate used as the period reference key
            fetch_fn=_trading_fetch,
            title="Products in Trading Period"
        )
        self._load_trading()

    def _load_trading(self):
        try:
            _, rows = db.fetchall(
                "SELECT StartDate, EndDate, Sales, Purchases, CostOfGoods, "
                "GrossProfit, OpeningStock, ClosingStock "
                "FROM dbo.Trading ORDER BY StartDate DESC")
            self.tr_tbl.load([[str(r[0])[:10], str(r[1])[:10],
                                money(r[2]), money(r[3]), money(r[4]),
                                money(r[5]), money(r[6]), money(r[7])] for r in rows])
            self.tr_status.config(text=f"{len(rows)} period(s) found")
        except Exception as e:
            self.tr_status.config(text=f"Error: {str(e)[:80]}")

    # =========================================================================
    # RECONCILE
    # =========================================================================
    def _build_reconcile(self, parent):
        self._date_ctrl(parent, "rc_from", "rc_to", self._load_reconcile)
        tk.Label(parent,
                 text="ℹ️ Reconcile table is currently empty (0 rows)",
                 font=FONT_SM, bg=CLR["bg"], fg="grey").pack(anchor="w", padx=12)

        cols = ["Date", "Cash Sale (KES)", "Credit Sale (KES)", "Invoices (KES)",
                "Expenses (KES)", "Net Cash (KES)", "Banked (KES)",
                "Surplus/Deficit (KES)", "Comment"]
        self._rc_rows = []
        self.rc_tbl = DataTable(parent, cols)
        self.rc_tbl.pack(fill="both", expand=True, padx=10, pady=4)

        self.rc_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.rc_status.pack(fill="x", padx=10)

        self._print_bar(parent, "Reconciliation Report",
                        lambda: cols, lambda: self._rc_rows)

        # Expander: date (col 0) used to pull all SaleItem products sold on that day
        def _reconcile_fetch(trade_date):
            try:
                _, rows = db.fetchall(
                    "SELECT si.description, SUM(si.qty) AS total_qty, "
                    "SUM(si.total) AS total_val "
                    "FROM dbo.SaleItem si "
                    "JOIN dbo.Sale s ON si.TraNo = s.TraNo "
                    "WHERE CAST(s.tradate AS DATE) = ? "
                    "GROUP BY si.description ORDER BY total_val DESC",
                    (trade_date,))
                if not rows:
                    return []
                return [
                    f"  ↳ {r[0]}  |  Total Qty: {r[1]}  |  "
                    f"Total Value: KES {money(r[2])}"
                    for r in rows
                ]
            except Exception:
                return []

        self._bind_expander(
            self.rc_tbl, parent,
            trano_col_index=0,   # TraDate column
            fetch_fn=_reconcile_fetch,
            title="Products Sold on This Date"
        )
        self._load_reconcile()

    def _load_reconcile(self):
        try:
            d1 = datetime.datetime.strptime(self.rc_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.rc_to.get(), "%Y-%m-%d")
        except ValueError:
            return
        try:
            _, rows = db.fetchall(
                "SELECT TraDate, CashSale, CreditSale, Invoices, "
                "Expenses, NetCash, Banked, DefSurp, Comment "
                "FROM dbo.Reconcile WHERE TraDate BETWEEN ? AND ? ORDER BY TraDate DESC",
                (d1, d2))
            fmt = [[str(r[0])[:10], money(r[1]), money(r[2]), money(r[3]),
                    money(r[4]), money(r[5]), money(r[6]), money(r[7]),
                    r[8] or ""] for r in rows]
            self._rc_rows = fmt
            self.rc_tbl.load(fmt)
            note = " (table is empty)" if not rows else ""
            self.rc_status.config(
                text=f"{len(rows)} reconciliation records{note}")
        except Exception as e:
            self.rc_status.config(text=f"Error: {str(e)[:120]}")

    # =========================================================================
    # DEBTOR AGEING
    # =========================================================================
    def _build_ageing(self, parent):
        ctrl = tk.Frame(parent, bg=CLR["bg"], padx=10, pady=8)
        ctrl.pack(fill="x")
        lb = tk.Button(ctrl, text="📋 Load Debtor Ageing", command=self._load_ageing)
        style_btn(lb)
        lb.pack(side="left")

        cols = ["Cust ID", "0-30 Days (KES)", "31-60 Days (KES)", "61-90 Days (KES)",
                "91-120 Days (KES)", "Over 120 (KES)", "Total (KES)", "Unallocated (KES)"]
        self._age_rows = []
        self.age_tbl = DataTable(parent, cols)
        self.age_tbl.pack(fill="both", expand=True, padx=10, pady=4)

        self.age_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.age_status.pack(fill="x", padx=10)

        self._print_bar(parent, "Debtor Ageing Report",
                        lambda: cols, lambda: self._age_rows)

        # Expander: Cust ID (col 0) — show all unpaid sale invoices for that customer
        def _ageing_fetch(cust_id):
            try:
                _, rows = db.fetchall(
                    "SELECT s.TraNo, CAST(s.tradate AS DATE), "
                    "si.description, si.qty, si.price, si.total "
                    "FROM dbo.Sale s "
                    "JOIN dbo.SaleItem si ON s.TraNo = si.TraNo "
                    "WHERE s.SoldTo = ? AND s.tratype = 'CREDIT' "
                    "ORDER BY s.tradate DESC",
                    (cust_id,))
                if not rows:
                    return []
                return [
                    f"  ↳ TraNo: {r[0]}  |  Date: {str(r[1])[:10]}  |  "
                    f"Product: {r[2]}  |  Qty: {r[3]}  |  "
                    f"Price: KES {money(r[4])}  |  Total: KES {money(r[5])}"
                    for r in rows
                ]
            except Exception:
                return []

        self._bind_expander(
            self.age_tbl, parent,
            trano_col_index=0,   # Cust ID column
            fetch_fn=_ageing_fetch,
            title="Customer Outstanding Items"
        )
        self._load_ageing()

    def _load_ageing(self):
        try:
            _, rows = db.fetchall(
                "SELECT sid, a30, a60, a90, a120, aover, atotal, UB "
                "FROM dbo.SDAS ORDER BY atotal DESC")
            fmt = [[r[0], money(r[1]), money(r[2]), money(r[3]),
                    money(r[4]), money(r[5]), money(r[6]), money(r[7])] for r in rows]
            self._age_rows = fmt
            self.age_tbl.load(fmt)
            grand = sum(float(r[6]) for r in rows if r[6])
            self.age_status.config(
                text=f"{len(rows)} debtors | Grand Total: KES {money(grand)}")
        except Exception as e:
            self.age_status.config(text=f"Error: {str(e)[:80]}")

    # =========================================================================
    # VOTE TRANSACTIONS
    # =========================================================================
    def _build_vote(self, parent):
        ctrl = self._date_ctrl(parent, "vt_from", "vt_to", self._load_vote)
        tk.Label(ctrl, text="Votehead:", font=FONT_SM,
                 bg=CLR["bg"]).pack(side="left", padx=(8, 0))
        self.vt_vh = tk.StringVar()
        ttk.Entry(ctrl, textvariable=self.vt_vh,
                  font=FONT_SM, width=16).pack(side="left", padx=2)

        cols = ["RecNo", "Date", "Votehead", "Narration", "CR (KES)", "DR (KES)", "Type"]
        self._vt_rows = []
        self.vt_tbl = DataTable(parent, cols)
        self.vt_tbl.pack(fill="both", expand=True, padx=10, pady=4)

        self.vt_status = tk.Label(parent, text="", font=FONT_SM, bg=CLR["bg"], anchor="w")
        self.vt_status.pack(fill="x", padx=10)

        self._print_bar(parent, "Vote Transactions",
                        lambda: cols, lambda: self._vt_rows)

        # Expander: RecNo (col 0) — show all sale items linked to this vote entry
        # via any matching TraNo recorded on the same date under same votehead
        def _vote_fetch(rec_no):
            try:
                # First resolve the TraNo and date for this VoteT record
                row = db.fetchone(
                    "SELECT RNo, TraDate, Votehead FROM dbo.VoteT WHERE RecNo = ?",
                    (rec_no,))
                if not row:
                    return []
                rno, tra_date, votehead = row

                # Pull SaleItem rows for matching TraNo if RNo maps to a Sale
                _, items = db.fetchall(
                    "SELECT si.description, si.qty, si.price, si.total "
                    "FROM dbo.SaleItem si "
                    "WHERE si.TraNo = ?",
                    (rno,))
                if items:
                    return [
                        f"  ↳ {r[0]}  |  Qty: {r[1]}  |  "
                        f"Price: KES {money(r[2])}  |  Total: KES {money(r[3])}"
                        for r in items
                    ]

                # Fallback: show all products sold on same date under same votehead
                _, items = db.fetchall(
                    "SELECT si.description, SUM(si.qty), SUM(si.total) "
                    "FROM dbo.SaleItem si "
                    "JOIN dbo.Sale s ON si.TraNo = s.TraNo "
                    "WHERE CAST(s.tradate AS DATE) = ? "
                    "GROUP BY si.description ORDER BY SUM(si.total) DESC",
                    (str(tra_date)[:10],))
                return [
                    f"  ↳ {r[0]}  |  Total Qty: {r[1]}  |  "
                    f"Total Value: KES {money(r[2])}"
                    for r in items
                ] if items else []
            except Exception:
                return []

        self._bind_expander(
            self.vt_tbl, parent,
            trano_col_index=0,   # RecNo column
            fetch_fn=_vote_fetch,
            title="Vote Transaction Line Items"
        )

    def _load_vote(self):
        try:
            d1 = datetime.datetime.strptime(self.vt_from.get(), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(self.vt_to.get(), "%Y-%m-%d")
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
            self._vt_rows = fmt
            self.vt_tbl.load(fmt)
            tc = sum(float(r[4]) for r in rows if r[4])
            td = sum(float(r[5]) for r in rows if r[5])
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
        self.title("FarmersDesk Ltd – Desktop Application v4")
        self.configure(bg=CLR["bg"])
        self.geometry("1280x780"); self.minsize(1000, 650)
        s = ttk.Style(self); s.theme_use("clam")
        s.configure("TFrame", background=CLR["bg"])
        s.configure("TNotebook", background=CLR["bg"])
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
        self._build_main(); self.deiconify()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"1280x780+{(sw-1280)//2}+{(sh-780)//2}")

    def _build_main(self):
        uname = self.current_user["name"]
        hdr = tk.Frame(self, bg=CLR["header"], height=56)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="🌾  FarmersDesk Ltd", font=FONT_H1,
                 bg=CLR["header"], fg=CLR["white"]).pack(side="left", padx=20)
        tk.Label(hdr,
                 text=f"👤  {uname}   |   {datetime.date.today().strftime('%d %b %Y')}",
                 font=FONT_SM, bg=CLR["header"], fg=CLR["white"]).pack(side="right", padx=20)
        cfg_btn = tk.Button(hdr, text="🖨 Printer", command=self._open_printer_cfg,
                            font=FONT_SM, bg=CLR["accent"], fg=CLR["white"],
                            relief="flat", padx=10, pady=4, cursor="hand2")
        cfg_btn.pack(side="right", padx=8)

        nb = ttk.Notebook(self); nb.pack(fill="both", expand=True, padx=4, pady=4)
        self._dashboard = DashboardFrame(nb, uname)
        self._dashboard.configure(style="TFrame")
        nb.add(self._dashboard, text="  🏠 Dashboard  ")
        sales_frame = CreateSalesFrame(nb, uname, on_sale_saved=self._dashboard.refresh)
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

        sb = tk.Frame(self, bg=CLR["border"], height=22)
        sb.pack(fill="x", side="bottom"); sb.pack_propagate(False)
        tk.Label(sb,
                 text=f"  {DB_CONFIG['server']} / {DB_CONFIG['database']}   |   User: {uname}   |   v4",
                 font=FONT_SM, bg=CLR["border"], fg=CLR["text_dark"]).pack(side="left")

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
except Exception:
    ESCPOS_OK = False

try:
    import qrcode; QR_OK = True
except Exception:
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
except Exception:
    RL_OK = False


# ═════════════════════════════════════════════════════════════════════════════
# KRA TAX COMPLIANCE QR CODE
# Kenya Revenue Authority eTIMS / TIMS QR format:
#   https://itax.kra.go.ke/KRA-Portal/
# QR content encodes:
#   PIN | Invoice No | Date | Time | Total | VAT | CU Serial
# ═════════════════════════════════════════════════════════════════════════════
def _make_kra_qr_image(
        invoice_no: str,
        total: float,
        vat: float = 0.0,
        date_str: str = "",
        time_str: str = "",
        cu_serial: str = ""):
    """
    Builds a KRA-compliant eTIMS QR code image.
    Format follows KRA eTIMS specification:
      PIN|InvoiceNo|Date|Time|GrossTotal|VATAmount|CUSerial
    The PIN and CU serial come from COMPANY config.
    """
    if not QR_OK:
        return None
    try:
        pin        = COMPANY.get("kra_pin", "P000000000A")
        cu_serial  = cu_serial or COMPANY.get("cu_serial", "CU000000")
        date_str   = date_str  or datetime.datetime.now().strftime("%Y%m%d")
        time_str   = time_str  or datetime.datetime.now().strftime("%H%M%S")

        # KRA eTIMS QR payload — pipe-delimited
        qr_payload = (
            f"{pin}|"
            f"{invoice_no}|"
            f"{date_str}|"
            f"{time_str}|"
            f"{total:.2f}|"
            f"{vat:.2f}|"
            f"{cu_serial}"
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=3,
            border=1)
        qr.add_data(qr_payload)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white").convert("RGB")
    except Exception:
        return None


# ═════════════════════════════════════════════════════════════════════════════
# PRINTER CONFIGURATION DIALOG
# ═════════════════════════════════════════════════════════════════════════════
class PrinterConfigDialog(tk.Toplevel):
    DEFAULTS = {
        "connection":   "USB",
        "usb_vendor":   "0x04B8",
        "usb_product":  "0x0202",
        "serial_port":  "COM3",
        "serial_baud":  "9600",
        "net_host":     "192.168.1.100",
        "net_port":     "9100",
    }

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
        tk.Label(self, text="Thermal Printer Settings", font=FONT_H2,
                 bg=CLR["bg"], fg=CLR["text_dark"]).pack(pady=(12, 6), padx=20)

        f = tk.Frame(self, bg=CLR["bg"], padx=20, pady=8)
        f.pack(fill="both")

        tk.Label(f, text="Connection:", font=FONT_SM,
                 bg=CLR["bg"]).grid(row=0, column=0, sticky="e", pady=4)
        self.conn_var = tk.StringVar(value=self.cfg["connection"])
        cb = ttk.Combobox(f, textvariable=self.conn_var, width=16,
                          values=["USB", "Serial", "Network"], state="readonly")
        cb.grid(row=0, column=1, sticky="w", padx=8, pady=4)
        cb.bind("<<ComboboxSelected>>", lambda _: self._toggle())

        def make_lf(text, row):
            lf = tk.LabelFrame(f, text=text, bg=CLR["bg"], font=FONT_SM)
            lf.grid(row=row, column=0, columnspan=2, sticky="ew", pady=4)
            return lf

        usb = make_lf("USB Settings", 1)
        self.usb_frame = usb
        for i, (lbl, attr, val) in enumerate([
            ("Vendor ID (hex):",  "usb_vendor",  self.cfg["usb_vendor"]),
            ("Product ID (hex):", "usb_product", self.cfg["usb_product"]),
        ]):
            tk.Label(usb, text=lbl, font=FONT_SM,
                     bg=CLR["bg"]).grid(row=i, column=0, sticky="e", padx=4, pady=3)
            e = ttk.Entry(usb, width=12)
            e.insert(0, val)
            e.grid(row=i, column=1, sticky="w", padx=4, pady=3)
            setattr(self, attr.replace(".", "_"), e)

        ser = make_lf("Serial Settings", 2)
        self.ser_frame = ser
        for i, (lbl, attr, val) in enumerate([
            ("COM Port:",  "ser_port", self.cfg["serial_port"]),
            ("Baud Rate:", "ser_baud", self.cfg["serial_baud"]),
        ]):
            tk.Label(ser, text=lbl, font=FONT_SM,
                     bg=CLR["bg"]).grid(row=i, column=0, sticky="e", padx=4, pady=3)
            e = ttk.Entry(ser, width=12)
            e.insert(0, val)
            e.grid(row=i, column=1, sticky="w", padx=4, pady=3)
            setattr(self, attr, e)

        net = make_lf("Network Settings", 3)
        self.net_frame = net
        for i, (lbl, attr, val) in enumerate([
            ("IP Address:", "net_host", self.cfg["net_host"]),
            ("Port:",       "net_port", self.cfg["net_port"]),
        ]):
            tk.Label(net, text=lbl, font=FONT_SM,
                     bg=CLR["bg"]).grid(row=i, column=0, sticky="e", padx=4, pady=3)
            e = ttk.Entry(net, width=16)
            e.insert(0, val)
            e.grid(row=i, column=1, sticky="w", padx=4, pady=3)
            setattr(self, attr, e)

        btn_row = tk.Frame(f, bg=CLR["bg"])
        btn_row.grid(row=4, column=0, columnspan=2, pady=10)

        test = tk.Button(btn_row, text="🖨 Test Print", command=self._test)
        style_btn(test)
        test.pack(side="left", padx=4)

        save = tk.Button(btn_row, text="💾 Save", command=self._save)
        style_btn(save, success=True)
        save.pack(side="left", padx=4)

        tk.Button(btn_row, text="Cancel", command=self.destroy,
                  font=FONT_SM).pack(side="left", padx=4)

        self._toggle()

    def _toggle(self):
        conn = self.conn_var.get()
        for frame, show in [
            (self.usb_frame, conn == "USB"),
            (self.ser_frame, conn == "Serial"),
            (self.net_frame, conn == "Network"),
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
        if not ESCPOS_OK:
            messagebox.showwarning(
                "Printer Library Missing",
                "ESC/POS library not installed.\n"
                "Run: pip install python-escpos")
            return
        self._save()
        p = _open_printer(self.result) if self.result else None
        if p:
            try:
                _set(p, align="center", bold=True)
                p.text(COMPANY["name"][:W_CONTENT] + "\n")
                _set(p, align="center", bold=False)
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


# ═════════════════════════════════════════════════════════════════════════════
# PRINTER HELPERS
# ═════════════════════════════════════════════════════════════════════════════
def _open_printer(cfg: dict):
    if not ESCPOS_OK:
        return None
    try:
        conn = cfg.get("connection", "USB")
        if conn == "USB":
            return Usb(
                int(cfg.get("usb_vendor",  "0x04B8"), 16),
                int(cfg.get("usb_product", "0x0202"), 16))
        elif conn == "Serial":
            return Serial(
                cfg.get("serial_port", "COM3"),
                baudrate=int(cfg.get("serial_baud", 9600)))
        else:
            return Network(
                cfg.get("net_host", "192.168.1.100"),
                port=int(cfg.get("net_port", 9100)))
    except Exception as e:
        messagebox.showerror("Printer Error", f"Cannot open printer:\n{e}")
        return None


def _set(p, align="left", bold=False):
    """
    Unified ESC/POS set() call that handles both old and new
    python-escpos API signatures gracefully.
    """
    try:
        p.set(align=align, font="b", custom_size=True,
              width=1, height=1, bold=bold)
    except TypeError:
        try:
            p.set(align=align, font=1, bold=bold)
        except Exception:
            pass


# ═════════════════════════════════════════════════════════════════════════════
# LAYOUT CONSTANTS  (42-char thermal width)
# ═════════════════════════════════════════════════════════════════════════════
W_CONTENT = 42


def _line(ch="-") -> str:
    return (ch * W_CONTENT) + "\n"


def _two_col(left: str, right: str, width=W_CONTENT) -> str:
    left  = str(left)[:width]
    right = str(right)[:width]
    gap   = max(1, width - len(left) - len(right))
    return left + " " * gap + right + "\n"


def _center(text: str) -> str:
    text    = str(text)[:W_CONTENT]
    padding = max(0, (W_CONTENT - len(text)) // 2)
    return " " * padding + text + "\n"


def _left(text: str) -> str:
    return str(text)[:W_CONTENT] + "\n"


def _right(text: str) -> str:
    text    = str(text)[:W_CONTENT]
    padding = max(0, W_CONTENT - len(text))
    return " " * padding + text + "\n"


# ═════════════════════════════════════════════════════════════════════════════
# SHARED BOLD HEADER BLOCK
# Printed at the top of every receipt type
# ═════════════════════════════════════════════════════════════════════════════
def _print_header(p, receipt_label: str, receipt_no: str):
    """
    Prints the company header in bold then the receipt type label and number.
    receipt_label : e.g. "CASH SALE RECEIPT", "PAYMENT RECEIPT", "CREDIT MEMO"
    receipt_no    : e.g. "TRN-00123" or "PAY-00456"
    """
    # ── Company name — large bold center ─────────────────────────────────────
    _set(p, align="center", bold=True)
    p.text(_center(COMPANY["name"].upper()))

    # ── Address, phone, email — normal center ────────────────────────────────
    _set(p, align="center", bold=False)
    if COMPANY.get("address"):
        p.text(_center(COMPANY["address"][:W_CONTENT]))
    if COMPANY.get("phone"):
        p.text(_center(f"Tel: {COMPANY['phone']}"))
    if COMPANY.get("email"):
        p.text(_center(COMPANY["email"][:W_CONTENT]))

    # ── KRA PIN — mandatory for tax compliance ────────────────────────────────
    kra_pin = COMPANY.get("kra_pin", "")
    if kra_pin:
        _set(p, align="center", bold=True)
        p.text(_center(f"KRA PIN: {kra_pin}"))

    p.text(_line("="))

    # ── Receipt type label — bold centered ───────────────────────────────────
    _set(p, align="center", bold=True)
    p.text(_center(receipt_label))

    # ── Receipt number — bold centered ───────────────────────────────────────
    p.text(_center(f"No: {receipt_no}"))

    _set(p, align="left", bold=False)
    p.text(_line("="))


# ═════════════════════════════════════════════════════════════════════════════
# SALE RECEIPT
# ═════════════════════════════════════════════════════════════════════════════
def print_sale_receipt(cfg: dict, sale: dict, items: List[Dict]):
    """
    Prints a full itemized sale receipt with:
    - Bold company header + KRA PIN
    - Receipt / TraNo number prominently displayed
    - All line items with qty, unit price, line total
    - VAT breakdown (16% standard Kenya rate)
    - KRA eTIMS QR code
    """
    p = _open_printer(cfg)
    if not p:
        return

    try:
        now        = datetime.datetime.now()
        date_str   = now.strftime("%Y%m%d")
        time_str   = now.strftime("%H%M%S")
        trano      = str(sale.get("trano", ""))
        receipt_no = f"RCP-{trano}" if trano else "RCP-UNKNOWN"

        # ── Bold header ───────────────────────────────────────────────────────
        _print_header(p, "CASH SALE RECEIPT", receipt_no)

        # ── Transaction metadata ──────────────────────────────────────────────
        _set(p, align="left", bold=False)
        p.text(_two_col("Receipt No.", f": {receipt_no}"))
        p.text(_two_col("Date",        f": {now.strftime('%d/%m/%Y')}"))
        p.text(_two_col("Time",        f": {now.strftime('%H:%M:%S')}"))

        cashier = sale.get("cashier", "")
        if cashier:
            p.text(_two_col("Cashier", f": {str(cashier)[:W_CONTENT-10]}"))

        cust = sale.get("customer", "")
        if cust and cust not in ("Walk-in", ""):
            p.text(_two_col("Customer", f": {str(cust)[:W_CONTENT-11]}"))

        inv_no = sale.get("invno", "")
        if inv_no:
            p.text(_two_col("Invoice Ref", f": {str(inv_no)[:W_CONTENT-14]}"))

        p.text(_line("-"))

        # ── Column headers ────────────────────────────────────────────────────
        _set(p, align="left", bold=True)
        p.text(_two_col("ITEM", "TOTAL"))
        _set(p, align="left", bold=False)
        p.text(_line("-"))

        # ── Line items ────────────────────────────────────────────────────────
        grand_total = 0.0
        vat_total   = 0.0

        for it in items:
            name  = str(it.get("name", "Unknown"))[:W_CONTENT]
            qty   = it.get("qty",   1)
            price = float(it.get("price", 0))
            tot   = float(it.get("total",  price * float(qty)))
            # Kenya standard VAT = 16%; back-calculate from inclusive price
            item_vat = tot - (tot / 1.16)

            grand_total += tot
            vat_total   += item_vat

            p.text(_left(name))
            p.text(_two_col(
                f"  {qty} x KES {money(price)}",
                f"KES {money(tot)}"))

        p.text(_line("-"))

        # ── Totals block ──────────────────────────────────────────────────────
        excl_total = grand_total - vat_total
        _set(p, align="left", bold=False)
        p.text(_two_col("Subtotal (excl. VAT)", f"KES {money(excl_total)}"))
        p.text(_two_col("VAT (16%)",            f"KES {money(vat_total)}"))

        _set(p, align="left", bold=True)
        p.text(_two_col("TOTAL (incl. VAT)",    f"KES {money(grand_total)}"))
        _set(p, align="left", bold=False)

        cash   = float(sale.get("cash",   0))
        change = float(sale.get("change", 0))
        if cash:
            p.text(_line("-"))
            p.text(_two_col("Cash Tendered", f"KES {money(cash)}"))
            p.text(_two_col("Change",        f"KES {money(change)}"))

        p.text(_line("="))

        # ── KRA compliance footer ─────────────────────────────────────────────
        _set(p, align="center", bold=True)
        p.text(_center("KRA TAX INVOICE"))
        _set(p, align="center", bold=False)
        p.text(_center(f"PIN: {COMPANY.get('kra_pin', 'N/A')}"))
        p.text(_center(f"CU Serial: {COMPANY.get('cu_serial', 'N/A')}"))
        p.text(_center(f"Invoice: {receipt_no}"))
        p.text(_center("This receipt is your tax document."))
        p.text(_center("Verify at itax.kra.go.ke"))

        # ── KRA QR code ───────────────────────────────────────────────────────
        qr_img = _make_kra_qr_image(
            invoice_no=receipt_no,
            total=grand_total,
            vat=vat_total,
            date_str=date_str,
            time_str=time_str)

        if qr_img:
            _set(p, align="center", bold=False)
            p.image(qr_img)
            p.text(_center("Scan QR to verify with KRA eTIMS"))

        p.text(_line("-"))
        _set(p, align="center", bold=False)
        p.text(_center("Thank you for your business!"))
        p.text(_center(now.strftime("%d/%m/%Y  %H:%M:%S")))

        p.text("\n\n")
        p.cut()

    except Exception as e:
        messagebox.showerror("Print Error", str(e))
    finally:
        try: p.close()
        except Exception: pass


# ═════════════════════════════════════════════════════════════════════════════
# PAYMENT RECEIPT
# ═════════════════════════════════════════════════════════════════════════════
def print_payment_receipt(cfg: dict, payment: dict):
    """
    Prints a payment/credit receipt with:
    - Bold company header + KRA PIN
    - Payment receipt number prominently displayed
    - Payment mode, cheque/bank details, balance after
    - KRA QR code referencing the payment
    """
    p = _open_printer(cfg)
    if not p:
        return

    try:
        now      = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")

        # Build a stable receipt number from payno or trano
        raw_no     = payment.get("payno") or payment.get("trano") or ""
        receipt_no = f"PAY-{raw_no}" if raw_no else f"PAY-{now.strftime('%Y%m%d%H%M%S')}"

        amount  = float(payment.get("amount",  0))
        balance = float(payment.get("balance", 0))

        # ── Bold header ───────────────────────────────────────────────────────
        _print_header(p, "PAYMENT RECEIPT", receipt_no)

        # ── Payment details ───────────────────────────────────────────────────
        _set(p, align="left", bold=False)
        p.text(_two_col("Receipt No.",  f": {receipt_no}"))
        p.text(_two_col("Date",         f": {now.strftime('%d/%m/%Y')}"))
        p.text(_two_col("Time",         f": {now.strftime('%H:%M:%S')}"))
        p.text(_two_col("Customer",
                        f": {str(payment.get('customer', ''))[:W_CONTENT-11]}"))

        mode = payment.get("mode", "CASH")
        p.text(_two_col("Payment Mode",  f": {mode}"))

        chequeno = payment.get("chequeno", "")
        if chequeno:
            p.text(_two_col("Cheque No.", f": {chequeno}"))

        bank = payment.get("dbank", "") or payment.get("bank", "")
        if bank:
            p.text(_two_col("Bank", f": {bank}"))

        trano = payment.get("trano", "")
        if trano:
            p.text(_two_col("Invoice Ref", f": {trano}"))

        doneby = payment.get("doneby", "")
        if doneby:
            p.text(_two_col("Received By", f": {doneby}"))

        p.text(_line("-"))

        # ── Amount block ──────────────────────────────────────────────────────
        _set(p, align="left", bold=True)
        p.text(_two_col("AMOUNT RECEIVED", f"KES {money(amount)}"))
        _set(p, align="left", bold=False)
        p.text(_two_col("Outstanding Bal.", f"KES {money(balance)}"))

        p.text(_line("="))

        # ── KRA compliance footer ─────────────────────────────────────────────
        _set(p, align="center", bold=True)
        p.text(_center("KRA PAYMENT ACKNOWLEDGEMENT"))
        _set(p, align="center", bold=False)
        p.text(_center(f"PIN: {COMPANY.get('kra_pin', 'N/A')}"))
        p.text(_center(f"Receipt: {receipt_no}"))
        p.text(_center("Verify at itax.kra.go.ke"))

        # ── KRA QR (references the payment receipt number) ────────────────────
        qr_img = _make_kra_qr_image(
            invoice_no=receipt_no,
            total=amount,
            vat=0.0,
            date_str=date_str,
            time_str=time_str)

        if qr_img:
            _set(p, align="center", bold=False)
            p.image(qr_img)
            p.text(_center("Scan QR to verify with KRA eTIMS"))

        p.text(_line("-"))
        _set(p, align="center", bold=False)
        p.text(_center("Thank you for your payment!"))
        p.text(_center(now.strftime("%d/%m/%Y  %H:%M:%S")))

        p.text("\n\n")
        p.cut()

    except Exception as e:
        messagebox.showerror("Print Error", str(e))
    finally:
        try: p.close()
        except Exception: pass


# ═════════════════════════════════════════════════════════════════════════════
# PDF REPORT BUILDER  (A4 — unchanged structure, updated styling)
# ═════════════════════════════════════════════════════════════════════════════
def _rl_color(h: str):
    h = h.lstrip("#")
    return colors.Color(
        int(h[0:2], 16) / 255,
        int(h[2:4], 16) / 255,
        int(h[4:6], 16) / 255)


def _build_pdf(filepath: str, title: str, columns: List[str],
               rows: List[List], subtitle: str = "",
               summary_rows=None) -> bool:
    if not RL_OK:
        messagebox.showerror(
            "Missing Library",
            "ReportLab not installed.\nRun: pip install reportlab")
        return False

    doc = SimpleDocTemplate(
        filepath, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm)

    accent = _rl_color("#1A3C5E")
    light  = _rl_color("#EAF2FF")
    white  = colors.white
    dark   = _rl_color("#1A1A2E")

    styles = getSampleStyleSheet()

    h1 = ParagraphStyle(
        "h1", parent=styles["Normal"],
        fontSize=18, textColor=accent,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=2)

    h2 = ParagraphStyle(
        "h2", parent=styles["Normal"],
        fontSize=10, textColor=dark,
        fontName="Helvetica",
        alignment=TA_CENTER, spaceAfter=2)

    kra_style = ParagraphStyle(
        "kra", parent=styles["Normal"],
        fontSize=9, textColor=accent,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=4)

    story = [
        # Company name — bold large
        Paragraph(COMPANY["name"].upper(), h1),
        Paragraph(
            f"{COMPANY.get('address', '')}  |  "
            f"Tel: {COMPANY.get('phone', '')}  |  "
            f"{COMPANY.get('email', '')}",
            h2),
        # KRA PIN line — bold for compliance
        Paragraph(
            f"KRA PIN: {COMPANY.get('kra_pin', 'N/A')}  |  "
            f"CU Serial: {COMPANY.get('cu_serial', 'N/A')}",
            kra_style),
        HRFlowable(width="100%", thickness=2, color=accent, spaceAfter=6),
        Paragraph(
            title,
            ParagraphStyle(
                "t", parent=styles["Normal"],
                fontSize=13, fontName="Helvetica-Bold",
                textColor=accent, alignment=TA_CENTER, spaceAfter=2)),
    ]

    if subtitle:
        story.append(Paragraph(subtitle, h2))

    story.append(Paragraph(
        f"Generated: {datetime.datetime.now().strftime('%d %b %Y  %H:%M')}",
        ParagraphStyle(
            "g", parent=styles["Normal"],
            fontSize=8, textColor=colors.grey,
            alignment=TA_CENTER)))

    story.append(Spacer(1, 5*mm))

    usable_w = A4[0] - 30*mm
    col_w    = [usable_w / max(len(columns), 1)] * len(columns)

    hdr_row = [
        Paragraph(
            f"<b>{c}</b>",
            ParagraphStyle(
                "th", parent=styles["Normal"],
                fontSize=8, textColor=white,
                fontName="Helvetica-Bold",
                alignment=TA_CENTER))
        for c in columns
    ]

    tdata = [hdr_row] + [
        [
            Paragraph(
                str(cell) if cell is not None else "",
                ParagraphStyle(
                    "td", parent=styles["Normal"],
                    fontSize=7, textColor=dark,
                    fontName="Helvetica"))
            for cell in r
        ]
        for r in rows
    ]

    tbl = Table(tdata, colWidths=col_w, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1,  0), accent),
        ("TEXTCOLOR",      (0, 0), (-1,  0), white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, light]),
        ("GRID",           (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",     (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 3),
    ]))
    story.append(tbl)

    if summary_rows:
        story += [
            Spacer(1, 5*mm),
            HRFlowable(width="100%", thickness=1,
                       color=accent, spaceAfter=4),
        ]
        for label, value in summary_rows:
            story.append(Paragraph(
                f"<b>{label}</b>  {value}",
                ParagraphStyle(
                    "sum", parent=styles["Normal"],
                    fontSize=9, fontName="Helvetica",
                    alignment=TA_RIGHT)))

    story += [
        Spacer(1, 8*mm),
        HRFlowable(width="100%", thickness=0.5,
                   color=colors.lightgrey),
        Paragraph(
            f"{COMPANY['name']}  –  KRA PIN: {COMPANY.get('kra_pin', 'N/A')}  –  Confidential",
            ParagraphStyle(
                "ft", parent=styles["Normal"],
                fontSize=7, textColor=colors.grey,
                alignment=TA_CENTER)),
    ]

    doc.build(story)
    return True


def save_pdf(title: str, columns: List[str], rows: List[List],
             subtitle: str = "", summary_rows=None, parent_window=None):
    filepath = filedialog.asksaveasfilename(
        parent=parent_window,
        title="Save Report as PDF",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        initialfile=re.sub(r"[^\w]", "_", title) + ".pdf")
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
            messagebox.showerror(
                "Print Error",
                f"Could not print.\n{e}\nTry 'Save PDF' instead.")
    except Exception as e:
        messagebox.showerror("Print Error", str(e))
# ═════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
