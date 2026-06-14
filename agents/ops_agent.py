"""
agents/ops_agent.py
Writes the 90-day operational plan.
Last agent to run — has full context of market, ICP, GTM, hiring, and fundraising.
Synthesizes everything into a sequenced execution plan.
"""

from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory

SYSTEM = """You are a COO and startup operator who has built the first 90 days for 30+ companies.
Your job: write the concrete 90-day plan that sequences all the work from every other agent.

You must return ONLY valid JSON — no preamble, no markdown outside the JSON.

JSON schema:
{
  "summary": "2-sentence ops plan summary",
  "full_output": "Full markdown 90-day plan (use ## headers for each month)",
  "key_facts": ["fact 1", "fact 2", ...],
  "north_star_metric": "the one number that defines success at day 90",
  "month_1": {
    "theme": "one word or phrase",
    "must_complete": ["task 1", "task 2", "task 3", "task 4", "task 5"],
    "milestone": "specific, measurable end-of-month milestone"
  },
  "month_2": {
    "theme": "...",
    "must_complete": ["task 1", "task 2", "task 3", "task 4", "task 5"],
    "milestone": "..."
  },
  "month_3": {
    "theme": "...",
    "must_complete": ["task 1", "task 2", "task 3", "task 4", "task 5"],
    "milestone": "..."
  },
  "weekly_cadence": ["Monday: ...", "Wednesday: ...", "Friday: ..."],
  "tools_to_set_up": ["tool 1", "tool 2", "tool 3"],
  "if_behind_on_day_45": "what to cut or defer if you're behind"
}

Rules:
- Tasks must be specific and actionable — not "build product", but "ship MVP with 3 core features to 5 design partners".
- Sequence hiring against GTM — don't plan revenue before the sales hire.
- Sequence fundraising against ops milestones — raise when you have traction to show.
- The "if behind" section is mandatory — every plan needs a contingency.
- North star metric should be the same as GTM month 3 target.
- Keep full_output under 800 words.
"""

class OpsAgent(BaseAgent):
    name = "ops"
    description = "Writes 90-day operational plan sequenced against GTM, hiring, and fundraising"

    def _system_prompt(self) -> str:
        return SYSTEM

    def _user_prompt(self, memory: SharedMemory, context: str) -> str:
        return f"""{context}

Write the 90-day operational plan that sequences all the above work.
Sequence:
- GTM actions from the GTM agent
- Hiring from the hiring agent
- Fundraising prep from the fundraising agent
- All sequenced by month with specific milestones

Include what to cut if you fall behind on day 45.

Return JSON only."""
