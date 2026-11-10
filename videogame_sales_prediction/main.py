"""
Video Game Sales Prediction API
FastAPI application that predicts global sales for a video game.
"""
import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

# ─── Initialize FastAPI ───────────────────────────────────────────────────────
app = FastAPI(
    title="Video Game Sales Prediction API",
    description="Predict global sales (in millions) for a video game based on platform, genre, publisher, and other attributes.",
    version="1.0.0",
)

# ─── Load Model ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "vgsales_model.pkl")

try:
    pipeline = joblib.load(MODEL_PATH)
    print("✅ Video Game Sales model loaded successfully!")
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}. Run 'python train.py' first.")


# ─── Schemas ─────────────────────────────────────────────────────────────────
class GameInput(BaseModel):
    """Input features for video game sales prediction."""
    Platform: str = Field(..., example="Wii", description="Gaming platform (e.g., Wii, PS4, X360, PC)")
    Year: float = Field(..., example=2006.0, description="Release year")
    Genre: str = Field(..., example="Sports", description="Game genre (e.g., Sports, Action, Racing)")
    Publisher: str = Field(..., example="Nintendo", description="Publisher name")
    NA_Sales: float = Field(..., example=41.49, description="North America sales in millions")
    EU_Sales: float = Field(..., example=29.02, description="Europe sales in millions")
    JP_Sales: float = Field(..., example=3.77, description="Japan sales in millions")
    Other_Sales: float = Field(..., example=8.46, description="Other regions sales in millions")


class SalesPredictionResponse(BaseModel):
    predicted_global_sales: float = Field(..., description="Predicted global sales in millions")
    message: str


# ─── Endpoints ────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "healthy", "model": "RandomForestRegressor Pipeline", "version": "1.0.0"}


@app.post("/predict", response_model=SalesPredictionResponse, tags=["Prediction"])
def predict_sales(game: GameInput):
    """Predict global sales for a video game given its attributes."""
    try:
        input_dict = game.model_dump()
        df = pd.DataFrame([input_dict])

        prediction = float(pipeline.predict(df)[0])

        return SalesPredictionResponse(
            predicted_global_sales=round(prediction, 4),
            message=f"Predicted global sales: {round(prediction, 2)}M units",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model-info", tags=["Info"])
def model_info():
    """Return metadata about the model."""
    return {
        "model_type": "RandomForestRegressor (with ColumnTransformer pipeline)",
        "features": ["Platform", "Year", "Genre", "Publisher", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"],
        "target": "Global_Sales",
    }
