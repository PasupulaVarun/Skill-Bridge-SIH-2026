from typing import List, Dict
import re

from models import StudentProfile
from data_loader import load_jobs


# =========================================================
# TEXT UTILITIES
# =========================================================

def normalize_text(text: str) -> str:

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-zA-Z0-9+#.\- ]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# CONVERT CSV SKILLS TO LIST
# =========================================================

def parse_skills(value) -> List[str]:

    if value is None:
        return []

    value = str(value).strip()

    if not value:
        return []

    # Supports:
    # Python, SQL, ML
    # Python | SQL | ML
    # Python; SQL; ML

    parts = re.split(
        r"[,|;]",
        value
    )

    return [
        normalize_text(x)
        for x in parts
        if normalize_text(x)
    ]


# =========================================================
# PROFILE SKILLS
# =========================================================

def get_student_skills(profile: StudentProfile) -> List[str]:

    skills = []

    for skill in profile.skills:
        normalized = normalize_text(skill)

        if normalized:
            skills.append(normalized)

    return list(set(skills))


# =========================================================
# GET ALL STUDENT TEXT
# =========================================================

def get_student_text(profile: StudentProfile) -> str:

    sections = []

    sections.extend(profile.skills)
    sections.extend(profile.certificates)
    sections.extend(profile.projects)
    sections.extend(profile.achievements)
    sections.extend(profile.interests)

    if profile.education:
        sections.append(profile.education)

    if profile.experience:
        sections.append(profile.experience)

    return normalize_text(
        " ".join(sections)
    )


# =========================================================
# SKILL MATCH
# =========================================================

def calculate_skill_match(
    student_skills: List[str],
    required_skills: List[str]
):

    if not required_skills:

        return 0.0, [], []

    matched = []
    missing = []

    for required in required_skills:

        required_normalized = normalize_text(
            required
        )

        found = False

        for student in student_skills:

            student_normalized = normalize_text(
                student
            )

            # Exact match
            if (
                student_normalized == required_normalized
            ):
                found = True
                break

            # Partial match
            if (
                required_normalized in student_normalized
                or student_normalized in required_normalized
            ):
                found = True
                break

        if found:
            matched.append(required)

        else:
            missing.append(required)

    score = (
        len(matched) /
        len(required_skills)
    ) * 100

    return score, matched, missing


# =========================================================
# INTEREST MATCH
# =========================================================

def calculate_interest_match(
    profile: StudentProfile,
    opportunity_text: str
) -> float:

    if not profile.interests:
        return 0.0

    opportunity_text = normalize_text(
        opportunity_text
    )

    matched = 0

    for interest in profile.interests:

        interest = normalize_text(interest)

        if not interest:
            continue

        if interest in opportunity_text:
            matched += 1

    return (
        matched /
        len(profile.interests)
    ) * 100


# =========================================================
# PROJECT MATCH
# =========================================================

def calculate_project_match(
    profile: StudentProfile,
    opportunity_text: str
) -> float:

    if not profile.projects:
        return 0.0

    opportunity_text = normalize_text(
        opportunity_text
    )

    matched = 0

    for project in profile.projects:

        words = normalize_text(
            project
        ).split()

        useful_words = [
            word
            for word in words
            if len(word) > 3
        ]

        if any(
            word in opportunity_text
            for word in useful_words
        ):
            matched += 1

    return (
        matched /
        len(profile.projects)
    ) * 100


# =========================================================
# FINAL SCORE
# =========================================================

def calculate_final_score(
    skill_score: float,
    interest_score: float,
    project_score: float
) -> float:

    # Skill = 60%
    # Interest = 25%
    # Project = 15%

    final_score = (
        skill_score * 0.60
        +
        interest_score * 0.25
        +
        project_score * 0.15
    )

    return round(
        min(final_score, 100),
        2
    )


# =========================================================
# GENERATE RECOMMENDATIONS
# =========================================================

def generate_recommendations(
    profile: StudentProfile
) -> List[Dict]:

    jobs = load_jobs()

    if jobs.empty:

        return []

    student_skills = get_student_skills(
        profile
    )

    student_text = get_student_text(
        profile
    )

    recommendations = []

    for _, job in jobs.iterrows():

        # -------------------------------------------------
        # Get fields safely
        # -------------------------------------------------

        title = str(
            job.get("title", "")
        )

        company = str(
            job.get("company", "")
        )

        required_skills = parse_skills(
            job.get("skills", "")
        )

        location = str(
            job.get("location", "")
        )

        opportunity_type = str(
            job.get("type", "Opportunity")
        )

        description = str(
            job.get("description", "")
        )

        eligibility = str(
            job.get(
                "eligibility",
                "Open to eligible candidates"
            )
        )

        link = str(
            job.get(
                "link",
                "#"
            )
        )

        # -------------------------------------------------
        # Opportunity text
        # -------------------------------------------------

        opportunity_text = normalize_text(
            " ".join([
                title,
                company,
                description,
                " ".join(required_skills)
            ])
        )

        # -------------------------------------------------
        # Skill score
        # -------------------------------------------------

        skill_score, matched, missing = (
            calculate_skill_match(
                student_skills,
                required_skills
            )
        )

        # -------------------------------------------------
        # Interest score
        # -------------------------------------------------

        interest_score = calculate_interest_match(
            profile,
            opportunity_text
        )

        # -------------------------------------------------
        # Project score
        # -------------------------------------------------

        project_score = calculate_project_match(
            profile,
            opportunity_text
        )

        # -------------------------------------------------
        # Final score
        # -------------------------------------------------

        final_score = calculate_final_score(
            skill_score,
            interest_score,
            project_score
        )

        # -------------------------------------------------
        # If no direct skills exist, use text relevance
        # -------------------------------------------------

        if (
            skill_score == 0
            and
            interest_score == 0
            and
            project_score == 0
        ):

            student_words = set(
                student_text.split()
            )

            opportunity_words = set(
                opportunity_text.split()
            )

            common_words = (
                student_words &
                opportunity_words
            )

            useful_common = [
                word
                for word in common_words
                if len(word) > 3
            ]

            if useful_common:

                final_score = min(
                    30 + len(useful_common) * 5,
                    60
                )

        # -------------------------------------------------
        # Add recommendation
        # -------------------------------------------------

        recommendations.append({

            "title": title,

            "company": company,

            "match_score": final_score,

            "type": opportunity_type,

            "location": location,

            "description": description,

            "matched_skills": matched,

            "missing_skills": missing,

            "eligibility": eligibility,

            "link": link

        })

    # =====================================================
    # SORT BY SCORE
    # =====================================================

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    # Return top 10
    return recommendations[:10]