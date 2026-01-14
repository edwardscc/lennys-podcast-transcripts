# Lenny's Podcast Knowledge Base

A structured, accessible knowledge base containing all 269 episodes from Lenny's Podcast, optimized for use with GPT projects, RAG (Retrieval-Augmented Generation), and AI applications.

## 📊 Overview

This knowledge base contains:
- **269 episodes** from Lenny's Podcast
- **4+ million words** of transcript content
- **31,459 text chunks** ready for embeddings
- Rich metadata for each episode (guest, title, duration, views, YouTube links, etc.)

## 📁 Files in This Directory

### 1. `knowledge_base.json` (Complete Knowledge Base)
**Size:** ~22MB  
**Use Case:** Full knowledge base with complete transcripts

Contains all episodes with full transcript text. Structure:
```json
{
  "metadata": {
    "total_episodes": 269,
    "total_chunks": 31459,
    "chunk_size": 1000,
    "chunk_overlap": 200
  },
  "episodes": [
    {
      "id": "marty-cagan",
      "guest": "Marty Cagan",
      "title": "Product management theater | Marty Cagan...",
      "youtube_url": "https://www.youtube.com/watch?v=...",
      "video_id": "9N4ZgNaWvI0",
      "description": "...",
      "duration_seconds": 5115.0,
      "duration": "1:25:15",
      "view_count": 226150,
      "channel": "Lenny's Podcast",
      "transcript": "Full transcript text...",
      "transcript_length": 123456,
      "word_count": 23456
    }
  ]
}
```

### 2. `index.json` (Metadata Only)
**Size:** ~500KB  
**Use Case:** Quick lookup, filtering, searching episodes without loading full transcripts

Contains all episode metadata but **no transcript text**. Perfect for:
- Building episode catalogs
- Filtering by guest, duration, views
- Creating navigation interfaces
- Quick searches without loading large files

### 3. `chunks_for_embeddings.json` (Embeddings-Ready)
**Size:** ~25MB  
**Use Case:** Vector embeddings, semantic search, RAG applications

Pre-chunked text segments optimized for embedding generation. Each chunk includes:
```json
{
  "episode_id": "marty-cagan",
  "episode_title": "Product management theater | Marty Cagan...",
  "guest": "Marty Cagan",
  "chunk_index": 0,
  "text": "Chunk of transcript text...",
  "start_char": 0,
  "end_char": 1000
}
```

**Chunking Details:**
- Chunk size: 1000 characters
- Overlap: 200 characters (for context preservation)
- Total chunks: 31,459

### 4. `episode_index.txt` (Human-Readable Index)
**Size:** ~50KB  
**Use Case:** Quick reference, browsing episodes

A simple text file listing all episodes with key information for easy browsing.

## 🚀 Usage Examples

### Python: Loading the Knowledge Base

```python
import json

# Load complete knowledge base
with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

print(f"Total episodes: {kb['metadata']['total_episodes']}")

# Access a specific episode
episode = next(ep for ep in kb['episodes'] if ep['id'] == 'marty-cagan')
print(f"Guest: {episode['guest']}")
print(f"Title: {episode['title']}")
print(f"Transcript length: {len(episode['transcript'])} characters")
```

### Python: Using the Index

```python
import json

# Load index (much faster, no transcripts)
with open('index.json', 'r', encoding='utf-8') as f:
    index = json.load(f)

# Find episodes by guest
marty_episodes = [ep for ep in index['episodes'] if 'Marty' in ep['guest']]

# Find most viewed episodes
top_episodes = sorted(
    index['episodes'], 
    key=lambda x: x['view_count'], 
    reverse=True
)[:10]

for ep in top_episodes:
    print(f"{ep['guest']}: {ep['view_count']:,} views")
```

### Python: Creating Embeddings for RAG

```python
import json
import openai  # or your preferred embedding service

# Load chunks
with open('chunks_for_embeddings.json', 'r', encoding='utf-8') as f:
    chunks_data = json.load(f)

chunks = chunks_data['chunks']

# Generate embeddings (example with OpenAI)
embeddings = []
for chunk in chunks[:100]:  # Process in batches
    response = openai.Embedding.create(
        input=chunk['text'],
        model="text-embedding-ada-002"
    )
    embeddings.append({
        'chunk_id': f"{chunk['episode_id']}_{chunk['chunk_index']}",
        'embedding': response['data'][0]['embedding'],
        'metadata': {
            'episode_id': chunk['episode_id'],
            'guest': chunk['guest'],
            'title': chunk['episode_title']
        }
    })

# Save embeddings for vector database
with open('embeddings.json', 'w') as f:
    json.dump(embeddings, f)
```

### Python: Semantic Search with RAG

