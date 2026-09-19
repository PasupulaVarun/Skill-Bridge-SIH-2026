# ============================================================
# SkillBridge
# Academia × Industry Collaboration Portal
#
# FastAPI Recommendation Engine
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field

from typing import List, Optional, Dict, Any

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import re
import os


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JOBS_FILE = os.path.join(BASE_DIR, "jobs.csv")
SKILLS_FILE = os.path.join(BASE_DIR, "skills.csv")

TOP_K = 20


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="SkillBridge Recommendation API",
    description="AI-powered Academia-Industry Opportunity Recommendation System",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# STUDENT PROFILE MODEL
# ============================================================

class StudentProfile(BaseModel):

    skills: List[str] = Field(default_factory=list)

    certificates: List[str] = Field(default_factory=list)

    projects: List[str] = Field(default_factory=list)

    achievements: List[str] = Field(default_factory=list)

    interests: List[str] = Field(default_factory=list)

    education: str = ""

    experience: List[str] = Field(default_factory=list)


# ============================================================
# GLOBAL DATA
# ============================================================

jobs_df = None
skills_df = None

vectorizer = None
job_vectors = None

normalized_job_skills = []


# ============================================================
# COLUMN HELPERS
# ============================================================

def find_column(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:

    """
    Find a column using several possible names.
    """

    normalized_columns = {
        str(column).strip().lower().replace(" ", "_"): column
        for column in df.columns
    }

    for name in possible_names:

        key = (
            name
            .strip()
            .lower()
            .replace(" ", "_")
        )

        if key in normalized_columns:
            return normalized_columns[key]

    return None


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: Any) -> str:

    if text is None:
        return ""

    if pd.isna(text):
        return ""

    text = str(text).lower().strip()

    # Replace &, slash and separators
    text = text.replace("&", " and ")
    text = text.replace("/", " ")
    text = text.replace("|", " ")
    text = text.replace(";", " ")

    # Keep letters, numbers, +, #
    text = re.sub(r"[^a-z0-9+#.\- ]", " ", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    "ml": "machine learning",

    "machinelearning": "machine learning",

    "ai": "artificial intelligence",

    "artificialintelligence":
        "artificial intelligence",

    "dl": "deep learning",

    "deeplearning":
        "deep learning",

    "nlp":
        "natural language processing",

    "naturallanguageprocessing":
        "natural language processing",

    "cv":
        "computer vision",

    "javascript":
        "javascript",

    "js":
        "javascript",

    "typescript":
        "typescript",

    "ts":
        "typescript",

    "reactjs":
        "react",

    "react.js":
        "react",

    "nodejs":
        "node.js",

    "node":
        "node.js",

    "postgres":
        "postgresql",

    "postgre":
        "postgresql",

    "py":
        "python",

    "python3":
        "python",

    "c++":
        "cpp",

    "c plus plus":
        "cpp",

    "scikit learn":
        "scikit-learn",

    "sklearn":
        "scikit-learn",

    "power bi":
        "powerbi",

    "ms excel":
        "excel",

    "aws cloud":
        "aws",

}


def normalize_skill(skill: str) -> str:

    skill = normalize_text(skill)

    if not skill:
        return ""

    compact = skill.replace(" ", "")

    if skill in SKILL_ALIASES:
        return SKILL_ALIASES[skill]

    if compact in SKILL_ALIASES:
        return SKILL_ALIASES[compact]

    return skill


# ============================================================
# SPLIT SKILLS FROM CSV
# ============================================================

def split_skills(value: Any) -> List[str]:

    if value is None or pd.isna(value):
        return []

    text = str(value)

    # Handle comma, semicolon, pipe and newline
    parts = re.split(
        r"[,;|\n]",
        text
    )

    result = []

    for part in parts:

        skill = normalize_skill(part)

        if skill and skill not in result:
            result.append(skill)

    return result


# ============================================================
# LOAD CSV FILES
# ============================================================

