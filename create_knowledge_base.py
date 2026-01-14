#!/usr/bin/env python3
"""
Create an accessible knowledge base from all Lenny's Podcast transcripts
for use with GPT projects.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
import re

# Configuration
EPISODES_DIR = Path("episodes")
OUTPUT_DIR = Path("knowledge_base")
CHUNK_SIZE = 1000  # Characters per chunk for embeddings
CHUNK_OVERLAP = 200  # Overlap between chunks


def parse_transcript(filepath: Path) -> Dict[str, Any]:
    """Parse a transcript markdown file and extract metadata and content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split frontmatter and content
    parts = content.split('---')
    
    if len(parts) < 3:
        # No frontmatter, return content only
        return {
            'metadata': {},
            'content': content,
            'transcript': content
        }
    
    # Parse YAML frontmatter manually
    metadata = {}
    try:
        frontmatter_lines = parts[1].strip().split('\n')
        current_key = None
        current_value = []
        
        for line in frontmatter_lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a key-value pair
            if ':' in line and not line.startswith(' '):
                # Save previous key-value if exists
                if current_key:
                    value = '\n'.join(current_value).strip()
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    metadata[current_key] = value
                
                # Parse new key-value
                key, value = line.split(':', 1)
                current_key = key.strip()
                value = value.strip()
                
                # Handle empty values or values on same line
                if value:
                    if value.startswith('|'):
                        # Multi-line string
                        current_value = []
                    else:
                        # Single line value
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        metadata[current_key] = value
                        current_key = None
                        current_value = []
                else:
                    current_value = []
            else:
                # Continuation of previous value
                if current_key:
                    current_value.append(line)
        
        # Save last key-value
        if current_key:
            value = '\n'.join(current_value).strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            metadata[current_key] = value
        
        # Convert numeric strings to numbers
        for key in ['duration_seconds', 'view_count']:
            if key in metadata:
                try:
                    metadata[key] = float(metadata[key])
                except (ValueError, TypeError):
                    pass
                    
    except Exception as e:
        print(f"Warning: Could not parse YAML for {filepath}: {e}")
        metadata = {}
    
    # Get transcript content (everything after frontmatter)
    transcript = '---'.join(parts[2:]).strip()
    
    # Extract episode slug from path
    episode_slug = filepath.parent.name
    
    return {
        'metadata': metadata or {},
        'content': transcript,
            'transcript': transcript,
            'episode_slug': episode_slug,
            'filepath': str(filepath)
    }


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[Dict[str, Any]]:
    """Split text into overlapping chunks for embeddings."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]
        
        # Try to break at sentence boundaries
        if end < len(text):
            # Look for sentence endings
            sentence_end = max(
                chunk_text.rfind('. '),
                chunk_text.rfind('.\n'),
                chunk_text.rfind('? '),
                chunk_text.rfind('! '),
                chunk_text.rfind('\n\n')
            )
            if sentence_end > chunk_size * 0.5:  # Only use if we're not too short
                chunk_text = chunk_text[:sentence_end + 1]
                end = start + sentence_end + 1
        
        # Calculate whitespace adjustments before stripping
        original_chunk = chunk_text
        stripped_chunk = chunk_text.strip()
        
        # Skip empty chunks (all whitespace)
        if not stripped_chunk:
            start = end - overlap
            if start >= len(text):
                break
            continue
        
        # Calculate leading and trailing whitespace
        leading_whitespace = len(original_chunk) - len(original_chunk.lstrip())
        trailing_whitespace = len(original_chunk) - len(original_chunk.rstrip())
        
        # Adjust positions to account for stripped whitespace
        adjusted_start = start + leading_whitespace
        adjusted_end = min(end - trailing_whitespace, len(text))
        
        # Ensure valid position range
        adjusted_start = max(0, min(adjusted_start, len(text)))
        adjusted_end = max(adjusted_start, min(adjusted_end, len(text)))
        
        chunks.append({
            'text': stripped_chunk,
            'start': adjusted_start,
            'end': adjusted_end
        })
        
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks


def create_knowledge_base():
    """Process all transcripts and create knowledge base files."""
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Find all transcript files
    transcript_files = list(EPISODES_DIR.glob("*/transcript.md"))
    print(f"Found {len(transcript_files)} transcript files")
    
    # Process all transcripts
    episodes = []
    all_chunks = []
    index = []
    
    for i, transcript_file in enumerate(sorted(transcript_files), 1):
        print(f"Processing {i}/{len(transcript_files)}: {transcript_file.parent.name}")
        
        try:
            episode_data = parse_transcript(transcript_file)
            if not episode_data:
                print(f"  Warning: No data extracted from {transcript_file.name}")
                continue
            metadata = episode_data.get('metadata', {})
            transcript = episode_data.get('transcript', '')
            
            # Create episode entry
            episode = {
                'id': episode_data['episode_slug'],
                'guest': metadata.get('guest', 'Unknown'),
                'title': metadata.get('title', 'Untitled'),
                'youtube_url': metadata.get('youtube_url', ''),
                'video_id': metadata.get('video_id', ''),
                'description': metadata.get('description', ''),
                'duration_seconds': metadata.get('duration_seconds', 0),
                'duration': metadata.get('duration', ''),
                'view_count': metadata.get('view_count', 0),
                'channel': metadata.get('channel', ''),
                'transcript': transcript,
                'transcript_length': len(transcript),
                'word_count': len(transcript.split())
            }
            
            episodes.append(episode)
            
            # Create index entry (without full transcript)
            index_entry = {k: v for k, v in episode.items() if k != 'transcript'}
            index.append(index_entry)
            
            # Create chunks for embeddings
            chunks = chunk_text(transcript, CHUNK_SIZE, CHUNK_OVERLAP)
            for chunk_idx, chunk in enumerate(chunks):
                chunk_entry = {
                    'episode_id': episode['id'],
                    'episode_title': episode['title'],
                    'guest': episode['guest'],
                    'chunk_index': chunk_idx,
                    'text': chunk['text'],
                    'start_char': chunk['start'],
                    'end_char': chunk['end']
                }
                all_chunks.append(chunk_entry)
        
        except Exception as e:
            import traceback
            print(f"Error processing {transcript_file}: {e}")
            print(f"  Traceback: {traceback.format_exc()}")
            continue
    
    # Save complete knowledge base (all episodes with full transcripts)
    kb_file = OUTPUT_DIR / "knowledge_base.json"
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'total_episodes': len(episodes),
                'total_chunks': len(all_chunks),
                'chunk_size': CHUNK_SIZE,
                'chunk_overlap': CHUNK_OVERLAP
            },
            'episodes': episodes
        }, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Created {kb_file} ({len(episodes)} episodes)")
    
    # Save index (metadata only, no transcripts)
    index_file = OUTPUT_DIR / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'total_episodes': len(index),
                'description': 'Index of all episodes with metadata only (no transcripts)'
            },
            'episodes': index
        }, f, indent=2, ensure_ascii=False)
    print(f"✓ Created {index_file} ({len(index)} episodes)")
    
    # Save chunks for embeddings
    chunks_file = OUTPUT_DIR / "chunks_for_embeddings.json"
    with open(chunks_file, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'total_chunks': len(all_chunks),
                'chunk_size': CHUNK_SIZE,
                'chunk_overlap': CHUNK_OVERLAP,
                'description': 'Text chunks ready for embedding generation and vector search'
            },
            'chunks': all_chunks
        }, f, indent=2, ensure_ascii=False)
    print(f"✓ Created {chunks_file} ({len(all_chunks)} chunks)")
    
    # Create a simple text index for quick reference
    text_index_file = OUTPUT_DIR / "episode_index.txt"
    with open(text_index_file, 'w', encoding='utf-8') as f:
        f.write("Lenny's Podcast - Episode Index\n")
        f.write("=" * 80 + "\n\n")
        for i, ep in enumerate(index, 1):
            f.write(f"{i}. {ep['title']}\n")
            f.write(f"   Guest: {ep['guest']}\n")
            f.write(f"   Duration: {ep['duration']} | Views: {ep['view_count']:,}\n")
            f.write(f"   ID: {ep['id']}\n")
            f.write(f"   YouTube: {ep['youtube_url']}\n\n")
    print(f"✓ Created {text_index_file}")
    
    # Print summary
    if episodes:
        total_words = sum(ep['word_count'] for ep in episodes)
        total_chars = sum(ep['transcript_length'] for ep in episodes)
        
        print("\n" + "=" * 80)
        print("Knowledge Base Summary")
        print("=" * 80)
        print(f"Total Episodes: {len(episodes)}")
        print(f"Total Words: {total_words:,}")
        print(f"Total Characters: {total_chars:,}")
        print(f"Total Chunks: {len(all_chunks)}")
        print(f"Average Words per Episode: {total_words // len(episodes):,}")
        print(f"Average Chunks per Episode: {len(all_chunks) // len(episodes)}")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("Knowledge Base Summary")
        print("=" * 80)
        print("No episodes processed successfully!")
        print("=" * 80)
    
    print(f"\nAll files saved to: {OUTPUT_DIR.absolute()}")


if __name__ == "__main__":
    create_knowledge_base()
