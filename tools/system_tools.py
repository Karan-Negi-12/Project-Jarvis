import os
import platform
import datetime
import pyautogui


def take_screenshot():
    """Capture the screen and save it with a timestamp."""
    try:
        os.makedirs("data/screenshots", exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"data/screenshots/shot_{ts}.png"
        img = pyautogui.screenshot()
        img.save(path)
        return f"Screenshot saved to {path}."
    except Exception as e:
        return f"Couldn't take screenshot: {e}"


def set_volume(direction: str):
    """Increase, decrease, or mute system volume."""
    try:
        direction = direction.lower()
        if direction == "up":
            for _ in range(5):
                pyautogui.press("volumeup")
            return "Volume increased."
        elif direction == "down":
            for _ in range(5):
                pyautogui.press("volumedown")
            return "Volume decreased."
        elif direction == "mute":
            pyautogui.press("volumemute")
            return "Volume muted/unmuted."
        return "Use 'up', 'down', or 'mute'."
    except Exception as e:
        return f"Couldn't change volume: {e}"


def lock_screen():
    """Lock the computer screen."""
    try:
        system = platform.system()
        if system == "Windows":
            import ctypes
            ctypes.windll.user32.LockWorkStation()
        elif system == "Darwin":
            os.system("pmset displaysleepnow")
        else:
            os.system("xdg-screensaver lock")
        return "Screen locked."
    except Exception as e:
        return f"Couldn't lock screen: {e}"


def register_system_tools(registry):
    registry.register(
        name="take_screenshot",
        func=take_screenshot,
        description="Capture a screenshot of the current screen.",
    )

    registry.register(
        name="set_volume",
        func=set_volume,
        description="Change system volume. direction must be 'up', 'down', or 'mute'.",
        parameters={
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "description": "One of: up, down, mute.",
                }
            },
            "required": ["direction"],
        },
    )

    registry.register(
        name="lock_screen",
        func=lock_screen,
        description="Lock the computer screen.",
        sensitive=True,   # 🔐 disruptive -> confirm first
    )