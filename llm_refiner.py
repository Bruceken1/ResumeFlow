import os
import json
from typing import Dict, Any, List
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

client = InferenceClient(model=MODEL, token=HF_TOKEN)


def refine_resume(resume_text: str, job_description: str | None = None) -> Dict[str, Any]:
    system = """
You MUST return ONLY valid JSON. No text before or after. No markdown. No explanations. No code fences.

Exact structure you must follow:

{
  "name": "full name here",
  "contact": {
    "address": "address here",
    "phone": "phone here",
    "email": "email here"
  },
  "career_objective": "one paragraph objective",
  "education": [
    {
      "degree": "degree name",
      "institution": "school name",
      "date": "date or expected date",
      "details": ["bullet 1", "bullet 2"]
    }
  ],
  "experience": [
    {
      "title": "job title",
      "company": "company name",
      "date": "date range",
      "bullets": ["improved bullet 1", "improved bullet 2"]
    }
  ],
  "skills": ["skill1", "skill2"],
  "references": [
    {
      "name": "ref name",
      "title": "ref title",
      "organization": "org",
      "contact": "phone/email"
    }
  ]
}

Improve wording and action verbs only. Do NOT invent facts, dates or skills.
Use the resume text as source. Be concise and professional.
"""

    user = f"""JOB: {job_description or "None"}

RESUME:
{resume_text[:6000]}

Return ONLY the JSON object above. Nothing else."""

    try:
        resp = client.chat_completion(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=2200,
            temperature=0.1,   # very low → more deterministic
            top_p=0.9
        )
        raw = resp.choices[0].message.content.strip()

        # Aggressive cleaning – remove any possible junk
        if '```' in raw:
            raw = raw.split('```')[1].split('```')[0].strip()
        if raw.startswith('json'):
            raw = raw[4:].strip()

        print("RAW LLM OUTPUT:\n", raw)  # ← important for debugging

        parsed = json.loads(raw)
        print("Parsed JSON keys:", list(parsed.keys()))  # debug
        return parsed
    except json.JSONDecodeError as e:
        print("JSON parse error:", e)
        print("Raw response was:", raw)
        return {"error": "Invalid JSON from LLM", "raw": raw}
    except Exception as e:
        print("LLM call failed:", e)
        return {"error": str(e)}

def generate_cover_letter(resume_text: str, job_description: str, user_name: str = "Ken Kaibe", contact_info: str = "") -> str:
    system = """Write professional cover letter. Only use resume facts. 320-430 words. Plain text only."""
    user = f"""Job description: {job_description}

Resume: {resume_text[:6500]}

Name: {user_name}
Contact: {contact_info}

Return only the letter text."""

    try:
        resp = client.chat_completion(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=1100,
            temperature=0.35
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print("Cover letter failed:", e)
        return "Could not generate cover letter."