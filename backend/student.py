# backend/app/ml/student.py

from pathlib import Path
import re

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SkillBridgeRecommender:

    def __init__(self, jobs_file=None):

        # =====================================================
        # FIND jobs.csv
        # =====================================================

        if jobs_file is None:

            # student.py is:
            # backend/app/ml/student.py

            current_file = Path(__file__).resolve()

            backend_folder = current_file.parents[2]

            jobs_file = backend_folder / "jobs.csv"

        else:

            jobs_file = Path(jobs_file)

            if not jobs_file.is_absolute():

                backend_folder = Path(__file__).resolve().parents[2]

                jobs_file = backend_folder / jobs_file


        # =====================================================
        # CHECK FILE
        # =====================================================

        if not jobs_file.exists():

            raise FileNotFoundError(
                f"jobs.csv not found at:\n{jobs_file}"
            )


        print(
            f"[SkillBridge AI] Loading:\n{jobs_file}"
        )


        # =====================================================
        # LOAD DATA
        # =====================================================

        self.jobs = pd.read_csv(
            jobs_file
        )

        self.jobs = self.jobs.fillna("")


        # =====================================================
        # REQUIRED COLUMNS
        # =====================================================

        required_columns = [

            "id",
            "company",
            "title",
            "type",
            "location",
            "skills",
            "description",
            "eligibility",
            "link"

        ]


        for column in required_columns:

            if column not in self.jobs.columns:

                raise ValueError(
                    f"Missing column in jobs.csv: {column}"
                )


        # =====================================================
        # COMBINE JOB INFORMATION
        # =====================================================

        self.jobs["combined_text"] = (

            self.jobs["title"].astype(str)
            + " "

            + self.jobs["skills"].astype(str)
            + " "

            + self.jobs["description"].astype(str)
            + " "

            + self.jobs["eligibility"].astype(str)

        )


        # =====================================================
        # TF-IDF MODEL
        # =====================================================

        self.vectorizer = TfidfVectorizer(

            stop_words="english",

            ngram_range=(1, 2)

        )


        self.job_vectors = (

            self.vectorizer.fit_transform(

                self.jobs["combined_text"]

            )

        )


        print(
            f"[SkillBridge AI] Loaded "
            f"{len(self.jobs)} opportunities."
        )


    # =========================================================
    # CLEAN TEXT
    # =========================================================

    def clean_text(self, text):

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
    # CONVERT TEXT/LIST TO SKILLS
    # =========================================================

    def normalize_skills(self, skills):

        if skills is None:

            return set()


        if isinstance(skills, str):

            skills = re.split(
                r",|;|\n",
                skills
            )


        result = set()


        for skill in skills:

            cleaned = self.clean_text(
                skill
            )

            if cleaned:

                result.add(cleaned)


        return result


    # =========================================================
    # BUILD STUDENT PROFILE
    # =========================================================

    def build_profile(self, student):

        skills = self.normalize_skills(
            student.get("skills", [])
        )


        certificates = self.normalize_skills(
            student.get("certificates", [])
        )


        projects = self.normalize_skills(
            student.get("projects", [])
        )


        achievements = self.normalize_skills(
            student.get("achievements", [])
        )


        interests = self.normalize_skills(
            student.get("interests", [])
        )


        experience = self.normalize_skills(
            student.get("experience", [])
        )


        education = self.clean_text(

            student.get(
                "education",
                ""
            )

        )


        # -----------------------------------------------------
        # PROFILE TEXT
        # -----------------------------------------------------

        profile_text = " ".join(

            list(skills)
            + list(certificates)
            + list(projects)
            + list(achievements)
            + list(interests)
            + list(experience)
            + [education]

        )


        return {

            "skills": skills,

            "certificates": certificates,

            "projects": projects,

            "achievements": achievements,

            "interests": interests,

            "experience": experience,

            "education": education,

            "profile_text": profile_text

        }


    # =========================================================
    # CALCULATE SKILL GAP
    # =========================================================

    def calculate_skill_gap(
        self,
        student_skills,
        required_skills
    ):

        student_skills = self.normalize_skills(
            student_skills
        )

        required_skills = self.normalize_skills(
            required_skills
        )


        matched = (
            student_skills
            &
            required_skills
        )


        missing = (
            required_skills
            -
            student_skills
        )


        return matched, missing


    # =========================================================
    # MATCH SCORE
    # =========================================================

    def calculate_match_score(
        self,
        similarity,
        matched_count,
        required_count
    ):

        if required_count == 0:

            skill_coverage = 0

        else:

            skill_coverage = (
                matched_count /
                required_count
            )


        similarity_score = (
            similarity * 100
        )


        coverage_score = (
            skill_coverage * 100
        )


        # -----------------------------------------------------
        # FINAL WEIGHT
        #
        # 60% semantic/text similarity
        # 40% actual skill coverage
        # -----------------------------------------------------

        final_score = (

            0.60 * similarity_score

            +

            0.40 * coverage_score

        )


        return round(

            min(
                final_score,
                100
            ),

            2

        )


    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    def recommend(
        self,
        student,
        top_k=5
    ):

        profile = self.build_profile(
            student
        )


        # =====================================================
        # STUDENT VECTOR
        # =====================================================

        student_vector = (

            self.vectorizer.transform(

                [
                    profile["profile_text"]
                ]

            )

        )


        # =====================================================
        # COSINE SIMILARITY
        # =====================================================

        similarities = cosine_similarity(

            student_vector,

            self.job_vectors

        )[0]


        recommendations = []


        # =====================================================
        # PROCESS OPPORTUNITIES
        # =====================================================

        for index, similarity in enumerate(
            similarities
        ):

            job = self.jobs.iloc[index]


            required_skills = (

                self.normalize_skills(

                    job["skills"]

                )

            )


            matched, missing = (

                self.calculate_skill_gap(

                    profile["skills"],

                    required_skills

                )

            )


            score = (

                self.calculate_match_score(

                    similarity,

                    len(matched),

                    len(required_skills)

                )

            )


            recommendations.append({

                "job_id": int(
                    job["id"]
                ),

                "company": str(
                    job["company"]
                ),

                "title": str(
                    job["title"]
                ),

                "type": str(
                    job["type"]
                ),

                "location": str(
                    job["location"]
                ),

                "match_score": score,

                "matched_skills": sorted(
                    matched
                ),

                "missing_skills": sorted(
                    missing
                ),

                "description": str(
                    job["description"]
                ),

                "eligibility": str(
                    job["eligibility"]
                ),

                "link": str(
                    job["link"]
                )

            })


        # =====================================================
        # SORT
        # =====================================================

        recommendations.sort(

            key=lambda item:
                item["match_score"],

            reverse=True

        )


        return recommendations[
            :top_k
        ]