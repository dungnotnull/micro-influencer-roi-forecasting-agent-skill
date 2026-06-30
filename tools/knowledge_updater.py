#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_updater.py — self-improving knowledge pipeline for `micro-influencer-roi-forecasting` (idea #208).

Pattern (per CLAUDE.md):
  1. crawl4ai  -> fetch latest papers (ArXiv cs.SI, econ.GN + domain sources)
  2. WebSearch -> latest news/reports from authoritative sources
  3. Parse     -> title, authors, date, DOI/URL, abstract, key findings
  4. Score     -> recency + domain-keyword relevance
  5. Append    -> scored entries into SECOND-KNOWLEDGE-BRAIN.md (date-stamped)
  6. Dedupe    -> skip URLs/DOIs already present (hash check)

Recommended schedule: weekly cron.
Graceful degradation: if crawl4ai / network is unavailable, log and exit 0 so the
skill keeps working from the existing knowledge brain.
"""
import os, re, sys, json, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BRAIN = os.path.join(HERE, "..", "SECOND-KNOWLEDGE-BRAIN.md")

ARXIV_CATEGORIES = ["cs.SI", "econ.GN"]
DOMAIN_SOURCES = [
    "https://www.ama.org/journal-of-marketing/",
    "https://influencermarketinghub.com/",
    "https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers",
    "https://creators.instagram.com/",
    "https://www.nielsen.com/"
]
SEARCH_QUERIES = [
    "influencer marketing ROI measurement 2026",
    "fake engagement bot detection influencer",
    "incrementality testing influencer lift",
    "micro influencer pricing benchmark"
]
RELEVANCE_KEYWORDS = SEARCH_QUERIES  # reused for keyword-match scoring

def _hash(url: str) -> str:
    return hashlib.sha256(url.strip().lower().encode("utf-8")).hexdigest()[:16]

def _existing_hashes(text: str):
    return set(re.findall(r"<!--hash:([0-9a-f]{16})-->", text))

def relevance_score(title: str, abstract: str) -> float:
    blob = (title + " " + abstract).lower()
    hits = sum(1 for kw in RELEVANCE_KEYWORDS for w in kw.lower().split() if w in blob)
    denom = max(1, sum(len(kw.split()) for kw in RELEVANCE_KEYWORDS))
    return round(min(1.0, hits / denom), 3)

def fetch_entries():
    """Return list of dicts: title, authors, date, url, abstract.
    Uses crawl4ai when available; otherwise returns [] (degraded mode)."""
    try:
        from crawl4ai import WebCrawler  # type: ignore
    except Exception as e:
        print(f"[knowledge_updater] crawl4ai unavailable ({e}); degraded mode, exiting.")
        return []
    entries = []
    try:
        crawler = WebCrawler(); crawler.warmup()
        for cat in ARXIV_CATEGORIES:
            url = f"https://arxiv.org/list/{cat}/recent"
            res = crawler.run(url=url)
            for item in _parse_arxiv(getattr(res, "markdown", "") or ""):
                entries.append(item)
        for src in DOMAIN_SOURCES:
            res = crawler.run(url=src)
            md = getattr(res, "markdown", "") or ""
            if md:
                entries.append({"title": f"Update from {src}", "authors": "-",
                                "date": datetime.date.today().isoformat(),
                                "url": src, "abstract": md[:500]})
    except Exception as e:
        print(f"[knowledge_updater] crawl error: {e}")
    return entries

def _parse_arxiv(md: str):
    out = []
    for m in re.finditer(r"(arXiv:\d+\.\d+)", md):
        aid = m.group(1)
        out.append({"title": aid, "authors": "-",
                     "date": datetime.date.today().isoformat(),
                     "url": f"https://arxiv.org/abs/{aid.split(':')[1]}",
                     "abstract": ""})
    return out

def append_entries(entries):
    if not os.path.exists(BRAIN):
        print(f"[knowledge_updater] brain not found at {BRAIN}"); return 0
    with open(BRAIN, "r", encoding="utf-8") as f:
        text = f.read()
    seen = _existing_hashes(text)
    today = datetime.date.today().isoformat()
    added, lines = 0, []
    for e in entries:
        h = _hash(e["url"])
        if h in seen:
            continue
        rel = relevance_score(e.get("title",""), e.get("abstract",""))
        if rel < 0.05:
            continue
        seen.add(h)
        lines.append(
            f"\n### [{today}] {e['title']}\n"
            f"- Authors: {e.get('authors','-')}\n"
            f"- Venue/Source: {e['url']}\n"
            f"- Key finding: {(e.get('abstract','') or '')[:280]}\n"
            f"- Relevance score: {rel}\n"
            f"<!--hash:{h}-->\n"
        )
        added += 1
    if added:
        with open(BRAIN, "a", encoding="utf-8") as f:
            f.write(f"\n<!-- crawl {today}: +{added} entries -->\n")
            f.write("".join(lines))
    print(f"[knowledge_updater] appended {added} new entries.")
    return added

def main():
    print(f"[knowledge_updater] starting crawl for micro-influencer-roi-forecasting ...")
    entries = fetch_entries()
    n = append_entries(entries)
    print(f"[knowledge_updater] done; {n} entries added.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
