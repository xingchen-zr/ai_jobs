from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from ai_fun import ai_fun

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuestion(BaseModel):
    human_question:str = Field(...,min_length=1,description="请输入问题")

class ChatResponse(BaseModel):
    answer: str

@app.post('/job')
def ask(human_question:UserQuestion):
    response = ai_fun(human_question.human_question)

    return ChatResponse(answer=response)