def load_data():

    global jobs_df
    global skills_df

    if not os.path.exists(JOBS_FILE):

        raise FileNotFoundError(
            f"jobs.csv not found at: {JOBS_FILE}"
        )

    if not os.path.exists(SKILLS_FILE):

        raise FileNotFoundError(
            f"skills.csv not found at: {SKILLS_FILE}"
        )


    # --------------------------------------------------------
    # Read CSV
    # --------------------------------------------------------

    jobs_df = pd.read_csv(
        JOBS_FILE,
        encoding="utf-8"
    )

    skills_df = pd.read_csv(
        SKILLS_FILE,
        encoding="utf-8"
    )


    # Remove completely empty rows

    jobs_df = jobs_df.dropna(
        how="all"
    ).reset_index(drop=True)

    skills_df = skills_df.dropna(
        how="all"
    ).reset_index(drop=True)


    print("\n==========================================")
    print("SkillBridge CSV DATA LOADED")
    print("==========================================")

    print(
        f"Jobs loaded   : {len(jobs_df)}"
    )

    print(
        f"Skills loaded : {len(skills_df)}"
    )

    print(
        f"Job columns   : {list(jobs_df.columns)}"
    )

    print(
        f"Skill columns : {list(skills_df.columns)}"
    )

    print("==========================================\n")


# ============================================================
# DETERMINE JOB SKILL COLUMN
# ============================================================

def get_job_skill_column():

    column = find_column(
        jobs_df,

        [
            "skills",
            "required_skills",
            "required skills",
            "technical_skills",
            "technical skills",
            "skill",
            "job_skills",
            "job skills"
        ]
    )

    return column


# ============================================================
# DETERMINE SKILLS CSV COLUMN
# ============================================================

def get_skills_column():

    column = find_column(
        skills_df,

        [
            "skill",
            "skills",
            "name",
            "skill_name",
            "skill name",
            "technology",
            "technologies"
        ]
    )

    return column


# ============================================================
# BUILD SKILL MASTER LIST
# ============================================================

def build_skill_master():

    skill_column = get_skills_column()

    if skill_column is None:

        print(
            "WARNING: Could not detect skill column in skills.csv"
        )

        return []


    master_skills = []

    for value in skills_df[skill_column]:

        for skill in split_skills(value):

            if skill not in master_skills:
                master_skills.append(skill)


    print(
        f"Master skill list: {len(master_skills)} skills"
    )

    return master_skills


# ============================================================
# JOB TEXT
# ============================================================

def get_job_text(job: pd.Series) -> str:

    """
    Build text used for cosine similarity.
    """

    fields = [

        "title",

        "job_title",

        "role",

        "description",

        "required_skills",

        "skills",

        "responsibilities",

        "requirements",

        "eligibility",

        "type",

        "interests"

    ]

    values = []

    for field in fields:

        column = find_column(
            jobs_df,
            [field]
        )

        if column is not None:

            value = job.get(
                column,
                ""
            )

            if not pd.isna(value):

                values.append(
                    str(value)
                )

    return " ".join(values)


# ============================================================
# PREPARE JOB SKILLS
# ============================================================

def prepare_job_skills():

    global normalized_job_skills

    normalized_job_skills = []

    skill_column = get_job_skill_column()


    for _, job in jobs_df.iterrows():

        if skill_column is not None:

            skills = split_skills(
                job.get(
                    skill_column,
                    ""
                )
            )

        else:

            skills = []


        normalized_job_skills.append(
            skills
        )


    print(
        "Job skill matching data prepared."
    )


# ============================================================
# BUILD TF-IDF VECTORS
# ============================================================

def build_vectors():

    global vectorizer
    global job_vectors

    job_texts = []

    for _, job in jobs_df.iterrows():

        text = get_job_text(job)

        text = normalize_text(text)

        job_texts.append(text)


    # Prevent empty documents
    job_texts = [
        text if text else "opportunity"
        for text in job_texts
    ]


    vectorizer = TfidfVectorizer(

        lowercase=True,

        stop_words="english",

        ngram_range=(1, 2),

        sublinear_tf=True
    )


    job_vectors = vectorizer.fit_transform(
        job_texts
    )


    print(
        f"Cosine similarity vectors created for {len(job_texts)} jobs."
    )


