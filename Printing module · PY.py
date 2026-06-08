"""
FarmersDesk Ltd – Printing Module
===================================
Adds two printing capabilities to the main application:

  1. ThermalPrintDialog  – 80mm thermal receipt with QR code
     • Uses escpos-python (python-escpos) for direct USB/serial/network printing
     • Falls back to PDF generation (reportlab) when no printer is attached
     • QR code encodes a URL: https://farmersdesk.local/price?code=<PCode>
       so a phone scan shows live item price

  2. A4ReportPrinter / ReportChooserDialog – full A4 reports via reportlab
     • Sales Summary Report
     • Credit Customers Statement
     • Supplier Statement
     • Stock Valuation Report
     • Debtor Ageing Report
     • Cash Book Summary
     All reports are generated as PDF and opened with the OS default viewer
     (which allows printing on any installed A4 printer).

INSTALLATION
============
  pip install python-escpos reportlab qrcode[pil] pillow

INTEGRATION
===========
In your main App._build_main() method add one more tab:

    from printing_module import PrintingFrame
    tabs.append(("🖨️ Print", PrintingFrame, (uname,)))

Or call the dialogs directly from any frame:

    from printing_module import ThermalPrintDialog, ReportChooserDialog

    # Thermal – pass a TraNo string:
    ThermalPrintDialog(parent_widget, trano="INV-0042",
                       current_user=self.current_user)

    # A4 – opens report picker:
    ReportChooserDialog(parent_widget, current_user=self.current_user)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import os
import io
import subprocess
import sys
import tempfile
from typing import Optional

# ── Lazy imports (give friendly errors if packages missing) ──────────────────
def _require(pkg: str, pip_name: str = ""):
    import importlib
    try:
        return importlib.import_module(pkg)
    except ImportError:
        pip_name = pip_name or pkg
        raise RuntimeError(
            f"Package '{pip_name}' is required.\n"
            f"Install it with:  pip install {pip_name}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Shared palette (must match main app CLR dict)
# ─────────────────────────────────────────────────────────────────────────────
CLR = {
    "bg":        "#F0F4F8",
    "sidebar":   "#1A3C5E",
    "header":    "#1A3C5E",
    "accent":    "#2E86AB",
    "btn":       "#2E86AB",
    "btn_hover": "#1B6CA8",
    "danger":    "#C0392B",
    "success":   "#27AE60",
    "white":     "#FFFFFF",
    "text_dark": "#1A1A2E",
    "text_light":"#FFFFFF",
    "border":    "#CBD5E0",
}
FONT_H2   = ("Helvetica Neue", 13, "bold")
FONT_BODY = ("Helvetica Neue", 11)
FONT_SM   = ("Helvetica Neue", 10)


def _style_btn(btn, danger=False, success=False):
    color = CLR["danger"] if danger else (CLR["success"] if success else CLR["btn"])
    btn.config(bg=color, fg=CLR["white"], font=FONT_BODY,
               relief="flat", cursor="hand2",
               padx=12, pady=5, bd=0,
               activebackground=CLR["btn_hover"])


def _money(v) -> str:
    try:
        return f"{float(v):,.2f}"
    except (TypeError, ValueError):
        return "0.00"


def _today_str() -> str:
    return datetime.date.today().strftime("%Y-%m-%d")


def _open_pdf(path: str):
    """Open a PDF with the OS default viewer."""
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


# ═════════════════════════════════════════════════════════════════════════════
# QR CODE HELPER
# ═════════════════════════════════════════════════════════════════════════════
def _make_qr_pil_image(data: str, box_size: int = 4):
    """Return a PIL Image of the QR code for the given data string."""
    qrcode = _require("qrcode")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def _make_qr_bytes(data: str, box_size: int = 4) -> bytes:
    """Return raw PNG bytes of the QR code."""
    img = _make_qr_pil_image(data, box_size)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ═════════════════════════════════════════════════════════════════════════════
# DATABASE ACCESSOR  (re-use the global db from main app)
# ═════════════════════════════════════════════════════════════════════════════
def _get_db():
    """Return the global db object from the main app module."""
    import importlib, sys
    # Try to get db from __main__ first, then from farmersdesk module
    for mod_name in ["__main__", "farmersdesk"]:
        mod = sys.modules.get(mod_name)
        if mod and hasattr(mod, "db"):
            return mod.db
    raise RuntimeError("Cannot find 'db' object – make sure printing_module "
                       "is imported AFTER the main app module.")


# ═════════════════════════════════════════════════════════════════════════════
# THERMAL RECEIPT BUILDER
# ═════════════════════════════════════════════════════════════════════════════
class ReceiptData:
    """Fetch all data needed for a receipt from the DB."""
    def __init__(self, trano: str):
        db = _get_db()
        self.trano   = trano
        self.sale     = None
        self.items    = []
        self.company  = "FarmersDesk Ltd"
        self.address  = "P.O. Box 0001, Nairobi"
        self.phone    = "+254 700 000 000"
        self.pin      = "P051234567X"
        self.vat_rate = 0.16

        row = db.fetchone(
            "SELECT tradate, SaleTime, cashier, tratype, "
            "total, vat, SoldTo, trano "
            "FROM dbo.Sale WHERE TraNo = ?", (trano,))
        if row:
            self.sale = {
                "date":    str(row[0])[:10],
                "time":    str(row[1])[11:19] if row[1] else "",
                "cashier": row[2] or "",
                "type":    row[3] or "CASH",
                "total":   float(row[4]) if row[4] else 0.0,
                "vat":     float(row[5]) if row[5] else 0.0,
                "sold_to": row[6] or "",
            }

        _, rows = db.fetchall(
            "SELECT ci.PCode, si.name, ci.Qty, ci.Price, ci.SubTotal "
            "FROM dbo.CItem ci "
            "LEFT JOIN dbo.Stock_item si ON si.pcode = ci.PCode "
            "WHERE ci.ItemId IN ("
            "  SELECT ItemId FROM dbo.CItem WHERE ItemId IN ("
            "    SELECT MIN(ItemId) FROM dbo.CItem"   # fallback join
            "  )"
            ") OR ci.ItemId IS NOT NULL "
            "ORDER BY ci.ItemId", ())

        # Simpler direct query
        _, rows = db.fetchall(
            "SELECT ci.PCode, si.name, ci.Qty, ci.Price, ci.SubTotal "
            "FROM dbo.CItem ci "
            "LEFT JOIN dbo.Stock_item si ON si.pcode = ci.PCode "
            "WHERE ci.ItemId IN ("
            "  SELECT ItemId FROM dbo.Sale WHERE TraNo = ?"
            ")",
            (trano,))
        self.items = rows


# ═════════════════════════════════════════════════════════════════════════════
# THERMAL PDF BUILDER  (80 mm width = 226 pt)
# ═════════════════════════════════════════════════════════════════════════════
THERMAL_W = 226   # 80mm in points
THERMAL_MARGIN = 8
THERMAL_FONT = "Courier"


def build_thermal_pdf(receipt: ReceiptData,
                      qr_base_url: str = "https://farmersdesk.local/price") -> bytes:
    """
    Generate a thermal-style PDF (80mm wide) and return the raw PDF bytes.
    Each line item carries a QR code URL: <qr_base_url>?code=<PCode>
    """
    rl = _require("reportlab.pdfgen.canvas", "reportlab")
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader

    buf = io.BytesIO()

    # Estimate height: header ~140pt + items*(40pt) + footer ~80pt
    n_items = max(len(receipt.items), 1)
    page_h = 160 + n_items * 42 + 100
    c = canvas.Canvas(buf, pagesize=(THERMAL_W, page_h))
    y = page_h - THERMAL_MARGIN

    def line(thickness=0.3):
        nonlocal y
        c.setLineWidth(thickness)
        c.line(THERMAL_MARGIN, y, THERMAL_W - THERMAL_MARGIN, y)
        y -= 4

    def text(txt, size=7, bold=False, center=False, indent=0):
        nonlocal y
        c.setFont(f"{THERMAL_FONT}-{'Bold' if bold else 'Roman'}", size)
        x = THERMAL_W / 2 if center else THERMAL_MARGIN + indent
        anchor = "c" if center else "l"
        if center:
            c.drawCentredString(THERMAL_W / 2, y, txt)
        else:
            c.drawString(THERMAL_MARGIN + indent, y, txt)
        y -= size + 2

    def two_col(left, right, size=7):
        nonlocal y
        c.setFont(f"{THERMAL_FONT}-Roman", size)
        c.drawString(THERMAL_MARGIN, y, left)
        c.drawRightString(THERMAL_W - THERMAL_MARGIN, y, right)
        y -= size + 2

    # ── Header ──────────────────────────────────────────────────────────
    y -= 4
    text(receipt.company, size=10, bold=True, center=True)
    text(receipt.address, size=6, center=True)
    text(receipt.phone, size=6, center=True)
    text(f"PIN: {receipt.pin}", size=6, center=True)
    y -= 2
    line()

    if receipt.sale:
        s = receipt.sale
        text(f"Receipt No : {receipt.trano}", size=7, bold=True)
        text(f"Date       : {s['date']}  {s['time']}", size=7)
        text(f"Cashier    : {s['cashier']}", size=7)
        text(f"Type       : {s['type']}", size=7)
        if s["sold_to"]:
            text(f"Customer   : {s['sold_to']}", size=7)
    else:
        text(f"Receipt No : {receipt.trano}", size=7, bold=True)
        text("(Sale record not found)", size=6)

    y -= 2
    line()
    text("ITEM                   QTY   PRICE   TOTAL", size=6, bold=True)
    line()

    # ── Line items with per-item QR ──────────────────────────────────────
    for row in receipt.items:
        pcode, name, qty, price, subtotal = row
        name_str = (name or str(pcode) or "")[:20]
        qty_str   = str(qty or 0)
        price_str = f"{_money(price)}"
        sub_str   = f"{_money(subtotal)}"

        # Item text line
        c.setFont(f"{THERMAL_FONT}-Roman", 6)
        item_line = f"{name_str:<20} {qty_str:>3}  {price_str:>7}  {sub_str:>7}"
        c.drawString(THERMAL_MARGIN, y, item_line)
        y -= 8

        # QR code (small, 18pt) for item price lookup
        qr_url = f"{qr_base_url}?code={pcode}"
        try:
            qr_bytes = _make_qr_bytes(qr_url, box_size=2)
            img = ImageReader(io.BytesIO(qr_bytes))
            c.drawImage(img, THERMAL_W - THERMAL_MARGIN - 18, y - 10,
                        width=18, height=18)
            c.setFont(f"{THERMAL_FONT}-Roman", 5)
            c.drawString(THERMAL_MARGIN, y - 4, f"Scan for price: {pcode}")
        except Exception:
            pass
        y -= 14

    # ── Totals ───────────────────────────────────────────────────────────
    y -= 2
    line()
    if receipt.sale:
        s = receipt.sale
        net = s["total"] - s["vat"]
        two_col("Sub-Total (excl VAT):", f"KES {_money(net)}", size=7)
        two_col(f"VAT (16%):", f"KES {_money(s['vat'])}", size=7)
        c.setFont(f"{THERMAL_FONT}-Bold", 8)
        two_col("TOTAL:", f"KES {_money(s['total'])}", size=8)
    line()

    # ── Footer QR (whole receipt URL) ────────────────────────────────────
    receipt_url = f"{qr_base_url.replace('/price','')}/receipt?trano={receipt.trano}"
    try:
        qr_bytes = _make_qr_bytes(receipt_url, box_size=3)
        qr_img = ImageReader(io.BytesIO(qr_bytes))
        qr_size = 44
        qr_x = (THERMAL_W - qr_size) / 2
        y -= 4
        c.drawImage(qr_img, qr_x, y - qr_size, width=qr_size, height=qr_size)
        y -= qr_size + 2
        c.setFont(f"{THERMAL_FONT}-Roman", 5)
        c.drawCentredString(THERMAL_W / 2, y, "Scan to view / verify receipt")
        y -= 8
    except Exception:
        pass

    text("Thank you for your business!", size=7, bold=True, center=True)
    text("Goods once sold are NOT returnable", size=5, center=True)
    text(f"Printed: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
         size=5, center=True)

    c.save()
    return buf.getvalue()


# ═════════════════════════════════════════════════════════════════════════════
# ESCPOS THERMAL PRINTER DRIVER
# ═════════════════════════════════════════════════════════════════════════════
class ThermalPrinter:
    """
    Wrapper around python-escpos.  Supports USB, Serial, and Network printers.
    If no printer config is provided, falls back to PDF generation.
    """

    PRINTER_CONFIG = {
        # ── Choose ONE of the connection methods below ──────────────────
        # USB:
        # "type": "usb",  "vendor_id": 0x04B8,  "product_id": 0x0202,
        # Serial:
        # "type": "serial",  "devfile": "COM3",  "baudrate": 9600,
        # Network:
        # "type": "network",  "host": "192.168.1.100",  "port": 9100,
        # ────────────────────────────────────────────────────────────────
        # Set "type" to one of the above to enable direct printing.
        "type": None,
    }

    @classmethod
    def _get_printer(cls):
        cfg = cls.PRINTER_CONFIG
        t = cfg.get("type")
        escpos = _require("escpos.printer", "python-escpos")
        from escpos import printer as ep
        if t == "usb":
            return ep.Usb(cfg["vendor_id"], cfg["product_id"])
        elif t == "serial":
            return ep.Serial(cfg.get("devfile", "COM1"),
                             baudrate=cfg.get("baudrate", 9600))
        elif t == "network":
            return ep.Network(cfg["host"], cfg.get("port", 9100))
        return None

    @classmethod
    def print_receipt(cls, receipt: ReceiptData,
                      qr_base_url: str = "https://farmersdesk.local/price"
                      ) -> str:
        """
        Print receipt to thermal printer.
        Returns "direct" if printed to hardware, "pdf" if saved to file.
        """
        p = None
        try:
            p = cls._get_printer()
        except Exception:
            p = None

        if p:
            return cls._print_escpos(p, receipt, qr_base_url)
        else:
            return cls._print_pdf_fallback(receipt, qr_base_url)

    @classmethod
    def _print_escpos(cls, p, receipt: ReceiptData, qr_base_url: str) -> str:
        from escpos import escpos as ep_base
        PIL_Image = _require("PIL.Image", "pillow").Image

        def row(left, right="", bold=False):
            p.set(bold=bold)
            if right:
                # Right-align in 32-char column
                space = max(1, 32 - len(left) - len(right))
                p.text(left + " " * space + right + "\n")
            else:
                p.text(left + "\n")

        # Header
        p.set(align="center", bold=True, width=2, height=2)
        p.text(f"{receipt.company}\n")
        p.set(align="center", bold=False, width=1, height=1)
        p.text(f"{receipt.address}\n{receipt.phone}\nPIN: {receipt.pin}\n")
        p.text("-" * 32 + "\n")

        if receipt.sale:
            s = receipt.sale
            p.set(bold=False)
            p.text(f"Receipt : {receipt.trano}\n")
            p.text(f"Date    : {s['date']}  {s['time']}\n")
            p.text(f"Cashier : {s['cashier']}\n")
            p.text(f"Type    : {s['type']}\n")
            if s["sold_to"]:
                p.text(f"Customer: {s['sold_to']}\n")

        p.text("-" * 32 + "\n")
        p.set(bold=True)
        p.text(f"{'ITEM':<16}{'QTY':>4}{'PRICE':>6}{'TOTAL':>6}\n")
        p.set(bold=False)
        p.text("-" * 32 + "\n")

        for item_row in receipt.items:
            pcode, name, qty, price, subtotal = item_row
            nm = (name or str(pcode) or "")[:15]
            p.text(f"{nm:<15} {str(qty or 0):>3} "
                   f"{_money(price):>6} {_money(subtotal):>6}\n")
            # Per-item QR
            qr_url = f"{qr_base_url}?code={pcode}"
            try:
                qr_img = _make_qr_pil_image(qr_url, box_size=2)
                p.image(qr_img)
                p.text(f"^ Scan: {pcode}\n")
            except Exception:
                pass

        p.text("-" * 32 + "\n")
        if receipt.sale:
            s = receipt.sale
            net = s["total"] - s["vat"]
            p.text(f"{'Sub-Total:':<18}{_money(net):>14}\n")
            p.text(f"{'VAT (16%):':<18}{_money(s['vat']):>14}\n")
            p.set(bold=True, width=1, height=1)
            p.text(f"{'TOTAL:':^18}{'KES '+_money(s['total']):>14}\n")
            p.set(bold=False)

        p.text("-" * 32 + "\n")

        # Footer QR (whole receipt)
        receipt_url = (f"{qr_base_url.replace('/price','')}"
                       f"/receipt?trano={receipt.trano}")
        try:
            qr_img = _make_qr_pil_image(receipt_url, box_size=3)
            p.set(align="center")
            p.image(qr_img)
            p.text("Scan to view/verify receipt\n")
        except Exception:
            pass

        p.set(align="center")
        p.text("Thank you for your business!\n")
        p.text("Goods once sold are NOT returnable\n")
        p.text(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        p.cut()
        return "direct"

    @classmethod
    def _print_pdf_fallback(cls, receipt: ReceiptData, qr_base_url: str) -> str:
        pdf_bytes = build_thermal_pdf(receipt, qr_base_url)
        path = os.path.join(
            tempfile.gettempdir(),
            f"receipt_{receipt.trano}_{datetime.datetime.now().strftime('%H%M%S')}.pdf"
        )
        with open(path, "wb") as f:
            f.write(pdf_bytes)
        _open_pdf(path)
        return path


# ═════════════════════════════════════════════════════════════════════════════
# THERMAL PRINT DIALOG  (Tkinter UI)
# ═════════════════════════════════════════════════════════════════════════════
class ThermalPrintDialog(tk.Toplevel):
    """
    Pop-up dialog to print or preview a thermal receipt.

    Usage:
        ThermalPrintDialog(parent, trano="INV-0042", current_user="admin")
    """

    def __init__(self, parent, trano: str = "", current_user: str = ""):
        super().__init__(parent)
        self.current_user = current_user
        self.title("🖨️  Thermal Receipt Printer")
        self.configure(bg=CLR["bg"])
        self.resizable(False, False)
        self._center(420, 360)
        self.grab_set()
        self._build(trano)

    def _center(self, w, h):
        self.geometry(f"{w}x{h}+"
                      f"{(self.winfo_screenwidth()-w)//2}+"
                      f"{(self.winfo_screenheight()-h)//2}")

    def _build(self, trano: str):
        hdr = tk.Frame(self, bg=CLR["header"], height=48)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🧾  Thermal Receipt",
                 font=FONT_H2, bg=CLR["header"],
                 fg=CLR["white"]).pack(expand=True)

        body = tk.Frame(self, bg=CLR["bg"], padx=24, pady=16)
        body.pack(fill="both", expand=True)

        # Receipt number
        f1 = tk.Frame(body, bg=CLR["bg"])
        f1.pack(fill="x", pady=4)
        tk.Label(f1, text="Receipt / TraNo:", font=FONT_SM,
                 bg=CLR["bg"], width=16, anchor="w").pack(side="left")
        self.trano_var = tk.StringVar(value=trano)
        ttk.Entry(f1, textvariable=self.trano_var,
                  font=FONT_BODY, width=20).pack(side="left")

        # QR base URL
        f2 = tk.Frame(body, bg=CLR["bg"])
        f2.pack(fill="x", pady=4)
        tk.Label(f2, text="QR Base URL:", font=FONT_SM,
                 bg=CLR["bg"], width=16, anchor="w").pack(side="left")
        self.qr_url_var = tk.StringVar(
            value="https://farmersdesk.local/price")
        ttk.Entry(f2, textvariable=self.qr_url_var,
                  font=FONT_BODY, width=30).pack(side="left")

        # Printer config quick-set
        f3 = tk.Frame(body, bg=CLR["bg"])
        f3.pack(fill="x", pady=4)
        tk.Label(f3, text="Printer Type:", font=FONT_SM,
                 bg=CLR["bg"], width=16, anchor="w").pack(side="left")
        self.printer_type = tk.StringVar(value="pdf_preview")
        cb = ttk.Combobox(f3, textvariable=self.printer_type,
                          font=FONT_SM, width=18,
                          values=["pdf_preview", "usb", "serial", "network"],
                          state="readonly")
        cb.pack(side="left")
        cb.bind("<<ComboboxSelected>>", self._on_printer_type)

        # Dynamic connection fields
        self.conn_frame = tk.Frame(body, bg=CLR["bg"])
        self.conn_frame.pack(fill="x", pady=4)
        self.conn_widgets = {}
        self._show_conn_fields("pdf_preview")

        self.status_lbl = tk.Label(body, text="", font=FONT_SM,
                                   bg=CLR["bg"], fg=CLR["accent"],
                                   wraplength=360)
        self.status_lbl.pack(pady=6)

        btn_row = tk.Frame(body, bg=CLR["bg"])
        btn_row.pack(pady=8)

        prev_btn = tk.Button(btn_row, text="👁  Preview PDF",
                             command=self._preview)
        _style_btn(prev_btn)
        prev_btn.pack(side="left", padx=6)

        print_btn = tk.Button(btn_row, text="🖨  Print",
                              command=self._print)
        _style_btn(print_btn, success=True)
        print_btn.pack(side="left", padx=6)

        save_btn = tk.Button(btn_row, text="💾  Save PDF",
                             command=self._save)
        _style_btn(save_btn)
        save_btn.pack(side="left", padx=6)

        close_btn = tk.Button(btn_row, text="✖  Close",
                              command=self.destroy)
        _style_btn(close_btn, danger=True)
        close_btn.pack(side="left", padx=6)

    def _on_printer_type(self, _event=None):
        self._show_conn_fields(self.printer_type.get())

    def _show_conn_fields(self, ptype: str):
        for w in self.conn_frame.winfo_children():
            w.destroy()
        self.conn_widgets = {}

        fields = {
            "usb":     [("Vendor ID (hex):", "vendor_id", "0x04B8"),
                        ("Product ID (hex):", "product_id", "0x0202")],
            "serial":  [("Port (e.g. COM3):", "devfile", "COM3"),
                        ("Baud Rate:", "baudrate", "9600")],
            "network": [("Printer IP:", "host", "192.168.1.100"),
                        ("Port:", "port", "9100")],
        }.get(ptype, [])

        for label, key, default in fields:
            row = tk.Frame(self.conn_frame, bg=CLR["bg"])
            row.pack(fill="x", pady=1)
            tk.Label(row, text=label, font=FONT_SM,
                     bg=CLR["bg"], width=18, anchor="w").pack(side="left")
            var = tk.StringVar(value=default)
            ttk.Entry(row, textvariable=var,
                      font=FONT_SM, width=18).pack(side="left")
            self.conn_widgets[key] = var

    def _apply_printer_config(self):
        ptype = self.printer_type.get()
        if ptype == "pdf_preview":
            ThermalPrinter.PRINTER_CONFIG["type"] = None
            return
        cfg = {"type": ptype}
        for key, var in self.conn_widgets.items():
            val = var.get().strip()
            if key in ("vendor_id", "product_id"):
                val = int(val, 16)
            elif key in ("baudrate", "port"):
                val = int(val)
            cfg[key] = val
        ThermalPrinter.PRINTER_CONFIG = cfg

    def _load_receipt(self) -> Optional[ReceiptData]:
        trano = self.trano_var.get().strip()
        if not trano:
            messagebox.showwarning("Missing", "Enter a Receipt / TraNo.")
            return None
        try:
            r = ReceiptData(trano)
            return r
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
            return None

    def _preview(self):
        r = self._load_receipt()
        if not r:
            return
        self.status_lbl.config(text="⏳ Generating preview…")
        self.update()
        try:
            pdf_bytes = build_thermal_pdf(r, self.qr_url_var.get().strip())
            path = os.path.join(
                tempfile.gettempdir(),
                f"receipt_preview_{r.trano}.pdf")
            with open(path, "wb") as f:
                f.write(pdf_bytes)
            _open_pdf(path)
            self.status_lbl.config(text=f"✅ Preview opened: {path}")
        except Exception as e:
            messagebox.showerror("Preview Error", str(e))
            self.status_lbl.config(text="")

    def _print(self):
        r = self._load_receipt()
        if not r:
            return
        self._apply_printer_config()
        self.status_lbl.config(text="⏳ Printing…")
        self.update()
        try:
            result = ThermalPrinter.print_receipt(
                r, self.qr_url_var.get().strip())
            if result == "direct":
                self.status_lbl.config(
                    text="✅ Sent to thermal printer.")
            else:
                self.status_lbl.config(
                    text=f"✅ No hardware printer – PDF saved:\n{result}")
        except Exception as e:
            messagebox.showerror("Print Error", str(e))
            self.status_lbl.config(text="")

    def _save(self):
        r = self._load_receipt()
        if not r:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"receipt_{r.trano}.pdf")
        if not path:
            return
        try:
            pdf_bytes = build_thermal_pdf(r, self.qr_url_var.get().strip())
            with open(path, "wb") as f:
                f.write(pdf_bytes)
            self.status_lbl.config(text=f"✅ Saved: {path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))


# ═════════════════════════════════════════════════════════════════════════════
# A4 REPORT GENERATORS
# ═════════════════════════════════════════════════════════════════════════════
A4_W  = 595   # A4 width in points
A4_H  = 842   # A4 height in points
A4_ML = 36    # left margin
A4_MR = 36    # right margin
A4_MT = 36    # top margin
A4_MB = 36    # bottom margin
BODY_W = A4_W - A4_ML - A4_MR

COL_HDR_BG = (26/255, 60/255, 94/255)   # #1A3C5E
COL_ODD    = (0.918, 0.949, 1.0)        # #EAF2FF
COL_WHITE  = (1, 1, 1)
COL_TEXT   = (0.1, 0.1, 0.18)
COL_ACCENT = (0.18, 0.525, 0.671)


class A4Report:
    """Base class for A4 PDF report generation via reportlab."""

    def __init__(self, title: str, subtitle: str = ""):
        self.title    = title
        self.subtitle = subtitle
        self.buf      = io.BytesIO()
        rl = _require("reportlab.pdfgen.canvas", "reportlab")
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        self.c = canvas.Canvas(self.buf, pagesize=A4)
        self.page_num = 0
        self.y = 0
        self._new_page()

    def _new_page(self):
        if self.page_num > 0:
            self.c.showPage()
        self.page_num += 1
        self.y = A4_H - A4_MT
        self._draw_header()
        self._draw_footer()

    def _draw_header(self):
        c = self.c
        # Background bar
        c.setFillColorRGB(*COL_HDR_BG)
        c.rect(A4_ML, self.y - 44, BODY_W, 44, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(A4_ML + 8, self.y - 20, "FarmersDesk Ltd")
        c.setFont("Helvetica", 9)
        c.drawString(A4_ML + 8, self.y - 34, self.title)
        if self.subtitle:
            c.drawRightString(A4_W - A4_MR - 4, self.y - 34, self.subtitle)
        self.y -= 56

    def _draw_footer(self):
        c = self.c
        c.setFont("Helvetica", 7)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.drawString(A4_ML, A4_MB, f"Printed: {ts}")
        c.drawRightString(A4_W - A4_MR,
                          A4_MB, f"Page {self.page_num}")
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.line(A4_ML, A4_MB + 10, A4_W - A4_MR, A4_MB + 10)

    def section_title(self, txt: str):
        self._check_space(24)
        self.y -= 6
        c = self.c
        c.setFillColorRGB(*COL_ACCENT)
        c.rect(A4_ML, self.y - 16, BODY_W, 16, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(A4_ML + 4, self.y - 11, txt.upper())
        self.y -= 22

    def kv_row(self, label: str, value: str):
        self._check_space(14)
        c = self.c
        c.setFont("Helvetica-Bold", 8)
        c.setFillColorRGB(*COL_TEXT)
        c.drawString(A4_ML, self.y, label)
        c.setFont("Helvetica", 8)
        c.drawString(A4_ML + 160, self.y, value)
        self.y -= 13

    def table(self, headers: list, rows: list,
              col_widths: list = None, money_cols: set = None):
        """Draw a table with header row and alternating row colours."""
        money_cols = money_cols or set()
        n = len(headers)
        if col_widths is None:
            col_widths = [BODY_W / n] * n

        row_h   = 13
        hdr_h   = 15
        self._check_space(hdr_h + row_h * min(len(rows), 3))

        c = self.c
        x0 = A4_ML

        # Header
        c.setFillColorRGB(*COL_HDR_BG)
        c.rect(x0, self.y - hdr_h, BODY_W, hdr_h, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 7)
        cur_x = x0
        for i, h in enumerate(headers):
            align = "right" if i in money_cols else "left"
            if align == "right":
                c.drawRightString(cur_x + col_widths[i] - 2,
                                  self.y - hdr_h + 4, h)
            else:
                c.drawString(cur_x + 2, self.y - hdr_h + 4, h)
            cur_x += col_widths[i]
        self.y -= hdr_h

        # Data rows
        c.setFont("Helvetica", 7)
        for idx, row in enumerate(rows):
            self._check_space(row_h)
            if idx % 2 == 0:
                c.setFillColorRGB(*COL_ODD)
                c.rect(x0, self.y - row_h, BODY_W, row_h, fill=1, stroke=0)
            c.setFillColorRGB(*COL_TEXT)
            cur_x = x0
            for i, val in enumerate(row):
                txt = str(val)
                align = "right" if i in money_cols else "left"
                # Clip text to column width
                max_chars = int(col_widths[i] / 5)
                txt = txt[:max_chars]
                if align == "right":
                    c.drawRightString(cur_x + col_widths[i] - 2,
                                      self.y - row_h + 3, txt)
                else:
                    c.drawString(cur_x + 2, self.y - row_h + 3, txt)
                cur_x += col_widths[i]
            self.y -= row_h

        # Bottom line
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setLineWidth(0.3)
        c.line(x0, self.y, x0 + BODY_W, self.y)
        self.y -= 4

    def _check_space(self, needed: int):
        if self.y - needed < A4_MB + 30:
            self._new_page()

    def build(self) -> bytes:
        self.c.save()
        return self.buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# Individual report functions
# ─────────────────────────────────────────────────────────────────────────────

def report_sales_summary(d1: str, d2: str, cashier: str = "") -> bytes:
    db = _get_db()
    r = A4Report("Sales Summary Report",
                 subtitle=f"{d1}  to  {d2}")
    r.kv_row("Period:", f"{d1}  –  {d2}")
    if cashier:
        r.kv_row("Cashier:", cashier)
    r.kv_row("Generated:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    cashier_like = f"%{cashier}%"
    _, rows = db.fetchall(
        "SELECT tradate, TraNo, tratype, cashier, total, vat, SoldTo "
        "FROM dbo.Sale "
        "WHERE tradate BETWEEN ? AND ? AND cashier LIKE ? "
        "ORDER BY tradate DESC",
        (d1, d2, cashier_like))

    total_sales = sum(float(x[4]) for x in rows if x[4])
    total_vat   = sum(float(x[5]) for x in rows if x[5])

    r.section_title(f"Sales Transactions  ({len(rows)} records)")
    headers = ["Date", "TraNo", "Type", "Cashier", "Total (KES)", "VAT (KES)", "Customer"]
    widths  = [55, 55, 50, 60, 65, 60, 128]
    fmt_rows = [[str(x[0])[:10], x[1], x[2] or "", x[3] or "",
                 _money(x[4]), _money(x[5]), x[6] or ""] for x in rows]
    r.table(headers, fmt_rows, widths, money_cols={4, 5})

    r.section_title("Totals")
    r.kv_row("Total Sales (KES):", _money(total_sales))
    r.kv_row("Total VAT (KES):",   _money(total_vat))
    r.kv_row("Net Sales (KES):",   _money(total_sales - total_vat))
    r.kv_row("No. of transactions:", str(len(rows)))

    return r.build()


def report_credit_customers(search: str = "") -> bytes:
    db = _get_db()
    r = A4Report("Credit Customers Report",
                 subtitle=datetime.date.today().isoformat())
    q = f"%{search}%"
    _, rows = db.fetchall(
        "SELECT id, name, phone, Route, balance, cperiod, datedue "
        "FROM dbo.Credit_Customer "
        "WHERE name LIKE ? OR phone LIKE ? ORDER BY name",
        (q, q))
    total_bal = sum(float(x[4]) for x in rows if x[4])
    r.kv_row("Generated:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    r.kv_row("Total Customers:", str(len(rows)))
    r.kv_row("Total Outstanding (KES):", _money(total_bal))
    r.section_title(f"Customer List  ({len(rows)} records)")
    headers = ["ID", "Name", "Phone", "Route", "Balance (KES)", "Period", "Date Due"]
    widths  = [35, 120, 75, 65, 70, 50, 58]
    fmt = [[x[0], x[1] or "", x[2] or "", x[3] or "",
            _money(x[4]), x[5] or "", str(x[6] or "")[:10]] for x in rows]
    r.table(headers, fmt, widths, money_cols={4})
    return r.build()


def report_supplier_statement(supplier_id, supplier_name: str,
                               d1: str, d2: str) -> bytes:
    db = _get_db()
    r = A4Report(f"Supplier Statement – {supplier_name}",
                 subtitle=f"{d1}  to  {d2}")
    r.kv_row("Supplier:", supplier_name)
    r.kv_row("Supplier ID:", str(supplier_id))
    r.kv_row("Period:", f"{d1}  –  {d2}")

    _, inv = db.fetchall(
        "SELECT RecId, InvDate, TraNo, Detail, InvAmount, Paid, Balance "
        "FROM dbo.SInv WHERE SId = ? AND InvDate BETWEEN ? AND ? "
        "ORDER BY InvDate DESC",
        (supplier_id, d1, d2))
    r.section_title(f"Invoices  ({len(inv)} records)")
    headers = ["RecId", "Inv Date", "TraNo", "Detail",
               "Inv Amount (KES)", "Paid (KES)", "Balance (KES)"]
    widths  = [40, 55, 55, 100, 80, 70, 73]
    fmt = [[x[0], str(x[1])[:10], x[2] or "", x[3] or "",
            _money(x[4]), _money(x[5]), _money(x[6])] for x in inv]
    r.table(headers, fmt, widths, money_cols={4, 5, 6})

    _, rep = db.fetchall(
        "SELECT trano, issuedate, datedue, docno, amount, vatamount, dmode "
        "FROM dbo.Stock_Replenish WHERE sid = ? AND issuedate BETWEEN ? AND ? "
        "ORDER BY issuedate DESC",
        (supplier_id, d1, d2))
    r.section_title(f"Replenishments / Purchases  ({len(rep)} records)")
    headers2 = ["TraNo", "Issue Date", "Due Date",
                "Doc No", "Amount (KES)", "VAT (KES)", "Mode"]
    widths2  = [55, 58, 58, 60, 70, 60, 112]
    fmt2 = [[x[0], str(x[1])[:10], str(x[2])[:10] if x[2] else "",
             x[3] or "", _money(x[4]), _money(x[5]), x[6] or ""] for x in rep]
    r.table(headers2, fmt2, widths2, money_cols={4, 5})
    return r.build()


def report_stock_valuation(category: str = "") -> bytes:
    db = _get_db()
    cat_like = f"%{category}%"
    r = A4Report("Stock Valuation Report",
                 subtitle=datetime.date.today().isoformat())
    _, rows = db.fetchall(
        "SELECT pcode, name, PCategory, qtystock, bpw, spw "
        "FROM dbo.Stock_item "
        "WHERE PCategory LIKE ? ORDER BY PCategory, name",
        (cat_like,))
    total_cost  = sum((float(x[3] or 0)) * (float(x[4] or 0)) for x in rows)
    total_value = sum((float(x[3] or 0)) * (float(x[5] or 0)) for x in rows)
    r.kv_row("Generated:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    r.kv_row("Total Items:", str(len(rows)))
    r.kv_row("Cost Value (KES):",  _money(total_cost))
    r.kv_row("Retail Value (KES):", _money(total_value))
    r.section_title(f"Stock Items  ({len(rows)} records)")
    headers = ["PCode", "Name", "Category",
               "Qty", "Buy Price", "Sale Price", "Cost Value", "Retail Value"]
    widths  = [45, 110, 70, 30, 55, 60, 65, 88]
    fmt = [[x[0], x[1] or "", x[2] or "",
            x[3] or 0, _money(x[4]), _money(x[5]),
            _money(float(x[3] or 0) * float(x[4] or 0)),
            _money(float(x[3] or 0) * float(x[5] or 0))] for x in rows]
    r.table(headers, fmt, widths, money_cols={4, 5, 6, 7})
    return r.build()


def report_debtor_ageing() -> bytes:
    db = _get_db()
    r = A4Report("Debtor Ageing Report",
                 subtitle=datetime.date.today().isoformat())
    _, rows = db.fetchall(
        "SELECT s.sid, cc.name, s.a30, s.a60, s.a90, "
        "s.a120, s.aover, s.atotal, s.UB "
        "FROM dbo.SDAS s "
        "LEFT JOIN dbo.Credit_Customer cc ON cc.id = s.sid "
        "ORDER BY s.atotal DESC")
    grand = sum(float(x[7]) for x in rows if x[7])
    r.kv_row("Generated:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    r.kv_row("Total Debtors:", str(len(rows)))
    r.kv_row("Grand Total Outstanding (KES):", _money(grand))
    r.section_title(f"Ageing Schedule  ({len(rows)} customers)")
    headers = ["Cust ID", "Name", "0-30 d", "31-60 d",
               "61-90 d", "91-120 d", "Over 120 d", "Total", "Unalloc"]
    widths  = [40, 100, 50, 50, 50, 55, 58, 60, 60]
    fmt = [[x[0], x[1] or "", _money(x[2]), _money(x[3]),
            _money(x[4]), _money(x[5]), _money(x[6]),
            _money(x[7]), _money(x[8])] for x in rows]
    r.table(headers, fmt, widths, money_cols={2, 3, 4, 5, 6, 7, 8})
    return r.build()


def report_cashbook(d1: str, d2: str) -> bytes:
    db = _get_db()
    r = A4Report("Cash Book Report",
                 subtitle=f"{d1}  to  {d2}")
    _, rows = db.fetchall(
        "SELECT Dt, Tm, MCat, MCat2, cin, cout, bin, bout, dby "
        "FROM dbo.CB WHERE Dt BETWEEN ? AND ? ORDER BY Dt DESC, Tm DESC",
        (d1, d2))
    total_in   = sum(float(x[4]) for x in rows if x[4])
    total_out  = sum(float(x[5]) for x in rows if x[5])
    bank_in    = sum(float(x[6]) for x in rows if x[6])
    bank_out   = sum(float(x[7]) for x in rows if x[7])
    r.kv_row("Period:", f"{d1}  –  {d2}")
    r.kv_row("Cash In (KES):",   _money(total_in))
    r.kv_row("Cash Out (KES):",  _money(total_out))
    r.kv_row("Bank In (KES):",   _money(bank_in))
    r.kv_row("Bank Out (KES):",  _money(bank_out))
    r.kv_row("Net Cash (KES):",  _money(total_in - total_out))
    r.section_title(f"Transactions  ({len(rows)} entries)")
    headers = ["Date", "Time", "Category", "Category2",
               "Cash In", "Cash Out", "Bank In", "Bank Out", "By"]
    widths  = [55, 45, 70, 70, 50, 55, 50, 55, 73]
    fmt = [[str(x[0])[:10], str(x[1])[11:19] if x[1] else "",
            x[2] or "", x[3] or "",
            _money(x[4]), _money(x[5]), _money(x[6]),
            _money(x[7]), x[8] or ""] for x in rows]
    r.table(headers, fmt, widths, money_cols={4, 5, 6, 7})
    return r.build()


# ═════════════════════════════════════════════════════════════════════════════
# A4 REPORT CHOOSER DIALOG  (Tkinter UI)
# ═════════════════════════════════════════════════════════════════════════════
class ReportChooserDialog(tk.Toplevel):
    """
    Full-featured A4 report generation dialog.
    All reports generate PDF and open with OS default PDF viewer/printer.
    """

    def __init__(self, parent, current_user: str = ""):
        super().__init__(parent)
        self.current_user = current_user
        self.title("📄  A4 Report Printer")
        self.configure(bg=CLR["bg"])
        self.resizable(True, True)
        self._center(620, 560)
        self.grab_set()
        self._build()

    def _center(self, w, h):
        self.geometry(f"{w}x{h}+"
                      f"{(self.winfo_screenwidth()-w)//2}+"
                      f"{(self.winfo_screenheight()-h)//2}")

    def _build(self):
        hdr = tk.Frame(self, bg=CLR["header"], height=48)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="📄  A4 Report Generator",
                 font=FONT_H2, bg=CLR["header"],
                 fg=CLR["white"]).pack(expand=True)

        body = tk.Frame(self, bg=CLR["bg"], padx=20, pady=12)
        body.pack(fill="both", expand=True)

        nb = ttk.Notebook(body)
        nb.pack(fill="both", expand=True)

        self._build_sales_tab(nb)
        self._build_customers_tab(nb)
        self._build_supplier_tab(nb)
        self._build_stock_tab(nb)
        self._build_ageing_tab(nb)
        self._build_cashbook_tab(nb)

        self.status_lbl = tk.Label(self, text="", font=FONT_SM,
                                   bg=CLR["bg"], fg=CLR["accent"],
                                   anchor="w")
        self.status_lbl.pack(fill="x", padx=20, pady=4)

        close_btn = tk.Button(self, text="✖  Close",
                              command=self.destroy)
        _style_btn(close_btn, danger=True)
        close_btn.pack(anchor="e", padx=20, pady=8)

    # ── Tab builders ─────────────────────────────────────────────────────
    def _build_sales_tab(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="  📊 Sales Summary  ")
        f = tk.Frame(tab, bg=CLR["bg"], padx=16, pady=12)
        f.pack(fill="both", expand=True)

        self._date_row(f, "From:", "ss_from")
        self._date_row(f, "To:",   "ss_to")

        row = tk.Frame(f, bg=CLR["bg"])
        row.pack(fill="x", pady=2)
        tk.Label(row, text="Cashier (optional):", font=FONT_SM,
                 bg=CLR["bg"], width=20, anchor="w").pack(side="left")
        self.ss_cashier = tk.StringVar()
        ttk.Entry(row, textvariable=self.ss_cashier,
                  font=FONT_SM, width=22).pack(side="left")

        self._gen_btn(f, self._gen_sales)

    def _build_customers_tab(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="  👥 Credit Customers  ")
        f = tk.Frame(tab, bg=CLR["bg"], padx=16, pady=12)
        f.pack(fill="both", expand=True)
        row = tk.Frame(f, bg=CLR["bg"])
        row.pack(fill="x", pady=2)
        tk.Label(row, text="Search (optional):", font=FONT_SM,
                 bg=CLR["bg"], width=20, anchor="w").pack(side="left")
        self.cc_search = tk.StringVar()
        ttk.Entry(row, textvariable=self.cc_search,
                  font=FONT_SM, width=28).pack(side="left")
        self._gen_btn(f, self._gen_customers)

    def _build_supplier_tab(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="  🏭 Supplier Statement  ")
        f = tk.Frame(tab, bg=CLR["bg"], padx=16, pady=12)
        f.pack(fill="both", expand=True)

        row = tk.Frame(f, bg=CLR["bg"])
        row.pack(fill="x", pady=2)
        tk.Label(row, text="Supplier ID:", font=FONT_SM,
                 bg=CLR["bg"], width=20, anchor="w").pack(side="left")
        self.sup_id = tk.StringVar()
        ttk.Entry(row, textvariable=self.sup_id,
                  font=FONT_SM, width=14).pack(side="left")

        row2 = tk.Frame(f, bg=CLR["bg"])
        row2.pack(fill="x", pady=2)
        tk.Label(row2, text="Supplier Name:", font=FONT_SM,
                 bg=CLR["bg"], width=20, anchor="w").pack(side="left")
        self.sup_name = tk.StringVar()
        ttk.Entry(row2, textvariable=self.sup_name,
                  font=FONT_SM, width=28).pack(side="left")

        self._date_row(f, "From:", "sup_from")
        self._date_row(f, "To:",   "sup_to")
        self._gen_btn(f, self._gen_supplier)

    def _build_stock_tab(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="  📦 Stock Valuation  ")
        f = tk.Frame(tab, bg=CLR["bg"], padx=16, pady=12)
        f.pack(fill="both", expand=True)
        row = tk.Frame(f, bg=CLR["bg"])
        row.pack(fill="x", pady=2)
        tk.Label(row, text="Category (optional):", font=FONT_SM,
                 bg=CLR["bg"], width=20, anchor="w").pack(side="left")
        self.stk_cat = tk.StringVar()
        ttk.Entry(row, textvariable=self.stk_cat,
                  font=FONT_SM, width=28).pack(side="left")
        self._gen_btn(f, self._gen_stock)

    def _build_ageing_tab(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="  📅 Debtor Ageing  ")
        f = tk.Frame(tab, bg=CLR["bg"], padx=16, pady=12)
        f.pack(fill="both", expand=True)
        tk.Label(f, text="No parameters needed – generates full ageing schedule.",
                 font=FONT_SM, bg=CLR["bg"],
                 fg=CLR["accent"]).pack(anchor="w", pady=8)
        self._gen_btn(f, self._gen_ageing)

    def _build_cashbook_tab(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="  📒 Cash Book  ")
        f = tk.Frame(tab, bg=CLR["bg"], padx=16, pady=12)
        f.pack(fill="both", expand=True)
        self._date_row(f, "From:", "cb_from")
        self._date_row(f, "To:",   "cb_to")
        self._gen_btn(f, self._gen_cashbook)

    # ── Shared helpers ────────────────────────────────────────────────────
    def _date_row(self, parent, label: str, attr: str):
        today = _today_str()
        month_start = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
        default = month_start if "from" in attr else today
        row = tk.Frame(parent, bg=CLR["bg"])
        row.pack(fill="x", pady=2)
        tk.Label(row, text=label, font=FONT_SM,
                 bg=CLR["bg"], width=20, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        ttk.Entry(row, textvariable=var,
                  font=FONT_SM, width=14).pack(side="left")
        setattr(self, attr, var)

    def _gen_btn(self, parent, cmd):
        row = tk.Frame(parent, bg=CLR["bg"])
        row.pack(fill="x", pady=12)
        prev = tk.Button(row, text="📄  Generate & Preview",
                         command=cmd)
        _style_btn(prev, success=True)
        prev.pack(side="left", padx=4)
        save = tk.Button(row, text="💾  Save PDF",
                         command=lambda: cmd(save=True))
        _style_btn(save)
        save.pack(side="left", padx=4)

    def _deliver(self, pdf_bytes: bytes, filename: str, save: bool = False):
        if save:
            path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=filename)
            if not path:
                return
            with open(path, "wb") as f:
                f.write(pdf_bytes)
            self.status_lbl.config(text=f"✅ Saved: {path}")
        else:
            path = os.path.join(tempfile.gettempdir(), filename)
            with open(path, "wb") as f:
                f.write(pdf_bytes)
            _open_pdf(path)
            self.status_lbl.config(text=f"✅ Opened: {path}")

    # ── Report generators ────────────────────────────────────────────────
    def _gen_sales(self, save: bool = False):
        self.status_lbl.config(text="⏳ Generating…")
        self.update()
        try:
            pdf = report_sales_summary(
                self.ss_from.get(), self.ss_to.get(),
                self.ss_cashier.get())
            self._deliver(pdf,
                f"sales_summary_{self.ss_from.get()}.pdf", save)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_lbl.config(text="")

    def _gen_customers(self, save: bool = False):
        self.status_lbl.config(text="⏳ Generating…")
        self.update()
        try:
            pdf = report_credit_customers(self.cc_search.get())
            self._deliver(pdf, "credit_customers.pdf", save)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_lbl.config(text="")

    def _gen_supplier(self, save: bool = False):
        sid = self.sup_id.get().strip()
        sname = self.sup_name.get().strip() or f"Supplier {sid}"
        if not sid:
            messagebox.showwarning("Missing", "Enter a Supplier ID.")
            return
        self.status_lbl.config(text="⏳ Generating…")
        self.update()
        try:
            pdf = report_supplier_statement(
                sid, sname,
                self.sup_from.get(), self.sup_to.get())
            self._deliver(pdf, f"supplier_{sid}.pdf", save)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_lbl.config(text="")

    def _gen_stock(self, save: bool = False):
        self.status_lbl.config(text="⏳ Generating…")
        self.update()
        try:
            pdf = report_stock_valuation(self.stk_cat.get())
            self._deliver(pdf, "stock_valuation.pdf", save)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_lbl.config(text="")

    def _gen_ageing(self, save: bool = False):
        self.status_lbl.config(text="⏳ Generating…")
        self.update()
        try:
            pdf = report_debtor_ageing()
            self._deliver(pdf, "debtor_ageing.pdf", save)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_lbl.config(text="")

    def _gen_cashbook(self, save: bool = False):
        self.status_lbl.config(text="⏳ Generating…")
        self.update()
        try:
            pdf = report_cashbook(self.cb_from.get(), self.cb_to.get())
            self._deliver(pdf, f"cashbook_{self.cb_from.get()}.pdf", save)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_lbl.config(text="")


# ═════════════════════════════════════════════════════════════════════════════
# PRINTING TAB  (drop-in Notebook tab for the main App)
# ═════════════════════════════════════════════════════════════════════════════
class PrintingFrame(ttk.Frame):
    """
    A complete tab frame combining thermal receipt printing and A4 report
    generation.  Add to the main app's tabs list:

        from printing_module import PrintingFrame
        tabs.append(("🖨️ Print", PrintingFrame, (uname,)))
    """

    def __init__(self, parent, current_user: str = ""):
        super().__init__(parent)
        self.current_user = current_user
        self._build()

    def _build(self):
        # ── Title ─────────────────────────────────────────────────────────
        tk.Label(self, text="Printing Centre",
                 font=("Helvetica Neue", 18, "bold"),
                 bg=CLR["bg"], fg=CLR["text_dark"]).pack(pady=(20, 6))

        # ── Two side-by-side panels ────────────────────────────────────────
        main = tk.Frame(self, bg=CLR["bg"])
        main.pack(fill="both", expand=True, padx=20, pady=8)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        # --- Thermal panel ------------------------------------------------
        tp = tk.LabelFrame(main, text="🧾  Thermal Receipt (80mm)",
                           font=FONT_H2, bg=CLR["bg"],
                           fg=CLR["text_dark"], padx=12, pady=12)
        tp.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        tk.Label(tp,
                 text=("Print receipts to an 80mm thermal printer.\n"
                       "Each line item includes a QR code – scan it to\n"
                       "look up the current price of that item.\n\n"
                       "A full-receipt QR code is printed at the bottom\n"
                       "for digital verification."),
                 font=FONT_SM, bg=CLR["bg"],
                 fg=CLR["text_dark"], justify="left",
                 wraplength=240).pack(anchor="w", pady=(0, 10))

        tk.Label(tp, text="Receipt / TraNo:", font=FONT_SM,
                 bg=CLR["bg"]).pack(anchor="w")
        self.trano_var = tk.StringVar()
        ttk.Entry(tp, textvariable=self.trano_var,
                  font=FONT_BODY, width=22).pack(anchor="w", pady=(2, 8))

        btn_t1 = tk.Button(tp, text="🖨  Print / Preview Receipt",
                           command=self._open_thermal)
        _style_btn(btn_t1, success=True)
        btn_t1.pack(fill="x", pady=2)

        tk.Label(tp, text="\nPrinter Setup", font=FONT_H2,
                 bg=CLR["bg"], fg=CLR["text_dark"]).pack(anchor="w")
        tk.Label(tp,
                 text=("Set PRINTER_CONFIG in ThermalPrinter\n"
                       "to point to your USB / Serial / Network\n"
                       "ESC/POS thermal printer.\n\n"
                       "Without hardware, a thermal-style PDF is\n"
                       "generated instead."),
                 font=FONT_SM, bg=CLR["bg"],
                 fg=CLR["text_dark"], justify="left",
                 wraplength=240).pack(anchor="w")

        # --- A4 panel -------------------------------------------------------
        ap = tk.LabelFrame(main, text="📄  A4 Reports (PDF)",
                           font=FONT_H2, bg=CLR["bg"],
                           fg=CLR["text_dark"], padx=12, pady=12)
        ap.grid(row=0, column=1, sticky="nsew")

        reports = [
            ("📊  Sales Summary",        self._gen_quick("sales")),
            ("👥  Credit Customers",     self._gen_quick("customers")),
            ("📦  Stock Valuation",      self._gen_quick("stock")),
            ("📅  Debtor Ageing",        self._gen_quick("ageing")),
            ("📒  Cash Book",            self._gen_quick("cashbook")),
        ]

        tk.Label(ap,
                 text=("Generate professional A4 PDF reports.\n"
                       "Quick-generate buttons below use\n"
                       "current month defaults.  Use the full\n"
                       "Report Chooser for date filtering."),
                 font=FONT_SM, bg=CLR["bg"],
                 fg=CLR["text_dark"], justify="left",
                 wraplength=240).pack(anchor="w", pady=(0, 10))

        for label, cmd in reports:
            b = tk.Button(ap, text=label, command=cmd)
            _style_btn(b)
            b.pack(fill="x", pady=2)

        full_btn = tk.Button(ap, text="⚙️  Full Report Chooser…",
                             command=self._open_report_chooser)
        _style_btn(full_btn, success=True)
        full_btn.pack(fill="x", pady=(12, 2))

        self.status_lbl = tk.Label(self, text="", font=FONT_SM,
                                   bg=CLR["bg"], fg=CLR["accent"],
                                   anchor="w")
        self.status_lbl.pack(fill="x", padx=20, pady=4)

    def _open_thermal(self):
        ThermalPrintDialog(self, trano=self.trano_var.get().strip(),
                           current_user=self.current_user)

    def _open_report_chooser(self):
        ReportChooserDialog(self, current_user=self.current_user)

    def _gen_quick(self, rtype: str):
        def _cmd():
            today = _today_str()
            ms    = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
            self.status_lbl.config(text="⏳ Generating…")
            self.update()
            try:
                if rtype == "sales":
                    pdf = report_sales_summary(ms, today)
                    fname = f"sales_summary_{ms}.pdf"
                elif rtype == "customers":
                    pdf = report_credit_customers()
                    fname = "credit_customers.pdf"
                elif rtype == "stock":
                    pdf = report_stock_valuation()
                    fname = "stock_valuation.pdf"
                elif rtype == "ageing":
                    pdf = report_debtor_ageing()
                    fname = "debtor_ageing.pdf"
                elif rtype == "cashbook":
                    pdf = report_cashbook(ms, today)
                    fname = f"cashbook_{ms}.pdf"
                else:
                    return
                path = os.path.join(tempfile.gettempdir(), fname)
                with open(path, "wb") as f:
                    f.write(pdf)
                _open_pdf(path)
                self.status_lbl.config(text=f"✅ Opened: {path}")
            except Exception as e:
                messagebox.showerror("Report Error", str(e))
                self.status_lbl.config(text="")
        return _cmd
