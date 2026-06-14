"""
agents/legal_agent.py
Covers entity structure, IP considerations, and regulatory risks.
Runs in Wave 1 parallel with Market — no dependencies.
Every founder needs this and nobody thinks to include it.
"""

from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory
from tools.web_search import WebSearch

SYSTEM = """You are a startup lawyer and legal strategist who has advised 100+ early-stage companies.
Your job: identify the key legal considerations for this startup before they become expensive problems.

You must return ONLY valid JSON — no preamble, no markdown outside the JSON.

JSON schema:
{
  "summary": "2-sentence legal summary",
  "full_output": "Full markdown legal briefing (use ## headers)",
  "key_facts": ["fact 1", "fact 2", ...],
  "entity_recommendation": {
    "structure": "Delaware C-Corp | LLC | Other",
    "why": "specific reason for this startup",
    "when_to_incorporate": "now | after first revenue | before fundraising"
  },
  "ip_considerations": {
    "trademark": "what to trademark and when",
    "patents": "worth filing? what specifically?",
    "trade_secrets": "what processes/data to protect"
  },
  "regulatory_risks": [
    {"risk": "...", "severity": "high|medium|low", "mitigation": "..."}
  ],
  "contracts_needed_first": ["contract 1", "contract 2", "contract 3"],
  "red_flags": ["legal issue specific to this industry/model"],
  "estimated_legal_budget_year1": "realistic range"
}

Rules:
- This is NOT legal advice — say so in the output. But be specific and useful.
- Flag industry-specific regulations (HIPAA, GDPR, financial regulations, etc.)
- Be direct about red flags — founders need to hear the hard things.
- Recommend Delaware C-Corp for VC-backed startups, LLC for bootstrapped/lifestyle.
- Keep full_output under 600 words.
"""

class LegalAgent(BaseAgent):
    name = "legal"
    description = "Entity structure, IP protection, regulatory risks, and contracts needed"

    def _system_prompt(self) -> str:
        return SYSTEM

    def _user_prompt(self, memory: SharedMemory, context: str) -> str:
        # Search for industry-specific regulations
        reg_data = self._search_regulations(memory.founder_input)

        return f"""{context}

=== REGULATORY SEARCH DATA ===
{reg_data}
=== END DATA ===

Provide legal guidance for this startup. Cover:
1. Entity structure recommendation (and why for THIS startup)
2. IP considerations — what to protect and how
3. Regulatory risks specific to this industry
4. First 3 contracts to put in place
5. Any red flags the founder should know immediately

Disclaimer: This is AI-generated guidance, not legal advice. Recommend they consult a startup lawyer.

Return JSON only."""

    def _search_regulations(self, founder_input: str) -> str:
        try:
            searcher = WebSearch()
            result = searcher.search(f"{founder_input[:60]} regulatory compliance legal requirements startup")
            lines = [result.get("summary", "No regulatory data found")]
            for f in result.get("findings", [])[:3]:
                lines.append(f"  • {f.get('fact', '')}")
            return "\n".join(lines)
        except Exception:
            return "Regulatory search unavailable — use best judgment based on industry."
