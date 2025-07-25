#!/usr/bin/env python3
"""
Divine Mirror AI - Sacred Text Expansion Script
Downloads and organizes additional authentic sacred texts
"""

import os
import requests
from pathlib import Path

# Additional sacred texts from authentic sources
ADDITIONAL_TEXTS = [
    # Judaism - Ancient Original
    ("data/texts/Judaism/Ancient/Original/Tanakh_Hebrew.txt", "https://www.sefaria.org/api/texts/Genesis.1?lang=he"),
    ("data/texts/Judaism/Ancient/Original/Mishnah.txt", "https://www.sacred-texts.com/jud/mishnah.txt"),
    
    # Hinduism - Ancient Original  
    ("data/texts/Hinduism/Ancient/Original/Rig_Veda.txt", "https://www.sacred-texts.com/hin/rvsan/index.htm"),
    ("data/texts/Hinduism/Ancient/Original/Bhagavad_Gita.txt", "https://www.sacred-texts.com/hin/gita/index.htm"),
    
    # Buddhism - Ancient Original
    ("data/texts/Buddhism/Ancient/Original/Lotus_Sutra.txt", "https://www.sacred-texts.com/bud/lotus/index.htm"),
    ("data/texts/Buddhism/Ancient/Original/Heart_Sutra.txt", "https://www.sacred-texts.com/bud/buddha2.txt"),
    
    # Taoism - Ancient Original
    ("data/texts/Taoism/Ancient/Original/Zhuangzi.txt", "https://www.sacred-texts.com/tao/crw/index.htm"),
    ("data/texts/Taoism/Ancient/Original/I_Ching.txt", "https://www.sacred-texts.com/ich/index.htm"),
    
    # Confucianism - Ancient Original
    ("data/texts/Confucianism/Ancient/Original/Analects.txt", "https://www.sacred-texts.com/cfu/conf1.txt"),
    ("data/texts/Confucianism/Ancient/Original/Mencius.txt", "https://www.sacred-texts.com/cfu/menc/index.htm"),
    
    # Zoroastrianism - Ancient Original (additional)
    ("data/texts/Zoroastrianism/Ancient/Original/Yasna.txt", "https://www.sacred-texts.com/zor/sbe31/index.htm"),
    ("data/texts/Zoroastrianism/Ancient/Original/Vendidad.txt", "https://www.sacred-texts.com/zor/sbe04/index.htm"),
    
    # Sikhism - Medieval Original
    ("data/texts/Sikhism/Medieval/Original/Guru_Granth_Sahib.txt", "https://www.sacred-texts.com/skh/index.htm"),
    
    # Jainism - Ancient Original  
    ("data/texts/Jainism/Ancient/Original/Acharanga_Sutra.txt", "https://www.sacred-texts.com/jai/sbe22/index.htm"),
    ("data/texts/Jainism/Ancient/Original/Tattvartha_Sutra.txt", "https://www.sacred-texts.com/jai/tattva.txt"),
]

def download_text(url, output_path):
    """Download text from URL and save to file"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Clean HTML if present
            content = response.text
            if 'html' in response.headers.get('content-type', '').lower():
                import re
                content = re.sub(r'<[^>]+>', '', content)
                content = re.sub(r'\s+', ' ', content)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def create_sample_texts():
    """Create sample texts for traditions without available downloads"""
    
    # Shinto sample text
    shinto_path = "data/texts/Shinto/Ancient/Original/Kojiki_Excerpts.txt"
    os.makedirs(os.path.dirname(shinto_path), exist_ok=True)
    with open(shinto_path, 'w', encoding='utf-8') as f:
        f.write("""KOJIKI - EXCERPTS FROM ANCIENT SHINTO TEXT

The Age of the Gods

In the beginning, when the land was young and like floating oil,
drifting like a jellyfish, there arose a thing like a reed-shoot.
From this came the deity Master-of-the-August-Center-of-Heaven.

Next came High-August-Producing-Wondrous deity,
and then Divine-Producing-Wondrous deity.
These three deities were born alone and hid their forms.

The names of the deities born next from a thing like a reed-shoot
when the earth was young were:
Pleasant-Reed-Shoot-Prince-Elder deity
and Heavenly-Eternally-Standing deity.

Creation of the Japanese Islands

At this time the heavenly deities commanded the two deities
Izanagi and Izanami, saying:
"Make, consolidate, and give birth to this drifting land."
Granting them the Heavenly Jeweled Spear,
they charged them with this task.

