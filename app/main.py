from fastapi import FastAPI
from pydantic import BaseModel
from src.reasoning_engine import recommend_careers

app = FastAPI(
    title="Career Recommendation API",
    description="Recommend careers based on user skills",
    version="1.0"
)

class SkillRequest(BaseModel):
    skills: list[str]


@app.post("/recommend")
def recommend(request: SkillRequest):

    recommendations = recommend_careers(request.skills)

    careers = [career for career, score in recommendations]

    return {
        "recommended_careers": careers
    }