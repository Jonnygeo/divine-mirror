#!/usr/bin/env python3
"""
Offline Search Engine for Divine Mirror AI
Provides spiritual text search without external API dependencies
"""

import json
import os
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class SearchResult:
    text: str
    source_file: str
    tradition: str
    period: str
    title: str
    relevance_score: float
    keywords: List[str]

class OfflineSearchEngine:
    def __init__(self, index_path="data/indexes/text_index.json"):
        self.index_path = index_path
        self.text_index = {}
        self.load_index()
    
    def load_index(self):
        """Load the text index"""
        try:
            if os.path.exists(self.index_path):
                with open(self.index_path, 'r') as f:
                    self.text_index = json.load(f)
                print(f"✓ Loaded {len(self.text_index)} text chunks for offline search")
            else:
                print("⚠️  No text index found. Run setup_sacred_database.py first.")
        except Exception as e:
            print(f"❌ Error loading index: {e}")
    
    def search_by_keywords(self, query: str, traditions: List[str] = None, limit: int = 10) -> List[SearchResult]:
        """Search using keyword matching"""
        if not self.text_index:
            return []
        
        query_words = set(query.lower().split())
        results = []
        
        for chunk_id, chunk_data in self.text_index.items():
            # Filter by tradition if specified
            if traditions and chunk_data['tradition'] not in traditions:
                continue
            
            # Calculate relevance score
            text_lower = chunk_data['text'].lower()
            title_lower = chunk_data['title'].lower()
            
            # Exact phrase match (highest score)
            if query.lower() in text_lower:
                score = 1.0
            else:
                # Word match scoring
                text_words = set(text_lower.split())
                matching_words = query_words.intersection(text_words)
                score = len(matching_words) / len(query_words) if query_words else 0
                
                # Boost score for title matches
                title_words = set(title_lower.split())
                title_matches = query_words.intersection(title_words)
                score += len(title_matches) * 0.2
                
                # Boost score for keyword matches
                keyword_matches = query_words.intersection(set(chunk_data.get('keywords', [])))
                score += len(keyword_matches) * 0.3
            
            if score > 0.1:  # Minimum relevance threshold
                result = SearchResult(
                    text=chunk_data['text'],
                    source_file=chunk_data['source_file'],
                    tradition=chunk_data['tradition'],
                    period=chunk_data['period'],
                    title=chunk_data['title'],
                    relevance_score=score,
                    keywords=chunk_data.get('keywords', [])
                )
                results.append(result)
        
        # Sort by relevance score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]
    
    def search_spiritual_themes(self, theme: str, traditions: List[str] = None) -> List[SearchResult]:
        """Search by spiritual themes"""
        theme_queries = {
            'kingdom_within': ['kingdom within', 'kingdom inside', 'kingdom of god within', 'inner kingdom'],
            'divine_nature': ['divine nature', 'god nature', 'divine essence', 'sacred'],
            'love_compassion': ['love', 'compassion', 'mercy', 'kindness', 'forgiveness'],
            'truth_wisdom': ['truth', 'wisdom', 'knowledge', 'understanding', 'enlightenment'],
            'spiritual_law': ['spiritual law', 'divine law', 'cosmic law', 'universal principle'],
            'prayer_meditation': ['prayer', 'meditation', 'contemplation', 'mindfulness'],
            'salvation': ['salvation', 'liberation', 'freedom', 'deliverance', 'redemption']
        }
        
        queries = theme_queries.get(theme, [theme])
        all_results = []
        
        for query in queries:
            results = self.search_by_keywords(query, traditions, limit=5)
            all_results.extend(results)
        
        # Remove duplicates and sort
        unique_results = {}
        for result in all_results:
            key = (result.text[:100], result.tradition)
            if key not in unique_results or result.relevance_score > unique_results[key].relevance_score:
                unique_results[key] = result
        
        final_results = list(unique_results.values())
        final_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return final_results[:10]
    
    def get_cross_tradition_insights(self, query: str, min_traditions: int = 2) -> Dict[str, List[SearchResult]]:
        """Get insights across multiple traditions"""
        all_results = self.search_by_keywords(query, limit=50)
        
        # Group by tradition
        by_tradition = {}
        for result in all_results:
            tradition = result.tradition
            if tradition not in by_tradition:
                by_tradition[tradition] = []
            by_tradition[tradition].append(result)
        
        # Filter to traditions with results and limit per tradition
        cross_tradition = {}
        for tradition, results in by_tradition.items():
            if len(results) > 0:
                cross_tradition[tradition] = results[:3]  # Top 3 per tradition
        
        # Only return if we have results from multiple traditions
        if len(cross_tradition) >= min_traditions:
            return cross_tradition
        return {}
    
    def search_by_tradition(self, query: str, tradition: str, limit: int = 5) -> List[SearchResult]:
        """Search within a specific tradition"""
        return self.search_by_keywords(query, [tradition], limit)
    
    def get_tradition_stats(self) -> Dict[str, int]:
        """Get statistics by tradition"""
        stats = {}
        for chunk_data in self.text_index.values():
            tradition = chunk_data['tradition']
            stats[tradition] = stats.get(tradition, 0) + 1
        return stats

# Test function
def test_search():
    """Test the search engine"""
    engine = OfflineSearchEngine()
    
    if not engine.text_index:
        print("❌ No search index available")
        return
    
    # Test searches
    test_queries = [
        "kingdom of god within",
        "love your enemies", 
        "meditation",
        "truth"
    ]
    
    print("🔍 Testing offline search engine...")
    for query in test_queries:
        results = engine.search_by_keywords(query, limit=3)
        print(f"\n📝 Query: '{query}' - {len(results)} results")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result.tradition} - {result.title} (score: {result.relevance_score:.2f})")
            print(f"     {result.text[:100]}...")
    
    # Test cross-tradition search
    cross_results = engine.get_cross_tradition_insights("kingdom")
    print(f"\n🌍 Cross-tradition search for 'kingdom': {len(cross_results)} traditions")
    for tradition, results in cross_results.items():
        print(f"  {tradition}: {len(results)} results")

if __name__ == "__main__":
    test_search()