"""
orchestrator.py
Master controller of FounderBrain.
Now supports parallel execution for independent agents.
Manages shared memory, conflict detection, and checkpoint/resume.
"""

import time
import uuid
import os
import json
import anthropic
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from memory.shared_memory import SharedMemory, AgentOutput
from agents.market_agent import MarketAgent
from agents.customer_agent import CustomerAgent
from agents.gtm_agent import GTMAgent
from agents.hiring_agent import HiringAgent
from agents.fundraising_agent import FundraisingAgent
from agents.ops_agent import OpsAgent
from agents.legal_agent import LegalAgent

PURPLE = "\033[95m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
GRAY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

CHECKPOINT_DIR = Path.home() / "FounderBrain" / "checkpoints"

# Execution plan:
# Wave 1 (parallel): Market + Legal — independent, no dependencies
# Wave 2 (parallel): Customer + GTM — both need market data
# Wave 3 (parallel): Hiring + Fundraising — both need GTM
# Wave 4 (sequential): Ops — needs everything
EXECUTION_WAVES = [
    ["market", "legal"],           # Wave 1 — parallel
    ["customer", "gtm"],           # Wave 2 — parallel (needs wave 1)
    ["hiring", "fundraising"],     # Wave 3 — parallel (needs wave 2)
    ["ops"],                       # Wave 4 — sequential (needs all)
]

AGENT_MAP = {
    "market":      MarketAgent,
    "customer":    CustomerAgent,
    "gtm":         GTMAgent,
    "hiring":      HiringAgent,
    "fundraising": FundraisingAgent,
    "ops":         OpsAgent,
    "legal":       LegalAgent,
}


