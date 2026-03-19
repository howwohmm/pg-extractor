#!/usr/bin/env python3
import json
import requests
from bs4 import BeautifulSoup
import re

def load_current_essays():
    """Load the current essays from JSON file"""
    with open('/Users/ohm./Desktop/ppt/paul_graham_essays.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_missing_essays():
    """List of missing essays with their likely URLs"""
    missing_essays = [
        {"title": "The Shape of the Essay Field", "url": "https://paulgraham.com/shape.html"},
        {"title": "Good Writing", "url": "https://paulgraham.com/goodwriting.html"},
        {"title": "What to Do", "url": "https://paulgraham.com/todo.html"},
        {"title": "The Origins of Wokeness", "url": "https://paulgraham.com/wokeness.html"},
        {"title": "Writes and Write-Nots", "url": "https://paulgraham.com/writes.html"},
        {"title": "When To Do What You Love", "url": "https://paulgraham.com/love.html"},
        {"title": "Founder Mode", "url": "https://paulgraham.com/foundermode.html"},
        {"title": "The Right Kind of Stubborn", "url": "https://paulgraham.com/stubborn.html"},
        {"title": "The Reddits", "url": "https://paulgraham.com/reddits.html"},
        {"title": "How to Start Google", "url": "https://paulgraham.com/google.html"},
        {"title": "The Best Essay", "url": "https://paulgraham.com/best.html"},
        {"title": "Can You Buy a Silicon Valley? Maybe", "url": "https://paulgraham.com/maybe.html"},
        {"title": "Writing, Briefly", "url": "https://paulgraham.com/writing44.html"}
    ]
    return missing_essays

def verify_essay_exists(url):
    """Check if an essay URL exists"""
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def find_essay_links_from_main_page():
    """Scrape the main page for essay links"""
    try:
        response = requests.get("https://paulgraham.com/", timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and href.endswith('.html') and 'paulgraham.com' in href:
                    title = link.get_text().strip()
                    if title and not title.lower().startswith('http'):
                        full_url = href if href.startswith('http') else f"https://paulgraham.com/{href}"
                        links.append({"title": title, "url": full_url})
            return links
    except Exception as e:
        print(f"Error scraping main page: {e}")
    return []

def update_json_with_missing():
    """Update the JSON file with missing essays"""
    data = load_current_essays()
    missing_essays = get_missing_essays()
    
    # Also try to find essays from main page
    main_page_essays = find_essay_links_from_main_page()
    print(f"Found {len(main_page_essays)} essays on main page")
    
    # Combine missing essays with main page essays
    all_potential = missing_essays + main_page_essays
    
    existing_titles = {essay['title'] for essay in data['essays']}
    added_count = 0
    
    for essay in all_potential:
        if essay['title'] not in existing_titles:
            if verify_essay_exists(essay['url']):
                # Extract filename from URL
                filename = essay['url'].split('/')[-1]
                new_essay = {
                    'title': essay['title'],
                    'url': essay['url'],
                    'filename': filename
                }
                data['essays'].append(new_essay)
                existing_titles.add(essay['title'])
                added_count += 1
                print(f"Added: {essay['title']}")
            else:
                print(f"Not found: {essay['title']} - {essay['url']}")
    
    # Update total count
    data['total_essays'] = len(data['essays'])
    
    # Sort essays by title
    data['essays'].sort(key=lambda x: x['title'])
    
    # Save updated JSON
    with open('/Users/ohm./Desktop/ppt/paul_graham_essays_updated.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nAdded {added_count} new essays")
    print(f"Total essays now: {data['total_essays']}")
    print(f"Saved to: paul_graham_essays_updated.json")

if __name__ == "__main__":
    update_json_with_missing()
