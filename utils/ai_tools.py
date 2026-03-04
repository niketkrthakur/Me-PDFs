from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_summary(text, mode="standard", tone="formal"):

    if mode == "short":
        instruction = "Provide a short structured summary."
    elif mode == "bullet":
        instruction = "Provide structured bullet point summary."
    elif mode == "detailed":
        instruction = "Provide a detailed structured professional summary."
    else:
        instruction = "Provide a clean structured summary."

    tone_instruction = {
        "formal": "Use professional formal tone.",
        "student": "Use simple language suitable for students.",
        "executive": "Use executive-level concise business tone."
    }.get(tone, "Use professional formal tone.")    

    prompt = f"""
You are a professional document summarizer.

{instruction}
{tone_instruction}

IMPORTANT RULES:
- Return ONLY clean HTML.
- Do NOT use markdown symbols like **, ###, --- or pipes.
- Use proper HTML tags: <h2>, <h3>, <p>, <ul>, <li>, <strong>.
- Format nicely with sections.
- Make it clean and readable.
- No backticks.
- No code blocks.

Document:
{text[:8000]}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content

def rewrite_text(text, action="rewrite"):

    action_prompts = {
        "rewrite": "Rewrite the following text clearly and professionally.",
        "improve": "Improve the writing quality and clarity.",
        "simplify": "Simplify the language for easy understanding.",
        "professional": "Make the tone more professional and executive.",
        "shorten": "Shorten the text while keeping key information.",
        "expand": "Expand the text with more details and explanation."
    }

    instruction = action_prompts.get(action, action_prompts["rewrite"])

    prompt = f"""
You are a professional writing assistant.

{instruction}

IMPORTANT:
- Return clean HTML only.
- Use <p>, <h2>, <ul>, <li> if needed.
- No markdown symbols.
- No backticks.

Text:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return response.choices[0].message.content

def translate_text(text, target_language="Hindi"):

    prompt = f"""
You are a professional translator.

Translate the following text into {target_language}.

IMPORTANT:
- Preserve meaning accurately.
- Keep formatting structure.
- Return clean HTML only.
- Use <p>, <h2>, <ul>, <li> if needed.
- Do NOT use markdown symbols.

Text:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content

def detect_language(text):

    prompt = f"""
Detect the language of the following text.

Respond ONLY with the language name in English.
Example: English, Hindi, Spanish, French, German, Japanese, Chinese.

Text:
{text[:2000]}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content.strip()

import json
import re

def chat_with_pdf(pdf_text, question):

    prompt = f"""
You are an AI assistant answering questions strictly based on the provided PDF content.

Return ONLY valid JSON (no markdown, no explanation):

{{
  "section": "Section Name",
  "snippet": "Exact paragraph from document",
  "answer": "Clear structured answer in HTML"
}}

PDF Content:
{pdf_text[:12000]}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown JSON fences if present
    content = re.sub(r"```json", "", content)
    content = re.sub(r"```", "", content)

    try:
        parsed = json.loads(content)
        return parsed
    except Exception as e:
        print("JSON parsing failed:", e)
        return {
            "section": "Unknown",
            "snippet": "",
            "answer": content
        }