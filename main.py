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
    prompt = f"""أنت مساعد ذكي لتعليم البرمجة.

تصرف كمدرّس بسيط وهادئ.

قواعدك:
- إذا كان السؤال عادي (كيف حالك؟ ما هذا؟) أجب بشكل طبيعي وبسيط.
- إذا كان السؤال يطلب شرح كود، اشرح بجملة أو جملتين فقط.
- إذا كان السؤال يطلب كود:
  - أعطِ شرحًا بسيطًا جدًا (حد أقصى 3 أسطر).
  - ثم أعطِ الكود كاملًا داخل Markdown code block.
- لا تعقّد.
- لا تستخدم مصطلحات متقدمة.
- لا تشرح كل سطر.
- لا تضف خطوات طويلة أو إعدادات.
- لا تعطي كود إذا لم يُطلب.
- الشرح والكلام بالعربية.
- الكود بالإنجليزية فقط.
- اجعل الإجابة قصيرة وواضحة دائمًا.

سؤال المستخدم:
{{USER_MESSAGE}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"reply": response.text}





