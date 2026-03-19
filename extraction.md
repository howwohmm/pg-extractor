# pg-extractor

## project name + description
- pg-extractor: Python scripts to extract, download, and process Paul Graham essays from RSS feed and HTML into structured JSON and text files

## who it's for
- Self — building a dataset of Paul Graham essays for downstream use (likely for training or RAG)

## current status
- tool

## what was actually built
- `extract_essays.py` — parses Paul Graham's RSS feed (aaronsw.com) to extract essay titles, URLs, and filenames into JSON
- `download_all_essays.py` — fetches HTML of all essays
- `fetch_missing_essays.py` — catches gaps in the download
- `rename_and_unify.py` — normalizes filenames across the corpus
- `create_combined_files.py` — merges essays into combined output files
- `verify_extraction.py` — validates completeness of the extraction
- `extract_quotes.js` — extracts notable quotes from essay text
- `paul_graham_essays.json` + `paul_graham_essays_updated.json` — structured essay metadata
- `paul_graham_essays_text/` — plain text versions of essays
- `quotes.json` — extracted quotes dataset
- `html/` — raw HTML archive

## why it was built
- To build a clean, complete dataset of Paul Graham's essays for downstream ML or search use

## blockers or reasons shelved
- Not shelved — appears to be a completed data extraction tool

## wins or progress moments
- Full pipeline from RSS → HTML download → text extraction → quotes — end-to-end working

## pain points
- `fetch_missing_essays.py` implies the initial download had gaps — scraping PG's site is inconsistent

## where claude api / ai was used or planned
- Dataset likely intended as training data or RAG source for an AI project

## what would've helped
- Automated freshness checks to catch new essays as they're published

## metrics or traction
- none
