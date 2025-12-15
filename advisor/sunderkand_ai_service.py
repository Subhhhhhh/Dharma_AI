import google.generativeai as genai
from django.conf import settings


def setup_sunder_model():
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-flash-latest")


def generate_sunder_story(user_message: str):
    model = setup_sunder_model()

    system_prompt = """
You are “Sankat Mochan Path,” a divine guide who teaches through:

- Shree Hanuman’s strength, devotion, humility, and wisdom  
- Sunderkand’s chopai meanings  
- Bhagvat Prapti teachings of Shree Hanuman and Bhakt tradition  

Your response MUST follow this structure:

🪔 1. Hanuman Ji’s Lesson for the User 
Give a powerful life lesson inspired by Hanuman Ji.

📜 2. Sunderkand Chopai (correct, traditional) 
Include a chopai relevant to the user's question (do not modify original text).

🌼 3. Meaning of the Chopai
Explain the chopai in simple modern English (2–3 lines).

💪 4. Strength + Devotion Insight
Explain how Hanuman Ji handled similar challenges through bhakti, courage, and wisdom.

💡 5. Real-Life Application  
Give 2–3 actionable steps the user can apply today.

🕉 6. Bhagvat Prapti Note
End with a devotional reminder on surrender, naam-jap, and seva.

Tone:  
Strong yet humble, devotional, uplifting, full of Hanuman’s courage & sweetness.

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
                "Sankat Mochan Path could not authenticate. Please check your API key settings."
            )

        elif "NotFound" in error_msg or "model" in error_msg.lower():
            return (
                "🚫 **Model Error**\n\n"
                "The selected Sankat Mochan Path model is unavailable. Please switch to:\n"
                "**gemini-flash-latest**"
            )

        else:
            # --- GENERIC FALLBACK ---
            return (
                "⚠️ ** Sankat Mochan Path Error**\n\n"
                "Something unexpected happened while generating the response.\n"
                "Please try again.\n\n"
                f"**Error Details:** {error_msg}"
            )
