from google import genai
from google.genai import types
from google.genai.errors import ClientError
import config


class GeminiLLM:
    """Gemini wrapper with function-calling + dynamic system prompt."""

    def __init__(self, tool_schemas=None):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model = config.MODEL_NAME
        self.tool_schemas = tool_schemas or []

    def think(self, contents, system_instruction: str):
        tools = None
        if self.tool_schemas:
            tools = [types.Tool(function_declarations=self.tool_schemas)]

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=tools,
                    temperature=0.7,
                ),
            )
            return response
        except ClientError as e:
            print(f"\n⚠️ Gemini API error: {e}")
            return None