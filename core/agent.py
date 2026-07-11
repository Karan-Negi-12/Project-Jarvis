from google.genai import types
import config


class Agent:
    """ReAct brain with 3-layer memory: Reason -> Act -> Observe."""

    def __init__(self, llm, tools, memory):
        self.llm = llm
        self.tools = tools
        self.memory = memory  # MemoryManager

    def run(self, user_input: str) -> str:
        # Log + add to working memory
        self.memory.log_interaction("user", user_input)
        self.memory.working.add_user(user_input)

        # Build the fresh system prompt WITH memory injected
        memory_context = self.memory.build_memory_context()
        system_prompt = config.SYSTEM_PROMPT.format(memory_context=memory_context)

        for step in range(config.MAX_STEPS):
            response = self.llm.think(self.memory.working.get(), system_prompt)

            if response is None:
                return "I couldn't reach my brain just now, Karan. Check the API/quota."

            candidate = response.candidates[0]
            parts = candidate.content.parts

            # Look for a tool call
            tool_call = None
            for part in parts:
                if hasattr(part, "function_call") and part.function_call:
                    tool_call = part.function_call
                    break

            if tool_call:
                # ---- ACT ----
                tool_name = tool_call.name
                args = dict(tool_call.args) if tool_call.args else {}
                print(f"   🔧 [JARVIS uses tool: {tool_name}({args})]")

                result = self.tools.execute(tool_name, args)

                # Save request + result into working memory
                self.memory.working.add_raw(candidate.content)
                self.memory.working.add_raw(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(
                                function_response=types.FunctionResponse(
                                    name=tool_name,
                                    response={"result": result},
                                )
                            )
                        ],
                    )
                )
                # ---- OBSERVE ---- loop again
                continue

            # Final answer
            final_text = response.text
            self.memory.working.add_model(final_text)
            self.memory.log_interaction("jarvis", final_text)
            return final_text

        return "I hit my step limit on that one, Karan. Want me to keep going?"