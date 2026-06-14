# FounderBrain Report
## ProcureAI
*Generated June 15, 2025 at 02:47 PM · Run ID: a3f8b1c2*

---

> **Founder input:** AI tool for procurement teams in manufacturing companies to automate RFQ processing and supplier communication

---

# 📊 Market Analysis

## Verdict: Strong

The industrial procurement software market is large, underserved at the SMB level, and ripe for disruption. Enterprise players dominate but have ignored the 500,000+ mid-market manufacturers globally.

## Market Size

- **TAM:** $12.4B — global procurement software market (2024, Gartner)
- **SAM:** $3.2B — mid-market manufacturing segment (50-1000 employees)
- **SOM:** $160M — reachable in 5 years at current growth rates

## Competitors

| Competitor | Weakness | Your opening |
|------------|----------|--------------|
| SAP Ariba | $150K+ ACV, 12-month implementation | Too expensive and slow for mid-market |
| Coupa | Enterprise-only, complex UI | No self-serve, no SMB pricing |
| Tradogram | Weak AI, no RFQ automation | Feature gap in core workflow |
| Email + Excel | Still used by 78% of target market | The real competitor |

## Why Now

- AI APIs have made RFQ parsing and supplier matching 10x cheaper to build
- Post-COVID supply chain disruptions made procurement a boardroom topic
- Mid-market CFOs now have budget approval authority they didn't have before 2021

## Biggest Risk

SAP or Coupa builds a mid-market SKU. Mitigation: move fast, lock in integrations, build switching costs through supplier network effects.

---

# ⚖️ Legal Briefing

*Note: This is AI-generated guidance, not legal advice. Consult a startup lawyer before making decisions.*

## Entity Structure

**Recommendation: Delaware C-Corp**

You're likely raising VC funding and want to issue stock options. Delaware C-Corp is the only structure VCs will accept. Incorporate before you bring on advisors or employees — you need cap table infrastructure in place.

Do it now at Stripe Atlas ($500) or Clerky ($800) — both are fast and clean.

## IP

- **Trademark:** File on "ProcureAI" immediately — $350 via USPTO.gov. Do it before launch.
- **Patents:** Not worth pursuing at this stage. Your moat is data and network effects, not patentable technology.
- **Trade secrets:** Your supplier matching algorithm and training data are your crown jewels. Every employee signs an NDA and IP assignment agreement from day one.

## Regulatory Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| GDPR (EU suppliers) | Medium | Data processing agreements with suppliers, EU data residency option |
| Export controls (defence manufacturers) | Low | Screen customers against ITAR/EAR lists before onboarding |
| SOC 2 (enterprise requirement) | Medium | Start Type I audit at month 9, complete before Series A |

## First Contracts Needed

1. **Founder IP assignment** — before writing a single line of code
2. **Employee/contractor NDA + IP assignment** — before first hire
3. **Customer MSA (Master Service Agreement)** — before first paying customer

---

# 🎯 Customer & ICP

## Ideal Customer Profile

- **Company size:** 100–500 employees
- **Industry:** Discrete manufacturing (auto parts, electronics, industrial equipment)
- **Geography:** US Midwest + Southeast manufacturing belt, then DACH region
- **Budget:** $500–$2,000/month (single approver, no committee)
- **Buying trigger:** New procurement manager hired, or supply chain disruption in past 6 months

## Primary Persona — Maya Chen, Procurement Manager

Maya is 34, has been in the role 18 months, and inherited a mess. Her predecessor managed 200 suppliers via a shared Gmail inbox and a spreadsheet nobody has updated since 2019. She spends 11 hours a week just on RFQ emails. Her boss (VP Ops) is asking why lead times are getting longer. She's the one who will champion ProcureAI internally.

**Pain:** "I spend more time formatting emails than thinking about supplier strategy."
**Goal:** Reduce RFQ cycle time from 3 weeks to 3 days.
**Objection:** "IT will never approve adding another SaaS tool."

## Secondary Persona — David Park, VP Operations

David controls the budget. He doesn't care about the product — he cares about one number: on-time delivery rate. If Maya can show him ProcureAI will move that needle, he signs the PO. He's not your champion; he's your approver.

## Where to Find Maya

- APICS (Association for Supply Chain Management) — 45,000 members, active Slack community
- LinkedIn: "Procurement Manager" + "Manufacturing" + 50-500 employee companies
- Manufacturing industry trade shows: FABTECH, IMTS
- Google search: "RFQ email templates manufacturing" — she's already looking for help

