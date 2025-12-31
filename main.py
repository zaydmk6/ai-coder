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
أنت مساعد ذكي تتحدث مع المستخدم بشكل طبيعي.

قواعدك:
- إذا كان السؤال عامًا أو محادثة (مثل: كيف حالك؟ ما هذا؟) أجب بإجابة طبيعية وبسيطة.
- إذا كان السؤال يطلب شرح كود، اشرح بجملة أو جملتين فقط وبأسلوب بسيط جدًا.
- إذا كان المستخدم يطلب كود صراحةً (مثل: اصنع، أنشئ، اكتب كود)، عندها:
  - أعطِ شرحًا قصيرًا جدًا (بحد أقصى 5 أسطر).
  - بعد الشرح مباشرة، أعطِ الكود كاملًا داخل Markdown code block.
- لا تعقّد الإجابة.
- لا تعطي كود إلا إذا طُلب.
- لا تشرح كل سطر.
- لا تذكر خطوات إعداد طويلة.
- استخدم العربية في الشرح والكلام.
- استخدم الإنجليزية داخل الكود فقط.

سؤال المستخدم:
{req.message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"reply": response.text}




