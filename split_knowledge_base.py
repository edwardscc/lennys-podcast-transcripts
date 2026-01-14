#!/usr/bin/env python3
"""
Split the knowledge base JSON into smaller files with 20 episodes each
"""

import json
from pathlib import Path

# Configuration
KB_FILE = Path("knowledge_base/knowledge_base.json")
OUTPUT_DIR = Path("knowledge_base/chunks")
EPISODES_PER_FILE = 1

def split_knowledge_base():
    """Split the knowledge base into smaller files"""
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Load the knowledge base
    print(f"Loading {KB_FILE}...")
    with open(KB_FILE, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    episodes = kb['episodes']
    total_episodes = len(episodes)
    total_chunks = (total_episodes + EPISODES_PER_FILE - 1) // EPISODES_PER_FILE
    
    print(f"Total episodes: {total_episodes}")
    print(f"Episodes per file: {EPISODES_PER_FILE}")
    print(f"Will create {total_chunks} files")
    print()
    
    # Create index file
    index = {
        "metadata": {
            "total_episodes": total_episodes,
            "episodes_per_file": EPISODES_PER_FILE,
            "total_files": total_chunks,
            "description": "Index of all knowledge base chunk files"
        },
        "chunks": []
    }
    
    # Split into chunks
    for i in range(0, total_episodes, EPISODES_PER_FILE):
        chunk_num = (i // EPISODES_PER_FILE) + 1
        chunk_episodes = episodes[i:i + EPISODES_PER_FILE]
        
        # Create chunk file
        chunk_data = {
            "metadata": {
                "chunk_number": chunk_num,
                "total_chunks": total_chunks,
                "episode_range": {
                    "start": i + 1,
                    "end": min(i + len(chunk_episodes), total_episodes)
                },
                "episodes_in_chunk": len(chunk_episodes),
                "total_episodes": total_episodes,
                "episodes_per_file": EPISODES_PER_FILE
            },
            "episodes": chunk_episodes
        }
        
        # Save chunk file
        chunk_filename = f"knowledge_base_chunk_{chunk_num:03d}.json"
        chunk_path = OUTPUT_DIR / chunk_filename
        
        with open(chunk_path, 'w', encoding='utf-8') as f:
            json.dump(chunk_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Created {chunk_filename} ({len(chunk_episodes)} episodes: {i+1}-{i+len(chunk_episodes)})")
        
        # Add to index
        index["chunks"].append({
            "chunk_number": chunk_num,
            "filename": chunk_filename,
            "episode_range": {
                "start": i + 1,
                "end": i + len(chunk_episodes)
            },
            "episodes_count": len(chunk_episodes),
            "first_episode": chunk_episodes[0]['title'],
            "last_episode": chunk_episodes[-1]['title']
        })
    
    # Save index file
    index_path = OUTPUT_DIR / "index.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Created index.json")
    
    # Create a simple text index for easy reference
    text_index_path = OUTPUT_DIR / "index.txt"
    with open(text_index_path, 'w', encoding='utf-8') as f:
        f.write("Knowledge Base Chunks Index\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Episodes: {total_episodes}\n")
        f.write(f"Episodes per File: {EPISODES_PER_FILE}\n")
        f.write(f"Total Files: {total_chunks}\n\n")
        f.write("=" * 80 + "\n\n")
        
        for chunk_info in index["chunks"]:
            f.write(f"Chunk {chunk_info['chunk_number']:03d}: {chunk_info['filename']}\n")
            f.write(f"  Episodes {chunk_info['episode_range']['start']}-{chunk_info['episode_range']['end']} ({chunk_info['episodes_count']} episodes)\n")
            f.write(f"  First: {chunk_info['first_episode'][:60]}...\n")
            f.write(f"  Last:  {chunk_info['last_episode'][:60]}...\n\n")
    
    print(f"✓ Created index.txt")
    
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Created {total_chunks} chunk files in {OUTPUT_DIR}")
    print(f"Each file contains up to {EPISODES_PER_FILE} episodes")
    print(f"Index file: {index_path}")
    print("=" * 80)

if __name__ == "__main__":
    split_knowledge_base()
