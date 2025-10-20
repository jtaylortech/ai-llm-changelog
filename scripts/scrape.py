#!/usr/bin/env python3
"""
AI Model Update Scraper
Scrapes Anthropic, OpenAI, and Google for model updates and changelogs
Outputs raw diffs to /raw/ directory for manual AI-assisted summarization
"""

import sys
import os
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
import gzip

try:
    from bs4 import BeautifulSoup
    import feedparser
except ImportError:
    print("Error: Required dependencies not installed.", file=sys.stderr)
    print("Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

def fetch_url(url, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'):
    """Fetch URL content with proper headers"""
    try:
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        req = Request(url, headers=headers)
        with urlopen(req, timeout=15) as response:
            data = response.read()
            # Handle gzip compression
            if response.headers.get('Content-Encoding') == 'gzip':
                data = gzip.decompress(data)
            return data.decode('utf-8')
    except (URLError, HTTPError) as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def parse_html_text(html, selector=None, limit=10):
    """Extract readable text from HTML"""
    if not html:
        return None

    soup = BeautifulSoup(html, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()

    # Get text
    text = soup.get_text(separator='\n', strip=True)
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Return first N meaningful lines
    return '\n'.join(lines[:limit]) if limit else '\n'.join(lines)

def fetch_rss(url):
    """Fetch and parse RSS/Atom feed"""
    try:
        feed = feedparser.parse(url)
        if not feed.entries:
            return None

        items = []
        for entry in feed.entries[:5]:  # Get latest 5 entries
            items.append({
                'title': entry.get('title', 'No title'),
                'link': entry.get('link', ''),
                'published': entry.get('published', entry.get('updated', 'Unknown date')),
                'summary': entry.get('summary', entry.get('description', ''))[:200]
            })
        return items
    except Exception as e:
        print(f"Error parsing RSS {url}: {e}", file=sys.stderr)
        return None

def scrape_anthropic():
    """Scrape Anthropic changelog and news"""
    print("Scraping Anthropic...")

    results = {
        'provider': 'Anthropic',
        'timestamp': datetime.now().isoformat(),
        'sources': []
    }

    # Anthropic Release Notes (changelog moved)
    changelog_url = 'https://docs.anthropic.com/en/release-notes'
    changelog_html = fetch_url(changelog_url)
    if changelog_html:
        parsed_text = parse_html_text(changelog_html, limit=50)
        results['sources'].append({
            'name': 'Release Notes',
            'url': changelog_url,
            'content_length': len(changelog_html),
            'parsed_content': parsed_text,
            'preview': parsed_text[:1000] if parsed_text else 'No content extracted'
        })

    # Anthropic News
    news_url = 'https://www.anthropic.com/news'
    news_html = fetch_url(news_url)
    if news_html:
        parsed_text = parse_html_text(news_html, limit=30)
        results['sources'].append({
            'name': 'News',
            'url': news_url,
            'content_length': len(news_html),
            'parsed_content': parsed_text,
            'preview': parsed_text[:1000] if parsed_text else 'No content extracted'
        })

    return results

def scrape_openai():
    """Scrape OpenAI changelog and research blog

    Note: OpenAI has strong bot detection. Using RSS feeds as workaround.
    """
    print("Scraping OpenAI...")

    results = {
        'provider': 'OpenAI',
        'timestamp': datetime.now().isoformat(),
        'sources': []
    }

    # Try RSS feed for OpenAI blog (workaround for 403 errors)
    rss_url = 'https://openai.com/blog/rss.xml'
    rss_items = fetch_rss(rss_url)
    if rss_items:
        feed_text = '\n\n'.join([
            f"[{item['published']}] {item['title']}\n{item['summary']}\nLink: {item['link']}"
            for item in rss_items
        ])
        results['sources'].append({
            'name': 'Blog RSS',
            'url': rss_url,
            'parsed_content': feed_text,
            'preview': feed_text[:1000],
            'item_count': len(rss_items)
        })

    # Fallback: Try HTML changelog (may be blocked)
    changelog_url = 'https://platform.openai.com/docs/changelog'
    changelog_html = fetch_url(changelog_url)
    if changelog_html:
        parsed_text = parse_html_text(changelog_html, limit=50)
        results['sources'].append({
            'name': 'API Changelog',
            'url': changelog_url,
            'content_length': len(changelog_html),
            'parsed_content': parsed_text,
            'preview': parsed_text[:1000] if parsed_text else 'No content extracted'
        })

    return results

def scrape_google():
    """Scrape Google AI blog and Vertex AI release notes"""
    print("Scraping Google...")

    results = {
        'provider': 'Google',
        'timestamp': datetime.now().isoformat(),
        'sources': []
    }

    # Google AI Blog RSS
    rss_url = 'https://blog.google/technology/ai/rss/'
    rss_items = fetch_rss(rss_url)
    if rss_items:
        feed_text = '\n\n'.join([
            f"[{item['published']}] {item['title']}\n{item['summary']}\nLink: {item['link']}"
            for item in rss_items
        ])
        results['sources'].append({
            'name': 'AI Blog RSS',
            'url': rss_url,
            'parsed_content': feed_text,
            'preview': feed_text[:1000],
            'item_count': len(rss_items)
        })

    # Vertex AI Release Notes
    vertex_url = 'https://cloud.google.com/vertex-ai/docs/release-notes'
    vertex_html = fetch_url(vertex_url)
    if vertex_html:
        parsed_text = parse_html_text(vertex_html, limit=50)
        results['sources'].append({
            'name': 'Vertex AI Release Notes',
            'url': vertex_url,
            'content_length': len(vertex_html),
            'parsed_content': parsed_text,
            'preview': parsed_text[:1000] if parsed_text else 'No content extracted'
        })

    return results

def compare_with_previous(current_data, provider_name):
    """Compare current scrape with previous scrape to detect changes"""
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'raw')
    os.makedirs(raw_dir, exist_ok=True)

    # Find most recent previous file for this provider
    previous_file = None
    previous_data = None

    if os.path.exists(raw_dir):
        files = sorted([f for f in os.listdir(raw_dir) if f.endswith('.json') and provider_name.lower() in f.lower()])
        if files:
            previous_file = os.path.join(raw_dir, files[-1])
            try:
                with open(previous_file, 'r') as f:
                    previous_data = json.load(f)
            except:
                pass

    # Simple diff: compare content lengths, item counts, or parsed content
    changes = []
    if previous_data:
        for curr_source in current_data.get('sources', []):
            prev_source = next((s for s in previous_data.get('sources', []) if s['name'] == curr_source['name']), None)
            if not prev_source:
                changes.append(f"NEW SOURCE: {curr_source['name']}")
            else:
                # Compare RSS feed items
                if 'item_count' in curr_source:
                    if curr_source.get('item_count') != prev_source.get('item_count'):
                        changes.append(f"CHANGED: {curr_source['name']} (RSS items updated)")
                # Compare HTML content length
                elif 'content_length' in curr_source:
                    if curr_source['content_length'] != prev_source.get('content_length', 0):
                        diff = curr_source['content_length'] - prev_source.get('content_length', 0)
                        changes.append(f"CHANGED: {curr_source['name']} ({diff:+d} chars)")
    else:
        changes.append("FIRST RUN - No previous data to compare")

    return changes

def save_results(all_results):
    """Save scraping results to raw directory"""
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'raw')
    os.makedirs(raw_dir, exist_ok=True)

    date_str = datetime.now().strftime('%Y-%m-%d')

    # Save detailed JSON for each provider
    for result in all_results:
        provider = result['provider'].lower()
        json_file = os.path.join(raw_dir, f'{date_str}-{provider}.json')
        with open(json_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Saved: {json_file}")

    # Save human-readable summary for AI-assisted review
    summary_file = os.path.join(raw_dir, f'{date_str}-summary.txt')
    with open(summary_file, 'w') as f:
        f.write(f"AI Model Update Scrape - {date_str}\n")
        f.write("=" * 60 + "\n\n")

        for result in all_results:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"PROVIDER: {result['provider']}\n")
            f.write(f"{'=' * 60}\n\n")

            # Detect changes
            changes = compare_with_previous(result, result['provider'])
            f.write("CHANGES DETECTED:\n")
            for change in changes:
                f.write(f"  - {change}\n")
            f.write("\n")

            # Write source content
            for source in result.get('sources', []):
                f.write(f"\nSOURCE: {source['name']}\n")
                f.write(f"URL: {source['url']}\n")

                # Handle RSS feeds differently
                if 'item_count' in source:
                    f.write(f"Items: {source['item_count']}\n")
                elif 'content_length' in source:
                    f.write(f"Size: {source['content_length']} chars\n")

                f.write(f"\nContent:\n{'-' * 60}\n")

                # Use parsed_content if available, otherwise fall back to preview
                content = source.get('parsed_content', source.get('preview', 'No content'))
                f.write(f"{content}\n")
                f.write(f"{'-' * 60}\n\n")

    print(f"\nSummary saved: {summary_file}")
    print(f"\nNext steps:")
    print(f"1. Review {summary_file}")
    print(f"2. Paste relevant sections into your AI assistant")
    print(f"3. Ask for a summary of the changes")
    print(f"4. Commit summary to /updates/")

def main():
    print("AI Model Update Scraper")
    print("=" * 60)
    print()

    all_results = []

    # Scrape all providers
    all_results.append(scrape_anthropic())
    all_results.append(scrape_openai())
    all_results.append(scrape_google())

    # Save results
    save_results(all_results)

    print("\nScraping complete!")

if __name__ == '__main__':
    main()
