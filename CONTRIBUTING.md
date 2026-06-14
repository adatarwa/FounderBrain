# Contributing to FounderBrain

Thank you for wanting to contribute. Here's how to do it well.

---

## What we need most

**New specialist agents** — the highest-leverage contribution. Each agent is ~60 lines.
Ideas: pricing strategy, product roadmap, competitive intelligence, legal (jurisdiction-specific), go-to-market for specific geographies.

**Better industry packs** — the prompts in `prompts/industry_packs.py` are the first version.
If you've worked in fintech, health tech, edtech, climate, or defence — your domain knowledge makes these dramatically better. Real startup examples, real benchmarks, real failure modes.

**Improved web search queries** — `tools/web_search.py` uses basic queries right now.
Better queries = sharper real-world data = better agent outputs.

**New export destinations** — `output/exporters.py` has Notion and Google Docs.
Linear, Airtable, HubSpot, Pitch.com, and Google Slides would all be valuable.

---

## How to add a new agent

1. Create `agents/your_agent.py` — inherit from `BaseAgent`, implement `_system_prompt` and `_user_prompt`
2. Add it to `AGENT_MAP` in `orchestrator.py`
3. Add it to the right wave in `EXECUTION_WAVES`
4. Add `your_output` field to `SharedMemory` in `memory/shared_memory.py`
5. Add it to the report in `output/report.py`

Minimal agent template:

```python
from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory

class YourAgent(BaseAgent):
    name = "your_agent"
    description = "One sentence describing what this agent does"

    def _system_prompt(self) -> str:
        return """You are an expert in X.
Return ONLY valid JSON: { "summary": "...", "full_output": "...", "key_facts": [] }"""

    def _user_prompt(self, memory: SharedMemory, context: str) -> str:
        return f"{context}\nYour specific task here.\nReturn JSON only."
```

---

## How to improve an industry pack

Open `prompts/industry_packs.py`. Each pack has four sections:
- `market_context` — metrics, moats, risks specific to this category
- `customer_context` — buying behaviour, personas, retention benchmarks
- `gtm_context` — motion, channels, pricing norms
- `fundraising_context` — round benchmarks, key metrics investors want

To add a new industry (e.g. fintech):
1. Add a new entry to `INDUSTRY_PACKS`
2. Add its keywords to the `keywords` list so auto-detection works
3. Fill in all four context sections with real, specific information

---

## Pull request checklist

- [ ] New agents include a system prompt that returns valid JSON
- [ ] New industry packs include all four context sections
- [ ] No hardcoded API keys or secrets anywhere
- [ ] README updated if you added something user-facing
- [ ] Tested locally with `python main.py "test startup description"`

---

## Setup for development

```bash
git clone https://github.com/adatarwa/FounderBrain.git
cd FounderBrain
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY
python main.py "test startup for development"
```

---

## Questions

Open a GitHub Issue with the `question` label. Response within 48 hours.
