from pathlib import Path
import joblib


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model.pkl"


model = None


# =========================================================
# LOAD MODEL
# =========================================================

def load_model():

    global model

    if not MODEL_PATH.exists():

        print(
            "model.pkl not found. "
            "ML prediction is disabled."
        )

        return None

    try:

        model = joblib.load(
            MODEL_PATH
        )

        print("ML model loaded successfully.")

        return model

    except Exception as e:

        print(
            f"Error loading ML model: {e}"
        )

        return None


# =========================================================
# PREDICT
# =========================================================

def predict(features):

    global model

    if model is None:

        model = load_model()

    if model is None:

        return None

    try:

        prediction = model.predict(
            [features]
        )

        return prediction[0]

    except Exception as e:

        print(
            f"Prediction error: {e}"
        )

        return None