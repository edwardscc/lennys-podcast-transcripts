#!/usr/bin/env python3
"""
Script to help ChatGPT read and process knowledge base chunk files.

Usage:
    python3 read_chunks.py [options]

Examples:
    # List all chunk files
    python3 read_chunks.py --list

    # Read a specific chunk file
    python3 read_chunks.py --file 001

    # Read multiple chunk files
    python3 read_chunks.py --file 001 002 003

    # Read a range of files
    python3 read_chunks.py --range 1 10

    # Read all files and display summary
    python3 read_chunks.py --summary

    # Read all files and combine into one output
    python3 read_chunks.py --all
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Configuration
CHUNKS_DIR = Path(__file__).parent / "chunks"
CHUNK_PATTERN = "knowledge_base_chunk_{:03d}.json"


def list_chunk_files() -> List[Path]:
    """List all chunk files in the chunks directory."""
    chunk_files = sorted(CHUNKS_DIR.glob("knowledge_base_chunk_*.json"))
    return chunk_files


def read_chunk_file(chunk_number: int) -> Dict[str, Any]:
    """Read a specific chunk file by number."""
    chunk_file = CHUNKS_DIR / CHUNK_PATTERN.format(chunk_number)
    
    if not chunk_file.exists():
        raise FileNotFoundError(f"Chunk file not found: {chunk_file}")
    
    with open(chunk_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def display_file_list():
    """Display a list of all chunk files."""
    files = list_chunk_files()
    print(f"\n📁 Found {len(files)} chunk files in {CHUNKS_DIR}\n")
    print("Available files:")
    print("-" * 60)
    
    for i, file_path in enumerate(files, 1):
        chunk_num = file_path.stem.split('_')[-1]
        try:
            data = json.load(open(file_path, 'r', encoding='utf-8'))
            episode = data['episodes'][0]
            title = episode.get('title', 'Unknown')[:50]
            guest = episode.get('guest', 'Unknown')
            print(f"{chunk_num:>3}. {title}... | Guest: {guest}")
        except Exception as e:
            print(f"{chunk_num:>3}. [Error reading file: {e}]")


def display_chunk(chunk_data: Dict[str, Any], chunk_number: int):
    """Display a chunk file's contents in a readable format."""
    metadata = chunk_data.get('metadata', {})
    episodes = chunk_data.get('episodes', [])
    
    print(f"\n{'='*80}")
    print(f"CHUNK {chunk_number:03d}")
    print(f"{'='*80}")
    print(f"Total chunks: {metadata.get('total_chunks', 'N/A')}")
    print(f"Episodes in chunk: {metadata.get('episodes_in_chunk', 'N/A')}")
    print(f"Episode range: {metadata.get('episode_range', {}).get('start', 'N/A')} - {metadata.get('episode_range', {}).get('end', 'N/A')}")
    print(f"\nEpisodes ({len(episodes)}):")
    print("-" * 80)
    
    for i, episode in enumerate(episodes, 1):
        print(f"\nEpisode {i}:")
        print(f"  ID: {episode.get('id', 'N/A')}")
        print(f"  Guest: {episode.get('guest', 'N/A')}")
        print(f"  Title: {episode.get('title', 'N/A')}")
        print(f"  YouTube: {episode.get('youtube_url', 'N/A')}")
        print(f"  Duration: {episode.get('duration', 'N/A')}")
        print(f"  Views: {episode.get('view_count', 'N/A')}")
        print(f"  Word count: {episode.get('word_count', 'N/A')}")
        
        transcript = episode.get('transcript', '')
        if transcript:
            transcript_preview = transcript[:200] + "..." if len(transcript) > 200 else transcript
            print(f"  Transcript preview: {transcript_preview}")
            print(f"  Full transcript length: {len(transcript)} characters")


