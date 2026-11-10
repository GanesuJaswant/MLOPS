"""
Customer Churn Prediction API
FastAPI application that loads pre-trained ML model artifacts and exposes prediction endpoints.
"""
import os
import json
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

# ─── Initialize FastAPI ───────────────────────────────────────────────────────
app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict whether a telecom customer is likely to churn based on their profile.",
    version="1.0.0",
)

# ─── Load Model Artifacts ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

try:
    scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    ohe = joblib.load(os.path.join(MODEL_DIR, "ohe.pkl"))
    model = joblib.load(os.path.join(MODEL_DIR, "random_forest_baseline.pkl"))
    with open(os.path.join(DATA_DIR, "dataset_metadata.json")) as f:
        metadata = json.load(f)
    NUM_FEATURES = metadata["numerical_features"]   # SeniorCitizen, tenure, MonthlyCharges, TotalCharges
    CAT_FEATURES = metadata["categorical_features"] # gender, Partner, Dependents, ...
    print("✅ Model artifacts loaded successfully!")
except Exception as e:
    raise RuntimeError(f"Failed to load model artifacts: {e}")


# ─── Request / Response Schemas ──────────────────────────────────────────────
class CustomerInput(BaseModel):
    """Input schema — mirrors the 19 raw features (excluding customerID and Churn)."""
    gender: str = Field(..., example="Female", description="Male / Female")
    SeniorCitizen: int = Field(..., example=0, description="1 if senior citizen, else 0")
    Partner: str = Field(..., example="Yes", description="Yes / No")
    Dependents: str = Field(..., example="No", description="Yes / No")
    tenure: int = Field(..., example=1, description="Number of months with the company")
    PhoneService: str = Field(..., example="No", description="Yes / No")
    MultipleLines: str = Field(..., example="No phone service", description="Yes / No / No phone service")
    InternetService: str = Field(..., example="DSL", description="DSL / Fiber optic / No")
    OnlineSecurity: str = Field(..., example="No", description="Yes / No / No internet service")
    OnlineBackup: str = Field(..., example="Yes", description="Yes / No / No internet service")
    DeviceProtection: str = Field(..., example="No", description="Yes / No / No internet service")
    TechSupport: str = Field(..., example="No", description="Yes / No / No internet service")
    StreamingTV: str = Field(..., example="No", description="Yes / No / No internet service")
    StreamingMovies: str = Field(..., example="No", description="Yes / No / No internet service")
    Contract: str = Field(..., example="Month-to-month", description="Month-to-month / One year / Two year")
    PaperlessBilling: str = Field(..., example="Yes", description="Yes / No")
    PaymentMethod: str = Field(..., example="Electronic check",
                               description="Electronic check / Mailed check / Bank transfer (automatic) / Credit card (automatic)")
    MonthlyCharges: float = Field(..., example=29.85)
    TotalCharges: float = Field(..., example=29.85)


class PredictionResponse(BaseModel):
    churn_prediction: int = Field(..., description="0 = No Churn, 1 = Churn")
    churn_probability: float = Field(..., description="Probability of churning (0-1)")
    message: str


# ─── Endpoints ────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "healthy", "model": "RandomForestClassifier", "version": "1.0.0"}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_churn(customer: CustomerInput):
    """
    Accepts a single customer's profile and returns a churn prediction.
    The pipeline: raw features → StandardScaler (numeric) + OneHotEncoder (categorical) → RandomForest → prediction.
    """
    try:
        # Build a DataFrame from the input
        input_dict = customer.model_dump()
        df = pd.DataFrame([input_dict])

        # Separate numeric and categorical columns (same order as training)
        num_data = df[NUM_FEATURES].values.astype(float)
        cat_data = df[CAT_FEATURES]

        # Transform
        num_scaled = scaler.transform(num_data)
        cat_encoded = ohe.transform(cat_data)

        # Combine
        X_final = np.hstack((num_scaled, cat_encoded))

        # Predict
        prediction = int(model.predict(X_final)[0])
        probability = float(model.predict_proba(X_final)[0][1])

        return PredictionResponse(
            churn_prediction=prediction,
            churn_probability=round(probability, 4),
            message="Customer is likely to churn." if prediction == 1 else "Customer is not likely to churn.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model-info", tags=["Info"])
def model_info():
    """Return metadata about the trained model and features."""
    return {
        "model_type": type(model).__name__,
        "numerical_features": NUM_FEATURES,
        "categorical_features": CAT_FEATURES,
        "total_features_after_encoding": metadata.get("train_shape_transformed", [None, None])[1],
    }
