# pg-extractor

These Python scripts scrape all Paul Graham essays and extract them into structured JSON and a quotes dataset.

## What it does

- Fetches all essays from paulgraham.com
- Cleans and normalizes the HTML
- Outputs `paul_graham_essays.json`, a structured dataset with title, URL, date, and full text
- `extract_quotes.js` extracts quotable sentences from the essays and writes them to a separate `quotes.json`

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

- `paul_graham_essays.json`: a structured dataset, about 1100 lines
- `paul_graham_essays_text/`: one `.txt` file per essay
- `quotes.json`: a curated quotes dataset

## Run it

```bash
python download_all_essays.py
python extract_essays.py
python verify_extraction.py
```

The scripts need no API keys. They only scrape and parse.

## Status

Done. The dataset supports AI training experiments and a quotes Chrome extension.
