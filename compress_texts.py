#!/usr/bin/env python3
"""
Divine Mirror AI Text Compression Script
Compresses the sacred texts database for distribution and backup
"""
import os
import zipfile
from pathlib import Path

def compress_texts():
    """Compress all texts in the Divine Mirror AI database"""
    
    # Define source and output paths
    source_dir = "data/texts"
    output_file = "DivineMirror_Filled_Texts.zip"
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"❌ Source directory '{source_dir}' not found")
        return False
    
    print(f"🗜️ Compressing Divine Mirror AI sacred texts database...")
    print(f"📁 Source: {source_dir}")
    print(f"📦 Output: {output_file}")
    
    # Create zip file
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        total_size = 0
        
        # Walk through all files in the texts directory
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.txt'):  # Only include text files
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, start='.')
                    
                    # Add file to zip
                    zipf.write(file_path, arc_path)
                    file_count += 1
                    total_size += os.path.getsize(file_path)
                    
                    # Show progress
                    tradition = root.split(os.sep)[2] if len(root.split(os.sep)) > 2 else "Unknown"
                    print(f"  ✅ Added: {file} ({tradition})")
    
    # Show completion stats
    compressed_size = os.path.getsize(output_file)
    compression_ratio = (1 - compressed_size / total_size) * 100 if total_size > 0 else 0
    
    print(f"\n🎉 Compression Complete!")
    print(f"📊 Files processed: {file_count}")
    print(f"📏 Original size: {total_size / (1024*1024):.2f} MB")
    print(f"📦 Compressed size: {compressed_size / (1024*1024):.2f} MB")
    print(f"🗜️ Compression ratio: {compression_ratio:.1f}%")
    print(f"💾 Output file: {output_file}")
    
    return True

def list_database_contents():
    """List all texts in the database by tradition"""
    print("\n📚 Divine Mirror AI Database Contents:")
    
    traditions = {}
    total_files = 0
    
    for root, dirs, files in os.walk("data/texts"):
        for file in files:
            if file.endswith('.txt'):
                path_parts = root.split(os.sep)
                if len(path_parts) >= 3:
                    tradition = path_parts[2]
                    if tradition not in traditions:
                        traditions[tradition] = []
                    traditions[tradition].append(file)
                    total_files += 1
    
    for tradition, files in sorted(traditions.items()):
        print(f"\n📖 {tradition} ({len(files)} texts):")
        for file in sorted(files)[:5]:  # Show first 5 files
            print(f"  • {file}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")
    
    print(f"\n🔢 Total: {total_files} sacred texts across {len(traditions)} traditions")

if __name__ == "__main__":
    print("🕊️ Divine Mirror AI - Sacred Text Compression Tool")
    print("=" * 50)
    
    # List current database contents
    list_database_contents()
    
    # Compress the database
    success = compress_texts()
    
    if success:
        print("\n✨ Ready for distribution and backup!")
        print("🎯 Use this compressed database to:")
        print("  • Share with other researchers")
        print("  • Backup your sacred text collection")  
        print("  • Deploy to other Divine Mirror AI instances")
    else:
        print("\n❌ Compression failed")