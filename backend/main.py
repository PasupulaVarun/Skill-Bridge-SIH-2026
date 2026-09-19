from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import StudentProfile, RecommendationResponse
from recommender import generate_recommendations


app = FastAPI(
    title="SkillBridge API",
    description="Academia-Industry Collaboration and Skill Matching API",
    version="1.0.0"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "service": "SkillBridge API",
        "status": "running",
        "version": "1.0.0"
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "SkillBridge API"
    }


# ---------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------

@app.post(
    "/api/recommend",
    response_model=RecommendationResponse
)
def recommend(profile: StudentProfile):

    try:
        recommendations = generate_recommendations(profile)

        return {
            "success": True,
            "count": len(recommendations),
            "recommendations": recommendations
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation error: {str(e)}"
        )


# ---------------------------------------------------------
# RUN DIRECTLY
# ---------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )