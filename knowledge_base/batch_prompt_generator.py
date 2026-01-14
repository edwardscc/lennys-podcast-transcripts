#!/usr/bin/env python3
"""
Generate batch prompts for ChatGPT to process episodes efficiently
"""

import json
from pathlib import Path

# Configuration
CHUNKS_DIR = Path("knowledge_base/chunks")
BATCH_SIZE = 5  # Episodes per message (will combine chunks as needed)
OUTPUT_DIR = Path("knowledge_base/batch_prompts")

def load_chunk(chunk_num):
    """Load a chunk file"""
    chunk_file = CHUNKS_DIR / f"knowledge_base_chunk_{chunk_num:03d}.json"
    with open(chunk_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_batch_prompts():
    """Generate batch prompt files for efficient ChatGPT processing"""
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Load index to get total episodes
    with open(CHUNKS_DIR / 'index.json', 'r') as f:
        index = json.load(f)
    
    total_episodes = index['metadata']['total_episodes']
    total_batches = (total_episodes + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"Generating batch prompts for {total_episodes} episodes")
    print(f"Batch size: {BATCH_SIZE} episodes per message")
    print(f"Total batches: {total_batches}\n")
    
    # Generate prompts
    for batch_num in range(total_batches):
        start_ep = batch_num * BATCH_SIZE + 1
        end_ep = min((batch_num + 1) * BATCH_SIZE, total_episodes)
        
        # Build prompt
        if batch_num == 0:
            # First batch - include system prompt
            prompt = """You are an expert at creating structured knowledge bases from podcast transcripts. I have 269 episodes from Lenny's Podcast that I want to turn into a comprehensive, searchable knowledge base.

## Your Task

Create a complete knowledge base that includes:

1. **Episode Index**: All episodes with metadata (guest, title, topics, key insights)
2. **Topic-Based Organization**: All insights organized by topic (e.g., Product-Market Fit, Growth Tactics, Team Building)
3. **Framework Library**: All frameworks, methodologies, and models extracted with step-by-step application guides
4. **Guest Expertise Map**: What each guest specializes in and their key contributions
5. **Cross-Reference System**: Connections between related episodes and topics
6. **Actionable Insights Database**: Practical advice, tips, and strategies organized by use case

## Output Format

For each episode, extract:
- Guest name and episode title
- 5-10 main topics discussed
- Key frameworks or methodologies shared
- 3-5 most actionable insights
- 3-5 memorable quotes
- Real-world examples or case studies mentioned
- Connections to other topics/episodes

## Processing Instructions

1. Process each transcript thoroughly
2. Extract all significant insights, frameworks, and actionable content
3. Maintain accuracy - only include what's actually in the transcripts
4. Create clear connections between related content
5. Focus on practical, applicable insights
6. Use consistent formatting and structure

## Workflow

I'll provide episodes in batches. For each batch:
- Process all episodes completely
- Add to the cumulative knowledge base (don't start over)
- Maintain cross-references with previously processed episodes
- Update the master index, topic organization, and framework library

Here are the first {} episodes to process:

""".format(end_ep - start_ep + 1)
        else:
            # Subsequent batches
            prompt = f"""Process episodes {start_ep} through {end_ep} and add them to the knowledge base:

"""
        
        # Add episodes to prompt
        for ep_num in range(start_ep, end_ep + 1):
            chunk_data = load_chunk(ep_num)
            episode = chunk_data['episodes'][0]  # Only one episode per file
            
            # Add episode to prompt
            prompt += f"""Episode {ep_num}: {episode['title']}
Guest: {episode['guest']}

"""
            prompt += "```json\n"
            prompt += json.dumps({
                "id": episode['id'],
                "guest": episode['guest'],
                "title": episode['title'],
                "transcript": episode['transcript']
            }, indent=2, ensure_ascii=False)
            prompt += "\n```\n\n"
        
        if batch_num == 0:
            prompt += "Please process these episodes and create the initial knowledge base structure.\n"
        else:
            prompt += f"""Maintain cross-references with all previously processed episodes (1-{start_ep-1}).
Update the master index, topic organization, and framework library.
"""
        
        # Save prompt
        prompt_file = OUTPUT_DIR / f"batch_{batch_num+1:03d}_episodes_{start_ep:03d}-{end_ep:03d}.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"✓ Created batch {batch_num+1:03d}: episodes {start_ep:03d}-{end_ep:03d}")
    
    # Create summary file
    summary = f"""Batch Prompt Generator Summary
{'='*80}

Total Episodes: {total_episodes}
Batch Size: {BATCH_SIZE} episodes per message
Total Batches: {total_batches}

Files Created:
"""
    for batch_num in range(total_batches):
        start_ep = batch_num * BATCH_SIZE + 1
        end_ep = min((batch_num + 1) * BATCH_SIZE, total_episodes)
        summary += f"  batch_{batch_num+1:03d}_episodes_{start_ep:03d}-{end_ep:03d}.txt\n"
    
    summary += f"""
Usage:
1. Copy batch_001 file and paste into ChatGPT (includes system prompt)
2. After ChatGPT responds, copy batch_002 and paste
3. Continue through all {total_batches} batches
4. Request final consolidation after batch {total_batches:03d}

Each batch file is ready to copy-paste directly into ChatGPT.
"""
    
    with open(OUTPUT_DIR / "README.txt", 'w') as f:
        f.write(summary)
    
    print(f"\n✓ Created {total_batches} batch prompt files in {OUTPUT_DIR}")
    print(f"✓ Created README.txt with usage instructions")

if __name__ == "__main__":
    generate_batch_prompts()
