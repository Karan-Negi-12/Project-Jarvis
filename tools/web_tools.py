import requests
import config


def web_search(query: str):
    """Search the web using Google Custom Search API."""
    if not config.GOOGLE_SEARCH_API_KEY or not config.GOOGLE_SEARCH_ENGINE_ID:
        return "Web search isn't configured. Add GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID to .env."

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": config.GOOGLE_SEARCH_API_KEY,
        "cx": config.GOOGLE_SEARCH_ENGINE_ID,
        "q": query,
        "num": 3,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if not items:
            return f"No results found for '{query}'."

        results = []
        for it in items:
            title = it.get("title", "")
            snippet = it.get("snippet", "")
            link = it.get("link", "")
            results.append(f"• {title}\n  {snippet}\n  {link}")
        return "\n\n".join(results)
    except Exception as e:
        return f"Web search failed: {e}"


def register_web_tools(registry):
    registry.register(
        name="web_search",
        func=web_search,
        description="Search the web for current information using Google Search.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query."}
            },
            "required": ["query"],
        },
    )