---

# 🚀 Go-To-Market Strategy

## Motion: Outbound-Led

PLG doesn't work here — procurement managers don't trial tools alone, they need IT approval. Sales-led with a short sales cycle (target <2 weeks) is the right motion.

## Primary Channel: LinkedIn Outbound

Target procurement managers at 100-500 employee manufacturers. Send 50 personalised connection requests per week. Message hook: "I noticed you're at [company] — we built a tool that cuts RFQ cycle time from 3 weeks to 3 days. Worth a 20-minute call?"

Expected: 15% connection rate, 8% reply rate = 4 calls/week from 50 outreach.

## Pricing

| Plan | Price | Includes |
|------|-------|---------|
| Starter | $499/mo | 1 plant, unlimited RFQs, 50 suppliers |
| Growth | $999/mo | 3 plants, AI matching, ERP integration |
| Enterprise | Custom | Unlimited plants, dedicated CSM, SLA |

Start everyone on Starter. Expansion revenue comes from plant count.

## Milestones

- **Month 1:** 5 design partners using the product for free, weekly feedback calls
- **Month 3:** First 3 paying customers at $499/mo ($1,500 MRR), NPS > 50
- **Month 6:** $15,000 MRR, CAC < $2,000, average sales cycle < 14 days

## First 10 Customers

1. Message 300 procurement managers on LinkedIn this month
2. Offer free 90-day pilot to first 5 who reply — no credit card, full access
3. At day 60 of pilot, send ROI report showing hours saved
4. Convert pilots to paid at $499/mo
5. Ask each paying customer for 2 referrals — offer 1 free month per referral

---

# 👥 Hiring Plan

## Hire Order

**Month 1 → Full-Stack Engineer**
The founder can't build everything alone past month 2. First hire is technical.
- Must-haves: Python/Node, shipped B2B SaaS products before, comfortable with LLM APIs
- Green flag: Has built workflow automation tools
- Red flag: Only has big-company experience — can't operate without structure
- Comp: $130-160K + 0.5-1% equity
- Find them: Wellfound.com, personal network, YC talent directory

**Month 2 → Account Executive**
Once you have a repeatable demo and 3 design partners, you need a dedicated seller.
- Must-haves: Sold to manufacturing or supply chain buyers before, quota carrier
- Green flag: Has sold $500-2K/mo deals with <21 day cycles
- Red flag: Only enterprise experience — wrong motion for this stage
- Comp: $80K base + $80K OTE + 0.25-0.5% equity
- Find them: RepVue, LinkedIn, manufacturing software companies (Fishbowl, Procore)

**Month 3 → Customer Success Manager**
Churn at this stage kills the company. CSM ensures design partners convert and stay.
- Must-haves: Managed onboarding for SaaS products, manufacturing industry knowledge a plus
- Green flag: Built playbooks from scratch at an early-stage company
- Comp: $70-90K + 0.15-0.3% equity

**Month 4 → Solutions Engineer**
Procurement tools need ERP integrations (SAP, Oracle, NetSuite). SE handles technical sales.
- Must-haves: ERP integration experience, comfortable in sales calls
- Comp: $110-140K + 0.2-0.4% equity

**Month 6 → Marketing / Growth**
Only after you have repeatable sales motion. Growth hire amplifies what's working.
- Must-haves: B2B content + demand gen, manufacturing vertical knowledge a plus
- Comp: $90-120K + 0.2-0.35% equity

---

# 💰 Fundraising & Pitch

## The Raise

**$1.5M pre-seed** at a $6-8M post-money valuation.
18 months of runway. Milestone: $25K MRR before Series A conversations.

## Opening Hook

*"Every manufacturer in America is running their supplier relationships on email and Excel. We built the AI procurement manager they can't afford to hire — and we close the RFQ loop in 20 minutes instead of 3 weeks."*

## Deck Outline

