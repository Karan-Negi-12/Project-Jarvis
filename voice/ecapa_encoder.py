import numpy as np
import torch
from speechbrain.inference.speaker import EncoderClassifier
from speechbrain.utils.fetching import LocalStrategy   # ✅ import strategy
import config


class ECAPAEncoder:
    """
    Speaker-embedding encoder using SpeechBrain's ECAPA-TDNN model.
    Produces a 192-dim voiceprint that strongly separates speakers.
    """

    _instance = None  # cache so we don't reload the model repeatedly

    def __init__(self):
        print("🔊 Loading ECAPA-TDNN speaker model...")
        self.model = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir=config.ECAPA_MODEL_DIR,
            run_opts={"device": "cpu"},
            local_strategy=LocalStrategy.COPY,   # ✅ COPY instead of SYMLINK (Windows-safe)
        )
        print("✅ ECAPA speaker model ready.")

    def embed(self, audio) -> np.ndarray:
        """Convert raw mono float32 audio (16kHz) into a 192-dim voiceprint."""
        audio = np.asarray(audio, dtype="float32").flatten()
        wav = torch.from_numpy(audio).unsqueeze(0)

        with torch.no_grad():
            emb = self.model.encode_batch(wav)

        return emb.squeeze().detach().cpu().numpy()


def get_encoder() -> "ECAPAEncoder":
    """Singleton accessor so the model loads only once."""
    if ECAPAEncoder._instance is None:
        ECAPAEncoder._instance = ECAPAEncoder()
    return ECAPAEncoder._instance