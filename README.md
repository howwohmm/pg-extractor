# pg-extractor

Python scripts to scrape all Paul Graham essays and extract them into structured JSON + a quotes dataset.

## What it does

- Fetches every essay from paulgraham.com
- Cleans and normalizes the HTML
- Outputs `paul_graham_essays.json` — structured dataset with title, URL, date, full text
- `extract_quotes.js` — pulls quotable sentences from the essays into a separate `quotes.json`

## Scripts

| Script | What it does |
|--------|-------------|
| `download_all_essays.py` | Fetches all essays from paulgraham.com, saves HTML |
| `extract_essays.py` | Parses HTML → structured JSON |
| `fetch_missing_essays.py` | Gap-fill for any essays missed in the first pass |
| `rename_and_unify.py` | Normalizes filenames and merges into single JSON |
| `create_combined_files.py` | Creates combined text corpus |
| `verify_extraction.py` | Sanity-checks the output dataset |
| `extract_quotes.js` | Node.js script — extracts quotable sentences into quotes.json |

## Output

- `paul_graham_essays.json` — ~1100-line structured dataset
- `paul_graham_essays_text/` — individual `.txt` files per essay
- `quotes.json` — curated quotes dataset

## Run it

```bash
python download_all_essays.py
python extract_essays.py
python verify_extraction.py
```

No API keys needed. Pure scraping + parsing.

## Status

Done. Used as a dataset for AI training experiments and a quotes Chrome extension.
