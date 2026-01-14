#!/usr/bin/env python3
"""
Basic usage examples for the Lenny's Podcast Knowledge Base
"""

import json
from pathlib import Path

# Get the knowledge base directory
KB_DIR = Path(__file__).parent.parent

# Example 1: Load and explore the knowledge base
print("=" * 80)
print("Example 1: Loading the Knowledge Base")
print("=" * 80)

with open(KB_DIR / 'knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

print(f"Total episodes: {kb['metadata']['total_episodes']}")
print(f"Total chunks: {kb['metadata']['total_chunks']}")

# Example 2: Find a specific episode
print("\n" + "=" * 80)
print("Example 2: Finding a Specific Episode")
print("=" * 80)

episode = next((ep for ep in kb['episodes'] if ep['id'] == 'marty-cagan'), None)
if episode:
    print(f"Guest: {episode['guest']}")
    print(f"Title: {episode['title']}")
    print(f"Duration: {episode['duration']}")
    print(f"Views: {episode['view_count']:,}")
    print(f"Transcript preview: {episode['transcript'][:200]}...")

# Example 3: Search episodes by guest name
print("\n" + "=" * 80)
print("Example 3: Finding Episodes by Guest")
print("=" * 80)

guest_name = "Shreyas Doshi"
matching_episodes = [ep for ep in kb['episodes'] if guest_name.lower() in ep['guest'].lower()]

print(f"Found {len(matching_episodes)} episode(s) with '{guest_name}':")
for ep in matching_episodes:
    print(f"  - {ep['title']}")

# Example 4: Get most popular episodes
print("\n" + "=" * 80)
print("Example 4: Most Popular Episodes (by views)")
print("=" * 80)

top_episodes = sorted(
    kb['episodes'],
    key=lambda x: x.get('view_count', 0),
    reverse=True
)[:5]

for i, ep in enumerate(top_episodes, 1):
    print(f"{i}. {ep['guest']}: {ep['view_count']:,.0f} views")
    print(f"   {ep['title'][:60]}...")

# Example 5: Search transcripts for keywords
print("\n" + "=" * 80)
print("Example 5: Searching Transcripts for Keywords")
print("=" * 80)

search_term = "product-market fit"
matching_episodes = []

for ep in kb['episodes']:
    if search_term.lower() in ep['transcript'].lower():
        # Count occurrences
        count = ep['transcript'].lower().count(search_term.lower())
        matching_episodes.append((ep, count))

# Sort by number of mentions
matching_episodes.sort(key=lambda x: x[1], reverse=True)

print(f"Episodes mentioning '{search_term}':")
for ep, count in matching_episodes[:5]:
    print(f"  - {ep['guest']}: {count} mentions")
    print(f"    {ep['title'][:60]}...")

# Example 6: Using the index (faster, no transcripts)
print("\n" + "=" * 80)
print("Example 6: Using the Index (Metadata Only)")
print("=" * 80)

with open(KB_DIR / 'index.json', 'r', encoding='utf-8') as f:
    index = json.load(f)

print(f"Index contains {len(index['episodes'])} episodes (no transcripts)")

# Find episodes by duration
long_episodes = [
    ep for ep in index['episodes']
    if ep.get('duration_seconds', 0) > 3600  # Longer than 1 hour
]

print(f"\nEpisodes longer than 1 hour: {len(long_episodes)}")
for ep in long_episodes[:3]:
    print(f"  - {ep['guest']}: {ep['duration']}")

print("\n" + "=" * 80)
print("Done! Check the other example files for more advanced usage.")
print("=" * 80)
