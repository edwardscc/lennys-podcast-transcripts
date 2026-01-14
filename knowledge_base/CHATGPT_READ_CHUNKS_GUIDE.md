# 📖 Guide: Using read_chunks.py with ChatGPT

This guide explains how to use the `read_chunks.py` script to help ChatGPT read and process the knowledge base chunk files.

## 🎯 Purpose

The `read_chunks.py` script allows ChatGPT to:
- List all available chunk files
- Read specific episode files
- Process multiple files at once
- Get summaries and statistics
- Access episode metadata and transcripts

## 📋 Basic Usage

### 1. List All Available Files

**In ChatGPT, you can say:**
```
Run this script to see all available chunk files:
python3 knowledge_base/read_chunks.py --list
```

**Or upload the script and ask:**
```
I've uploaded read_chunks.py. Please run it with --list to show me all available episode files.
```

### 2. Read a Specific Episode

**To read episode 1:**
```
python3 knowledge_base/read_chunks.py --file 1
```

**To read multiple episodes:**
```
python3 knowledge_base/read_chunks.py --file 1 2 3
```

### 3. Read a Range of Episodes

**To read episodes 1-10:**
```
python3 knowledge_base/read_chunks.py --range 1 10
```

### 4. Get Summary Statistics

**To see overall statistics:**
```
python3 knowledge_base/read_chunks.py --summary
```

### 5. Read All Files (Metadata Only)

**To see metadata for all files:**
```
python3 knowledge_base/read_chunks.py --all
```

## 🔧 Advanced Options

### Metadata Only (No Full Transcripts)

When you want to see episode info without the full transcript:

```
python3 knowledge_base/read_chunks.py --file 1 --metadata-only
```

### Custom Directory

If the chunks are in a different location:

```
python3 knowledge_base/read_chunks.py --file 1 --dir /path/to/chunks
```

## 💡 ChatGPT Workflow Examples

### Example 1: Process Episodes Incrementally

**You (to ChatGPT):**
```
I have a knowledge base split into 269 episode files. 
Please use read_chunks.py to read episode 1, process it, 
then I'll give you episode 2, and so on.
```

**ChatGPT can then:**
```python
# Run this to see what's available
python3 knowledge_base/read_chunks.py --list

# Then read episode 1
python3 knowledge_base/read_chunks.py --file 1
```

### Example 2: Batch Processing

**You (to ChatGPT):**
```
Please read episodes 1-5 and create a knowledge base from them.
```

**ChatGPT can:**
```python
python3 knowledge_base/read_chunks.py --range 1 5
```

### Example 3: Find Specific Episodes

**You (to ChatGPT):**
```
I want to find episodes about "growth". Can you list all files 
and help me identify which ones to read?
```

**ChatGPT can:**
```python
# First, list all files
python3 knowledge_base/read_chunks.py --list

# Then read specific ones based on titles
python3 knowledge_base/read_chunks.py --file 2 3 6
```

## 📝 File Structure

The script expects chunk files in this structure:
```
knowledge_base/
├── chunks/
│   ├── knowledge_base_chunk_001.json
│   ├── knowledge_base_chunk_002.json
│   └── ...
└── read_chunks.py
```

Each chunk file contains:
- `metadata`: File number, episode info, totals
- `episodes`: Array with episode data including full transcript

## 🚀 Quick Start for ChatGPT

**Copy this prompt to ChatGPT:**

```
I have a knowledge base with 269 podcast episode transcripts 
organized as JSON files. I've uploaded a script called 
read_chunks.py that can help you read these files.

Please:
1. First, run: python3 knowledge_base/read_chunks.py --list
   This will show you all available episodes.

2. Then, let's start processing episodes one at a time.
   Run: python3 knowledge_base/read_chunks.py --file 1
   
3. After you process episode 1, I'll give you episode 2, and so on.

The script can also:
- Read multiple files: --file 1 2 3
- Read ranges: --range 1 10
- Show summaries: --summary
- Show metadata only: --file 1 --metadata-only

Let's begin!
```

## 📊 Output Format

The script displays:
- **File list**: Episode number, title preview, guest name
- **Chunk details**: Metadata, episode info, transcript preview
- **Summary**: Total files, episodes, words, characters

## ⚠️ Notes

- The script reads files from `knowledge_base/chunks/` by default
- Full transcripts can be very long - use `--metadata-only` to avoid overwhelming output
- File numbers correspond directly to episode numbers (chunk 001 = episode 1)

## 🔗 Related Files

- `CHATGPT_PROMPT_SIMPLE.txt` - Simple prompt for ChatGPT
- `CHATGPT_PROMPT_JSON_VERSION.txt` - JSON-focused prompt
- `CHATGPT_KNOWLEDGE_BASE_PROMPT.md` - Comprehensive prompt
- `CHUNKS_README.md` - Detailed chunk file structure
