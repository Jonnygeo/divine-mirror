import os
import requests
import re

BASE_DIR = "data/texts"
DEFINITIONS = {
    "Christianity/Ancient/Original": {
        "KJV": "https://www.gutenberg.org/cache/epub/10/pg10.txt",
        "YLT": "https://www.gutenberg.org/cache/epub/11031/pg11031.txt",
        "Septuagint": "https://www.sacred-texts.com/bib/sep/sep01.htm"
    },
    "Christianity/Non-Canonical/Original": {
        "Book_of_Enoch": "https://www.sacred-texts.com/bib/boe/boe.txt",
        "Nag_Hammadi_Library": "https://www.sacred-texts.com/gnosis/nhl/index.htm"
    },
    "Judaism/Ancient/Original": {
        "DeadSeaScrolls": "https://www.sacred-texts.com/bib/dss/index.htm",
        "Masoretic_Text": "https://www.sacred-texts.com/bib/jps/index.htm"
    },
    "Islam/Ancient/Original": {
        "Quran_Yusuf_Ali": "https://www.sacred-texts.com/isl/quran/yusufali/index.htm",
        "Quran_Pickthall": "https://www.sacred-texts.com/isl/quran/pickthall/index.htm"
    },
    "Buddhism/Ancient/Original": {
        "Dhammapada": "https://www.sacred-texts.com/bud/sbe10/index.htm"
    },
    "Hinduism/Ancient/Original": {
        "Upanishads": "https://www.sacred-texts.com/hin/upanindex.htm"
    },
    "Taoism/Ancient/Original": {
        "Tao_Te_Ching": "https://www.sacred-texts.com/tao/taote.htm"
    },
    "Zoroastrianism/Ancient/Original": {
        "Avesta": "https://www.sacred-texts.com/zor/sbe04/index.htm"
    }
}

def make_dirs(path):
    os.makedirs(path, exist_ok=True)

def clean_html(html):
    text = re.sub(r'<[^>]+>', '', html)
    return text

def download_text(url, dest):
    try:
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            content = r.text
            if '<html' in content.lower():
                content = clean_html(content)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content)
            print("Saved:", dest)
        else:
            print("Failed:", url, r.status_code)
    except Exception as e:
        print("Error:", url, str(e))

def run_loader():
    for rel_path, books in DEFINITIONS.items():
        base = os.path.join(BASE_DIR, rel_path)
        make_dirs(base)
        for name, url in books.items():
            fname = f"{name}.txt"
            dest = os.path.join(base, fname)
            download_text(url, dest)

if __name__ == "__main__":
    run_loader()