# Knowledge Base Chunks Guide

The knowledge base has been split into **269 individual files**, one episode per file, to make it very easy to work with ChatGPT and process one episode at a time.

## 📁 Episode Files

All files are located in: `knowledge_base/chunks/`

- `knowledge_base_chunk_001.json` - Episode 1
- `knowledge_base_chunk_002.json` - Episode 2
- `knowledge_base_chunk_003.json` - Episode 3
- ... and so on through ...
- `knowledge_base_chunk_269.json` - Episode 269

**Total: 269 files, each with exactly 1 episode**

## 📊 File Structure

Each chunk file follows this structure:

```json
{
  "metadata": {
    "chunk_number": 1,
    "total_chunks": 269,
    "episode_range": {
      "start": 1,
      "end": 1
    },
    "episodes_in_chunk": 1,
    "total_episodes": 269,
    "episodes_per_file": 1
  },
  "episodes": [
    {
      "id": "episode-slug",
      "guest": "Guest Name",
      "title": "Episode Title",
      "youtube_url": "https://...",
      "video_id": "...",
      "description": "...",
      "duration_seconds": 3600,
      "duration": "1:00:00",
      "view_count": 10000,
      "channel": "Lenny's Podcast",
      "transcript": "Full transcript text...",
      "transcript_length": 50000,
      "word_count": 10000
    }
  ]
}
```

## 🔍 Index Files

- `index.json` - JSON index with metadata for all chunks
- `index.txt` - Human-readable text index for quick reference

## 💡 Using with ChatGPT

### Recommended Workflow

1. **Start with the prompt**: Use one of the updated prompt files:
   - `CHATGPT_PROMPT_SIMPLE.txt` - Simple, direct prompt
   - `CHATGPT_PROMPT_JSON_VERSION.txt` - Optimized for JSON chunks
   - `CHATGPT_KNOWLEDGE_BASE_PROMPT.md` - Detailed comprehensive prompt

2. **Provide episodes incrementally**:
   ```
   Here is knowledge_base_chunk_001.json (episode 1):
   [paste file content]
   
   Please process this episode and create the initial knowledge base structure.
   ```

3. **Build incrementally**:
   ```
   Now process knowledge_base_chunk_002.json (episode 2):
   [paste file content]
   
   Add this episode to the existing knowledge base, maintaining 
   cross-references with episode 1.
   ```

4. **Continue through all episodes**: Process chunks 003-269 in the same way

### Key Instructions for ChatGPT

- Process each chunk completely before moving to the next
- Build the knowledge base cumulatively (don't start over)
- Maintain cross-references across chunks
- Update topic lists, framework library, and guest maps as you go
- Look for connections between episodes in different chunks

## 📈 Benefits of Chunked Approach

- **Easier to upload**: Each file is ~80-100KB vs 22MB for the full file
- **Incremental processing**: Build knowledge base one episode at a time
- **Better context management**: ChatGPT can focus on exactly 1 episode at a time
- **Easier error recovery**: If something goes wrong, you only lose one episode's progress
- **Flexible workflow**: Process episodes in any order or skip specific ones
- **Maximum granular control**: Process one episode at a time for best focus
- **Easy to reference**: Each file number directly corresponds to episode number

## 🎯 Finding Specific Episodes

Use `index.json` or `index.txt` to find which chunk contains a specific episode:

```bash
# Check index.txt for quick reference
cat knowledge_base/chunks/index.txt

# Or search index.json programmatically
# Episode 50 is in knowledge_base_chunk_050.json
# Episode 150 is in knowledge_base_chunk_150.json
# The file number directly matches the episode number!
```

## 📝 Example ChatGPT Conversation

```
You: [Paste prompt from CHATGPT_PROMPT_SIMPLE.txt]

ChatGPT: I understand. I'm ready to process the chunk files...

You: Here is knowledge_base_chunk_001.json:
[paste chunk 001 content]

ChatGPT: [Processes and creates initial knowledge base]

You: Great! Now here is knowledge_base_chunk_002.json:
[paste chunk 002 content]

ChatGPT: [Adds to existing knowledge base, maintains cross-references]

... continue for all 269 episodes ...
```

---

**All chunk files are ready to use!** Start with any of the prompt files and begin processing.
