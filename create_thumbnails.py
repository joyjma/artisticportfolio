#!/usr/bin/env python3
"""
Script to create compressed thumbnails for all gallery images.
This will create a 'thumbnails' subfolder in each image directory
and generate optimized versions of the images.
"""

import os
from pathlib import Path
from PIL import Image

# Configuration
MAX_SIZE = 800  # Maximum dimension (width or height) for thumbnails
QUALITY = 75    # JPEG quality (1-100, lower = smaller file size)

# Directories containing images
IMAGE_DIRS = [
    'images/Not Sightly',
    'images/la vida/ben rose la vida',
    'images/adlad',
    'images/Headshots',
    'images/sfb',
    'images/multiself',
    'images/videos',
    'images/la vida',
]

def create_thumbnail(source_path, dest_path, max_size=MAX_SIZE, quality=QUALITY):
    """Create a compressed thumbnail from source image."""
    try:
        # Open image
        with Image.open(source_path) as img:
            # Convert RGBA to RGB if necessary (for PNG with transparency)
            if img.mode == 'RGBA':
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate new size maintaining aspect ratio
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Save with compression
            img.save(dest_path, 'JPEG', quality=quality, optimize=True)
            
            # Get file sizes
            original_size = os.path.getsize(source_path) / 1024  # KB
            new_size = os.path.getsize(dest_path) / 1024  # KB
            reduction = ((original_size - new_size) / original_size) * 100
            
            print(f"✓ {source_path.name}")
            print(f"  {original_size:.1f}KB → {new_size:.1f}KB ({reduction:.1f}% reduction)")
            
            return True
    except Exception as e:
        print(f"✗ Error processing {source_path}: {e}")
        return False

def process_directory(dir_path):
    """Process all images in a directory."""
    dir_path = Path(dir_path)
    
    if not dir_path.exists():
        print(f"⚠ Directory not found: {dir_path}")
        return
    
    # Create thumbnails subdirectory
    thumbnails_dir = dir_path / 'thumbnails'
    thumbnails_dir.mkdir(exist_ok=True)
    
    print(f"\n📁 Processing: {dir_path}")
    print("─" * 60)
    
    # Supported image extensions
    extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    
    # Process each image
    processed = 0
    for img_path in dir_path.iterdir():
        if img_path.suffix in extensions and img_path.is_file():
            # Determine output filename (always .jpg for thumbnails)
            thumb_name = img_path.stem + '.jpg'
            thumb_path = thumbnails_dir / thumb_name
            
            if create_thumbnail(img_path, thumb_path):
                processed += 1
    
    print(f"Processed {processed} images in {dir_path.name}")

def main():
    """Main function to process all image directories."""
    print("🖼️  Creating thumbnails for gallery images...")
    print("=" * 60)
    
    total_dirs = 0
    for dir_path in IMAGE_DIRS:
        full_path = Path(dir_path)
        if full_path.exists():
            process_directory(full_path)
            total_dirs += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Complete! Processed {total_dirs} directories.")
    print("\nNext steps:")
    print("1. Check the 'thumbnails' folders in each image directory")
    print("2. The gallery pages will now load faster with compressed images")
    print("3. High-resolution images will still load in the lightbox")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
