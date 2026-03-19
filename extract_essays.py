#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import requests
from urllib.parse import urlparse
import os
import time

def extract_essays_from_rss(rss_url):
    """Extract essays from RSS feed and return as list of dictionaries"""
    
    # Fetch RSS content
    response = requests.get(rss_url)
    response.raise_for_status()
    
    # Parse XML
    root = ET.fromstring(response.text)
    
    # Define namespace
    namespaces = {
        'rss': 'http://www.w3.org/2005/Atom',
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }
    
    essays = []
    
    # Find all items
    items = root.findall('.//item')
    
    for item in items:
        title_elem = item.find('title')
        link_elem = item.find('link')
        
        if title_elem is not None and link_elem is not None:
            essay = {
                'title': title_elem.text.strip(),
                'url': link_elem.text.strip(),
                'filename': extract_filename_from_url(link_elem.text.strip())
            }
            essays.append(essay)
    
    return essays

def extract_filename_from_url(url):
    """Extract filename from URL"""
    parsed = urlparse(url)
    path = parsed.path
    filename = os.path.basename(path)
    
    # Handle special cases for URLs that don't end with .html
    if not filename or '.' not in filename:
        # Extract the last part of the path
        parts = path.strip('/').split('/')
        if parts:
            filename = parts[-1] + '.html'
        else:
            filename = 'essay.html'
    
    return filename

def save_essays_to_json(essays, output_file):
    """Save essays list to JSON file"""
    data = {
        'source': 'http://www.aaronsw.com/2002/feeds/pgessays.rss',
        'description': 'Paul Graham Essays RSS Feed',
        'total_essays': len(essays),
        'essays': essays
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(essays)} essays to {output_file}")

def main():
    rss_url = 'http://www.aaronsw.com/2002/feeds/pgessays.rss'
    output_file = '/Users/ohm./Desktop/ppt/paul_graham_essays.json'
    
    print("Extracting essays from RSS feed...")
    essays = extract_essays_from_rss(rss_url)
    
    print(f"Found {len(essays)} essays")
    
    # Save to JSON
    save_essays_to_json(essays, output_file)
    
    # Display first few essays as preview
    print("\nFirst 5 essays:")
    for i, essay in enumerate(essays[:5]):
        print(f"{i+1}. {essay['title']} - {essay['url']}")

if __name__ == "__main__":
    main()
