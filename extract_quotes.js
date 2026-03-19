#!/usr/bin/env node
// Extract quotable sentences from PG essays + curated quotes.txt
// Output: quotes.json

const fs = require('fs');
const path = require('path');

const ESSAYS_DIR = '/Users/ohm./Desktop/ppt/paul_graham_essays_text';
const QUOTES_TXT = '/Users/ohm./Desktop/vibe-code/pg-quotes/quotes.txt';
const OUT_FILE   = '/Users/ohm./Desktop/ppt/quotes.json';

// ── 1. Parse curated quotes.txt ──────────────────────────────────────────────
function parseCuratedQuotes(raw) {
  const quotes = [];
  const blocks = raw.split(/\n\n+/);
  for (const block of blocks) {
    const lines = block.trim().split('\n').map(l => l.trim()).filter(Boolean);
    if (lines.length < 2) continue;
    // First line: quoted text (wrapped in "")
    // Second line: – Author
    const textLine = lines[0];
    const authorLine = lines.slice(1).join(' ');
    const text = textLine.replace(/^[""]|[""]$/g, '').trim();
    const author = authorLine.replace(/^[–—-]\s*/, '').trim();
    if (text.length > 10 && author.length > 1) {
      quotes.push({ text, author, source: 'curated' });
    }
  }
  return quotes;
}