# ============================================================
# INITIALIZE RECOMMENDATION ENGINE
# ============================================================

def initialize_engine():

    load_data()

    build_skill_master()

    prepare_job_skills()

    build_vectors()


# ============================================================
# STUDENT PROFILE TEXT
# ============================================================

def build_student_text(
    profile: StudentProfile
) -> str:

    parts = []

    parts.extend(
        profile.skills
    )

    parts.extend(
        profile.certificates
    )

    parts.extend(
        profile.projects
    )

    parts.extend(
        profile.achievements
    )

    parts.extend(
        profile.interests
    )

    parts.append(
        profile.education
    )

    parts.extend(
        profile.experience
    )


    return normalize_text(
        " ".join(
            str(item)
            for item in parts
            if item
        )
    )


# ============================================================
# STUDENT SKILLS
# ============================================================

def get_student_skills(
    profile: StudentProfile
) -> List[str]:

    skills = []

    # Direct skills
    for skill in profile.skills:

        normalized = normalize_skill(
            skill
        )

        if normalized and normalized not in skills:

            skills.append(
                normalized
            )


    # Interests can also contribute
    for interest in profile.interests:

        normalized = normalize_skill(
            interest
        )

        if normalized and normalized not in skills:

            skills.append(
                normalized
            )


    return skills


# ============================================================
# EXACT SKILL MATCHING
# ============================================================

def calculate_skill_match(
    student_skills: List[str],
    job_skills: List[str]
):

    student_set = set(
        normalize_skill(skill)
        for skill in student_skills
        if skill
    )

    job_set = set(
        normalize_skill(skill)
        for skill in job_skills
        if skill
    )


    if not job_set:

        return (
            [],
            [],
            0.0
        )


    matched = sorted(
        student_set.intersection(
            job_set
        )
    )


    missing = sorted(
        job_set.difference(
            student_set
        )
    )


    skill_score = (
        len(matched) /
        len(job_set)
    ) * 100


    return (
        matched,
        missing,
        skill_score
    )


# ============================================================
# EDUCATION MATCH
# ============================================================

def calculate_education_match(
    education: str,
    job: pd.Series
) -> float:

    education = normalize_text(
        education
    )

    if not education:

        return 50.0


    eligibility_column = find_column(
        jobs_df,
        [
            "eligibility",
            "education",
            "qualification",
            "qualifications"
        ]
    )


    if eligibility_column is None:

        return 50.0


    eligibility = normalize_text(
        job.get(
            eligibility_column,
            ""
        )
    )


    if not eligibility:

        return 50.0


    education_words = set(
        education.split()
    )


    eligibility_words = set(
        eligibility.split()
    )


    overlap = education_words.intersection(
        eligibility_words
    )


    if overlap:

        return 100.0


    # Common degree/CSE keywords
    keywords = [
        "b.tech",
        "btech",
        "b.e",
        "be",
        "cse",
        "computer science",
        "engineering",
        "computer"
    ]


    if any(
        keyword in eligibility
        for keyword in keywords
    ):

        if any(
            keyword in education
            for keyword in keywords
        ):

            return 100.0


    return 50.0


# ============================================================
# INTEREST MATCH
# ============================================================

def calculate_interest_match(
    profile: StudentProfile,
    job: pd.Series
) -> float:

    interests = [
        normalize_text(item)
        for item in profile.interests
        if item
    ]


    if not interests:

        return 50.0


    job_text = normalize_text(
        get_job_text(job)
    )


    matches = 0

    for interest in interests:

        if interest in job_text:

            matches += 1


    return (
        matches /
        len(interests)
    ) * 100


# ============================================================
# COSINE SIMILARITY
# ============================================================

def calculate_cosine_score(
    student_text: str
) -> np.ndarray:

    student_vector = vectorizer.transform(
        [student_text]
    )


    similarities = cosine_similarity(
        student_vector,
        job_vectors
    )[0]


    return similarities


# ============================================================
# FINAL MATCH SCORE
# ============================================================

