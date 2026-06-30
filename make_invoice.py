"""
Generate a monthly PraxSim VR invoice in the standard template.

Usage:
    python make_invoice.py --year 2026 --month 8 --number 53

Outputs:  2026_MM_-_Max_Inv_for_PraxSim.pdf  in the current directory.

Requires: reportlab  (pip install reportlab)
"""
import argparse
import calendar
from datetime import date
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

BLUE = colors.HexColor("#3a7a9b")
GREY = colors.HexColor("#666666")
PAGE_W, PAGE_H = LETTER

MONTH_ABBR = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
              7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}


def build(year: int, month: int, number: int, out_path: str):
    last_day = calendar.monthrange(year, month)[1]
    abbr = MONTH_ABBR[month]
    date_str = f"{month:02d}/01/{year}"
    invoice_number = f"{number:04d}"
    line1 = f"{abbr} 01 - {abbr} 15, {year}"
    line2 = f"{abbr} 16 - {abbr} {last_day}, {year}"

    c = canvas.Canvas(out_path, pagesize=LETTER)

    # top rule
    c.setStrokeColor(BLUE); c.setLineWidth(2)
    c.line(0.6*inch, PAGE_H - 0.7*inch, PAGE_W - 0.6*inch, PAGE_H - 0.7*inch)

    # MAX COHEN
    c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 14)
    c.drawString(0.85*inch, PAGE_H - 1.05*inch, "MAX COHEN")

    # INVOICE
    c.setFillColor(GREY); c.setFont("Helvetica", 36)
    c.drawString(0.85*inch, PAGE_H - 2.35*inch, "INVOICE")

    # left contact column
    c.setFillColor(BLUE); c.setFont("Helvetica", 10)
    c.drawString(0.85*inch, PAGE_H - 2.75*inch, "518-683-1589")
    c.drawString(0.85*inch, PAGE_H - 2.92*inch, "maxrcohen@gmail.com")
    email_w = c.stringWidth("maxrcohen@gmail.com", "Helvetica", 10)
    c.setStrokeColor(BLUE); c.setLineWidth(0.5)
    c.line(0.85*inch, PAGE_H - 2.94*inch, 0.85*inch + email_w, PAGE_H - 2.94*inch)
    c.setFillColor(colors.black); c.setFont("Helvetica-Bold", 10)
    c.drawString(0.85*inch, PAGE_H - 3.12*inch, "20 North 5th St, Apt 611")
    c.drawString(0.85*inch, PAGE_H - 3.27*inch, "Brooklyn, NY 11249")

    # right column
    right_x = 3.0*inch
    y = PAGE_H - 2.25*inch
    c.setFillColor(colors.black); c.setFont("Helvetica", 10)
    c.drawString(right_x, y, "Attn: PraxSim VR (c/o Shareene Lindquist)")
    c.drawRightString(PAGE_W - 0.85*inch, y, date_str)
    y -= 0.16*inch; c.drawString(right_x, y, "5859 Buena Vista Ave, Oakland, CA 94618")
    y -= 0.16*inch; c.drawString(right_x, y, "Project Title: PraxSim VR")
    y -= 0.16*inch; c.drawString(right_x, y, "Project Description: Grant Writing & Product Design Consultation")
    y -= 0.16*inch; c.drawString(right_x, y, f"Invoice Number: {invoice_number}")
    y -= 0.16*inch; c.drawString(right_x, y, "Terms: 30 Days")

    # table
    table_x = right_x
    table_top_y = y - 0.4*inch
    data = [
        ["Description", "Quantity", "Unit Price", "Cost"],
        [line1, "1", "$1,000.00", "$1,000.00"],
        [line2, "1", "$1,000.00", "$1,000.00"],
        ["", "", "", ""],
        ["", "", "Subtotal", "$2,000.00"],
        ["", "Tax", "0.00%", "$0.00"],
        ["", "", "Total", "$2,000.00"],
    ]
    col_widths = [2.5*inch, 0.85*inch, 0.95*inch, 0.95*inch]
    tbl = Table(data, colWidths=col_widths, rowHeights=[0.32*inch] + [0.28*inch]*6)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 10),
        ("ALIGN", (1,1), (1,2), "RIGHT"),
        ("ALIGN", (2,1), (3,-1), "RIGHT"),
        ("ALIGN", (1,5), (1,5), "RIGHT"),
        ("ALIGN", (2,4), (2,6), "RIGHT"),
        ("LINEBELOW", (0,1), (-1,1), 0.4, colors.lightgrey, None, [1,2]),
        ("LINEBELOW", (0,2), (-1,2), 0.4, colors.lightgrey, None, [1,2]),
        ("LINEBELOW", (0,3), (-1,3), 0.4, colors.lightgrey, None, [1,2]),
        ("LINEBELOW", (0,4), (-1,4), 0.4, colors.lightgrey, None, [1,2]),
        ("LINEBELOW", (0,5), (-1,5), 0.4, colors.lightgrey, None, [1,2]),
        ("LINEAFTER", (0,1), (0,-1), 0.4, colors.lightgrey, None, [1,2]),
        ("LINEAFTER", (1,1), (1,-1), 0.4, colors.lightgrey, None, [1,2]),
        ("LINEAFTER", (2,1), (2,-1), 0.4, colors.lightgrey, None, [1,2]),
    ]))
    w, h = tbl.wrapOn(c, sum(col_widths), 3*inch)
    tbl.drawOn(c, table_x, table_top_y - h)

    # closing
    msg_y = table_top_y - h - 0.5*inch
    c.setFillColor(colors.black); c.setFont("Helvetica", 10)
    c.drawString(table_x, msg_y, "Thank you for your business, it is a pleasure to work with you on this project.")
    c.drawString(table_x, msg_y - 0.35*inch, "Sincerely yours,")
    c.drawString(table_x, msg_y - 0.7*inch, "Max Cohen")

    # bottom rule + page no.
    c.setStrokeColor(BLUE); c.setLineWidth(2)
    c.line(0.6*inch, 0.7*inch, PAGE_W - 0.6*inch, 0.7*inch)
    c.setFillColor(colors.black); c.setFont("Helvetica", 10)
    c.drawRightString(PAGE_W - 0.85*inch, 0.5*inch, "1")
    c.save()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--month", type=int, required=True, help="1-12")
    ap.add_argument("--number", type=int, required=True, help="invoice number, e.g. 53")
    ap.add_argument("--out", default=None, help="output path; default: 2026_MM_-_Max_Inv_for_PraxSim.pdf")
    args = ap.parse_args()
    out = args.out or f"{args.year}_{args.month:02d}_-_Max_Inv_for_PraxSim.pdf"
    build(args.year, args.month, args.number, out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
