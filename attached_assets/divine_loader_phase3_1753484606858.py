
import os
import requests

# Directory structure
BASE_DIR = "data/texts"
TRADITIONS = {
    "Christianity": {
        "Ancient": {
            "Original": {
                "KJV": "https://www.gutenberg.org/cache/epub/10/pg10.txt",
                "YLT": "https://www.gutenberg.org/cache/epub/11031/pg11031.txt",
                "Septuagint": "https://www.sacred-texts.com/bib/sep/index.htm"
            }
        }
    },
    "Judaism": {
        "Ancient": {
            "Original": {
                "DeadSeaScrolls": "https://www.sacred-texts.com/bib/dss/index.htm",
                "MasoreticText": "https://www.sacred-texts.com/bib/jps/index.htm"
            }
        }
    },
    "Islam": {
        "Ancient": {
            "Original": {
                "QuranYusufAli": "https://www.sacred-texts.com/isl/quran/yusufali/index.htm",
                "QuranPickthall": "https://www.sacred-texts.com/isl/quran/pickthall/index.htm"
            }
        }
    },
    "Buddhism": {
        "Ancient": {
            "Original": {
                "Dhammapada": "https://www.sacred-texts.com/bud/sbe10/index.htm"
            }
        }
    },
    "Hinduism": {
        "Ancient": {
            "Original": {
                "Upanishads": "https://www.sacred-texts.com/hin/index.htm"
            }
        }
    },
    "Taoism": {
        "Ancient": {
            "Original": {
                "TaoTeChing": "https://www.sacred-texts.com/tao/taote.htm"
            }
        }
    },
    "Zoroastrianism": {
        "Ancient": {
            "Original": {
                "Avesta": "https://www.sacred-texts.com/zor/index.htm"
            }
        }
    }
}

def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_text(url, path):
    try:
        if "gutenberg" in url:
            response = requests.get(url)
            if response.status_code == 200:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print(f"Downloaded {path}")
        else:
            with open(path, "w") as f:
                f.write(f"Manual download may be required for {url}")
            print(f"URL noted (manual): {url}")
    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")

def run_loader():
    for tradition, periods in TRADITIONS.items():
        for period, types in periods.items():
            for text_type, books in types.items():
                for book_name, url in books.items():
                    dir_path = os.path.join(BASE_DIR, tradition, period, text_type)
                    make_dirs(dir_path)
                    file_path = os.path.join(dir_path, f"{book_name}.txt")
                    download_text(url, file_path)

if __name__ == "__main__":
    run_loader()
