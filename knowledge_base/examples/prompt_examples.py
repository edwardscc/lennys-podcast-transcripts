#!/usr/bin/env python3
"""
Example: Using GPT prompts with the knowledge base
Shows how to combine prompts with actual transcript content
"""

import json
from pathlib import Path

# Get the knowledge base directory
KB_DIR = Path(__file__).parent.parent

def load_knowledge_base():
    """Load the knowledge base"""
    with open(KB_DIR / 'knowledge_base.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def find_relevant_episodes(kb, topic, max_episodes=3):
    """Find episodes relevant to a topic"""
    topic_lower = topic.lower()
    scored = []
    
    for ep in kb['episodes']:
        transcript_lower = ep['transcript'].lower()
        # Simple keyword matching - in production, use embeddings
        score = transcript_lower.count(topic_lower)
        if score > 0:
            scored.append((score, ep))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    return [ep for _, ep in scored[:max_episodes]]

def build_prompt_with_context(prompt_template, relevant_episodes, max_chars_per_episode=3000):
    """
    Build a GPT prompt with relevant transcript context
    """
    # Build context from episodes
    context_parts = []
    for ep in relevant_episodes:
        context_parts.append(
            f"Episode: {ep['title']}\n"
            f"Guest: {ep['guest']}\n"
            f"Transcript excerpt:\n{ep['transcript'][:max_chars_per_episode]}...\n"
        )
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Combine with prompt template
    full_prompt = f"""Based on these transcripts from Lenny's Podcast:

{context}

{prompt_template}"""
    
    return full_prompt

def example_prompts():
    """Show example prompts you can use"""
    
    prompts = {
        "product_market_fit": """
Based on Lenny's Podcast interviews, what are the key frameworks and signals for 
identifying product-market fit? Share insights from multiple guests.
""",
        
        "building_teams": """
How do top product leaders structure and build their product teams? 
What are the common patterns and best practices from Lenny's Podcast?
""",
        
        "prioritization": """
What prioritization frameworks have been shared on Lenny's Podcast? 
Compare different approaches and when to use each.
""",
        
        "growth_tactics": """
What growth tactics have been discussed on Lenny's Podcast? 
Which ones work, which don't, and why?
""",
        
        "career_advice": """
Based on Lenny's Podcast interviews, what advice do product leaders give 
for building a successful product management career?
""",
        
        "custom": """
I'm facing [your specific challenge]. Based on Lenny's Podcast interviews, 
how have other product leaders solved similar problems? Provide actionable steps.
"""
    }
    
    return prompts

def main():
    print("=" * 80)
    print("GPT Prompt Examples with Knowledge Base")
    print("=" * 80)
    
    # Load knowledge base
    print("\nLoading knowledge base...")
    kb = load_knowledge_base()
    print(f"Loaded {len(kb['episodes'])} episodes")
    
    # Example 1: Product-Market Fit
    print("\n" + "=" * 80)
    print("Example 1: Product-Market Fit Prompt")
    print("=" * 80)
    
    topic = "product-market fit"
    relevant = find_relevant_episodes(kb, topic, max_episodes=3)
    
    print(f"\nFound {len(relevant)} relevant episodes:")
    for ep in relevant:
        print(f"  - {ep['guest']}: {ep['title'][:60]}...")
    
    prompt = example_prompts()["product_market_fit"]
    full_prompt = build_prompt_with_context(prompt, relevant)
    
    print(f"\nFull prompt length: {len(full_prompt)} characters")
    print(f"\nPrompt preview (first 500 chars):")
    print("-" * 80)
    print(full_prompt[:500] + "...")
    
    # Example 2: Building Teams
    print("\n" + "=" * 80)
    print("Example 2: Building Product Teams Prompt")
    print("=" * 80)
    
    topic = "product team"
    relevant = find_relevant_episodes(kb, topic, max_episodes=2)
    
    print(f"\nFound {len(relevant)} relevant episodes:")
    for ep in relevant:
        print(f"  - {ep['guest']}: {ep['title'][:60]}...")
    
    prompt = example_prompts()["building_teams"]
    full_prompt = build_prompt_with_context(prompt, relevant)
    
    print(f"\nFull prompt length: {len(full_prompt)} characters")
    
    # Show how to use with OpenAI
    print("\n" + "=" * 80)
    print("How to Use with OpenAI API")
    print("=" * 80)
    
    print("""
from openai import OpenAI

client = OpenAI()

# Use the prompt we built
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are an expert product management assistant with access to transcripts from Lenny's Podcast."
        },
        {
            "role": "user",
            "content": full_prompt  # The prompt we built above
        }
    ]
)

answer = response.choices[0].message.content
print(answer)
""")
    
    # Show available prompts
    print("\n" + "=" * 80)
    print("Available Prompt Templates")
    print("=" * 80)
    
    prompts = example_prompts()
    for key, prompt in prompts.items():
        print(f"\n{key.upper().replace('_', ' ')}:")
        print(prompt[:100] + "...")
    
    print("\n" + "=" * 80)
    print("See GPT_PROMPTS.md for 50+ more prompts!")
    print("=" * 80)

if __name__ == "__main__":
    main()