```python
import json
import numpy as np
from openai import OpenAI

client = OpenAI()

# Load your embeddings (from previous step)
with open('embeddings.json', 'r') as f:
    embeddings = json.load(f)

# Load chunks for retrieval
with open('chunks_for_embeddings.json', 'r', encoding='utf-8') as f:
    chunks_data = json.load(f)
chunks_dict = {
    f"{ch['episode_id']}_{ch['chunk_index']}": ch 
    for ch in chunks_data['chunks']
}

def search_knowledge_base(query, top_k=5):
    # Generate query embedding
    query_embedding = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    ).data[0].embedding
    
    # Find similar chunks
    similarities = []
    for emb in embeddings:
        similarity = np.dot(query_embedding, emb['embedding'])
        similarities.append((similarity, emb['chunk_id']))
    
    # Get top results
    similarities.sort(reverse=True)
    results = []
    for similarity, chunk_id in similarities[:top_k]:
        chunk = chunks_dict[chunk_id]
        results.append({
            'similarity': similarity,
            'text': chunk['text'],
            'episode': chunk['episode_title'],
            'guest': chunk['guest']
        })
    
    return results

# Example search
results = search_knowledge_base("How to build a product team?")
for result in results:
    print(f"\nEpisode: {result['episode']}")
    print(f"Guest: {result['guest']}")
    print(f"Relevance: {result['similarity']:.3f}")
    print(f"Text: {result['text'][:200]}...")
```

### JavaScript/Node.js: Loading the Knowledge Base

```javascript
const fs = require('fs');

// Load complete knowledge base
const kb = JSON.parse(fs.readFileSync('knowledge_base.json', 'utf8'));

console.log(`Total episodes: ${kb.metadata.total_episodes}`);

// Find specific episode
const episode = kb.episodes.find(ep => ep.id === 'marty-cagan');
console.log(`Guest: ${episode.guest}`);
console.log(`Title: ${episode.title}`);
```

## 🔍 Use Cases

### 1. **RAG (Retrieval-Augmented Generation)**
Use `chunks_for_embeddings.json` to:
- Generate vector embeddings
- Build a semantic search system
- Power GPT applications with relevant context
- Create Q&A systems about product management

### 2. **Content Analysis**
Use `knowledge_base.json` to:
- Analyze topics across all episodes
- Extract insights and patterns
- Build topic models
- Generate summaries

### 3. **Episode Discovery**
Use `index.json` to:
- Build search interfaces
- Filter by guest, duration, popularity
- Create recommendation systems
- Generate episode lists

### 4. **GPT Context Injection**
Use `knowledge_base.json` or `chunks_for_embeddings.json` to:
- Provide context to GPT prompts
- Build specialized GPT assistants
- Create domain-specific knowledge bases
- Enhance GPT responses with podcast insights

## 📈 Statistics

- **Total Episodes:** 269
- **Total Words:** 4,071,099
- **Total Characters:** 22,712,368
- **Total Chunks:** 31,459
- **Average Words per Episode:** 15,134
- **Average Chunks per Episode:** 116

## 🔄 Regenerating the Knowledge Base

If you add new episodes or need to regenerate the knowledge base:

```bash
python3 create_knowledge_base.py
```

This will:
1. Scan all transcripts in the `episodes/` directory
2. Extract metadata and content
3. Generate all knowledge base files
4. Create chunked versions for embeddings

## 📝 Notes

- All transcripts are in markdown format
- Metadata is extracted from YAML frontmatter
- Chunks are optimized for embedding models (1000 chars with 200 char overlap)
- All files use UTF-8 encoding
- JSON files are formatted with 2-space indentation for readability

## 🤝 Integration with Vector Databases

This knowledge base is ready to use with:
- **Pinecone** - Upload chunks with embeddings
- **Weaviate** - Import as documents with metadata
- **Chroma** - Load chunks as collection
- **Qdrant** - Index chunks with vectors
- **Milvus** - Store embeddings and metadata
- **FAISS** - Build local vector index

## 📚 Example: Building a GPT Assistant

```python
import json
from openai import OpenAI

client = OpenAI()

# Load knowledge base
with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

def ask_about_product_management(question):
    # Find relevant episodes (simplified - use embeddings in production)
    relevant_episodes = [
        ep for ep in kb['episodes'] 
        if any(keyword in ep['transcript'].lower() 
               for keyword in question.lower().split())
    ][:3]
    
    # Build context
    context = "\n\n".join([
        f"Episode: {ep['title']}\nGuest: {ep['guest']}\n\n{ep['transcript'][:5000]}"
        for ep in relevant_episodes
    ])
    
    # Query GPT with context
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert on product management, drawing insights from Lenny's Podcast."},
            {"role": "user", "content": f"Based on these podcast transcripts:\n\n{context}\n\nQuestion: {question}"}
        ]
    )
    
    return response.choices[0].message.content

# Example
answer = ask_about_product_management("How do I build a great product team?")
print(answer)
```

## 🎯 Best Practices

1. **For RAG Applications:** Use `chunks_for_embeddings.json` with vector search
2. **For Full-Text Search:** Use `knowledge_base.json` with traditional search
3. **For Metadata Queries:** Use `index.json` for fast lookups
4. **For Browsing:** Use `episode_index.txt` for human review
5. **Memory Management:** Load only what you need (index vs full transcripts)

## 📄 License

This knowledge base is derived from Lenny's Podcast transcripts. Please respect the original content creators' rights. See the main repository README for license information.

---

**Generated:** Automatically created from 269 episode transcripts  
**Last Updated:** Run `create_knowledge_base.py` to regenerate with latest episodes
