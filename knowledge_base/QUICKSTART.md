# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Try the Basic Example

```bash
cd knowledge_base/examples
python3 basic_usage.py
```

This will show you:
- How to load the knowledge base
- How to find specific episodes
- How to search by guest or keywords
- How to get the most popular episodes

**No dependencies needed!** This example uses only Python's standard library.

### Step 2: Load Data in Your Code

```python
import json

# Load the complete knowledge base
with open('knowledge_base/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

# Access episodes
for episode in kb['episodes']:
    print(f"{episode['guest']}: {episode['title']}")
    print(f"Transcript: {episode['transcript'][:100]}...")
```

### Step 3: Choose Your Use Case

#### For Simple Queries (No AI needed)
```python
# Use index.json - faster, no transcripts
with open('knowledge_base/index.json', 'r') as f:
    index = json.load(f)

# Filter episodes
long_episodes = [ep for ep in index['episodes'] 
                 if ep['duration_seconds'] > 3600]
```

#### For GPT Integration
```bash
# Set your API key
export OPENAI_API_KEY="your-key-here"

# Run the GPT example
python3 knowledge_base/examples/gpt_integration.py
```

#### For RAG/Semantic Search
```bash
# Set your API key
export OPENAI_API_KEY="your-key-here"

# Run the embeddings example
python3 knowledge_base/examples/embeddings_example.py
```

## 📚 File Reference

| File | Size | Use When |
|------|------|----------|
| `knowledge_base.json` | ~22MB | You need full transcripts |
| `index.json` | ~500KB | You only need metadata (faster) |
| `chunks_for_embeddings.json` | ~25MB | Building RAG/vector search |
| `episode_index.txt` | ~50KB | Quick human browsing |

## 💡 Common Tasks

### Find an Episode by Guest
```python
episode = next(ep for ep in kb['episodes'] 
               if ep['guest'] == 'Marty Cagan', None)
```

### Search for Keywords
```python
results = [ep for ep in kb['episodes'] 
           if 'product-market fit' in ep['transcript'].lower()]
```

### Get Most Popular Episodes
```python
top_10 = sorted(kb['episodes'], 
                key=lambda x: x['view_count'], 
                reverse=True)[:10]
```

### Use with GPT
```python
# Find relevant episodes
relevant = [ep for ep in kb['episodes'] 
            if 'product team' in ep['transcript'].lower()][:3]

# Build context
context = "\n\n".join([ep['transcript'][:2000] for ep in relevant])

# Send to GPT
# (see gpt_integration.py for full example)
```

## 🎯 Next Steps

1. **Explore**: Run `basic_usage.py` to see what's possible
2. **Read**: Check `README.md` for detailed documentation
3. **Build**: Use the examples as templates for your project
4. **Scale**: Process all chunks for production RAG systems

## ❓ Need Help?

- See `README.md` for comprehensive documentation
- Check `examples/` directory for working code
- All examples are commented and easy to modify
