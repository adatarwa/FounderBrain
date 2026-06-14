"""
main.py
FounderBrain — entry point.

Usage:
  python main.py                          # interactive
  python main.py "my startup description" # direct
  python main.py --resume RUN_ID          # resume failed run
"""

import sys
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

from orchestrator import Orchestrator
from output.report import generate_report, print_summary


PURPLE = "\033[95m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
GRAY   = "\033[90m"
YELLOW = "\033[93m"
RESET  = "\033[0m"


def header():
    print(f"""
{PURPLE}{BOLD}  ╔══════════════════════════════════════╗
  ║         FounderBrain v2.0            ║
  ║   Multi-agent startup co-pilot       ║
  ╚══════════════════════════════════════╝{RESET}

  7 specialist AI agents. One cohesive startup OS.
  Market · Legal · Customer · GTM · Hiring · Fundraising · Ops

{GRAY}  Agents run in parallel waves.
  Each one reads what the previous ones found.
  Nothing repeated. Everything connected.{RESET}
""")


def check_api_key():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print(f"""
  {YELLOW}⚠  ANTHROPIC_API_KEY is not set.{RESET}

  Fix it in 3 steps:
  1. Copy the config file:   cp .env.example .env
  2. Open .env in any editor
  3. Replace 'your_key_here' with your actual key

  Get a free key at: https://console.anthropic.com

""")
        sys.exit(1)


def get_input() -> tuple[str, str]:
    """Interactive input — asks what the founder is building."""
    print(f"{CYAN}  What are you building?{RESET}")
    print(f"  {GRAY}Be specific — industry, who you sell to, what problem you solve.{RESET}")
    print(f"  {GRAY}Example: 'AI tool for procurement teams in manufacturing to automate RFQ processing'{RESET}\n")

    description = input(f"  {BOLD}>{RESET} ").strip()
    if not description:
        print(f"  {YELLOW}Please describe your startup.{RESET}")
        sys.exit(1)

    print(f"\n{CYAN}  What's the startup name? (press Enter to skip){RESET}")
    name = input(f"  {BOLD}>{RESET} ").strip() or "My Startup"
    return description, name


def main():
    header()
    check_api_key()

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--resume", metavar="RUN_ID", help="Resume a previous run from checkpoint")
    parser.add_argument("description", nargs="*", help="Startup description")
    args = parser.parse_args()

    orchestrator = Orchestrator()

    # Resume mode
    if args.resume:
        print(f"  {CYAN}Resuming run {args.resume}...{RESET}\n")
        print("  " + "─" * 50 + "\n")
        memory = orchestrator.run(
            founder_input="",
            startup_name="",
            resume_id=args.resume
        )

    # Direct CLI mode: python main.py "my startup"
    elif args.description:
        description = " ".join(args.description)
        name = "My Startup"
        print(f"  {GRAY}Running for: {description[:80]}{RESET}\n")
        print("  " + "─" * 50 + "\n")
        memory = orchestrator.run(description, name)

    # Interactive mode
    else:
        description, name = get_input()
        print(f"\n  {GRAY}Starting agent run for: {name}{RESET}\n")
        print("  " + "─" * 50 + "\n")
        memory = orchestrator.run(description, name)

    # Output
    print_summary(memory)
    report_path = generate_report(memory)
    print(f"  Full report saved → {report_path}\n")
    print(f"  {GRAY}Run ID: {memory.run_id} (use --resume {memory.run_id} if you need to retry){RESET}\n")
    print(f"{PURPLE}{BOLD}  FounderBrain complete.{RESET}\n")


if __name__ == "__main__":
    main()
