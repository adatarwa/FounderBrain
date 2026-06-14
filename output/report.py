"""
output/report.py
Assembles all agent outputs into a single beautiful markdown report.
Saves to ~/FounderBrain/reports/ for the founder to keep.
"""

import os
from pathlib import Path
from datetime import datetime
from memory.shared_memory import SharedMemory


REPORTS_DIR = Path.home() / "FounderBrain" / "reports"


def generate_report(memory: SharedMemory) -> str:
    """Generate full markdown report from all agent outputs."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    filename = f"{memory.startup_name.replace(' ', '_')}_{now.strftime('%Y%m%d_%H%M%S')}.md"
    output_path = REPORTS_DIR / filename

    sections = []

    # Header
    sections.append(f"""# FounderBrain Report
## {memory.startup_name}
*Generated {now.strftime('%B %d, %Y at %I:%M %p')} · Run ID: {memory.run_id}*

---

> **Founder input:** {memory.founder_input}

---
""")

    # Agent outputs
    agents = [
        ("market_output",      "Market Analysis",        "📊"),
        ("customer_output",    "Customer & ICP",         "🎯"),
        ("gtm_output",         "Go-To-Market Strategy",  "🚀"),
        ("hiring_output",      "Hiring Plan",            "👥"),
        ("fundraising_output", "Fundraising & Pitch",    "💰"),
        ("ops_output",         "90-Day Ops Plan",        "📅"),
    ]

    for attr, title, emoji in agents:
        output = getattr(memory, attr)
        if output and output.status == "complete":
            sections.append(f"# {emoji} {title}\n")
            sections.append(output.full_output)
            sections.append("\n---\n")
        else:
            sections.append(f"# {emoji} {title}\n\n*Agent did not complete.*\n\n---\n")

    # Conflicts resolved
    if memory.conflicts_resolved:
        sections.append("# ⚖️ Conflicts Resolved Between Agents\n")
        for c in memory.conflicts_resolved:
            sections.append(f"**Issue:** {c['conflict']}  ")
            sections.append(f"**Resolution:** {c['resolution']}\n")
        sections.append("\n---\n")

    # Summary card
    sections.append("# 🧠 Executive Summary\n")
    for attr, title, emoji in agents:
        output = getattr(memory, attr)
        if output and output.status == "complete":
            sections.append(f"**{title}:** {output.summary}\n")

    content = "\n".join(sections)
    output_path.write_text(content)

    return str(output_path)


def print_summary(memory: SharedMemory):
    """Print a clean terminal summary after all agents complete."""
    GREEN  = "\033[92m"
    CYAN   = "\033[96m"
    PURPLE = "\033[95m"
    BOLD   = "\033[1m"
    GRAY   = "\033[90m"
    RESET  = "\033[0m"

    print(f"\n{PURPLE}{BOLD}{'─' * 60}{RESET}")
    print(f"{PURPLE}{BOLD}  FounderBrain — {memory.startup_name}{RESET}")
    print(f"{PURPLE}{BOLD}{'─' * 60}{RESET}\n")

    agents = [
        ("market_output",      "Market",      "📊"),
        ("customer_output",    "Customer",    "🎯"),
        ("gtm_output",         "GTM",         "🚀"),
        ("hiring_output",      "Hiring",      "👥"),
        ("fundraising_output", "Fundraising", "💰"),
        ("ops_output",         "Ops",         "📅"),
    ]

    for attr, label, emoji in agents:
        output = getattr(memory, attr)
        if output and output.status == "complete":
            status = f"{GREEN}✓{RESET}"
            summary = output.summary[:75] + "..." if len(output.summary) > 75 else output.summary
            print(f"  {status} {emoji} {BOLD}{label:<14}{RESET} {GRAY}{summary}{RESET}")
        else:
            print(f"  {CYAN}✗{RESET} {emoji} {BOLD}{label:<14}{RESET} {GRAY}Failed{RESET}")

    print()
