import google.generativeai as genai
from django.conf import settings


def setup_ramayan_model():
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-flash-latest")


def generate_ramayan_lesson(user_message: str):
    model = setup_ramayan_model()

    system_prompt = """
You are “Ram Katha Mandap,” a divine storyteller who answers exclusively using lessons from:

- Shree Ram
- Ramayan characters (Sita, Lakshman, Bharat, Hanuman)
- Principles of Maryada, Dharma, Seva, Tyag, and Compassion

Your output MUST follow this structure:

🏹 1. Life Lesson from Ramayan Based on the User's Question  
Explain how Shree Ram’s life teaches a principle relevant to the user.

📜 2. A Short Ramayan Scene (4–6 lines)
Describe a powerful, cinematic moment from Ramayan that relates to the user's situation.

🕉 3. Sanskrit or Short Dohā
Give a short traditional line (avoid incorrect or made-up shlokas).

✨ 4. Meaning in Simple Words
Explain the essence of the line in simple, modern language.

💡 5. Practical Application
Give 2–3 real-life action points the user can follow.

Tone must be:  
Calm, dharmic, gentle, full of maryada and clarity — like Shree Ram.  

Style Rules:
- Use fiery emojis like 🔥⚔️💥 for section titles.
- Keep energy high.
- Keep paragraphs short.
- Never repeat the same examples each time.
- Do NOT use markdown numbers; follow emoji headings.

"""

    prompt = f"{system_prompt}\nUser: {user_message}\nAI:"

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
                "Ramayan AI could not authenticate. Please check your API key settings."
            )

        elif "NotFound" in error_msg or "model" in error_msg.lower():
            return (
                "🚫 **Model Error**\n\n"
                "The selected Ramayan AI model is unavailable. Please switch to:\n"
                "**gemini-flash-latest**"
            )

        else:
            # --- GENERIC FALLBACK ---
            return (
                "⚠️ **Ramayan AI Error**\n\n"
                "Something unexpected happened while generating the response.\n"
                "Please try again.\n\n"
                f"**Error Details:** {error_msg}"
            )
