"""
tools/web_scraper.py
Scrapes competitor landing pages, pricing pages, and job boards.
Gives agents real intelligence about what competitors are doing right now.
"""

import os
import anthropic
import json
from typing import Optional


class WebScraper:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def scrape(self, url: str, extract_what: str = "key information") -> dict:
        """
        Fetch and extract structured data from a URL.
        Uses Claude to intelligently extract relevant content.
        """
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                tools=[{"type": "web_search_20250305", "name": "web_search"}],
                messages=[{
                    "role": "user",
                    "content": f"""Visit this URL and extract {extract_what}: {url}

Return JSON:
{{
  "url": "{url}",
  "title": "page title",
  "extracted": {{
    "pricing": "pricing info if found",
    "value_prop": "main value proposition",
    "target_customer": "who they target",
    "key_features": ["feature 1", "feature 2"],
    "company_size": "employee count if found"
  }},
  "summary": "2-sentence summary"
}}

Return only JSON."""
                }]
            )

            text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    text += block.text

            clean = text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean)

        except Exception as e:
            return {"url": url, "error": str(e), "extracted": {}}

    def scrape_competitor(self, competitor_name: str) -> dict:
        """Scrape a competitor's website for pricing and positioning."""
        return self.scrape(
            f"https://www.{competitor_name.lower().replace(' ', '')}.com/pricing",
            extract_what="pricing plans, target customers, and value proposition"
        )

    def scrape_jobs(self, company_name: str) -> dict:
        """Scrape a competitor's job listings to understand their growth areas."""
        return self.scrape(
            f"https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')}/jobs",
            extract_what="job titles, departments hiring, and seniority levels"
        )

    def scrape_product_hunt(self, keywords: str) -> dict:
        """Find similar products launched on Product Hunt."""
        return self.scrape(
            f"https://www.producthunt.com/search?q={keywords.replace(' ', '+')}",
            extract_what="product names, upvotes, descriptions, and launch dates"
        )

    def analyze_competitor_list(self, competitors: list[str]) -> list[dict]:
        """Scrape multiple competitors and return comparative data."""
        results = []
        for name in competitors[:3]:  # Limit to 3 to avoid rate limiting
            print(f"    Scraping {name}...")
            result = self.scrape_competitor(name)
            result["competitor"] = name
            results.append(result)
        return results