def display_summary():
    """Display a summary of all chunk files."""
    files = list_chunk_files()
    print(f"\n📊 SUMMARY: {len(files)} chunk files\n")
    print("-" * 80)
    
    total_episodes = 0
    total_words = 0
    total_chars = 0
    
    for file_path in files:
        try:
            data = json.load(open(file_path, 'r', encoding='utf-8'))
            episodes = data.get('episodes', [])
            total_episodes += len(episodes)
            
            for episode in episodes:
                total_words += episode.get('word_count', 0)
                total_chars += episode.get('transcript_length', 0)
        except Exception as e:
            print(f"Error reading {file_path.name}: {e}")
    
    print(f"Total chunk files: {len(files)}")
    print(f"Total episodes: {total_episodes}")
    print(f"Total words: {total_words:,}")
    print(f"Total characters: {total_chars:,}")
    print(f"Average words per episode: {total_words // total_episodes if total_episodes > 0 else 0:,}")


def read_chunks(chunk_numbers: List[int], show_content: bool = True):
    """Read and display multiple chunk files."""
    for chunk_num in chunk_numbers:
        try:
            chunk_data = read_chunk_file(chunk_num)
            if show_content:
                display_chunk(chunk_data, chunk_num)
            else:
                # Just show metadata
                metadata = chunk_data.get('metadata', {})
                episodes = chunk_data.get('episodes', [])
                print(f"\nChunk {chunk_num:03d}: {len(episodes)} episode(s)")
                for ep in episodes:
                    print(f"  - {ep.get('title', 'Unknown')[:60]}")
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error reading chunk {chunk_num}: {e}")


def read_range(start: int, end: int, show_content: bool = True):
    """Read a range of chunk files."""
    chunk_numbers = list(range(start, end + 1))
    read_chunks(chunk_numbers, show_content)


def read_all(show_content: bool = False):
    """Read all chunk files (metadata only to avoid overwhelming output)."""
    files = list_chunk_files()
    chunk_numbers = []
    
    for file_path in files:
        chunk_num = int(file_path.stem.split('_')[-1])
        chunk_numbers.append(chunk_num)
    
    print(f"Reading {len(chunk_numbers)} chunk files...")
    read_chunks(sorted(chunk_numbers), show_content)


def main():
    parser = argparse.ArgumentParser(
        description="Read and display knowledge base chunk files for ChatGPT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available chunk files'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=int,
        nargs='+',
        metavar='N',
        help='Read specific chunk file(s) by number (e.g., --file 1 2 3)'
    )
    
    parser.add_argument(
        '--range', '-r',
        type=int,
        nargs=2,
        metavar=('START', 'END'),
        help='Read a range of chunk files (e.g., --range 1 10)'
    )
    
    parser.add_argument(
        '--summary', '-s',
        action='store_true',
        help='Display summary statistics for all chunk files'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Read all chunk files (shows metadata only)'
    )
    
    parser.add_argument(
        '--metadata-only',
        action='store_true',
        help='Show only metadata, not full transcript content'
    )
    
    parser.add_argument(
        '--dir',
        type=str,
        default=None,
        help='Override chunks directory path'
    )
    
    args = parser.parse_args()
    
    # Override directory if specified
    global CHUNKS_DIR
    if args.dir:
        CHUNKS_DIR = Path(args.dir)
    
    # Check if chunks directory exists
    if not CHUNKS_DIR.exists():
        print(f"❌ Error: Chunks directory not found: {CHUNKS_DIR}")
        print(f"   Please ensure the chunks directory exists.")
        sys.exit(1)
    
    # Execute requested action
    if args.list:
        display_file_list()
    elif args.summary:
        display_summary()
    elif args.all:
        read_all(show_content=False)
    elif args.range:
        start, end = args.range
        read_range(start, end, show_content=not args.metadata_only)
    elif args.file:
        read_chunks(args.file, show_content=not args.metadata_only)
    else:
        # Default: show list
        display_file_list()
        print("\n💡 Use --help to see all available options")


if __name__ == "__main__":
    main()
