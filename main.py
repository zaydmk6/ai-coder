import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    prompt = f"""
أنت مولد كود.

المطلوب:
- أعطِ شرحًا قصيرًا جدًا (بحد أقصى 5 أسطر).
- الشرح يكون بسيط للمبتدئ.
- بعد الشرح مباشرة، أعطِ الكود كاملًا داخل Markdown code block.
- لا تشرح كل سطر.
- لا تذكر خطوات طويلة أو إعدادات معقدة.

الطلب:
{req.message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"reply": response.text}