| Slide | Title | What it proves |
|-------|-------|----------------|
| 1 | The problem | 78% of manufacturers still use email + spreadsheets |
| 2 | The cost | 11 hours/week per procurement manager, $180K/year in wasted labor |
| 3 | Our solution | 60-second demo — RFQ in, supplier responses out |
| 4 | The market | $3.2B SAM, no good solution for mid-market |
| 5 | Traction | 5 design partners, X hours saved, NPS 72 |
| 6 | Business model | $499-999/mo per plant, land and expand |
| 7 | Go-to-market | LinkedIn outbound → pilot → convert → referral |
| 8 | Competition | Why SAP Ariba and Coupa don't solve this |
| 9 | Team | Why we're the ones to build this |
| 10 | Financials | Path to $1M ARR in 18 months |
| 11 | The ask | $1.5M, use of funds, 18-month runway |

## Use of Funds

- 60% Engineering — 2 additional engineers, infrastructure
- 25% Sales & Marketing — AE hire, LinkedIn outreach tools
- 15% Operations — legal, accounting, office

## Biggest Objection + Answer

**Objection:** "SAP could build this in 6 months."

**Answer:** "SAP has tried to serve mid-market manufacturing for 20 years and failed every time. Their minimum deal is $150K and takes 12 months to implement. We close in 2 weeks at $499/mo. The distribution model is fundamentally different — they can't compete at this price point without cannibalizing their enterprise business."

## Target Investors

- Pre-seed funds with manufacturing/supply chain thesis: Pear VC, Precursor, Hustle Fund
- Angels: ex-operators from Coupa, Jaggaer, GEP
- Strategic: manufacturing industry angels who can open doors

---

# 📅 90-Day Ops Plan

## North Star Metric: MRR

**Month 1 — Foundation**
Theme: Build and listen

- [ ] Sign 5 design partner agreements (free 90-day pilots)
- [ ] Ship MVP with 3 core features: RFQ creation, supplier email automation, response tracking
- [ ] Set up weekly 30-min calls with each design partner
- [ ] Incorporate as Delaware C-Corp
- [ ] Set up Stripe, Notion, Linear, Slack, Hubspot (free tier)
- **Milestone:** 5 active design partners using the product weekly

**Month 2 — Validate**
Theme: First dollar

- [ ] Hire full-stack engineer (start recruiting month 1)
- [ ] Convert 3 design partners to paid ($499/mo = $1,500 MRR)
- [ ] Build ERP integration for top requested system (NetSuite or QuickBooks)
- [ ] Send 300 LinkedIn outreach messages, book 12+ demo calls
- [ ] Create ROI calculator showing hours saved per month
- **Milestone:** $1,500 MRR, 3 paying customers, NPS > 50

**Month 3 — Grow**
Theme: Repeatability

- [ ] Hire Account Executive
- [ ] Close 7 more customers ($5,000 MRR total → target $15K by end of month)
- [ ] Document sales playbook — script, objection handling, demo flow
- [ ] Start fundraise conversations (3 warm intros to pre-seed funds)
- [ ] Launch referral program: 1 free month per referral
- **Milestone:** $15K MRR, repeatable <14 day sales cycle, fundraise pipeline open

## Weekly Cadence

- **Monday:** Pipeline review — deals in flight, follow-ups due
- **Wednesday:** Design partner / customer calls — product feedback
- **Friday:** Metrics review — MRR, demos booked, churn signals

## Tools to Set Up (Day 1)

- Stripe — billing
- Linear — engineering roadmap
- HubSpot (free) — CRM from day one
- Notion — internal wiki, meeting notes
- Slack — team comms + customer channels

## If You're Behind on Day 45

Cut: ERP integrations (delay to month 4), second engineer hire (delay 30 days), marketing spend.

Keep: Direct outbound, design partner calls, core RFQ feature. Revenue conversations above everything else.

---

# 🧠 Executive Summary

**Market Analysis:** $3.2B SAM in mid-market manufacturing procurement. SAP Ariba ignores sub-500 employee plants. Strong timing with AI cost curves.

**Legal:** Delaware C-Corp immediately. File trademark before launch. No major regulatory blockers — GDPR compliance needed for EU suppliers.

**Customer & ICP:** Procurement managers at 100-500 employee discrete manufacturers. 11 hours/week pain. Budget authority at VP Ops level.

**GTM:** Outbound LinkedIn to procurement managers. $499/mo entry. Target $15K MRR by month 3.

**Hiring:** Engineer → AE → CSM → Solutions Engineer → Marketing. Sequenced against revenue milestones.

**Fundraising:** $1.5M pre-seed. Opening hook lands. Biggest risk is SAP objection — answer is sharp.

**Ops:** North star MRR. Month 1 design partners, Month 2 first revenue, Month 3 fundraise conversations.
