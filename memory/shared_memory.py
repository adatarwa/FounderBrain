"""
memory/shared_memory.py

The central nervous system of FounderBrain.
Every agent reads from and writes to this shared store.
Each new agent has full context of what every prior agent discovered.
This is what makes it a real multi-agent system — not just chained prompts.
"""

import json
import time
from dataclasses import dataclass, field, asdict
from typing import Any
from pathlib import Path


@dataclass
class AgentOutput:
    agent: str
    status: str          # "running" | "complete" | "failed"
    summary: str         # Short summary for other agents to read
    full_output: str     # Complete detailed output
    key_facts: list      # Bullet facts extracted for cross-agent use
    timestamp: float     # When this was written
    duration_seconds: float = 0.0


@dataclass
class SharedMemory:
    """
    The shared context object passed between all agents.
    Each agent reads everything written before it,
    then writes its own AgentOutput back here.
    """
    # Founder's original input
    founder_input: str = ""
    startup_name: str = ""

    # What we know about the startup (filled by agents progressively)
    industry: str = ""
    target_customer: str = ""
    problem_statement: str = ""
    solution: str = ""
    business_model: str = ""
    geography: str = ""
    stage: str = ""

    # Agent outputs (written as each agent completes)
    market_output: AgentOutput = None
    customer_output: AgentOutput = None
    gtm_output: AgentOutput = None
    hiring_output: AgentOutput = None
    fundraising_output: AgentOutput = None
    ops_output: AgentOutput = None

    # Orchestrator meta
    run_id: str = ""
    start_time: float = field(default_factory=time.time)
    conflicts_resolved: list = field(default_factory=list)

    def get_context_for_agent(self, agent_name: str) -> str:
        """
        Returns a formatted context string for an agent to read.
        Contains everything discovered so far by prior agents.
        This is the key to inter-agent communication.
        """
        lines = [
            f"=== FOUNDERBRAIN SHARED CONTEXT ===",
            f"Startup: {self.startup_name or 'Unknown'}",
            f"Founder input: {self.founder_input}",
            "",
            "--- What we know so far ---",
        ]

        if self.industry:
            lines.append(f"Industry: {self.industry}")
        if self.target_customer:
            lines.append(f"Target customer: {self.target_customer}")
        if self.problem_statement:
            lines.append(f"Problem: {self.problem_statement}")
        if self.solution:
            lines.append(f"Solution: {self.solution}")
        if self.business_model:
            lines.append(f"Business model: {self.business_model}")
        if self.geography:
            lines.append(f"Geography: {self.geography}")
        if self.stage:
            lines.append(f"Stage: {self.stage}")

        lines.append("")
        lines.append("--- Outputs from agents that ran before you ---")

        completed = []
        for attr in ["market_output", "customer_output", "gtm_output",
                     "hiring_output", "fundraising_output", "ops_output"]:
            output = getattr(self, attr)
            if output and output.status == "complete":
                completed.append(output)

        if not completed:
            lines.append("(You are the first agent to run)")
        else:
            for out in completed:
                lines.append(f"\n[{out.agent.upper()} AGENT — completed]")
                lines.append(f"Summary: {out.summary}")
                if out.key_facts:
                    lines.append("Key facts:")
                    for fact in out.key_facts:
                        lines.append(f"  • {fact}")

        lines.append(f"\n=== YOU ARE: {agent_name.upper()} AGENT ===")
        lines.append("Build on everything above. Don't repeat what other agents said.")
        lines.append("Your output will be read by agents that run after you.\n")

        return "\n".join(lines)

    def write_output(self, agent_name: str, output: AgentOutput):
        """Write an agent's completed output to shared memory."""
        attr_map = {
            "market": "market_output",
            "customer": "customer_output",
            "gtm": "gtm_output",
            "hiring": "hiring_output",
            "fundraising": "fundraising_output",
            "ops": "ops_output",
        }
        attr = attr_map.get(agent_name.lower())
        if attr:
            setattr(self, attr, output)

    def is_complete(self) -> bool:
        """True when all six agents have finished."""
        outputs = [
            self.market_output, self.customer_output, self.gtm_output,
            self.hiring_output, self.fundraising_output, self.ops_output
        ]
        return all(o and o.status == "complete" for o in outputs)

    def save(self, path: str):
        """Save full memory state to JSON for inspection/resume."""
        data = {
            "founder_input": self.founder_input,
            "startup_name": self.startup_name,
            "run_id": self.run_id,
            "agents": {}
        }
        for attr in ["market_output", "customer_output", "gtm_output",
                     "hiring_output", "fundraising_output", "ops_output"]:
            output = getattr(self, attr)
            if output:
                data["agents"][attr] = asdict(output)
        Path(path).write_text(json.dumps(data, indent=2))


# Monkey-patch legal_output into SharedMemory
# (cleaner than modifying the dataclass directly for backward compat)
SharedMemory.legal_output = None

_original_write = SharedMemory.write_output
def _new_write(self, agent_name, output):
    if agent_name.lower() == "legal":
        self.legal_output = output
    else:
        _original_write(self, agent_name, output)
SharedMemory.write_output = _new_write

_original_context = SharedMemory.get_context_for_agent
def _new_context(self, agent_name):
    base = _original_context(self, agent_name)
    if self.legal_output and self.legal_output.status == "complete":
        addition = f"\n[LEGAL AGENT — completed]\nSummary: {self.legal_output.summary}\n"
        if self.legal_output.key_facts:
            addition += "Key facts:\n" + "\n".join(f"  • {f}" for f in self.legal_output.key_facts)
        base = base.replace("(You are the first agent to run)", "").replace(
            f"=== YOU ARE: {agent_name.upper()} AGENT ===",
            addition + f"\n=== YOU ARE: {agent_name.upper()} AGENT ==="
        )
    return base
SharedMemory.get_context_for_agent = _new_context
