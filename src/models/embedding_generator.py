"""
Generate embeddings and build FAISS search index
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import json
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm


class EmbeddingGenerator:
    """Generate embeddings and build searchable index"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize embedding model
        
        Why this model?
        - Fast: Generates embeddings in milliseconds
        - Good quality: 384 dimensions
        - Small size: ~90MB
        - Trained on diverse text
        """
        print(f"🤖 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        print(f"✅ Model loaded! Embedding dimension: {self.dimension}\n")
    
    def generate_embeddings(self, chunks: List[Dict], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for all chunks
        
        Args:
            chunks: List of chunk dictionaries with 'text' field
            batch_size: Process this many chunks at once (faster)
        
        Returns:
            numpy array of embeddings (shape: [num_chunks, dimension])
        """
        texts = [chunk['text'] for chunk in chunks]
        
        print(f"🔄 Generating embeddings for {len(texts)} chunks...")
        print(f"   Using batch size: {batch_size}")
        
        # Generate embeddings with progress bar
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # L2 normalization for better similarity
        )
        
        print(f"✅ Generated embeddings shape: {embeddings.shape}\n")
        return embeddings
    
    def build_faiss_index(self, embeddings: np.ndarray) -> faiss.Index:
        """
        Build FAISS index for fast similarity search
        
        FAISS = Facebook AI Similarity Search
        - Searches through millions of vectors in milliseconds
        - Uses approximate nearest neighbor algorithms
        
        Args:
            embeddings: numpy array of embeddings
        
        Returns:
            FAISS index
        """
        print("🔨 Building FAISS search index...")
        
        # Use flat index (exact search, reliable for small datasets)
        index = faiss.IndexFlatIP(self.dimension)

        # Add embeddings to index
        print(f"   Adding {len(embeddings)} vectors to index...")
        index.add(embeddings.astype('float32'))
        
        print(f"✅ FAISS index built! Total vectors: {index.ntotal}\n")
        return index
    
    def save_all(self, index: faiss.Index, chunks: List[Dict], 
                 embeddings: np.ndarray, output_dir: str = "data/index"):
        """
        Save index, chunks, and embeddings to disk
        
        Args:
            index: FAISS index
            chunks: Original chunk data
            embeddings: Numpy array of embeddings
            output_dir: Where to save files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print("💾 Saving files...")
        
        # Save FAISS index
        index_file = output_path / "benefits.index"
        faiss.write_index(index, str(index_file))
        print(f"   ✅ Saved FAISS index: {index_file}")
        
        # Save chunks (needed to retrieve original text)
        chunks_file = output_path / "chunks.pkl"
        with open(chunks_file, 'wb') as f:
            pickle.dump(chunks, f)
        print(f"   ✅ Saved chunks: {chunks_file}")
        
        # Save embeddings (useful for analysis)
        embeddings_file = output_path / "embeddings.npy"
        np.save(embeddings_file, embeddings)
        print(f"   ✅ Saved embeddings: {embeddings_file}")
        
        # Save metadata
        metadata = {
            'total_chunks': len(chunks),
            'embedding_dimension': self.dimension,
            'model_name': 'all-MiniLM-L6-v2',
            'index_type': 'FlatIP',
            'plans': list(set(c.get('plan_name', 'Unknown') for c in chunks)),
            'categories': list(set(c.get('category', 'unknown') for c in chunks)),
            'total_plans': len(set(c.get('plan_name', 'Unknown') for c in chunks))
        }
        
        metadata_file = output_path / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"   ✅ Saved metadata: {metadata_file}")
        
        print(f"\n🎉 All files saved to: {output_path}")
        
        # Print summary
        print("\n📊 Index Summary:")
        print(f"   Total chunks: {metadata['total_chunks']}")
        print(f"   Plans indexed: {metadata['total_plans']}")
        print(f"   Categories: {len(metadata['categories'])}")
        print(f"   Embedding dimensions: {metadata['embedding_dimension']}")
    
    def load_all(self, index_dir: str = "data/index"):
        """
        Load saved index and data
        
        Args:
            index_dir: Directory with saved files
        
        Returns:
            tuple: (index, chunks, embeddings)
        """
        index_path = Path(index_dir)
        
        print("📂 Loading index from disk...")
        
        # Load FAISS index
        index = faiss.read_index(str(index_path / "benefits.index"))
        print(f"   ✅ Loaded index with {index.ntotal} vectors")
        
        # Load chunks
        with open(index_path / "chunks.pkl", 'rb') as f:
            chunks = pickle.load(f)
        print(f"   ✅ Loaded {len(chunks)} chunks")
        
        # Load embeddings
        embeddings = np.load(index_path / "embeddings.npy")
        print(f"   ✅ Loaded embeddings: {embeddings.shape}")
        
        return index, chunks, embeddings


def build_search_index():
    """
    Complete pipeline: Load chunks → Generate embeddings → Build index → Save
    """
    print("="*60)
    print("🚀 BUILDING HEALTHCARE BENEFITS SEARCH INDEX")
    print("="*60)
    print()
    
    # Load chunks
    chunks_file = Path("data/processed/all_chunks.json")
    
    if not chunks_file.exists():
        print("❌ Error: all_chunks.json not found!")
        print("   Please run chunker.py first.")
        return None, None, None
    
    print("📂 Loading chunks...")
    with open(chunks_file, 'r') as f:
        chunks = json.load(f)
    
    print(f"✅ Loaded {len(chunks)} chunks\n")
    
    # Initialize generator
    generator = EmbeddingGenerator()
    
    # Generate embeddings
    embeddings = generator.generate_embeddings(chunks, batch_size=32)
    
    # Build index
    index = generator.build_faiss_index(embeddings)
    
    # Save everything
    generator.save_all(index, chunks, embeddings)
    
    print("\n" + "="*60)
    print("✅ INDEX BUILD COMPLETE!")
    print("="*60)
    
    return index, chunks, embeddings


if __name__ == "__main__":
    build_search_index()