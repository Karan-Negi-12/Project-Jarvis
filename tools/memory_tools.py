def register_memory_tools(registry, memory_manager):
    """Register memory tools, wired to the shared MemoryManager."""

    def save_memory(memory_type: str, content: str):
        return memory_manager.remember_fact(memory_type, content)

    def recall_memory():
        return memory_manager.summary()

    registry.register(
        name="save_memory",
        func=save_memory,
        description=(
            "Save an important, durable piece of information about Karan "
            "(a fact, preference, project, or goal). Use this whenever Karan "
            "shares something worth remembering long-term."
        ),
        parameters={
            "type": "object",
            "properties": {
                "memory_type": {
                    "type": "string",
                    "description": "One of: fact, preference, project, goal.",
                },
                "content": {
                    "type": "string",
                    "description": "The information to remember, in a clear sentence.",
                },
            },
            "required": ["memory_type", "content"],
        },
    )

    registry.register(
        name="recall_memory",
        func=recall_memory,
        description="Retrieve everything JARVIS remembers about Karan.",
    )