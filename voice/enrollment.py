import numpy as np
import sounddevice as sd
import config
from voice.voiceprint_store import VoiceprintStore
from voice.ecapa_encoder import get_encoder


class VoiceEnrollment:
    """One-time voiceprint setup — stores Karan's ECAPA voice vectors in ChromaDB."""

    def __init__(self, store: VoiceprintStore):
        self.encoder = get_encoder()      # shared ECAPA model
        self.store = store

    def is_enrolled(self) -> bool:
        return self.store.is_enrolled()

    def _record_sample(self) -> np.ndarray:
        audio = sd.rec(
            int(config.ENROLL_SECONDS * config.SAMPLE_RATE),
            samplerate=config.SAMPLE_RATE,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        return audio.flatten()

    def enroll(self, tts):
        """Record several samples and store their ECAPA embeddings in Chroma."""
        tts.speak(
            "Let's set up my voice recognition, Karan. "
            f"I'll ask you to read a sentence {config.ENROLL_SAMPLES} times. "
            "Please speak clearly."
        )

        sentences = [
            "My name is Karan and JARVIS is my personal assistant.",
            "Hey JARVIS, this is Karan speaking.",
            "JARVIS, remember the sound of my voice.",
            "I am the only person who can command JARVIS.",
            "This is Karan, confirming my identity.",
        ]

        for i in range(config.ENROLL_SAMPLES):
            sentence = sentences[i % len(sentences)]
            tts.speak(f"Sample {i + 1}. Please say: {sentence}")
            print(f"🎙️  Recording sample {i + 1}/{config.ENROLL_SAMPLES}...")

            audio = self._record_sample()
            embedding = self.encoder.embed(audio)
            self.store.add_voiceprint(embedding, sample_id=f"karan_{i}")
            print(f"   ✅ Sample {i + 1} stored in ChromaDB.")

        tts.speak("Perfect. Your voiceprint is saved. I'll recognize you from now on.")
        print("✅ Enrollment complete —", config.ENROLL_SAMPLES, "ECAPA vectors stored.")