class Orchestrator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    def run(self, founder_input: str, startup_name: str = "My Startup",
            resume_id: str = None) -> SharedMemory:
        """
        Run all agents with parallel execution where possible.
        Supports resume from checkpoint if resume_id provided.
        """
        # Load or create memory
        if resume_id:
            memory = self._load_checkpoint(resume_id)
            if memory:
                print(f"  {GREEN}Resuming from checkpoint {resume_id}{RESET}\n")
            else:
                print(f"  {YELLOW}Checkpoint not found — starting fresh{RESET}\n")
                memory = self._new_memory(founder_input, startup_name)
        else:
            memory = self._new_memory(founder_input, startup_name)

        print(f"\n{PURPLE}{BOLD}FounderBrain{RESET} — {startup_name}")
        print(f"{GRAY}Run ID: {memory.run_id}{RESET}\n")
        print(f"{BOLD}Running agents in parallel waves...{RESET}\n")

        total_start = time.time()

        for wave_idx, wave in enumerate(EXECUTION_WAVES):
            # Filter out already-completed agents (for resume)
            pending = [name for name in wave
                       if not self._is_complete(memory, name)]

            if not pending:
                print(f"  {GRAY}Wave {wave_idx+1} — already complete, skipping{RESET}")
                continue

            if len(pending) == 1:
                print(f"\n{CYAN}Wave {wave_idx+1}{RESET} — {pending[0].upper()}")
                self._run_single(pending[0], memory)
            else:
                print(f"\n{CYAN}Wave {wave_idx+1}{RESET} — running {' + '.join(p.upper() for p in pending)} in parallel")
                self._run_parallel(pending, memory)

            # Save checkpoint after each wave
            self._save_checkpoint(memory)

        # Detect and resolve conflicts
        conflicts = self._detect_conflicts(memory)
        if conflicts:
            print(f"\n{YELLOW}Resolving {len(conflicts)} conflict(s)...{RESET}")
            memory.conflicts_resolved = self._resolve_conflicts(memory, conflicts)

        elapsed = round(time.time() - total_start, 1)
        print(f"\n{GREEN}{BOLD}All agents complete in {elapsed}s{RESET}\n")

        return memory

    def _run_single(self, agent_name: str, memory: SharedMemory):
        AgentClass = AGENT_MAP[agent_name]
        agent = AgentClass()
        print(f"  → {agent.description}")
        output = agent.run(memory)
        memory.write_output(agent_name, output)
        if output.status == "complete":
            print(f"  {GREEN}✓{RESET} {output.summary[:90]}\n")
        else:
            print(f"  {YELLOW}✗ Failed{RESET}\n")

    def _run_parallel(self, agent_names: list, memory: SharedMemory):
        """Run multiple agents simultaneously using thread pool."""
        results = {}

        def run_agent(name):
            AgentClass = AGENT_MAP[name]
            agent = AgentClass()
            return name, agent.run(memory)

        with ThreadPoolExecutor(max_workers=len(agent_names)) as ex:
            futures = {ex.submit(run_agent, name): name for name in agent_names}
            for future in as_completed(futures):
                name, output = future.result()
                results[name] = output

        # Write results to memory in deterministic order
        for name in agent_names:
            output = results.get(name)
            if output:
                memory.write_output(name, output)
                status = f"{GREEN}✓{RESET}" if output.status == "complete" else f"{YELLOW}✗{RESET}"
                print(f"  {status} [{name.upper()}] {output.summary[:80]}")
        print()

    def _is_complete(self, memory: SharedMemory, agent_name: str) -> bool:
        attr_map = {
            "market": "market_output", "customer": "customer_output",
            "gtm": "gtm_output", "hiring": "hiring_output",
            "fundraising": "fundraising_output", "ops": "ops_output",
            "legal": "legal_output",
        }
        attr = attr_map.get(agent_name)
        if not attr:
            return False
        output = getattr(memory, attr, None)
        return output and output.status == "complete"

    def _new_memory(self, founder_input: str, startup_name: str) -> SharedMemory:
        memory = SharedMemory(
            founder_input=founder_input,
            startup_name=startup_name,
            run_id=str(uuid.uuid4())[:8],
        )
        return memory

    def _save_checkpoint(self, memory: SharedMemory):
        """Save memory state after each wave for resume capability."""
        path = CHECKPOINT_DIR / f"{memory.run_id}.json"
        memory.save(str(path))

    def _load_checkpoint(self, run_id: str) -> SharedMemory:
        """Load memory from a previous checkpoint."""
        path = CHECKPOINT_DIR / f"{run_id}.json"
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text())
            memory = SharedMemory(
                founder_input=data.get("founder_input", ""),
                startup_name=data.get("startup_name", ""),
                run_id=run_id,
            )
            return memory
        except Exception:
            return None

    def _detect_conflicts(self, memory: SharedMemory) -> list:
        conflicts = []
        if memory.gtm_output and memory.customer_output:
            gtm = " ".join(memory.gtm_output.key_facts or []).lower()
            cust = " ".join(memory.customer_output.key_facts or []).lower()
            if "enterprise" in gtm and "smb" in cust:
                conflicts.append({"agents": ["gtm", "customer"],
                                  "issue": "GTM targets enterprise but ICP is SMB"})
        return conflicts

    def _resolve_conflicts(self, memory: SharedMemory, conflicts: list) -> list:
        resolved = []
        for conflict in conflicts:
            try:
                r = self.client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=120,
                    messages=[{"role": "user", "content":
                        f"Resolve this startup strategy conflict in one sentence: {conflict['issue']}\n"
                        f"Market: {memory.market_output.summary if memory.market_output else 'N/A'}\n"
                        f"Customer: {memory.customer_output.summary if memory.customer_output else 'N/A'}\n"
                        f"GTM: {memory.gtm_output.summary if memory.gtm_output else 'N/A'}"}]
                )
                resolution = r.content[0].text.strip()
                resolved.append({"conflict": conflict["issue"], "resolution": resolution})
                print(f"  {GREEN}✓{RESET} {resolution[:80]}")
            except Exception as e:
                resolved.append({"conflict": conflict["issue"], "resolution": str(e)})
        return resolved
