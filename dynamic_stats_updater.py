#!/usr/bin/env python3
"""
Dynamic Stats Updater for Divine Mirror AI
Fetches stats from backend API and updates frontend components
"""

import asyncio
import httpx
import json
import os
from typing import Dict, Any

API_BASE_URL = "http://localhost:8000"

async def fetch_backend_stats() -> Dict[str, Any]:
    """Fetch stats from backend API"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/stats", timeout=30.0)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API returned status {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching backend stats: {e}")
            return None

def update_about_section_template(stats_data: Dict[str, Any]) -> str:
    """Generate dynamic about section with live stats"""
    
    if stats_data and stats_data.get("status") == "success":
        formatted_stats = stats_data["formatted"]
        raw_stats = stats_data["data"]
    else:
        # Fallback to local stats calculator
        try:
            from stats_calculator import get_homepage_stats
            raw_stats = get_homepage_stats()
            formatted_stats = {
                "sacred_texts": f"{raw_stats['sacred_texts']:,}",
                "analyzed_documents": f"{raw_stats['analyzed_documents']:,}",
                "traditions": str(raw_stats["traditions"]),
                "semantic_tags": f"{raw_stats['semantic_tags']}+",
                "ai_phases": f"{raw_stats['ai_phases']} Complete"
            }
        except:
            formatted_stats = {
                "sacred_texts": "164",
                "analyzed_documents": "64,998",
                "traditions": "17",
                "semantic_tags": "32+",
                "ai_phases": "9 Complete"
            }
    
    about_template = f"""
    <div style="color: #9ca3af; font-size: 14px; line-height: 1.6; max-width: 900px; margin: 30px auto;">
      <h3 style="color: #60a5fa;">About Divine Mirror AI</h3>
      <p>
        This platform is the culmination of <strong>{formatted_stats['ai_phases']}</strong>, combining semantic chunking, spiritual metadata, voice recognition, and sacred symbolism analysis. 
        It's built to uncover the original teachings of Yeshua, Buddha, Lao Tzu, and others — across time, culture, and institutional filters.
      </p>
      <p>
        With <strong>{formatted_stats['sacred_texts']} documents</strong> from <strong>{formatted_stats['traditions']} traditions</strong>, mapped by <strong>{formatted_stats['semantic_tags']} semantic tags</strong>, this AI is more than an assistant. It's a truth engine.
        It works fully offline, honors user privacy, and cites real sources — no vague answers, no agenda. 
      </p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; margin: 1.5rem 0; padding: 1.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2);">
        <div style="text-align: center;">
          <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{formatted_stats['sacred_texts']}</div>
          <div style="color: #94a3b8; font-size: 0.9rem;">Sacred Texts</div>
        </div>
        <div style="text-align: center;">
          <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{formatted_stats['analyzed_documents']}</div>
          <div style="color: #94a3b8; font-size: 0.9rem;">Analyzed Documents</div>
        </div>
        <div style="text-align: center;">
          <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{formatted_stats['traditions']}</div>
          <div style="color: #94a3b8; font-size: 0.9rem;">Traditions</div>
        </div>
        <div style="text-align: center;">
          <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{formatted_stats['semantic_tags']}</div>
          <div style="color: #94a3b8; font-size: 0.9rem;">Semantic Tags</div>
        </div>
        <div style="text-align: center;">
          <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{formatted_stats['ai_phases']}</div>
          <div style="color: #94a3b8; font-size: 0.9rem;">AI Phases</div>
        </div>
      </div>
      <p><em>"Truth doesn't need to be sold — it just needs to be found."</em></p>
    </div>
    """
    
    return about_template

async def get_dynamic_stats_for_streamlit():
    """Get stats formatted for Streamlit display"""
    stats_data = await fetch_backend_stats()
    
    if stats_data and stats_data.get("status") == "success":
        return {
            "Sacred Texts": stats_data["formatted"]["sacred_texts"],
            "Analyzed Documents": stats_data["formatted"]["analyzed_documents"],
            "Traditions": stats_data["formatted"]["traditions"],
            "Semantic Tags": stats_data["formatted"]["semantic_tags"],
            "AI Phases": stats_data["formatted"]["ai_phases"]
        }
    else:
        # Fallback to local calculation
        try:
            from stats_calculator import get_homepage_stats
            stats = get_homepage_stats()
            return {
                "Sacred Texts": f"{stats['sacred_texts']:,}",
                "Analyzed Documents": f"{stats['analyzed_documents']:,}",
                "Traditions": str(stats['traditions']),
                "Semantic Tags": f"{stats['semantic_tags']}+",
                "AI Phases": f"{stats['ai_phases']} Complete"
            }
        except:
            return {
                "Sacred Texts": "164",
                "Analyzed Documents": "64,998",
                "Traditions": "17",
                "Semantic Tags": "32+",
                "AI Phases": "9 Complete"
            }

def save_stats_cache(stats_data: Dict[str, Any]):
    """Save stats to cache file for quick access"""
    os.makedirs("data/metadata", exist_ok=True)
    
    with open("data/metadata/live_stats_cache.json", 'w') as f:
        json.dump(stats_data, f, indent=2)

async def main():
    """Test the dynamic stats system"""
    print("🔮 Testing Dynamic Stats System")
    print("=" * 50)
    
    # Test backend API
    stats_data = await fetch_backend_stats()
    if stats_data:
        print("✅ Backend API stats fetched successfully")
        print(json.dumps(stats_data, indent=2))
        
        # Save to cache
        save_stats_cache(stats_data)
        print("✅ Stats cached to file")
        
        # Generate about section
        about_html = update_about_section_template(stats_data)
        print("✅ Dynamic about section generated")
        
    else:
        print("❌ Backend API failed, using fallback")
        
        # Test Streamlit function
        streamlit_stats = await get_dynamic_stats_for_streamlit()
        print("✅ Streamlit fallback stats:")
        print(json.dumps(streamlit_stats, indent=2))

if __name__ == "__main__":
    asyncio.run(main())