"""
agents/fundraising_agent.py
Builds pitch narrative. Reads ALL prior agents.
"""

from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory
from prompts.industry_packs import inject_into_prompt

SYSTEM = """You are a pitch coach who has helped founders raise $500M+ across 80+ deals.
Build the pitch narrative using everything the other agents found.

Return ONLY valid JSON:
{
  "summary": "2-sentence fundraising summary",
  "full_output": "Full markdown pitch narrative + deck outline (## headers)",
  "key_facts": ["fact 1", "fact 2", "fact 3"],
  "raise_amount": "recommended raise with rationale",
  "round_type": "pre-seed / seed / series A",
  "use_of_funds": ["bucket 1 with %", "bucket 2 with %", "bucket 3 with %"],
  "target_investors": ["investor type 1", "investor type 2"],
  "deck_slides": [
    {"slide": 1, "title": "...", "one_liner": "what this slide proves"}
  ],
  "opening_hook": "the 2-sentence opening that stops an investor cold",
  "the_ask": "exact ask with runway calculation",
  "biggest_investor_objection": "what every investor will push back on",
  "answer_to_objection": "the honest, sharp response"
}

Rules: Opening hook must be specific. 10-12 slides max. Under 800 words."""


class FundraisingAgent(BaseAgent):
    name = "fundraising"
    description = "Pitch narrative, deck outline, and investor objection handling"

    def _system_prompt(self) -> str:
        return inject_into_prompt(SYSTEM, self._founder_input, "fundraising_context")

    def _user_prompt(self, memory: SharedMemory, context: str) -> str:
        self._founder_input = memory.founder_input
        return f"""{context}

Build the fundraising narrative using everything above:
1. Recommended raise and round type
2. 10-12 slide deck outline
3. Opening hook — 2 sentences that open the pitch
4. Use of funds breakdown
5. Biggest investor objection and your sharp answer

Return JSON only."""
