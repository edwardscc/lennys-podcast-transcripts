# 🚀 Quick Start: read_chunks.py

A Python script to help ChatGPT read and process knowledge base chunk files.

## 📦 What It Does

- Lists all 269 episode files
- Reads specific episodes or ranges
- Shows metadata and full transcripts
- Provides summary statistics

## 🎯 Quick Commands

```bash
# List all files
python3 knowledge_base/read_chunks.py --list

# Read episode 1
python3 knowledge_base/read_chunks.py --file 1

# Read episodes 1-5
python3 knowledge_base/read_chunks.py --range 1 5

# Get summary stats
python3 knowledge_base/read_chunks.py --summary

# Read multiple specific episodes
python3 knowledge_base/read_chunks.py --file 1 2 3 10 25
```

## 💬 For ChatGPT

**Upload the script and say:**
```
I've uploaded read_chunks.py. Please use it to:
1. List all available episodes (--list)
2. Read episode 1 (--file 1)
3. Process it and build a knowledge base
```

**Or use it directly:**
```
Run: python3 knowledge_base/read_chunks.py --file 1
```

## 📖 Full Documentation

See `CHATGPT_READ_CHUNKS_GUIDE.md` for complete usage instructions.
