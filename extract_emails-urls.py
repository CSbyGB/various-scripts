#!/usr/bin/env python3
"""
Extract email addresses and URLs found in the source code of a web page.

Usage:
    python extract_emails-urls.py https://example.com/contact
    python extract_emails-urls.py https://example.com --only urls
    python extract_emails-urls.py https://example.com --only emails -o results.txt
    python extract_emails-urls.py page.html --base https://example.com   # local file

Dependency: pip install requests
"""

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urljoin, urldefrag

import requests

# ---------- Email patterns ----------

# Standard email address pattern
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# Common obfuscated forms: name [at] domain [dot] com, name (arobase) domain (point) fr...
OBFUSCATED_RE = re.compile(
    r"([A-Za-z0-9._%+\-]+)\s*[\[\(\{]\s*(?:at|arobase|@)\s*[\]\)\}]\s*"
    r"([A-Za-z0-9\-]+(?:\s*[\[\(\{]\s*(?:dot|point|\.)\s*[\]\)\}]\s*[A-Za-z0-9\-]+)+)",
    re.IGNORECASE,
)
DOT_RE = re.compile(r"\s*[\[\(\{]\s*(?:dot|point|\.)\s*[\]\)\}]\s*", re.IGNORECASE)

# Cloudflare email protection: data-cfemail="..." or /cdn-cgi/l/email-protection#...
CF_RE = re.compile(r'(?:data-cfemail="|email-protection#)([0-9a-fA-F]+)')

# Extensions that look like emails but aren't (e.g. logo@2x.png)
FALSE_POSITIVES = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".css", ".js")

# ---------- URL patterns ----------

# Links in HTML attributes: href, src, action, data-src, poster...
ATTR_URL_RE = re.compile(
    r'\b(?:href|src|action|data-src|data-href|poster)\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)
# Absolute URLs anywhere in the code (text, scripts, JSON...)
BARE_URL_RE = re.compile(r'https?://[^\s"\'<>()\\]+', re.IGNORECASE)
# srcset can hold several URLs: "img1.jpg 1x, img2.jpg 2x"
SRCSET_RE = re.compile(r'\bsrcset\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)

# Schemes that are not real web links
IGNORED_SCHEMES = ("mailto:", "javascript:", "tel:", "data:", "sms:", "#")


def fetch_source(target: str) -> tuple[str, str | None]:
    """Download the page (URL) or read the local file. Returns (html, final_url)."""
    if Path(target).is_file():
        return Path(target).read_text(encoding="utf-8", errors="ignore"), None

    if not target.startswith(("http://", "https://")):
        target = "https://" + target

    headers = {"User-Agent": "Mozilla/5.0 (compatible; EmailExtractor/1.0)"}
    response = requests.get(target, headers=headers, timeout=15)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response.text, response.url  # response.url follows redirects


def decode_cloudflare(code: str) -> str:
    key = int(code[:2], 16)
    return "".join(chr(int(code[i:i + 2], 16) ^ key) for i in range(2, len(code), 2))


def extract_emails(source: str) -> list[str]:
    # Decode HTML entities (&#64; -> @) and URL encoding (%40 -> @)
    text = unquote(html.unescape(source))

    found = set(EMAIL_RE.findall(text))

    for name, domain in OBFUSCATED_RE.findall(text):
        found.add(f"{name}@{DOT_RE.sub('.', domain)}")

    for code in CF_RE.findall(source):
        try:
            found.update(EMAIL_RE.findall(decode_cloudflare(code)))
        except ValueError:
            pass

    cleaned = {
        e.strip(".").lower()
        for e in found
        if not e.lower().endswith(FALSE_POSITIVES)
    }
    return sorted(cleaned)


def extract_urls(source: str, base_url: str | None) -> list[str]:
    text = html.unescape(source)

    # A <base href="..."> tag overrides the page URL for relative links
    base_tag = re.search(r'<base\s[^>]*href\s*=\s*["\']([^"\']+)["\']', text, re.IGNORECASE)
    if base_tag:
        base_url = urljoin(base_url or "", base_tag.group(1))

    raw = list(ATTR_URL_RE.findall(text))
    raw += BARE_URL_RE.findall(text)
    for srcset in SRCSET_RE.findall(text):
        raw += [part.strip().split()[0] for part in srcset.split(",") if part.strip()]

    found = set()
    for url in raw:
        url = url.strip()
        if not url or url.lower().startswith(IGNORED_SCHEMES):
            continue
        if url.startswith("//"):  # protocol-relative link
            url = "https:" + url
        if base_url:
            url = urljoin(base_url, url)
        url, _ = urldefrag(url)  # drop "#section" fragments
        url = url.rstrip(".,;")
        if url:
            found.add(url)

    return sorted(found)


def main():
    parser = argparse.ArgumentParser(description="Extract email addresses and URLs from a web page.")
    parser.add_argument("target", help="Page URL or path to a local HTML file")
    parser.add_argument("--only", choices=["emails", "urls"], help="Extract only emails or only URLs")
    parser.add_argument("--base", help="Base URL used to resolve relative links (useful for local files)")
    parser.add_argument("-o", "--output", help="File to save the results to")
    args = parser.parse_args()

    try:
        source, final_url = fetch_source(args.target)
    except requests.RequestException as e:
        sys.exit(f"Error while fetching the page: {e}")

    sections = []

    if args.only != "urls":
        emails = extract_emails(source)
        sections.append(("Email address(es)", emails))

    if args.only != "emails":
        urls = extract_urls(source, args.base or final_url)
        sections.append(("URL(s)", urls))

    output_lines = []
    for title, items in sections:
        print(f"{len(items)} {title.lower()} found:")
        for item in items:
            print(f"  {item}")
        print()
        output_lines += [f"# {title}"] + items + [""]

    if args.output:
        Path(args.output).write_text("\n".join(output_lines), encoding="utf-8")
        print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
