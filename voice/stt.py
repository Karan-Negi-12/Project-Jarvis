import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
import config

class SpeechToText:
    """Records mic audio and transcribes it locally with faster-whisper."""

    def __init__(self):
        print("🎤 Loading Whisper model (first run downloads it)...")
        # compute_type="int8" keeps it light on CPU
        self.model = WhisperModel(
            config.WHISPER_MODEL, device="cpu", compute_type="int8"
        )
        print("✅ Whisper ready.")

    def record(self, seconds: int = None) -> np.ndarray:
        """Record audio from the microphone."""
        seconds = seconds or config.RECORD_SECONDS
        print(f"🎙️  Listening for {seconds}s... (speak now)")
        audio = sd.rec(
            int(seconds * config.SAMPLE_RATE),
            samplerate=config.SAMPLE_RATE,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        return audio.flatten()

    def transcribe(self, audio: np.ndarray) -> str:
        """Convert recorded audio into text."""
        segments, _ = self.model.transcribe(audio, language="en")
        text = " ".join(seg.text for seg in segments).strip()
        return text

    def listen(self, seconds: int = None) -> str:
        """Record + transcribe in one call."""
        audio = self.record(seconds)
        print("🧠 Transcribing...")
        text = self.transcribe(audio)
        return text