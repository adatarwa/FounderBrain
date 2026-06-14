# 🧠 FounderBrain

**A multi-agent AI system that builds your entire startup OS in under 60 seconds.**

Describe your startup. Seven specialist AI agents run in parallel waves — each one reading what the previous ones found — and together produce a complete founder playbook: market validation with real web data, ICP, go-to-market strategy, legal briefing, first 5 job specs, pitch narrative, and a 90-day ops plan.

---

## What makes this different

Every "AI business plan tool" out there runs one prompt and returns one answer. FounderBrain runs **seven specialist agents that talk to each other.**

The market agent searches the web for real competitor pricing and funding data before writing its analysis. The GTM agent reads what the market and customer agents found before designing the strategy. The hiring agent reads the GTM plan before writing job specs — so it hires for the roles the strategy actually requires. The fundraising agent reads everything before building the pitch. The ops agent sequences all of it into a 90-day plan that reflects the actual work.

Agents run in parallel waves — independent agents run simultaneously, cutting total runtime in half.

This is the architecture nobody has open-sourced.

---

## Demo

```
╔══════════════════════════════════════╗
║         FounderBrain v2.0            ║
║   Multi-agent startup co-pilot       ║
╚══════════════════════════════════════╝

What are you building?
> AI tool for procurement teams in manufacturing to automate RFQ processing

Wave 1 — running MARKET + LEGAL in parallel
  [MARKET] Searching web for real market data...
  [LEGAL]  Searching regulatory requirements...
  ✓ [MARKET] $4.2B TAM in industrial procurement. SAP Ariba dominates enterprise
             but ignores sub-500 employee plants. Strong timing.
  ✓ [LEGAL]  Delaware C-Corp recommended. No industry-specific regulations.
             File trademark on brand name before launch.

Wave 2 — running CUSTOMER + GTM in parallel
  ✓ [CUSTOMER] ICP: 100-500 employee manufacturers. Procurement manager is the
               champion, VP Operations controls the budget.
  ✓ [GTM]      Outbound-led. LinkedIn targeting. $499/mo per plant.
               First 10 customers via APICS community outreach.

Wave 3 — running HIRING + FUNDRAISING in parallel
  ✓ [HIRING]      Hire order: Full-stack engineer → AE → CS → Solutions Engineer
  ✓ [FUNDRAISING] Raise $1.2M pre-seed. Hook: "Manufacturers lose 11hrs/week
                  to RFQ emails. We automate that in 20 minutes."

Wave 4
  ✓ [OPS] Month 1: 5 design partners. Month 2: MVP + first paying customer.
           Month 3: $15K MRR, start fundraise. North star: MRR.

All agents complete in 47s

Full report saved → ~/FounderBrain/reports/MyStartup_20250615.md
```

---

## Architecture

```
Founder input
      │
      ▼
 Orchestrator           ← plans waves, routes outputs, resolves conflicts
      │
   Wave 1 (parallel)
      ├─→ Market agent  ← web search: real competitors, funding, market size
      └─→ Legal agent   ← entity structure, IP, regulatory risks
      │
   Wave 2 (parallel)
      ├─→ Customer agent ← reads market output
      └─→ GTM agent      ← reads market + customer
      │
   Wave 3 (parallel)
      ├─→ Hiring agent      ← reads market + customer + GTM
      └─→ Fundraising agent ← reads all four above
      │
   Wave 4
      └─→ Ops agent         ← reads all six above
              │
              ▼
      Shared memory layer   ← all agents read/write here
              │
              ▼
      Full report           ← markdown + JSON, export to Notion/Google Docs
```

The shared memory layer is the key. Every agent gets the full context of everything discovered before it — not just the previous step, but all previous steps. Each agent's output enriches the next agent's prompt automatically.

---

## Agents

| Agent | Wave | Reads | Produces |
|-------|------|-------|---------|
| Market | 1 | Web search data | TAM/SAM/SOM, competitors, verdict |
| Legal | 1 | Web search data | Entity structure, IP, regulatory risks |
| Customer | 2 | Market output | ICP, buyer personas, where to find them |
| GTM | 2 | Market + Customer | Motion, pricing, first 10 customers |
| Hiring | 3 | Market + Customer + GTM | First 5 job specs sequenced by strategy |
| Fundraising | 3 | All four above | Pitch narrative, deck outline, objection handling |
| Ops | 4 | All six above | 90-day plan across all workstreams |

---

## Industry modes

FounderBrain auto-detects your industry and injects the right framework into every agent.

| Detected | Framework includes |
|----------|--------------------|
| **B2B SaaS** | ARR metrics, PLG vs sales-led decision, churn benchmarks, valuation multiples |
| **Marketplace** | Two-sided ICP, liquidity threshold, take rate benchmarks, cold start strategy |
| **Hardware** | BOM cost targets, certification requirements, channel strategy, NRE funding |
| **Consumer** | DAU/MAU benchmarks, K-factor, retention curves, DTC acquisition channels |

