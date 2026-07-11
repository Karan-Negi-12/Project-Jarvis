import time
import numpy as np
import sounddevice as sd
from openwakeword.model import Model
import config


class WakeWordListener:
    """Always-on 'Hey Jarvis' listener with anti-feedback protection."""

    def __init__(self):
        print("🎙️  Loading wake word model...")
        self.model = Model(
            wakeword_models=[config.WAKE_WORD_MODEL],
            inference_framework="onnx",
        )
        self.chunk = 1280  # 80ms @ 16kHz
        print("✅ Wake word ready. Say 'Hey Jarvis' to activate.")

    def _reset_model(self):
        """Clear openWakeWord's internal prediction buffer to stop stale re-triggers."""
        try:
            self.model.reset()
        except Exception:
            # Fallback for versions without reset(): manually clear buffers
            for k in self.model.prediction_buffer:
                self.model.prediction_buffer[k].clear()

    def wait_for_wake(self, warmup_frames: int = 15):
        # 1. 🧠 Reset stale buffer so old audio can't re-trigger
        self._reset_model()

        with sd.InputStream(
            samplerate=config.SAMPLE_RATE,
            channels=1,
            dtype="int16",
            blocksize=self.chunk,
        ) as stream:
            # 2. 🚿 Flush leftover mic audio (JARVIS's own voice tail, echo)
            for _ in range(warmup_frames):
                stream.read(self.chunk)
            self._reset_model()  # reset again after flushing

            # 3. 👂 Now actually listen
            while True:
                audio, _ = stream.read(self.chunk)
                audio = np.frombuffer(audio, dtype=np.int16)

                prediction = self.model.predict(audio)
                score = prediction.get(config.WAKE_WORD_MODEL, 0)

                if score >= config.WAKE_THRESHOLD:
                    print(f"   🔔 Wake word detected! (score: {score:.2f})")
                    # 4. 🕒 Small cooldown so the trigger word itself
                    #    doesn't bleed into the command recording
                    time.sleep(0.3)
                    return True