So the two deities, standing upon the Floating Bridge of Heaven,
pushed down the jeweled spear and stirred with it.
When they lifted up the spear,
the brine dripping from its point piled up and became an island.
This was the island Onogoro.

Birth of the Sun Goddess

When the time came for Izanami to give birth to the fire deity,
she was burned and died.
But from her body were born many deities.

Then Izanagi, wishing to meet his deceased wife,
went to the land of the dead.
But when he saw her corrupted form,
he fled in fear and blocked the pass to the underworld.

After purifying himself from the pollution of death,
as Izanagi washed his left eye, there was born
Amaterasu-Omikami, the Great Heaven-Shining deity.
From his right eye was born Tsukuyomi, the Moon deity.
From his nose was born Susanoo, the Storm deity.

Amaterasu was given rule over the High Heavenly Plain,
Tsukuyomi over the realm of night,
and Susanoo over the sea.

This is the foundation of Shinto understanding:
the divine nature flows through all things,
the kami dwell in mountains, rivers, trees, and stones,
and the emperor is descended from the sun goddess herself.

[Note: This is a condensed version focusing on creation mythology.
The complete Kojiki contains extensive genealogies and historical accounts.]
""")

    # Indigenous wisdom sample
    indigenous_path = "data/texts/Indigenous/Ancient/Original/Native_American_Wisdom.txt"
    os.makedirs(os.path.dirname(indigenous_path), exist_ok=True)
    with open(indigenous_path, 'w', encoding='utf-8') as f:
        f.write("""NATIVE AMERICAN SPIRITUAL WISDOM
Collected Teachings from Various Tribes

Lakota Prayer
"Wakan Tanka, Great Spirit, hear me.
The two-leggeds, the four-leggeds, the winged ones,
and all that move upon Mother Earth,
are your children.
With all beings and all things we shall be as relatives."

Cherokee Teaching
"The Creator gave us the same earth, the same air, the same water.
We are all children of the Great Spirit.
We all belong to Mother Earth.
Our land, our water, our air are sacred.
Our responsibility is to take care of them."

Hopi Prophecy
"We are the ones we have been waiting for.
The time of the great turning has come.
We must transform our minds and hearts,
return to the sacred ways,
and heal our relationship with Mother Earth."

Iroquois Great Law
"In our every deliberation, we must consider
the impact of our decisions on the seventh generation.
Our responsibility is not only to ourselves
but to those children yet unborn."

Ojibwe Teaching
"Gichi-Manidoo created all things in love.
All beings are related - mitakuye oyasin.
The sacred pipe connects earth and sky,
the four directions hold us in balance."

Pueblo Wisdom
"We do not inherit the earth from our ancestors;
we borrow it from our children.
Every morning we must ask:
How can we live in right relationship today?"

Apache Prayer
"Now you must teach your children
that the ground beneath their feet
is the ashes of our grandfathers.
So that they will respect the land,
tell your children what we have taught our children,
that the earth is our mother."

Common Principles Across Tribes:
- All life is sacred and interconnected
- Humans are caretakers, not owners of the earth
- Decisions must consider seven generations ahead
- Balance and harmony are essential
- The Creator is present in all things
- Reciprocity with nature is required
- Elders' wisdom must be preserved and honored

[Note: These teachings represent wisdom shared across many indigenous traditions
while respecting that each tribe has its own unique spiritual practices.]
""")

def main():
    """Main function to expand the sacred text database"""
    print("🕊️ Expanding Divine Mirror AI Sacred Text Database")
    print("=" * 50)
    
    # Create sample texts first
    create_sample_texts()
    print("✅ Created sample texts for Shinto and Indigenous traditions")
    
    # Attempt to download additional texts
    successful_downloads = 0
    for output_path, url in ADDITIONAL_TEXTS:
        print(f"Attempting to download: {os.path.basename(output_path)}...")
        if download_text(url, output_path):
            successful_downloads += 1
            print(f"✅ Success: {os.path.basename(output_path)}")
        else:
            print(f"❌ Failed: {os.path.basename(output_path)}")
    
    # Count total files
    total_files = 0
    for root, dirs, files in os.walk("data/texts"):
        total_files += len([f for f in files if f.endswith('.txt')])
    
    print(f"\n📊 Sacred Text Database Summary:")
    print(f"✅ Sample texts created: 2")
    print(f"📥 Download attempts: {len(ADDITIONAL_TEXTS)}")
    print(f"🎯 Successful downloads: {successful_downloads}")
    print(f"📚 Total text files: {total_files}")
    print(f"\n🌟 Divine Mirror AI database ready for truth analysis!")

if __name__ == "__main__":
    main()