import pyttsx3
import config


class TextToSpeech:
    """Speaks text aloud using offline pyttsx3 (fresh engine per call = most reliable)."""

    def speak(self, text: str):
        if not text:
            return
        print(f"🔊 JARVIS: {text}")
        try:
            engine = pyttsx3.init()                       # fresh engine each call
            engine.setProperty("rate", config.TTS_RATE)

            voices = engine.getProperty("voices")
            if voices and config.TTS_VOICE_INDEX < len(voices):
                engine.setProperty("voice", voices[config.TTS_VOICE_INDEX].id)

            engine.say(text)
            engine.runAndWait()
            engine.stop()                                 # clean shutdown
        except Exception as e:
            print(f"   ❌ [TTS error: {e}]")