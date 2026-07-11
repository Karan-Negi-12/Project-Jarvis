class PermissionManager:
    """
    Confirms sensitive actions (send/delete/post/create) before they run.
    In Phase 3 it asks via text input. Later (voice phase) we just swap
    the `ask` function for a spoken yes/no — the rest stays the same.
    """

    def __init__(self, confirm_func=None):
        # Default confirmation = terminal input
        self.confirm_func = confirm_func or self._default_confirm

    def _default_confirm(self, message: str) -> bool:
        answer = input(f"\n⚠️  {message} (yes/no): ").strip().lower()
        return answer in {"yes", "y", "yeah", "yep", "confirm", "ok"}

    def request(self, tool_name: str, args: dict) -> bool:
        """Ask Karan to approve a sensitive action."""
        pretty_args = ", ".join(f"{k}={v}" for k, v in args.items())
        message = f"JARVIS wants to run '{tool_name}' ({pretty_args}). Allow this?"
        return self.confirm_func(message)