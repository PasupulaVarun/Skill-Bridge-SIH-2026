# test.py

from backend.student import SkillBridgeRecommender


# ======================================================
# STUDENT DATA
# ======================================================

student = {

    "skills": [

        "Python",
        "SQL",
        "Pandas",
        "Machine Learning"

    ],

    "certificates": [

        "Python for Data Science",
        "Machine Learning Fundamentals"

    ],

    "projects": [

        "Movie Recommendation System",
        "Student Performance Prediction"

    ],

    "achievements": [

        "Hackathon Finalist"

    ],

    "interests": [

        "Artificial Intelligence",
        "Data Science"

    ],

    "experience": [],

    "education":
        "B.Tech Computer Science"

}


# ======================================================
# CREATE AI MODEL
# ======================================================

model = SkillBridgeRecommender()


# ======================================================
# GET RECOMMENDATIONS
# ======================================================

results = model.recommend(

    student,

    top_k=5

)


# ======================================================
# DISPLAY RESULTS
# ======================================================

print("\n")
print("=" * 70)
print("        SKILLBRIDGE AI RECOMMENDATION ENGINE")
print("=" * 70)


for i, result in enumerate(
    results,
    start=1
):

    print("\n")
    print("-" * 70)

    print(
        f"#{i} {result['title']}"
    )

    print(
        f"Company    : {result['company']}"
    )

    print(
        f"Type       : {result['type']}"
    )

    print(
        f"Location   : {result['location']}"
    )

    print(
        f"Match Score: {result['match_score']}%"
    )

    print(
        "\nMatched Skills:"
    )

    if result["matched_skills"]:

        print(
            ", ".join(
                result["matched_skills"]
            )
        )

    else:

        print("None")


    print(
        "\nSkills to Learn:"
    )

    if result["missing_skills"]:

        print(
            ", ".join(
                result["missing_skills"]
            )
        )

    else:

        print(
            "No major skill gaps!"
        )


    print(
        "\nDescription:"
    )

    print(
        result["description"]
    )

    print(
        "\nEligibility:"
    )

    print(
        result["eligibility"]
    )

    print(
        "\nOpportunity:"
    )

    print(
        result["link"]
    )


print("\n")
print("=" * 70)
print("Recommendation complete.")
print("=" * 70)