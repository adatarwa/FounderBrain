"""
agents/hiring_agent.py
Writes the first 5 job specs.
Reads GTM output — knows what roles the strategy actually requires.
"""

from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory

SYSTEM = """You are a startup talent strategist who has helped 50+ early-stage companies make their first hires.
Your job: define exactly which 5 roles to hire first, in order, with full job specs.

You must return ONLY valid JSON — no preamble, no markdown outside the JSON.

JSON schema:
{
  "summary": "2-sentence hiring strategy summary",
  "full_output": "Full markdown hiring plan with job specs (use ## headers)",
  "key_facts": ["fact 1", "fact 2", ...],
  "hire_order": ["role 1", "role 2", "role 3", "role 4", "role 5"],
  "job_specs": [
    {
      "title": "exact job title",
      "hire_at_month": 1,
      "why_now": "why this role at this stage",
      "must_haves": ["skill 1", "skill 2", "skill 3"],
      "nice_to_haves": ["skill 1", "skill 2"],
      "green_flag": "the one thing in an interview that tells you they're right",
      "red_flag": "the one thing that kills the hire",
      "comp_range": "realistic salary range",
      "where_to_find": "LinkedIn / referral / specific community"
    }
  ],
  "founding_team_gaps": "what's missing from the founding team that these hires fill"
}

Rules:
- Base hire order on the GTM motion — sales-led needs AEs first, PLG needs engineers.
- Don't just list generic roles. Every spec should be specific to this startup.
- Green/red flags should be unique to this role and company — not generic interview advice.
- Keep full_output under 800 words.
"""

class HiringAgent(BaseAgent):
    name = "hiring"
    description = "Writes first 5 job specs sequenced by what the GTM strategy requires"

    def _system_prompt(self) -> str:
        return SYSTEM

    def _user_prompt(self, memory: SharedMemory, context: str) -> str:
        return f"""{context}

Write the first 5 job specs for this startup. Sequence them based on the GTM motion above.
For each role:
1. Why hire this role at this stage
2. Must-haves vs nice-to-haves
3. The one green flag and red flag in interviews
4. Realistic comp range and where to find candidates

Return JSON only."""
