#!/usr/bin/env python3
"""
Script to update gallery HTML files to use thumbnail images for display
while keeping high-resolution images for the lightbox.
"""

import re
from pathlib import Path

def update_gallery_html(file_path):
    """Update gallery HTML to use thumbnails."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to match image tags in gallery items
    # Matches: <img src="path/to/image.ext" ...>
    pattern = r'<img\s+src="(images/[^"]+\.(jpg|JPG|jpeg|JPEG|png|PNG))"([^>]*?)>'
    
    def replace_img(match):
        full_path = match.group(1)
        ext = match.group(2)
        rest_of_tag = match.group(3)
        
        # Skip if already has thumbnails in path
        if '/thumbnails/' in full_path:
            return match.group(0)
        
        # Create thumbnail path
        path_parts = full_path.rsplit('/', 1)
        if len(path_parts) == 2:
            dir_path, filename = path_parts
            # Change extension to .jpg for thumbnails
            thumb_filename = filename.rsplit('.', 1)[0] + '.jpg'
            thumb_path = f"{dir_path}/thumbnails/{thumb_filename}"
            
            # Check if data-fullres already exists
            if 'data-fullres=' not in rest_of_tag:
                # Add data-fullres and loading=lazy
                if 'loading=' not in rest_of_tag:
                    rest_of_tag += ' loading="lazy"'
                return f'<img src="{thumb_path}" data-fullres="{full_path}"{rest_of_tag}>'
        
        return match.group(0)
    
    # Replace all image tags
    content = re.sub(pattern, replace_img, content)
    
    # Write back if changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Update all gallery HTML files."""
    gallery_files = [
        'index.html',
        'lifeIsADream.html',
        'headshots.html',
        'adlad.html',
        'stupidBird.html',
        'multiself.html',
        'not-sightly.html'
    ]
    
    print("🔧 Updating gallery HTML files to use thumbnails...")
    print("=" * 60)
    
    updated = 0
    for filename in gallery_files:
        filepath = Path(filename)
        if filepath.exists():
            if update_gallery_html(filepath):
                print(f"✓ Updated {filename}")
                updated += 1
            else:
                print(f"- {filename} (no changes needed)")
        else:
            print(f"⚠ {filename} not found")
    
    print("=" * 60)
    print(f"✅ Updated {updated} files")
    print("\nYour galleries will now load much faster!")
    print("Thumbnails display in gallery, high-res loads in lightbox.")

if __name__ == "__main__":
    main()
