# localhost:8000/docs
from fastapi import FastAPI
from NLP import NLP
import uvicorn
from pydantic import BaseModel

app = FastAPI()

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
    return {"generated": nlp.generate(req.category, req.sentence, req.number)}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