def calculate_final_score(
    cosine_score: float,
    skill_score: float,
    interest_score: float,
    education_score: float
) -> float:

    """
    Weighted recommendation score.

    40% = cosine similarity
    40% = exact skill matching
    10% = interest matching
    10% = education matching
    """

    final_score = (

        (cosine_score * 100) * 0.40

        +

        skill_score * 0.40

        +

        interest_score * 0.10

        +

        education_score * 0.10

    )


    final_score = max(
        0,
        min(
            100,
            final_score
        )
    )


    return round(
        final_score,
        2
    )


# ============================================================
# GET JOB FIELD
# ============================================================

def get_job_value(
    job: pd.Series,
    names: List[str],
    default: str = ""
) -> str:

    column = find_column(
        jobs_df,
        names
    )


    if column is None:

        return default


    value = job.get(
        column,
        default
    )


    if pd.isna(value):

        return default


    return str(value).strip()


# ============================================================
# CREATE RECOMMENDATION OBJECT
# ============================================================

def create_recommendation(
    job: pd.Series,
    index: int,
    score: float,
    matched_skills: List[str],
    missing_skills: List[str]
) -> Dict[str, Any]:

    title = get_job_value(
        job,
        [
            "title",
            "job_title",
            "role",
            "position"
        ],
        "Opportunity"
    )


    company = get_job_value(
        job,
        [
            "company",
            "company_name",
            "organization",
            "organisation"
        ],
        "Company"
    )


    job_type = get_job_value(
        job,
        [
            "type",
            "job_type",
            "opportunity_type"
        ],
        "Opportunity"
    )


    location = get_job_value(
        job,
        [
            "location",
            "city",
            "job_location"
        ],
        "Not specified"
    )


    description = get_job_value(
        job,
        [
            "description",
            "job_description",
            "about",
            "details"
        ],
        "No description available."
    )


    eligibility = get_job_value(
        job,
        [
            "eligibility",
            "qualification",
            "qualifications",
            "education"
        ],
        "Eligibility information not specified."
    )


    link = get_job_value(
        job,
        [
            "link",
            "url",
            "apply_link",
            "application_link"
        ],
        "#"
    )


    return {

        "title": title,

        "company": company,

        "match_score": score,

        "type": job_type,

        "location": location,

        "description": description,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "eligibility": eligibility,

        "link": link
    }


# ============================================================
# PRINT TOP RECOMMENDATIONS
# ============================================================

def print_recommendations(
    recommendations: List[Dict[str, Any]]
):

    print("\n")
    print("=" * 75)
    print("SKILLBRIDGE — TOP RECOMMENDED OPPORTUNITIES")
    print("=" * 75)


    if not recommendations:

        print(
            "No recommendations found."
        )

        print("=" * 75)

        return


    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"\n#{index} "
            f"{recommendation['title']}"
        )

        print(
            f"Company     : "
            f"{recommendation['company']}"
        )

        print(
            f"Match Score : "
            f"{recommendation['match_score']}%"
        )

        print(
            f"Type        : "
            f"{recommendation['type']}"
        )

        print(
            f"Location    : "
            f"{recommendation['location']}"
        )

        print(
            "Matched     : "
            + (
                ", ".join(
                    recommendation[
                        "matched_skills"
                    ]
                )
                if recommendation[
                    "matched_skills"
                ]
                else "None"
            )
        )

        print(
            "Missing     : "
            + (
                ", ".join(
                    recommendation[
                        "missing_skills"
                    ]
                )
                if recommendation[
                    "missing_skills"
                ]
                else "None"
            )
        )

        print("-" * 75)


    print(
        f"\nTotal returned: "
        f"{len(recommendations)}"
    )

    print("=" * 75)
    print()


# ============================================================
# API — HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {

        "message":
            "SkillBridge Recommendation API is running.",

        "endpoint":
            "/api/recommend",

        "jobs_loaded":
            len(jobs_df)
            if jobs_df is not None
            else 0,

        "skills_loaded":
            len(skills_df)
            if skills_df is not None
            else 0
    }


# ============================================================
# API — RECOMMENDATIONS
# ============================================================

