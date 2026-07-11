import os
import sqlite3

from memory.working_memory import WorkingMemory
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory


class MemoryManager:
    """Coordinates working, short-term, and long-term memory."""

    def __init__(self, db_path: str = "memory/memory.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # check_same_thread=False so it's safe for later voice threads
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

        self.working = WorkingMemory()
        self.short = ShortTermMemory(self.conn)
        self.long = LongTermMemory(self.conn)

    # ---------- WRITE ----------
    def remember_fact(self, memory_type: str, content: str) -> str:
        """Save something durable about Karan."""
        valid = {"fact", "preference", "project", "goal"}
        if memory_type not in valid:
            memory_type = "fact"
        return self.long.add(memory_type, content)

    def log_interaction(self, role: str, content: str):
        """Record a turn into short-term memory."""
        self.short.add(role, content)

    # ---------- READ ----------
    def build_memory_context(self) -> str:
        """
        Build the text block injected into the system prompt so
        JARVIS 'knows' Karan every turn.
        """
        parts = []

        long_mems = self.long.get_all()
        if long_mems:
            parts.append("What you know about Karan:")
            for mtype, content in long_mems:
                parts.append(f"- ({mtype}) {content}")

        recent = self.short.get_recent()
        if recent:
            parts.append("\nRecent interactions:")
            for role, content, _ in recent:
                parts.append(f"- {role}: {content}")

        if not parts:
            return "You don't have any stored memories about Karan yet."

        return "\n".join(parts)

    def summary(self) -> str:
        """Human-readable dump for 'what do you know about me?'"""
        long_mems = self.long.get_all()
        if not long_mems:
            return "I don't know anything about you yet, Karan."
        lines = [f"- {content}" for _, content in long_mems]
        return "Here's what I remember about you:\n" + "\n".join(lines)

    def close(self):
        self.conn.close()