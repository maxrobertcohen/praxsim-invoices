# PraxSim VR — Monthly Invoices

Auto-generated invoices for Max Cohen → PraxSim VR.

## Files

- `make_invoice.py` — generator (reportlab)
- `2026_MM_-_Max_Inv_for_PraxSim.pdf` — one per month

## Generate a new month manually

```bash
pip install reportlab
python make_invoice.py --year 2026 --month 8 --number 53
# → 2026_08_-_Max_Inv_for_PraxSim.pdf
```

## Standing details

- Recipient: PraxSim VR (c/o Shareene Lindquist), 5859 Buena Vista Ave, Oakland CA 94618
- Project: Grant Writing & Product Design Consultation
- Terms: 30 Days
- Two line items per month: 1st–15th and 16th–end-of-month, $1,000 each → $2,000 total
- Invoice number advances by 1 each month (June 2026 = 0051, July = 0052, …)
