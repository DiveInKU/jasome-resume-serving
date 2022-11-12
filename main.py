# localhost:8000/docs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from NLP import NLP
import uvicorn
from pydantic import BaseModel
import re

app = FastAPI()

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = NLP()


class PredictReq(BaseModel):
    category: str
    sentence: str
    number: int


@app.post(
    path="/generate",
    description="category는 'it', 'business', 'marketing', 'total'로만 입력해주세요."
)
async def generate(req: PredictReq):
    if req.category not in nlp.categories:
        return {"error": "{}는 지정된 카테고리가 아닙니다. category는 'it', 'business', 'marketing', 'total'로만 입력해주세요.".format(
            req.category)}
    if req.number == 0:
        return {"error": "생성하고 싶은 문장 개수를 입력해주세요."}
    sentences = re.findall('[^.]+.', req.sentence)
    print(sentences)
    last_sentence = sentences[-1]
    if req.sentence.strip() == '':
        return {"error": "입력 '{}'이 너무 짧습니다. 더 길게 입력해주세요.".format(req.sentence)}
    # 마지막 문장 너무 짧은 경우 앞에 문장도 추가한다
    if len(sentences) > 1 and (len(last_sentence.strip()) < 10):
        last_sentence = sentences[-2] + sentences[-1]
    print(last_sentence)
    return {"generated": nlp.generate(req.category, last_sentence.strip(), req.number)}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
