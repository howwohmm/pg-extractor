#!/usr/bin/env python3
import json
import os
import re
import glob

def load_essays():
    """Load the essays list from JSON file"""
    with open('/Users/ohm./Desktop/ppt/paul_graham_essays_updated.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['essays']

def sanitize_filename(title):
    """Convert title to a valid filename"""
    # Remove or replace invalid characters
    filename = title.lower()
    
    # Replace special characters with underscores or remove them
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    
    # Remove leading/trailing underscores
    filename = filename.strip('_')
    
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename + '.txt'

def rename_files():
    """Rename files to match their actual titles"""
    essays_dir = '/Users/ohm./Desktop/ppt/paul_graham_essays_text'
    essays = load_essays()
    
    # Create mapping from old filename to new filename
    rename_map = {}
    
    for essay in essays:
        old_filename = essay['filename'].replace('.html', '.txt')
        title = essay['title']
        new_filename = sanitize_filename(title)
        
        # Find the actual file (it might have slightly different name)
        old_path = None
        for file in glob.glob(os.path.join(essays_dir, '*.txt')):
            basename = os.path.basename(file)
            if basename.startswith(old_filename.split('.')[0]) or basename == old_filename:
                old_path = file
                break
        
        if old_path and os.path.exists(old_path):
            new_path = os.path.join(essays_dir, new_filename)
            
            # Avoid overwriting existing files
            counter = 1
            while os.path.exists(new_path):
                name_part = new_filename.rsplit('.', 1)[0]
                new_path = os.path.join(essays_dir, f"{name_part}_{counter}.txt")
                counter += 1
            
            rename_map[old_path] = {
                'new_path': new_path,
                'title': title,
                'old_name': os.path.basename(old_path),
                'new_name': os.path.basename(new_path)
            }
        else:
            print(f"File not found for: {title} ({old_filename})")
    
    # Perform the renaming
    renamed_count = 0
    for old_path, info in rename_map.items():
        try:
            os.rename(old_path, info['new_path'])
            print(f"Renamed: {info['old_name']} -> {info['new_name']}")
            print(f"  Title: {info['title']}")
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")
    
    return renamed_count

def create_unified_file():
    """Create a unified file with all essays"""
    essays_dir = '/Users/ohm./Desktop/ppt/paul_graham_essays_text'
    essays = load_essays()
    
    unified_file = os.path.join(essays_dir, 'paul_graham_unified_essays.txt')
    
    with open(unified_file, 'w', encoding='utf-8') as outfile:
        outfile.write("PAUL GRAHAM - COMPLETE ESSAYS COLLECTION\n")
        outfile.write("=" * 100 + "\n\n")
        
        for essay in essays:
            title = essay['title']
            url = essay['url']
            
            # Find the renamed file
            expected_filename = sanitize_filename(title)
            essay_path = os.path.join(essays_dir, expected_filename)
            
            # If exact match not found, try to find similar
            if not os.path.exists(essay_path):
                # Try to find any file that contains the title
                found = False
                for file in glob.glob(os.path.join(essays_dir, '*.txt')):
                    if 'unified' not in file and 'combined' not in file and 'jsonl' not in file:
                        with open(file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if title in content.split('\n')[0:5]:  # Check first few lines
                                essay_path = file
                                found = True
                                break
                
                if not found:
                    print(f"Could not find file for: {title}")
                    continue
            
            # Read and add essay content
            try:
                with open(essay_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                
                # Extract just the essay content (after metadata)
                parts = content.split('=' * 80)
                if len(parts) > 1:
                    essay_content = parts[1].strip()
                else:
                    essay_content = content.strip()
                
                outfile.write(f"ESSAY: {title}\n")
                outfile.write(f"URL: {url}\n")
                outfile.write("-" * 100 + "\n\n")
                outfile.write(essay_content)
                outfile.write("\n\n" + "=" * 100 + "\n\n")
                
                print(f"Added to unified file: {title}")
                
            except Exception as e:
                print(f"Error processing {title}: {e}")
    
    print(f"\nUnified file created: {unified_file}")
    return unified_file

def main():
    essays_dir = '/Users/ohm./Desktop/ppt/paul_graham_essays_text'
    
    print("Renaming files to match essay titles...")
    renamed_count = rename_files()
    print(f"Renamed {renamed_count} files\n")
    
    print("Creating unified file with all essays...")
    unified_path = create_unified_file()
    
    print(f"\nAll done!")
    print(f"Files renamed and unified file created at:")
    print(f"  {unified_path}")

if __name__ == "__main__":
    main()
