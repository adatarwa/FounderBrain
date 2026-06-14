"""
tools/web_search.py
Gives FounderBrain agents access to real live data.
Uses Claude's built-in web search tool so agents can find:
- Real competitor pricing and positioning
- Recent funding rounds
- Live market size data
- Industry news and trends
"""

import os
import anthropic
from typing import Optional


class WebSearch:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def search(self, query: str, max_results: int = 5) -> dict:
        """
        Run a web search and return structured results.
        Uses Claude's web_search tool to find real data.
        """
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1500,
                tools=[{"type": "web_search_20250305", "name": "web_search"}],
                messages=[{
                    "role": "user",
                    "content": f"""Search for: {query}

Return a JSON object with:
{{
  "query": "{query}",
  "findings": [
    {{"source": "...", "fact": "...", "relevance": "high|medium|low"}}
  ],
  "summary": "2-3 sentence summary of what you found"
}}

Return only the JSON, no other text."""
                }]
            )

            # Extract text from response (may include tool use blocks)
            text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    text += block.text

            # Try to parse JSON
            import json
            clean = text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean)

        except Exception as e:
            return {
                "query": query,
                "findings": [],
                "summary": f"Search failed: {e}",
                "error": str(e)
            }

    def search_competitors(self, startup_description: str, industry: str) -> dict:
        """Find real competitors with pricing and positioning."""
        query = f"{industry} startups competitors pricing 2024 2025"
        return self.search(query)

    def search_market_size(self, industry: str, keywords: str) -> dict:
        """Find real market size data."""
        query = f"{industry} {keywords} market size TAM 2024 2025 billion"
        return self.search(query)

    def search_funding(self, industry: str) -> dict:
        """Find recent funding rounds in the space."""
        query = f"{industry} startup funding rounds 2024 2025 seed series A"
        return self.search(query)

    def search_icp(self, target_customer: str, industry: str) -> dict:
        """Find data about the target customer segment."""
        query = f"{target_customer} {industry} pain points challenges software tools"
        return self.search(query)
