"""
prompts/industry_packs.py
Industry-specific context injected into agent prompts.
A SaaS startup and hardware startup need completely different frameworks.
The orchestrator detects the industry and injects the right pack.
"""


INDUSTRY_PACKS = {

    "saas": {
        "label": "B2B SaaS",
        "keywords": ["saas", "software", "platform", "api", "tool", "dashboard", "subscription"],
        "market_context": """
SaaS-specific market considerations:
- Key metric: Annual Recurring Revenue (ARR) and growth rate
- Valuation multiples: typically 5-15x ARR for early stage
- Competitive moat: integrations, data network effects, switching costs
- Market sizing: number of target companies × average ACV
- Watch for: feature commoditization, big-tech entry (Microsoft/Salesforce)
""",
        "customer_context": """
SaaS-specific customer considerations:
- Champion vs economic buyer distinction is critical
- Average sales cycle: SMB (1-2 weeks), mid-market (1-3 months), enterprise (3-12 months)
- Expansion revenue (NRR) is as important as new ARR
- Churn benchmark: <5% annual for good B2B SaaS
- Key buying triggers: pain point reaches breaking point, new budget cycle, team growth
""",
        "gtm_context": """
SaaS GTM frameworks:
- PLG (Product-Led Growth): freemium → paid, best for bottom-up SMB
- Sales-Led: outbound + inbound, best for mid-market/enterprise
- Channel: resellers/VARs, best for geographic or vertical expansion
- Community-Led: build audience first, best for developer tools
- Pricing models: per seat, usage-based, flat, tiered — choose one for launch
""",
        "fundraising_context": """
SaaS fundraising benchmarks:
- Pre-seed: $500K-$2M, idea/MVP stage, 0-$10K MRR
- Seed: $1M-$5M, product-market fit signals, $10K-$100K MRR
- Series A: $5M-$20M, proven growth, $100K+ MRR, 3x YoY growth
- Key metrics investors want: MRR, MoM growth %, churn, CAC, LTV, NRR
- Lead with growth rate, not absolute numbers at early stage
"""
    },

    "marketplace": {
        "label": "Marketplace",
        "keywords": ["marketplace", "platform", "connect", "buyers", "sellers", "matching", "two-sided"],
        "market_context": """
Marketplace-specific market considerations:
- Two-sided network effects are the primary moat
- Take rate benchmarks: 10-30% for most categories
- GMV (Gross Merchandise Value) is the primary top-line metric
- Cold start problem: must solve supply OR demand first
- Vertical marketplaces beat horizontal — niche wins
""",
        "customer_context": """
Marketplace-specific customer considerations:
- Two ICPs: supply side AND demand side — define both
- Which side is harder to acquire? Start there.
- Liquidity threshold: the minimum supply needed before demand converts
- Trust mechanisms: reviews, verification, insurance, escrow
- Retention on both sides is equally critical
""",
        "gtm_context": """
Marketplace GTM frameworks:
- Constrained launch: one city, one vertical, one use case first
- Supply-first strategy: lock in supply before marketing to demand
- Demand-first strategy: prove demand exists, then recruit supply
- Community seeding: find existing communities of your supply side
- Referral loops: both sides should want to refer others
""",
        "fundraising_context": """
Marketplace fundraising benchmarks:
- GMV growth rate is the headline metric
- Take rate × GMV = revenue — investors value both
- Cohort retention on both sides matters more than overall numbers
- Pre-seed/seed: prove liquidity in a single market
- Series A: prove the model is repeatable across markets
"""
    },

    "hardware": {
        "label": "Hardware / Deep Tech",
        "keywords": ["hardware", "device", "sensor", "iot", "physical", "manufacturing", "robot", "chip"],
        "market_context": """
Hardware-specific market considerations:
- BOM (Bill of Materials) cost must be <30% of selling price at scale
- Manufacturing lead times: 6-18 months from design to production
- Regulatory certifications required before sale: FCC, CE, UL, FDA (medical)
- IP and patents matter more than software — file early
- Contract manufacturers in Asia vs. domestic — strategic decision
""",
        "customer_context": """
Hardware-specific customer considerations:
- Pilot programs before volume commitment is standard
- Procurement cycles are long: 6-24 months for enterprise hardware
- Total cost of ownership (TCO) matters more than unit price
- Service contracts and support are critical for retention
- Reference customers open doors — prioritize lighthouse accounts
""",
        "gtm_context": """
Hardware GTM frameworks:
- Pilot → expansion model: 1 site → 10 sites → 100 sites
- Channel partners (VARs, distributors) essential for scale
- Direct sales for first 10 customers, channel for growth
- Trade shows are still relevant for hardware
- Service revenue model: hardware at cost + recurring software/service fees
""",
        "fundraising_context": """
Hardware fundraising reality:
- Hardware startups need 3x more capital than software equivalents
- SBIR/STTR grants: non-dilutive funding for deep tech
- Hardware-friendly VCs: Lux Capital, Bolt, SOSV, Catapult
- Milestones that matter: working prototype → pilot → first production run
- NRE (Non-Recurring Engineering) costs must be funded before revenue
"""
    },

    "consumer": {
        "label": "Consumer / DTC",
        "keywords": ["consumer", "b2c", "app", "social", "community", "content", "dtc", "direct"],
        "market_context": """
Consumer-specific market considerations:
- DAU/MAU ratio is the engagement health metric (target >50%)
- CAC through paid channels is often unsustainable — organic is the moat
- Brand and community are the defensible assets
- Viral coefficient (K-factor) determines capital efficiency
- Winner-take-most dynamics: be the best in your category or die
""",
        "customer_context": """
Consumer-specific customer considerations:
- Retention curve: what % of users are active at day 1, 7, 30, 90?
- Jobs-to-be-done: what is the user actually hiring this product for?
- Emotional triggers matter more than features
- Power users (top 10%) drive 90% of engagement and referrals — serve them
- Age/demographic cohort behavior differs dramatically
""",
        "gtm_context": """
Consumer GTM frameworks:
- Influencer seeding: gifting to micro-influencers in your niche
- Community-first: build an audience before building the product
- Content marketing: own a keyword or topic, not just a product
- Referral programs: Dropbox-style two-sided incentives
- Paid social: Meta + TikTok for discovery, but unit economics must work
""",
        "fundraising_context": """
Consumer fundraising benchmarks:
- Consumer investors want to see retention curves, not just downloads
- D30 retention >20% is strong; >40% is exceptional
- Monthly active users and MoM growth rate are headline metrics
- Revenue per user and LTV vs CAC ratio
- Consumer-focused VCs: Forerunner, Benchmark, Greylock, a16z Consumer
"""
    },
}


def detect_industry(founder_input: str) -> str:
    """Detect the most likely industry from the founder's description."""
    text = founder_input.lower()
    scores = {}
    for industry, pack in INDUSTRY_PACKS.items():
        score = sum(1 for kw in pack["keywords"] if kw in text)
        scores[industry] = score
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "saas"  # default to SaaS


def get_pack(industry: str) -> dict:
    """Return the industry pack for a given industry."""
    return INDUSTRY_PACKS.get(industry, INDUSTRY_PACKS["saas"])


def inject_into_prompt(base_prompt: str, founder_input: str, section: str) -> str:
    """
    Inject industry-specific context into an agent prompt.
    section = "market_context" | "customer_context" | "gtm_context" | "fundraising_context"
    """
    industry = detect_industry(founder_input)
    pack = get_pack(industry)
    context = pack.get(section, "")
    if not context:
        return base_prompt
    return f"{base_prompt}\n\n=== INDUSTRY CONTEXT ({pack['label']}) ===\n{context}\n=== END ===\n"
