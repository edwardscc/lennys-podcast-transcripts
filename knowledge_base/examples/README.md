# Knowledge Base Usage Examples

This directory contains practical examples showing how to use the Lenny's Podcast knowledge base.

## Quick Start

### 1. Basic Usage
```bash
python3 examples/basic_usage.py
```

This demonstrates:
- Loading the knowledge base
- Finding specific episodes
- Searching by guest name
- Finding most popular episodes
- Keyword search in transcripts

### 2. GPT Integration
```bash
# First, set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Then run the example
python3 examples/gpt_integration.py
```

This shows how to:
- Find relevant episodes for a question
- Provide context to GPT
- Get answers based on podcast content

### 3. Embeddings for RAG
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the embeddings example
python3 examples/embeddings_example.py
```

This demonstrates:
- Creating vector embeddings from chunks
- Semantic search using cosine similarity
- Building a RAG system

## Requirements

### For Basic Usage
- Python 3.6+
- No external dependencies (uses only standard library)

### For GPT Integration
```bash
pip install openai
```

### For Embeddings Example
```bash
pip install openai numpy
```

## Next Steps

1. **Start Simple**: Run `basic_usage.py` to understand the data structure
2. **Add GPT**: Use `gpt_integration.py` to see how to query with context
3. **Build RAG**: Use `embeddings_example.py` as a foundation for semantic search
4. **Scale Up**: Process all chunks (not just 100) for production use
5. **Integrate**: Connect to vector databases like Pinecone, Weaviate, or Chroma

## Customization

All examples are designed to be easily modified:
- Change search queries
- Adjust number of results
- Modify GPT prompts
- Add your own filtering logic
- Integrate with your existing systems
