#!/usr/bin/env python3
"""
Example: Using the knowledge base with GPT/OpenAI
"""

import json
from pathlib import Path
from openai import OpenAI

# Get the knowledge base directory
KB_DIR = Path(__file__).parent.parent

# Initialize OpenAI client (you'll need to set OPENAI_API_KEY)
client = OpenAI()

def load_knowledge_base():
    """Load the knowledge base"""
    with open(KB_DIR / 'knowledge_base.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def find_relevant_episodes(kb, query, top_n=3):
    """
    Simple keyword-based search to find relevant episodes.
    For production, use embeddings + vector search instead.
    """
    query_words = set(query.lower().split())
    scored_episodes = []
    
    for ep in kb['episodes']:
        transcript_lower = ep['transcript'].lower()
        # Count how many query words appear in transcript
        matches = sum(1 for word in query_words if word in transcript_lower)
        if matches > 0:
            scored_episodes.append((matches, ep))
    
    # Sort by relevance
    scored_episodes.sort(reverse=True)
    return [ep for _, ep in scored_episodes[:top_n]]

def ask_gpt_with_context(question, episodes):
    """
    Ask GPT a question with relevant podcast context
    """
    # Build context from relevant episodes
    context_parts = []
    for ep in episodes:
        # Use first 3000 chars of transcript to stay within token limits
        context_parts.append(
            f"Episode: {ep['title']}\n"
            f"Guest: {ep['guest']}\n"
            f"Transcript excerpt:\n{ep['transcript'][:3000]}...\n"
        )
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Create the prompt
    system_prompt = """You are an expert assistant with access to transcripts from Lenny's Podcast, 
which features interviews with world-class product leaders and growth experts. 
Answer questions based on the provided transcript excerpts."""
    
    user_prompt = f"""Based on these podcast transcripts from Lenny's Podcast:

{context}

Question: {question}

Please provide a comprehensive answer based on the information in these transcripts."""

    # Call GPT
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content

def main():
    print("=" * 80)
    print("GPT Integration Example")
    print("=" * 80)
    
    # Load knowledge base
    print("\nLoading knowledge base...")
    kb = load_knowledge_base()
    print(f"Loaded {len(kb['episodes'])} episodes")
    
    # Example question
    question = "How do I build a great product team?"
    
    print(f"\nQuestion: {question}")
    print("\nFinding relevant episodes...")
    
    # Find relevant episodes
    relevant_episodes = find_relevant_episodes(kb, question, top_n=3)
    
    print(f"Found {len(relevant_episodes)} relevant episodes:")
    for ep in relevant_episodes:
        print(f"  - {ep['guest']}: {ep['title'][:60]}...")
    
    # Ask GPT with context
    print("\nQuerying GPT with context...")
    try:
        answer = ask_gpt_with_context(question, relevant_episodes)
        print("\n" + "=" * 80)
        print("GPT Answer:")
        print("=" * 80)
        print(answer)
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Installed openai package: pip install openai")
        print("3. Have API credits available")

if __name__ == "__main__":
    main()
