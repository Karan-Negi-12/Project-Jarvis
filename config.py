import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")


# LLM
MODEL_NAME = "gemini-3.1-flash-lite"
MAX_STEPS = 5


# Speech-to-Text
WHISPER_MODEL = "base" # tiny | base | small | medium (bigger = slower/accurate)
SAMPLE_RATE = 16000 # Whisper expects 16kHz
RECORD_SECONDS = 7 # how long to listen per turn


# Text-to-Speech
TTS_RATE = 175 # speech speed (words per min)
TTS_VOICE_INDEX = 0 # 0 or 1 — try both to pick a voice you like


# --- Phase 6: Wake word + Speaker ID ---
CHROMA_DB_PATH = "data/chroma_voiceprints"
WAKE_WORD_MODEL = "hey_jarvis"      # openWakeWord has a built-in "hey_jarvis" model 🎯
WAKE_THRESHOLD = 0.80                # 0-1, higher = stricter wake detection
VOICEPRINT_PATH = "data/voiceprint.npy"
SPEAKER_THRESHOLD = 0.55            # 0-1 cosine similarity; tune if too strict/loose
ENROLL_SECONDS = 6                  # how long to record for enrollment
GREETING_STATE_PATH = "data/last_greeting.txt"
VOICEPRINT_COLLECTION = "karan_voiceprint"
ECAPA_MODEL_DIR = "data/ecapa_model"
CONFIRM_LISTEN = 3
ENROLL_SAMPLES = 5


#Wake up and follow-up settings
FOLLOWUP_ENABLED = True
FOLLOWUP_WINDOW = 10      # seconds to wait for a follow-up before sleeping
FOLLOWUP_LISTEN = 7       # how long each follow-up recording captures


# {memory_context} is filled in fresh on every turn by the agent.
SYSTEM_PROMPT = """You are JARVIS, Karan's polite and friendly personal assistant.
You are helpful, warm, and efficient. Keep spoken-style answers concise.

Use the tools available to accomplish tasks. Think step by step.
When Karan shares durable information about himself (facts, preferences,
projects, goals), call the save_memory tool. When asked what you know
about him, use recall_memory or the memory context below.

--- MEMORY ---
{memory_context}
--- END MEMORY ---

Always address the user as Karan when appropriate."""