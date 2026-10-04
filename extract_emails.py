#!/usr/bin/env python3
"""
Extract email addresses found in the source code of a web page.

Usage:
    python extract_emails_en.py https://example.com/contact
    python extract_emails_en.py page.html            # also works with a local file
    python extract_emails_en.py https://example.com -o results.txt

Dependency: pip install requests
"""

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import requests

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


def fetch_source(target: str) -> str:
    """Download the page (URL) or read the local file."""
    if Path(target).is_file():
        return Path(target).read_text(encoding="utf-8", errors="ignore")

    if not target.startswith(("http://", "https://")):
        target = "https://" + target

    headers = {"User-Agent": "Mozilla/5.0 (compatible; EmailExtractor/1.0)"}
    response = requests.get(target, headers=headers, timeout=15)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response.text


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


def main():
    parser = argparse.ArgumentParser(description="Extract email addresses from a web page.")
    parser.add_argument("target", help="Page URL or path to a local HTML file")
    parser.add_argument("-o", "--output", help="File to save the results to")
    args = parser.parse_args()

    try:
        source = fetch_source(args.target)
    except requests.RequestException as e:
        sys.exit(f"Error while fetching the page: {e}")

    emails = extract_emails(source)

    if not emails:
        print("No email addresses found.")
        return

    print(f"{len(emails)} address(es) found:")
    for email in emails:
        print(f"  {email}")

    if args.output:
        Path(args.output).write_text("\n".join(emails) + "\n", encoding="utf-8")
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
