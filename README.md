# Reglex · FPI Game

**Custody Desk League** — an adaptive, case-based quiz on India's foreign portfolio investor (FPI) regulations: Regular FPI, SWAGAT-FI and GS-FPI.

**Play:** [https://ironmanbro.github.io/reglex-fpi-game/](http://reglex.netlify.app)

## What it does

- **175 case files** built from public SEBI material, covering Chapters II–VI and the Second Schedule of the SEBI (FPI) Regulations 2019, plus SWAGAT-FI and GS-FPI.
- **Adaptive difficulty:** a right answer brings a harder case (Easy → Medium → Hard); a wrong answer an easier one. Rounds of 10, 15, 20 or 25.
- **After every answer:** why the right option is right, why each other option is wrong, and **the exact wording of the regulation** behind it.
- **Look back during a round:** revisit earlier answers read-only; answers are locked.
- **End-of-round review:** every question, your answer vs the correct one, filters, copy as text, download as CSV.
- **Live league table** (Supabase).

All entities are fictional. Built only from public SEBI material. Not legal advice.

## Project layout

| Path | What it is |
|---|---|
| `index.html` | The game (served by GitHub Pages from the repo root) |
| `questions.csv` | The question bank the game reads at load time |
| `config.js` | Public league-table settings (Supabase URL + anon key; database rules allow read + insert only) |
| `question-bank/Question_Bank.xlsx` | Master question bank: edit and review here (status, checks, summary) |
| `supabase/supabase-setup.sql` | Creates the `scores` table and its access rules |
| `designs/noir/index.html` | Alternative noir "detective desk" design (self-contained, built-in questions) |
| `tools/` | Scripts that rebuild the workbook and CSV from `tools/data/questions.json`, and extract regulation quotes |
| `tests/` | Playwright scripts used to test rounds, the answer review and locked review (reference) |

## Updating questions

1. Edit `question-bank/Question_Bank.xlsx` (Questions sheet). Only `status = live` rows reach players; the `check` column must say OK.
2. File → Save As → **CSV UTF-8** → `questions.csv` (Questions sheet open), replacing the one in the repo root.
3. Commit and push. GitHub Pages republishes in about a minute.

The start screen shows how many live questions loaded and names any skipped rows.

## Sources

- SEBI (Foreign Portfolio Investors) Regulations, 2019 (consolidated text, amended to Dec 2023)
- SEBI Operational Guidelines for FPIs, DDPs and EFIs (2019; since folded into the FPI Master Circular of 30 May 2024)
- SEBI circular HO/19/34/14(5)2025-AFD-POD2/I/2703/2026, 16 January 2026 (SWAGAT-FI)
- CDSSF SOP for Registration as SWAGAT-FI, updated 27 May 2026

Questions tagged **Verify** rely on secondary summaries (GS-FPI circulars of Sep 2025 / Sep 2026).
