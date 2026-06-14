"""
agents/customer_agent.py
Builds ICP and buyer personas. Reads market output.
"""

from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory
from prompts.industry_packs import inject_into_prompt

SYSTEM = """You are a customer research expert and B2B sales strategist.
Define exactly who the startup should sell to first and how those buyers think.

Return ONLY valid JSON:
{
  "summary": "2-sentence ICP summary",
  "full_output": "Full markdown ICP + persona doc (## headers)",
  "key_facts": ["fact 1", "fact 2", "fact 3"],
  "icp": {
    "company_size": "e.g. 50-500 employees",
    "industry": "...",
    "geography": "...",
    "budget_range": "...",
    "buying_trigger": "what makes them look NOW"
  },
  "primary_persona": {
    "title": "job title",
    "name": "fictional name",
    "pain": "their #1 pain",
    "goal": "what success looks like",
    "objection": "most likely objection"
  },
  "secondary_persona": {
    "title": "...",
    "role": "economic buyer / champion / blocker",
    "influence": "how they affect the deal"
  },
  "where_to_find_them": ["channel 1", "channel 2", "channel 3"]
}

Rules: Be specific. Use what market agent found. Keep full_output under 600 words."""


class CustomerAgent(BaseAgent):
    name = "customer"
    description = "Builds ICP and buyer personas based on market findings"

    def _system_prompt(self) -> str:
        return inject_into_prompt(SYSTEM, self._founder_input, "customer_context")

    def _user_prompt(self, memory: SharedMemory, context: str) -> str:
        self._founder_input = memory.founder_input
        return f"""{context}

Define the ICP using the market data above. Build:
1. Precise ICP (not vague categories)
2. Primary persona — who feels the pain
3. Secondary persona — who controls the budget
4. Where to find them
5. What triggers them to buy now

Return JSON only."""

    def _update_memory(self, memory: SharedMemory, parsed: dict):
        if parsed.get("primary_persona", {}).get("pain"):
            memory.problem_statement = parsed["primary_persona"]["pain"]
