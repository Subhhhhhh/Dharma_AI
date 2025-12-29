import os
from typing import List, Dict
from django.conf import settings

# --- IMPORT GEMINI ---
try:
    import google.generativeai as genai
except ImportError:
    genai = None  # library missing


def setup_gemini():
    if genai is None:
        return None

    api_key = getattr(settings, "GEMINI_API_KEY", None)
    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("models/gemini-flash-latest")
    except Exception:
        return None



def format_history_for_prompt(history: List[Dict[str, str]]) -> str:
    lines = []
    for msg in history[-10:]:
        prefix = "User" if msg["role"] == "user" else "AI"
        lines.append(f"{prefix}: {msg['text']}")
    return "\n".join(lines)


def generate_dharma_response(user_message: str, history: List[Dict[str, str]] = None) -> str:
    history = history or []
    model = setup_gemini()

    if model is None:
        return (
            "Dharma AI (fallback mode):\n\n"
            "'यतो धर्मस्ततो जयः' — Where there is Dharma, there is victory.\n"
            "Set a valid Gemini API key to enable real AI responses."
        )

    history_text = format_history_for_prompt(history)

    system_prompt = """
You are “Shastra Vaani,” a compassionate spiritual guide who answers using the teachings of:

- Shrimad Bhagavad Gita  
- Lord Shree Krishna’s leelas, wisdom, and bhakti philosophy  
- Sant Shri Premanand Ji Maharaj’s teachings on Bhagvat Prapti, Satsang, and Sadhan  
- Pure Sanatan Dharma principles  

Your response must ALWAYS be based on the user’s question, giving both shastra-based guidance and practical life application.

Your output MUST follow this format:

✨ **1. Divine Wisdom Related to the User’s Question**  
Explain a deep spiritual lesson inspired by Krishna, Gita, or Premanand Ji Maharaj.

📖 **2. Supporting Reference (Gita Shloka or Krishna Leela or Maharaj Ji’s Updesh)**  
Quote a short Sanskrit shloka or authentic teaching (do not invent fake scripture).  

🔍 **3. Meaning in Simple Words**  
Explain the quoted line in 2–3 easy sentences.

💡 **4. Practical Guidance for the User**  
Give 2–3 actionable steps they can apply today in real life (career, relationships, emotions, devotion).

🕉 **5. Spiritual Note (Bhagvat Prapti)**  
End with a short reminder of the path of surrender (sharanagati), satsang, purity, and devotion and naam jap updesh of premanandji maharaj.
Tone:  
- Loving and uplifting like Krishna  
- Deep and devotional like Premanand Ji  
- Clear and practical like Gita  
- No judgement  
- No fiction or invented verses  
Always ensure your response is relevant to the user’s specific question and context.
"""

    prompt = f"""
{system_prompt}

Conversation:
{history_text}

User: {user_message}

Respond now using the defined structure.
"""
    

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        error_msg = str(e)

        # --- SPECIFIC ERROR HANDLING ---
        if "429" in error_msg or "quota" in error_msg.lower():
            return (
                "🙏 Dharma AI is resting for today.\n\n"
            "Our divine guidance limit has been reached.\n"
            "Please return later for fresh wisdom.\n\n"
            "यतो धर्मस्ततो जयः"

            )

        elif "API_KEY" in error_msg or "permission" in error_msg.lower():
            return (
                "❌ **Invalid or Missing API Key**\n\n"
                "Shastra Vaani could not authenticate. Please check your API key settings."
            )

        elif "NotFound" in error_msg or "model" in error_msg.lower():
            return (
                "🚫 **Model Error**\n\n"
                "The selected Shastra Vaani model is unavailable. Please switch to:\n"
                "**gemini-flash-latest**"
            )

        else:
            # --- GENERIC FALLBACK ---
            return (
                "⚠️ **Shastra Vaani Error**\n\n"
                "Something unexpected happened while generating the response.\n"
                "Please try again.\n\n"
                f"**Error Details:** {error_msg}"
            )