// ── 2. Sentence splitter ──────────────────────────────────────────────────────
function splitSentences(text) {
  // Split on . ! ? followed by space + capital, but preserve abbreviations poorly
  return text
    .replace(/\n+/g, ' ')
    .split(/(?<=[.!?])\s+(?=[A-Z"'])/)
    .map(s => s.trim())
    .filter(Boolean);
}

// ── 3. Quality filter for a sentence ─────────────────────────────────────────
const BAD_STARTS = [
  /^(I |We |You |He |She |They |It |This |That |These |Those |There |Here |In |On |At |By |For |From |With |But |And |Or |So |As |If |When |While |After |Before |Since |Though |Although |Because |However |Note |See |Read |Thanks |The (reason|problem|question|answer|fact|thing|point|way|idea|key|best|worst|most|least))/i,
  /^\[/, /^\(/, /^http/, /^\d/, /^e\.g/, /^i\.e/, /^etc/i,
  /^(My |Our |Your |His |Her |Their )/i,
  /^(A lot|Some|Many|Most|Few|All|Both|Each|Every|No |Any )/i,
];

const BAD_PATTERNS = [
  /\b(footnote|endnote|figure|table|section|chapter|appendix)\b/i,
  /\b(click here|see also|read more|subscribe)\b/i,
  /\(.*\).*\(.*\)/, // multiple parens = footnote-heavy
  /\.{3}/, // ellipsis = incomplete
  /\[.*\]/, // brackets = editorial
  /https?:\/\//, // URLs
  /\bI (was|am|have|had|did|went|said|think|thought|feel|felt|know|knew|saw|see)\b/,
  /[.!?][^.!?"]*[.!?]/, // two sentences merged (two terminal punctuation marks)
  /\b(above|below|previous|following|section|paragraph|essay|article|post)\b/i,
  /\b(Pittsburgh|Cambridge|Silicon Valley|San Francisco|New York|Boston|London|Harvard|MIT|Stanford|Google|Facebook|Apple|Yahoo|Microsoft|Twitter|YC|Y Combinator)\b/, // too place/name specific
  /\d{4}/, // years make it dated
  /\bhe said\b|\bshe said\b|\bthey said\b/i,
];

const GOOD_KEYWORDS = [
  'startup', 'founder', 'idea', 'work', 'people', 'make', 'build', 'create',
  'success', 'fail', 'money', 'invest', 'learn', 'school', 'smart', 'smart',
  'best', 'good', 'great', 'important', 'never', 'always', 'most', 'real',
  'true', 'false', 'wrong', 'right', 'better', 'worse', 'world', 'change',
  'problem', 'solution', 'think', 'believe', 'simple', 'hard', 'easy',
  'design', 'product', 'user', 'growth', 'power', 'talent', 'ambition',
  'wealth', 'rich', 'poor', 'fear', 'courage', 'risk', 'opportunity',
];

function isQuotable(sentence) {
  const len = sentence.length;
  if (len < 45 || len > 220) return false;

  // Must end with punctuation
  if (!/[.!?]$/.test(sentence)) return false;

  // No bad starts
  for (const pat of BAD_STARTS) {
    if (pat.test(sentence)) return false;
  }

  // No bad patterns
  for (const pat of BAD_PATTERNS) {
    if (pat.test(sentence)) return false;
  }

  // Must contain at least one good keyword
  const lower = sentence.toLowerCase();
  const hasKeyword = GOOD_KEYWORDS.some(kw => lower.includes(kw));
  if (!hasKeyword) return false;

  // Avoid sentences with too many proper nouns (hard to judge without NLP)
  // Rough heuristic: not too many capitalized words mid-sentence
  const midCapitals = (sentence.slice(5).match(/\b[A-Z][a-z]+/g) || []).length;
  if (midCapitals > 3) return false;

  // Must read as a standalone insight (not just description)
  const insightPatterns = [
    /\b(never|always|often|rarely|best|worst|most|least|only|every|all|none)\b/i,
    /\b(better|worse|more|less|harder|easier|faster|slower)\b/i,
    /\b(important|crucial|essential|key|critical|vital|fundamental)\b/i,
    /\b(wrong|right|true|false|real|fake|good|bad|great|terrible)\b/i,
    /\b(should|must|need|have to|ought to)\b/i,
    /\b(means|implies|requires|leads to|causes|results in)\b/i,
    /\b(surprising|unexpected|counterintuitive|paradox|irony)\b/i,
  ];
  const hasInsight = insightPatterns.some(p => p.test(sentence));
  if (!hasInsight) return false;

  return true;
}

// ── 4. Extract essay title from header ───────────────────────────────────────
function extractTitle(raw) {
  const m = raw.match(/^Title:\s*(.+)/m);
  return m ? m[1].trim() : 'Paul Graham';
}

// ── 5. Strip essay header ─────────────────────────────────────────────────────
function stripHeader(raw) {
  const sep = '================================================================================';
  const idx = raw.indexOf(sep);
  return idx >= 0 ? raw.slice(idx + sep.length) : raw;
}

// ── 6. Main ───────────────────────────────────────────────────────────────────
const curatedRaw = fs.readFileSync(QUOTES_TXT, 'utf8');
const curated = parseCuratedQuotes(curatedRaw);
console.log(`Curated quotes: ${curated.length}`);

const essayFiles = fs.readdirSync(ESSAYS_DIR).filter(f => f.endsWith('.txt'));
console.log(`Essays to process: ${essayFiles.length}`);

const pgQuotes = [];
const seen = new Set();

for (const file of essayFiles) {
  const raw  = fs.readFileSync(path.join(ESSAYS_DIR, file), 'utf8');
  const title = extractTitle(raw);
  const body  = stripHeader(raw);
  const sentences = splitSentences(body);

  for (const s of sentences) {
    const clean = s.replace(/\s+/g, ' ').trim();
    if (isQuotable(clean) && !seen.has(clean)) {
      seen.add(clean);
      pgQuotes.push({ text: clean, author: 'Paul Graham', source: title });
    }
  }
}

console.log(`PG essay quotes extracted: ${pgQuotes.length}`);

// Combine: curated first (they're gold), then PG's own words
const all = [...curated, ...pgQuotes];

// Shuffle PG quotes for variety (keep curated in order)
for (let i = pgQuotes.length - 1; i > 0; i--) {
  const j = Math.floor(Math.random() * (i + 1));
  [all[curated.length + i], all[curated.length + j]] =
  [all[curated.length + j], all[curated.length + i]];
}

fs.writeFileSync(OUT_FILE, JSON.stringify(all, null, 2));
console.log(`\nTotal quotes: ${all.length}`);
console.log(`Output: ${OUT_FILE}`);

// Preview 10 random PG quotes
console.log('\n── Sample PG quotes ──────────────────────────────');
const sample = pgQuotes.sort(() => Math.random() - 0.5).slice(0, 10);
sample.forEach(q => console.log(`• "${q.text}"\n  — ${q.source}\n`));
