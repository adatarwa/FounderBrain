"""
agents/gtm_agent.py
Designs go-to-market strategy. Reads market + customer outputs.
"""

from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory
from prompts.industry_packs import inject_into_prompt

SYSTEM = """You are a go-to-market strategist who has taken 10+ B2B startups from 0 to $1M ARR.
Design a specific, executable GTM strategy for the first 6 months.

Return ONLY valid JSON:
{
  "summary": "2-sentence GTM summary",
  "full_output": "Full markdown GTM plan (## headers)",
  "key_facts": ["fact 1", "fact 2", "fact 3"],
  "motion": "PLG | sales-led | channel | community | outbound",
  "first_channel": "single channel to dominate first",
  "pricing": {
    "model": "per seat / usage / flat",
    "entry_price": "...",
    "rationale": "why this pricing"
  },
  "month_1_actions": ["action 1", "action 2", "action 3"],
  "month_3_target": "specific measurable milestone",
  "month_6_target": "specific measurable milestone",
  "first_10_customers": "exactly how to get the first 10 paying customers"
}

Rules: Pick ONE primary channel. Be specific about first 10 customers. Under 700 words."""


class GTMAgent(BaseAgent):
    name = "gtm"
    description = "Go-to-market strategy, pricing, and first customer acquisition plan"

    def _system_prompt(self) -> str:
        return inject_into_prompt(SYSTEM, self._founder_input, "gtm_context")

    def _user_prompt(self, memory: SharedMemory, context: str) -> str:
        self._founder_input = memory.founder_input
        return f"""{context}

Design the GTM for the first 6 months using the ICP and market data above:
1. GTM motion — pick one
2. Primary channel to dominate
3. Pricing model and entry price
4. Month 1 / 3 / 6 targets
5. Exactly how to get first 10 paying customers

Return JSON only."""

    def _update_memory(self, memory: SharedMemory, parsed: dict):
        if parsed.get("motion"):
            memory.business_model = parsed["motion"]
