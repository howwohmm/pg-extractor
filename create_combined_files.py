#!/usr/bin/env python3
import json
import os
import glob

def load_essays():
    """Load the essays list from JSON file"""
    with open('/Users/ohm./Desktop/ppt/paul_graham_essays_updated.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['essays']

def create_combined_file_from_individuals():
    """Create combined files from the already downloaded individual files"""
    essays_dir = '/Users/ohm./Desktop/ppt/paul_graham_essays_text'
    
    # Create combined text file
    combined_file = os.path.join(essays_dir, 'paul_graham_essays_combined.txt')
    
    with open(combined_file, 'w', encoding='utf-8') as outfile:
        outfile.write("Paul Graham Essays - Complete Collection\n")
        outfile.write("=" * 80 + "\n\n")
        
        # Get all txt files
        txt_files = glob.glob(os.path.join(essays_dir, '*.txt'))
        
        for txt_file in sorted(txt_files):
            filename = os.path.basename(txt_file)
            
            # Skip the combined file itself if it exists
            if 'combined' in filename or 'jsonl' in filename:
                continue
                
            print(f"Adding: {filename}")
            
            with open(txt_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
                outfile.write("\n\n" + "=" * 80 + "\n\n")
    
    print(f"Combined file created: {combined_file}")
    
    # Create JSONL file
    jsonl_file = os.path.join(essays_dir, 'paul_graham_essays.jsonl')
    essays = load_essays()
    
    with open(jsonl_file, 'w', encoding='utf-8') as outfile:
        for txt_file in sorted(txt_files):
            filename = os.path.basename(txt_file)
            
            # Skip the combined file itself if it exists
            if 'combined' in filename or 'jsonl' in filename:
                continue
            
            # Read the content
            with open(txt_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
            
            # Extract title from content
            title = "Unknown"
            for line in content.split('\n')[:10]:
                if line.startswith('Title: '):
                    title = line.replace('Title: ', '').strip()
                    break
            
            # Find matching essay data
            essay_data = next((e for e in essays if e['title'] == title), None)
            
            if essay_data:
                # Extract just the essay content (after the metadata)
                parts = content.split('=' * 80)
                if len(parts) > 1:
                    essay_content = '=' * 80 + '=' * 80 + parts[1]
                    essay_content = essay_content.strip()
                else:
                    essay_content = content
                
                # Create JSONL entry
                entry = {
                    "text": essay_content,
                    "meta": {
                        "title": title,
                        "url": essay_data['url'],
                        "author": "Paul Graham",
                        "source": "paulgraham.com"
                    }
                }
                
                outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')
                print(f"Added to JSONL: {title}")
    
    print(f"JSONL file created: {jsonl_file}")

def main():
    print("Creating combined training files from individual essays...")
    create_combined_file_from_individuals()
    print("\nDone! Combined training files are ready for LLM training.")

if __name__ == "__main__":
    main()
