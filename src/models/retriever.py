"""
Retrieve relevant chunks from FAISS index
"""

import faiss
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer


class BenefitRetriever:
    """Search through insurance benefits using semantic similarity"""
    
    def __init__(self, index_dir: str = "data/index"):
        """
        Load the search index and model
        
        Args:
            index_dir: Directory containing saved index files
        """
        self.index_dir = Path(index_dir)
        
        # Check if index exists
        if not self.index_dir.exists():
            raise FileNotFoundError(
                f"Index directory not found: {index_dir}\n"
                "Please run embedding_generator.py first!"
            )
        
        print("🔍 Loading retrieval system...")
        
        # Load FAISS index
        print("   Loading FAISS index...")
        self.index = faiss.read_index(str(self.index_dir / "benefits.index"))
        
        # Load chunks
        print("   Loading chunks...")
        with open(self.index_dir / "chunks.pkl", 'rb') as f:
            self.chunks = pickle.load(f)
        
        # Load embedding model (same one used to create embeddings)
        print("   Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        print(f"✅ Retriever ready! Indexed {len(self.chunks)} chunks\n")
    
    def search(self, query: str, top_k: int = 5, 
               plan_filter: str = None, category_filter: str = None) -> List[Dict]:
        """
        Search for relevant chunks
        
        Args:
            query: User's question (e.g., "Does this cover gym membership?")
            top_k: How many results to return
            plan_filter: Optional - only search specific plan
            category_filter: Optional - only search specific category
        
        Returns:
            List of relevant chunks with similarity scores
        """
        # Convert query to embedding
        query_embedding = self.model.encode(
            [query], 
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        
        # Search FAISS index
        # Returns: distances (similarity scores) and indices (chunk IDs)
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            min(top_k * 3, len(self.chunks))  # Get more, then filter
        )
        
        # Collect results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx == -1:  # FAISS returns -1 for empty results
                continue
            
            chunk = self.chunks[idx].copy()
            
            # Apply filters
            if plan_filter and chunk.get('plan_name') != plan_filter:
                continue
            
            if category_filter and chunk.get('category') != category_filter:
                continue
            
            # Add search metadata
            chunk['similarity_score'] = float(1 - distance)  # Convert distance to similarity
            chunk['rank'] = i + 1
            chunk['chunk_id'] = int(idx)
            
            results.append(chunk)
            
            # Stop when we have enough results
            if len(results) >= top_k:
                break
        
        return results
    
    def search_with_context(self, query: str, top_k: int = 5) -> Dict:
        """
        Search and provide additional context
        
        Returns results grouped by plan with statistics
        """
        results = self.search(query, top_k=top_k)
        
        # Group by plan
        by_plan = {}
        for result in results:
            plan = result.get('plan_name', 'Unknown')
            if plan not in by_plan:
                by_plan[plan] = []
            by_plan[plan].append(result)
        
        return {
            'query': query,
            'total_results': len(results),
            'results': results,
            'by_plan': by_plan,
            'plans_found': list(by_plan.keys())
        }
    
    def compare_plans(self, query: str, plan_names: List[str]) -> Dict:
        """
        Compare specific benefit across multiple plans
        
        Args:
            query: Benefit to compare (e.g., "gym membership")
            plan_names: List of plan names to compare
        
        Returns:
            Comparison data for each plan
        """
        comparison = {}
        
        for plan_name in plan_names:
            results = self.search(query, top_k=3, plan_filter=plan_name)
            comparison[plan_name] = results
        
        return {
            'query': query,
            'comparison': comparison
        }
    
    def get_plan_overview(self, plan_name: str) -> Dict:
        """
        Get overview chunk for a specific plan
        
        Args:
            plan_name: Name of the plan
        
        Returns:
            Overview chunk with plan details
        """
        for chunk in self.chunks:
            if (chunk.get('plan_name') == plan_name and 
                chunk.get('type') == 'overview'):
                return chunk
        
        return None
    
    def list_plans(self) -> List[str]:
        """Get list of all available plans"""
        plans = set()
        for chunk in self.chunks:
            if 'plan_name' in chunk:
                plans.add(chunk['plan_name'])
        return sorted(list(plans))
    
    def list_categories(self) -> List[str]:
        """Get list of all benefit categories"""
        categories = set()
        for chunk in self.chunks:
            if 'category' in chunk:
                categories.add(chunk['category'])
        return sorted(list(categories))
    
    def get_statistics(self) -> Dict:
        """Get statistics about indexed data"""
        stats = {
            'total_chunks': len(self.chunks),
            'total_plans': len(self.list_plans()),
            'plans': self.list_plans(),
            'categories': self.list_categories(),
            'chunks_by_plan': {},
            'chunks_by_category': {}
        }
        
        # Count by plan
        for chunk in self.chunks:
            plan = chunk.get('plan_name', 'Unknown')
            stats['chunks_by_plan'][plan] = stats['chunks_by_plan'].get(plan, 0) + 1
        
        # Count by category
        for chunk in self.chunks:
            cat = chunk.get('category', 'unknown')
            stats['chunks_by_category'][cat] = stats['chunks_by_category'].get(cat, 0) + 1
        
        return stats


def test_retriever():
    """
    Test the retriever with sample queries
    """
    print("="*60)
    print("🧪 TESTING RETRIEVAL SYSTEM")
    print("="*60)
    print()
    
    # Initialize retriever
    retriever = BenefitRetriever()
    
    # Get statistics
    print("📊 Index Statistics:")
    stats = retriever.get_statistics()
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   Total plans: {stats['total_plans']}")
    print(f"   Plans: {', '.join(stats['plans'])}")
    print(f"   Categories: {len(stats['categories'])}")
    print()
    
    # Test queries
    test_queries = [
        "Does this plan cover gym membership?",
        "What's the copay for primary care visits?",
        "Is dental care covered?",
        "How much do I pay for prescription drugs?",
        "Does the plan cover telehealth?",
    ]
    
    print("🔍 Testing Sample Queries:\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"{'='*60}")
        print(f"Query {i}: {query}")
        print(f"{'='*60}")
        
        results = retriever.search(query, top_k=3)
        
        if not results:
            print("❌ No results found\n")
            continue
        
        for j, result in enumerate(results, 1):
            print(f"\n{j}. [{result['plan_name']}]")
            print(f"   Category: {result['category']}")
            print(f"   Similarity: {result['similarity_score']:.3f}")
            print(f"   Text: {result['text'][:150]}...")
        
        print("\n")
    
    print("="*60)
    print("✅ RETRIEVAL SYSTEM TEST COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    test_retriever()