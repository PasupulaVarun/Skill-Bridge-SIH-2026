from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

JOBS_FILE = BASE_DIR / "jobs.csv"
SKILLS_FILE = BASE_DIR / "skills.csv"


# =========================================================
# LOAD JOBS
# =========================================================

def load_jobs():

    if not JOBS_FILE.exists():
        return pd.DataFrame()

    try:
        df = pd.read_csv(JOBS_FILE)

        # Convert NaN to empty strings
        df = df.fillna("")

        return df

    except Exception as e:

        print(f"Error loading jobs.csv: {e}")

        return pd.DataFrame()


# =========================================================
# LOAD SKILLS
# =========================================================

def load_skills():

    if not SKILLS_FILE.exists():
        return pd.DataFrame()

    try:

        df = pd.read_csv(SKILLS_FILE)

        df = df.fillna("")

        return df

    except Exception as e:

        print(f"Error loading skills.csv: {e}")

        return pd.DataFrame()