"""
agents/base_agent.py

Base class for all FounderBrain agents.
Every agent: reads shared memory → calls Claude → writes back to memory.
The shared context is what makes agents aware of each other's work.
"""

import time
import os
import json
import anthropic
from memory.shared_memory import SharedMemory, AgentOutput


class BaseAgent:
    name: str = "base"
    description: str = ""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def run(self, memory: SharedMemory) -> AgentOutput:
        """Main entry point. Reads memory, calls Claude, writes output."""
        start = time.time()

        print(f"  [{self.name.upper()}] Starting...")

        # Get full context of what all prior agents found
        context = memory.get_context_for_agent(self.name)

        # Build the prompt specific to this agent
        system_prompt = self._system_prompt()
        user_prompt = self._user_prompt(memory, context)

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            raw = response.content[0].text.strip()
            parsed = self._parse_response(raw)

            output = AgentOutput(
                agent=self.name,
                status="complete",
                summary=parsed.get("summary", ""),
                full_output=parsed.get("full_output", raw),
                key_facts=parsed.get("key_facts", []),
                timestamp=time.time(),
                duration_seconds=round(time.time() - start, 1),
            )

            # Let agent update shared memory fields if relevant
            self._update_memory(memory, parsed)

            print(f"  [{self.name.upper()}] Done in {output.duration_seconds}s")
            return output

        except Exception as e:
            print(f"  [{self.name.upper()}] Error: {e}")
            return AgentOutput(
                agent=self.name,
                status="failed",
                summary=f"Agent failed: {e}",
                full_output="",
                key_facts=[],
                timestamp=time.time(),
            )

    def _system_prompt(self) -> str:
        raise NotImplementedError

    def _user_prompt(self, memory: SharedMemory, context: str) -> str:
        raise NotImplementedError

    def _parse_response(self, raw: str) -> dict:
        """
        Try to parse JSON response. Fall back to treating raw as full_output.
        All agents should return JSON with: summary, full_output, key_facts.
        """
        try:
            clean = raw.replace("```json", "").replace("```", "").strip()
            return json.loads(clean)
        except Exception:
            return {
                "summary": raw[:200],
                "full_output": raw,
                "key_facts": [],
            }

    def _update_memory(self, memory: SharedMemory, parsed: dict):
        """Override in subclasses to update shared memory fields."""
        pass
