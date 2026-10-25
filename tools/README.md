# Tools

- `build_question_bank.py` — rebuilds `../question-bank/Question_Bank.xlsx` and `../questions.csv` from `data/questions.json` (run from this folder: `python3 build_question_bank.py`; needs `openpyxl`). Formulas in the workbook need recalculating in Excel/LibreOffice after a rebuild.
- `quotes_lib.py`, `quotes_map.py` — extract exact regulation wording from text versions of the SEBI PDFs (expects `src/regs.raw.txt`, `src/og.raw.txt`, `src/circ.raw.txt`, `src/sop.raw.txt` made with `pdftotext`; the PDFs aren't included). Output: `data/quotes.json`.
- `data/new1.py`–`new3.py` — the source of the 107 questions added in October 2026.
