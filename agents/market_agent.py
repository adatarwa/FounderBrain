"""
agents/market_agent.py
Validates the market opportunity. Runs first in Wave 1.
Uses real web search + industry-specific framework.
"""

from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory
from tools.web_search import WebSearch
from prompts.industry_packs import inject_into_prompt

SYSTEM = """You are a world-class market analyst and venture scout.
Validate or challenge a startup's market opportunity with sharp, specific analysis.
Use the real web search data provided. Cite it. Don't invent numbers.

Return ONLY valid JSON:
{
  "summary": "2-sentence market verdict",
  "full_output": "Full markdown market analysis (## headers)",
  "key_facts": ["fact 1", "fact 2", "fact 3"],
  "industry": "one-word industry label",
  "market_size": "TAM / SAM / SOM with sources",
  "verdict": "strong | moderate | weak",
  "top_competitors": ["name", "name", "name"],
  "biggest_risk": "the single biggest market risk"
}

Rules: Be honest. Weak markets get called weak. Keep full_output under 700 words."""


class MarketAgent(BaseAgent):
    name = "market"
    description = "Market validation + real web search — TAM/SAM/SOM, competitors, timing"

    def _system_prompt(self) -> str:
        return inject_into_prompt(SYSTEM, self._founder_input, "market_context")

    def _user_prompt(self, memory: SharedMemory, context: str) -> str:
        self._founder_input = memory.founder_input
        web_data = self._gather_web_data(memory.founder_input)
        return f"""{context}

=== REAL WEB DATA ===
{web_data}
=== END ===

Analyze the market using the real data above. Cover:
1. TAM / SAM / SOM — cite the web data
2. Why now? Market timing rationale
3. Top 3-5 competitors and their gaps
4. Biggest risk
5. Honest verdict

Return JSON only."""

    def _gather_web_data(self, founder_input: str) -> str:
        searcher = WebSearch()
        lines = []
        print("    [MARKET] Searching web for live data...")
        keywords = founder_input[:60]
        for query, label in [
            (f"market size {keywords} industry 2024 2025", "Market size"),
            (f"{keywords} startup funding 2024 2025", "Recent funding"),
            (f"{keywords} software competitors alternatives", "Competitors"),
        ]:
            try:
                r = searcher.search(query)
                lines.append(f"{label}: {r.get('summary','No data')}")
                for f in r.get("findings", [])[:2]:
                    lines.append(f"  • {f.get('fact','')}")
            except Exception:
                lines.append(f"{label}: unavailable")
        return "\n".join(lines)

    def _update_memory(self, memory: SharedMemory, parsed: dict):
        if parsed.get("industry"):
            memory.industry = parsed["industry"]

    def _scrape_competitors(self, competitors: list) -> str:
        """Scrape real competitor pages for pricing and positioning."""
        if not competitors:
            return ""
        from tools.web_scraper import WebScraper
        scraper = WebScraper()
        print("    [MARKET] Scraping competitor pages...")
        results = scraper.analyze_competitor_list(competitors[:2])
        lines = []
        for r in results:
            if r.get("extracted"):
                ex = r["extracted"]
                lines.append(f"  {r['competitor']}: {ex.get('value_prop','N/A')} | Pricing: {ex.get('pricing','N/A')}")
        return "\n".join(lines) if lines else ""
