
import os
import shutil
import json
from pathlib import Path

def delete_vector_db(db_path="db/chroma"):
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
        print(f"✅ Deleted old vector DB at: {db_path}")
    else:
        print(f"⚠️ Vector DB path not found: {db_path}")

def scan_sacred_texts(base_path="data/texts"):
    sacred_text_count = 0
    traditions = set()
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith((".txt", ".md", ".json")):
                sacred_text_count += 1
        for d in dirs:
            traditions.add(d)
    return sacred_text_count, len(traditions)

def write_metadata(counts, output_file="sacred_counts.json"):
    data = {
        "sacred_texts": counts[0],
        "traditions": counts[1]
    }
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
    print(f"📦 Saved metadata to {output_file}")

def main():
    delete_vector_db()
    print("🔁 Ready to re-ingest texts manually after this step.")
    counts = scan_sacred_texts()
    write_metadata(counts)

if __name__ == "__main__":
    main()
