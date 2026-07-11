from google.genai import types


class WorkingMemory:
    """The active conversation for THIS session (in RAM)."""

    def __init__(self, max_turns: int = 20):
        self.history = []          # list of types.Content
        self.max_turns = max_turns # keep last N turns to control tokens

    def add_user(self, text: str):
        self.history.append(
            types.Content(role="user", parts=[types.Part(text=text)])
        )
        self._trim()

    def add_model(self, text: str):
        self.history.append(
            types.Content(role="model", parts=[types.Part(text=text)])
        )
        self._trim()

    def add_raw(self, content):
        """For tool-call / tool-response Content objects."""
        self.history.append(content)
        self._trim()

    def get(self):
        return self.history

    def _trim(self):
        # Keep the history from growing forever (protect token budget)
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]

    def clear(self):
        self.history = []