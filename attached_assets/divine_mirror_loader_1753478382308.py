
import os
import requests

# Define the download targets: (filename, URL)
downloads = [
    ("King James Version (KJV).txt", "https://www.gutenberg.org/cache/epub/10/pg10.txt"),
    ("Young's Literal Translation (YLT).txt", "https://www.gutenberg.org/cache/epub/8210/pg8210.txt"),
    ("Book of Enoch.txt", "https://www.sacred-texts.com/bib/boe/boe.txt"),
    ("Tao Te Ching.txt", "https://www.sacred-texts.com/tao/taote.txt"),
    ("Quran (Yusuf Ali).txt", "https://www.sacred-texts.com/isl/yusufali.txt"),
    ("Quran (Pickthall).txt", "https://www.sacred-texts.com/isl/pick.txt"),
    ("Gospel of Thomas.txt", "https://www.gnosis.org/naghamm/gosthom.html"),
    ("Dhammapada.txt", "https://www.sacred-texts.com/bud/ptf/dhp0001.htm"),
    ("Avesta.txt", "https://www.sacred-texts.com/zor/sbe04/index.htm")
]

# Define output folder
output_folder = "data/texts/Imported/Downloads"
os.makedirs(output_folder, exist_ok=True)

# Function to clean basic HTML if needed
def strip_html(text):
    import re
    return re.sub('<[^<]+?>', '', text)

# Download and save files
for name, url in downloads:
    try:
        print(f"Downloading {name}...")
        response = requests.get(url)
        content = response.text
        if "html" in response.headers.get("Content-Type", ""):
            content = strip_html(content)
        with open(os.path.join(output_folder, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
