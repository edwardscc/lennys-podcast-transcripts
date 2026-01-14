#!/usr/bin/env python3
"""
Example: Creating embeddings for RAG (Retrieval-Augmented Generation)
"""

import json
import numpy as np
from pathlib import Path
from openai import OpenAI

# Get the knowledge base directory
KB_DIR = Path(__file__).parent.parent

# Initialize OpenAI client
client = OpenAI()

def load_chunks():
    """Load the chunks for embeddings"""
    with open(KB_DIR / 'chunks_for_embeddings.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_embeddings(chunks_data, max_chunks=100):
    """
    Create embeddings for chunks using OpenAI's embedding model.
    In production, process all chunks in batches.
    """
    print(f"Creating embeddings for {min(max_chunks, len(chunks_data['chunks']))} chunks...")
    
    embeddings = []
    chunks_to_process = chunks_data['chunks'][:max_chunks]
    
    for i, chunk in enumerate(chunks_to_process):
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(chunks_to_process)} chunks...")
        
        try:
            response = client.embeddings.create(
                input=chunk['text'],
                model="text-embedding-ada-002"
            )
            
            embeddings.append({
                'chunk_id': f"{chunk['episode_id']}_{chunk['chunk_index']}",
                'embedding': response.data[0].embedding,
                'episode_id': chunk['episode_id'],
                'episode_title': chunk['episode_title'],
                'guest': chunk['guest'],
                'text': chunk['text']
            })
        except Exception as e:
            print(f"Error processing chunk {i}: {e}")
            continue
    
    return embeddings

def search_similar_chunks(query, embeddings, chunks_data, top_k=5):
    """
    Search for similar chunks using cosine similarity
    """
    # Create query embedding
    query_response = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_embedding = np.array(query_response.data[0].embedding)
    
    # Calculate similarities
    similarities = []
    for emb in embeddings:
        chunk_embedding = np.array(emb['embedding'])
        # Cosine similarity
        similarity = np.dot(query_embedding, chunk_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding)
        )
        similarities.append((similarity, emb))
    
    # Sort by similarity
    similarities.sort(reverse=True)
    
    # Return top results
    results = []
    for similarity, emb in similarities[:top_k]:
        results.append({
            'similarity': float(similarity),
            'text': emb['text'],
            'episode': emb['episode_title'],
            'guest': emb['guest']
        })
    
    return results

def main():
    print("=" * 80)
    print("Embeddings Example for RAG")
    print("=" * 80)
    
    # Load chunks
    print("\nLoading chunks...")
    chunks_data = load_chunks()
    print(f"Total chunks available: {chunks_data['metadata']['total_chunks']}")
    
    # Create embeddings (limiting to 100 for demo - use all in production)
    print("\nCreating embeddings...")
    try:
        embeddings = create_embeddings(chunks_data, max_chunks=100)
        print(f"\nCreated {len(embeddings)} embeddings")
        
        # Example search
        query = "How to prioritize product features?"
        print(f"\nSearching for: '{query}'")
        
        results = search_similar_chunks(query, embeddings, chunks_data, top_k=3)
        
        print("\n" + "=" * 80)
        print("Top Results:")
        print("=" * 80)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Similarity: {result['similarity']:.3f}")
            print(f"   Episode: {result['episode']}")
            print(f"   Guest: {result['guest']}")
            print(f"   Text: {result['text'][:200]}...")
        
        # Save embeddings for later use
        output_file = KB_DIR / 'embeddings_sample.json'
        with open(output_file, 'w') as f:
            json.dump(embeddings, f, indent=2)
        print(f"\n✓ Saved embeddings to {output_file}")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Installed openai package: pip install openai")
        print("3. Installed numpy: pip install numpy")
        print("4. Have API credits available")

if __name__ == "__main__":
    main()