@app.post("/api/recommend")
def recommend(
    profile: StudentProfile
):

    if jobs_df is None:

        raise HTTPException(
            status_code=500,
            detail="Job database is not loaded."
        )


    if vectorizer is None:

        raise HTTPException(
            status_code=500,
            detail="Recommendation engine is not initialized."
        )


    # --------------------------------------------------------
    # Student skills
    # --------------------------------------------------------

    student_skills = get_student_skills(
        profile
    )


    # --------------------------------------------------------
    # Student profile text
    # --------------------------------------------------------

    student_text = build_student_text(
        profile
    )


    if not student_text:

        raise HTTPException(
            status_code=400,
            detail=(
                "Student profile is empty. "
                "Please add skills, interests, "
                "education, projects or experience."
            )
        )


    # --------------------------------------------------------
    # Cosine similarity
    # --------------------------------------------------------

    cosine_scores = calculate_cosine_score(
        student_text
    )


    recommendations = []


    # --------------------------------------------------------
    # Calculate score for every job
    # --------------------------------------------------------

    for index, (_, job) in enumerate(
        jobs_df.iterrows()
    ):

        job_skills = (
            normalized_job_skills[index]
            if index < len(
                normalized_job_skills
            )
            else []
        )


        # Exact skill matching

        (
            matched_skills,
            missing_skills,
            skill_score

        ) = calculate_skill_match(

            student_skills,

            job_skills
        )


        # Cosine score

        cosine_score = float(
            cosine_scores[index]
        )


        # Interest score

        interest_score = (
            calculate_interest_match(
                profile,
                job
            )
        )


        # Education score

        education_score = (
            calculate_education_match(
                profile.education,
                job
            )
        )


        # Final score

        final_score = calculate_final_score(

            cosine_score,

            skill_score,

            interest_score,

            education_score
        )


        recommendation = create_recommendation(

            job,

            index,

            final_score,

            matched_skills,

            missing_skills
        )


        # Store extra internal values
        # for debugging/ranking

        recommendation["_cosine_score"] = round(
            cosine_score * 100,
            2
        )

        recommendation["_skill_score"] = round(
            skill_score,
            2
        )

        recommendation["_interest_score"] = round(
            interest_score,
            2
        )

        recommendation["_education_score"] = round(
            education_score,
            2
        )


        recommendations.append(
            recommendation
        )


    # --------------------------------------------------------
    # Sort by final score
    # --------------------------------------------------------

    recommendations.sort(
        key=lambda item:
            item["match_score"],
        reverse=True
    )


    # --------------------------------------------------------
    # Take top K
    # --------------------------------------------------------

    top_recommendations = (
        recommendations[:TOP_K]
    )


    # --------------------------------------------------------
    # Print in terminal
    # --------------------------------------------------------

    print_recommendations(
        top_recommendations
    )


    # --------------------------------------------------------
    # Remove internal debug values
    # --------------------------------------------------------

    for recommendation in top_recommendations:

        recommendation.pop(
            "_cosine_score",
            None
        )

        recommendation.pop(
            "_skill_score",
            None
        )

        recommendation.pop(
            "_interest_score",
            None
        )

        recommendation.pop(
            "_education_score",
            None
        )


    # --------------------------------------------------------
    # Return to student.js
    # --------------------------------------------------------

    return {

        "recommendations":
            top_recommendations

    }


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():

    print("\n")
    print("=" * 75)
    print("STARTING SKILLBRIDGE RECOMMENDATION ENGINE")
    print("=" * 75)


    try:

        initialize_engine()

        print(
            "✓ Recommendation engine ready."
        )

        print(
            f"✓ {len(jobs_df)} jobs available."
        )

        print(
            "✓ Cosine similarity enabled."
        )

        print(
            "✓ Skill matching enabled."
        )

        print(
            "✓ Recommendation ranking enabled."
        )

        print("=" * 75)
        print()


    except Exception as error:

        print(
            "\nERROR INITIALIZING ENGINE:"
        )

        print(error)

        print(
            "\nCheck your CSV files and column names."
        )

        print("=" * 75)