import subprocess
import platform
from datetime import datetime


def get_time():
    """Return the current date and time as a friendly string."""
    now = datetime.now()
    return now.strftime("It's %A, %d %B %Y, %I:%M %p.")


def open_app(app_name: str):
    """Open an application on the laptop by name."""
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen(["cmd", "/c", "start", "", app_name], shell=False)
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", app_name])
        else:  # Linux
            subprocess.Popen([app_name])
        return f"Opening {app_name}."
    except Exception as e:
        return f"Couldn't open {app_name}: {e}"


def register_basic_tools(registry):
    """Register all basic tools into the given registry."""
    registry.register(
        name="get_time",
        func=get_time,
        description="Get the current date and time.",
    )
    registry.register(
        name="open_app",
        func=open_app,
        description="Open an application on the laptop by its name, e.g. notepad, calc, code.",
        parameters={
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the application to open.",
                }
            },
            "required": ["app_name"],
        },
    )