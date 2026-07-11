import config
from voice.voiceprint_store import VoiceprintStore
from voice.ecapa_encoder import get_encoder


class SpeakerVerifier:
    """Verifies a voice sample against Karan's ECAPA voiceprint (cosine, via ChromaDB)."""

    def __init__(self, store: VoiceprintStore):
        self.encoder = get_encoder()      # shared ECAPA model
        self.store = store

    def verify(self, audio):
        """
        Returns (is_karan, similarity_score).
        """
        try:
            embedding = self.encoder.embed(audio)
            similarity, owner = self.store.verify(embedding)

            is_karan = (owner == "karan") and (similarity >= config.SPEAKER_THRESHOLD)
            return is_karan, similarity
        except Exception as e:
            print(f"   ❌ [Speaker verify error: {e}]")
            return False, 0.0