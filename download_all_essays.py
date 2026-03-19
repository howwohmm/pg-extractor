#!/usr/bin/env python3
import json
import requests
from bs4 import BeautifulSoup
import time
import os
import re
from urllib.parse import urljoin

def load_essays():
    """Load the essays list from JSON file"""
    with open('/Users/ohm./Desktop/ppt/paul_graham_essays_updated.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['essays']

def clean_text(text):
    """Clean and format the extracted text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove HTML entities
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#39;', "'", text)
    # Clean up line breaks
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def extract_essay_content(url, title):
    """Extract the main content from an essay URL"""
    try:
        print(f"Downloading: {title}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        # Try to find the main content - Paul Graham's essays are usually in a specific format
        content = ""
        
        # Look for common content containers
        content_selectors = [
            'body',
            '.content',
            '.post-content',
            '.entry-content',
            'main',
            'article'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                content = element.get_text()
                break
        
        if not content:
            # Fallback to body text
            content = soup.get_text()
        
        # Clean the text
        content = clean_text(content)
        
        return content
        
    except Exception as e:
        print(f"Error downloading {title}: {e}")
        return None

def create_training_data(essays, output_dir):
    """Create training data files for LLM"""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Create individual essay files
    successful_downloads = 0
    failed_downloads = []
    
    for essay in essays:
        title = essay['title']
        url = essay['url']
        filename = essay['filename'].replace('.html', '.txt')
        
        # Sanitize filename
        filename = re.sub(r'[^\w\s.-]', '', filename)
        
        content = extract_essay_content(url, title)
        
        if content and len(content) > 100:  # Only save if we got substantial content
            filepath = os.path.join(output_dir, filename)
            
            # Create a formatted text file with metadata
            formatted_content = f"""Title: {title}
URL: {url}
Filename: {essay['filename']}

{'='*80}

{content}
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            successful_downloads += 1
            print(f"✓ Saved: {filename}")
            
        else:
            failed_downloads.append(title)
            print(f"✗ Failed: {title}")
        
        # Be respectful to the server
        time.sleep(1)
    
    return successful_downloads, failed_downloads

def create_combined_training_file(essays, output_dir):
    """Create a single combined file for training"""
    combined_file = os.path.join(output_dir, 'paul_graham_essays_combined.txt')
    
    with open(combined_file, 'w', encoding='utf-8') as f:
        f.write("Paul Graham Essays - Complete Collection\n")
        f.write("=" * 80 + "\n\n")
        
        for essay in essays:
            title = essay['title']
            url = essay['url']
            
            print(f"Adding to combined file: {title}")
            content = extract_essay_content(url, title)
            
            if content and len(content) > 100:
                f.write(f"ESSAY: {title}\n")
                f.write(f"URL: {url}\n")
                f.write("-" * 80 + "\n\n")
                f.write(content)
                f.write("\n\n" + "=" * 80 + "\n\n")
            
            time.sleep(0.5)  # Small delay between requests
    
    print(f"Combined file created: {combined_file}")

def create_json_training_data(essays, output_dir):
    """Create JSON format training data"""
    json_file = os.path.join(output_dir, 'paul_graham_essays.jsonl')
    
    with open(json_file, 'w', encoding='utf-8') as f:
        for essay in essays:
            title = essay['title']
            url = essay['url']
            
            print(f"Adding to JSONL: {title}")
            content = extract_essay_content(url, title)
            
            if content and len(content) > 100:
                # Create JSONL entry
                entry = {
                    "text": content,
                    "meta": {
                        "title": title,
                        "url": url,
                        "author": "Paul Graham",
                        "source": "paulgraham.com"
                    }
                }
                
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
            time.sleep(0.5)
    
    print(f"JSONL training file created: {json_file}")

def main():
    print("Loading essays list...")
    essays = load_essays()
    print(f"Found {len(essays)} essays to download")
    
    output_dir = '/Users/ohm./Desktop/ppt/paul_graham_essays_text'
    
    print(f"\nDownloading essays to: {output_dir}")
    print("This may take a while...\n")
    
    # Download individual files
    successful, failed = create_training_data(essays, output_dir)
    
    print(f"\nDownload Summary:")
    print(f"✓ Successfully downloaded: {successful}")
    print(f"✗ Failed downloads: {len(failed)}")
    
    if failed:
        print("\nFailed essays:")
        for title in failed[:10]:  # Show first 10 failures
            print(f"  - {title}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more")
    
    # Create combined training files
    print(f"\nCreating combined training files...")
    create_combined_training_file(essays, output_dir)
    create_json_training_data(essays, output_dir)
    
    print(f"\nAll done! Training data saved in: {output_dir}")
    print("Files created:")
    print("  - Individual essay files (.txt)")
    print("  - paul_graham_essays_combined.txt (single file)")
    print("  - paul_graham_essays.jsonl (JSONL format for training)")

if __name__ == "__main__":
    main()