Detection is automatic from your description — no configuration needed.

---

## What you get

**Market Analysis** — TAM/SAM/SOM with real web sources, top competitors with positioning gaps, market timing rationale, honest verdict.

**Legal Briefing** — Entity structure recommendation, IP considerations, regulatory risks by industry, first 3 contracts needed, red flags.

**Customer & ICP** — Precise ICP definition, primary persona (who feels the pain), secondary persona (who controls the budget), where to find them, buying triggers.

**GTM Strategy** — GTM motion, primary channel, pricing model, Month 1 / 3 / 6 milestones, exactly how to get the first 10 paying customers.

**Hiring Plan** — First 5 job specs sequenced by GTM strategy, with timing, must-haves, interview green/red flags, comp ranges, sourcing.

**Fundraising & Pitch** — Raise amount, round type, 10-12 slide deck outline, opening hook, use of funds, biggest objection and sharp answer.

**90-Day Ops Plan** — North star metric, monthly themes and milestones, weekly cadence, tools to set up, contingency if behind on day 45.

Everything saves as a markdown report to `~/FounderBrain/reports/`.

---

## Installation

```bash
git clone https://github.com/adatarwa/FounderBrain.git
cd FounderBrain
pip install -r requirements.txt
cp .env.example .env
# Add your Anthropic API key to .env
```

Get a free API key at [console.anthropic.com](https://console.anthropic.com)

---

## Usage

**CLI:**
```bash
python main.py
```

Or pass your description directly:
```bash
python main.py "B2B SaaS for restaurant inventory management targeting independent restaurants"
```

**Web app** — no Python knowledge needed:
```bash
python app.py
# Open http://localhost:5000
```

Watch each agent turn green in real time. Download your report as markdown or JSON.

**Resume a failed run:**
```bash
python main.py --resume RUN_ID
```

Checkpoints save after every wave. Resume picks up from the last completed wave.

---

## Export

| Destination | How |
|-------------|-----|
| **Markdown** | Automatic — saved to `~/FounderBrain/reports/` |
| **JSON** | `from output.exporters import JSONExporter` |
| **Notion** | Add `NOTION_TOKEN` + `NOTION_DATABASE_ID` to `.env` |
| **Google Docs** | Add `credentials.json` — see `output/exporters.py` for setup |

---

## Project structure

```
FounderBrain/
├── agents/
│   ├── base_agent.py        — base class all agents inherit
│   ├── market_agent.py      — market validation + real web search
│   ├── legal_agent.py       — entity, IP, regulatory risks
│   ├── customer_agent.py    — ICP + buyer personas
│   ├── gtm_agent.py         — go-to-market strategy
│   ├── hiring_agent.py      — first 5 job specs
│   ├── fundraising_agent.py — pitch narrative + deck outline
│   └── ops_agent.py         — 90-day operational plan
├── memory/
│   └── shared_memory.py     — inter-agent communication layer
├── tools/
│   ├── web_search.py        — real-time web search for agents
│   └── web_scraper.py       — competitor page scraping
├── prompts/
│   └── industry_packs.py    — SaaS / marketplace / hardware / consumer packs
├── output/
│   ├── report.py            — markdown report generator
│   └── exporters.py         — Notion, Google Docs, JSON export
├── orchestrator.py          — parallel wave execution + conflict resolution
├── main.py                  — CLI entry point
├── app.py                   — web interface (Flask)
├── requirements.txt
└── .env.example
```

---

## Adding a new agent

Every agent is ~60 lines. To add a new specialist:

```python
from agents.base_agent import BaseAgent

class PricingAgent(BaseAgent):
    name = "pricing"
    description = "Deep pricing strategy and packaging analysis"

    def _system_prompt(self):
        return "You are a SaaS pricing expert..."

    def _user_prompt(self, memory, context):
        return f"{context}\nDesign the pricing strategy..."
```

Add it to the execution waves in `orchestrator.py`. Done.

---

## Roadmap

- [ ] Async streaming — show agent output word by word in web app
- [ ] Notion template with linked databases per section
- [ ] Investor database matching — match pitch to real investors by thesis
- [ ] Competitor monitoring — re-run market agent weekly, alert on changes
- [ ] Export to pitch deck (PPTX)
- [ ] More industry packs: fintech, health tech, edtech, climate
- [ ] Team mode — multiple founders edit the plan collaboratively

---

## Contributing

Most valuable contributions:
- New specialist agents (pricing, product roadmap, competitive intel)
- Better industry prompt packs with real startup examples
- Improved web search queries for sharper market data
- Additional export destinations

---

## License

MIT

---

*Built with [Claude](https://anthropic.com) · 7 agents · parallel execution · real web data*
