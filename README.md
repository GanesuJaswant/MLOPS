# Machine Learning APIs with Docker

This workspace contains two containerized Machine Learning FastAPI microservices:

1. **Customer Churn Prediction API** (Port `8000`)
2. **Video Game Sales Prediction API** (Port `8001`)

---

## 0. Prerequisites & Docker Installation

If Docker is not yet installed on your Windows machine:

1. **Download Docker Desktop for Windows**:
   - Official installer: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
   - Direct download: [Docker Desktop Installer.exe](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)
2. **Run Installer**:
   - Make sure **"Use WSL 2 instead of Hyper-V"** is checked during installation.
   - Restart your computer if prompted.
3. **Verify Installation** (in PowerShell or CMD):
   ```cmd
   docker --version
   docker compose version
   ```

---

## Quick Start (Run Both Projects Together)

You can launch both services simultaneously using Docker Compose:

```cmd
cd c:\Users\ganes\Desktop\churn-prediction

:: Step 1: Copy churn model files
cd churn_prediction
setup.bat
cd ..

:: Step 2: Build and start both containers
docker compose up --build -d
```

Once running:
- **Customer Churn API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Video Game Sales API**: [http://localhost:8001/docs](http://localhost:8001/docs)

To stop both services:
```cmd
docker compose down
```

---

## Project 1: Customer Churn Prediction API

Predicts whether a telecom customer is likely to churn using a pre-trained **RandomForestClassifier**.

### Directory Structure
```
churn_prediction/
├── Dockerfile
├── requirements.txt
├── main.py
├── setup.bat
├── copy_artifacts.py
├── data/
│   └── processed/
│       └── dataset_metadata.json
└── models/
    ├── random_forest_baseline.pkl
    ├── scaler.pkl
    └── ohe.pkl
```

### Build & Run Commands

```cmd
cd c:\Users\ganes\Desktop\churn-prediction\churn_prediction

:: 1. Copy model files from Downloads
setup.bat

:: 2. Build the Docker image
docker build -t churn-api .

:: 3. Run the Docker container
docker run -d --name churn-container -p 8000:8000 churn-api
```

### Interactive API Docs
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Test the Endpoint
```cmd
curl -X POST "http://localhost:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"gender\": \"Female\", \"SeniorCitizen\": 0, \"Partner\": \"Yes\", \"Dependents\": \"No\", \"tenure\": 1, \"PhoneService\": \"No\", \"MultipleLines\": \"No phone service\", \"InternetService\": \"DSL\", \"OnlineSecurity\": \"No\", \"OnlineBackup\": \"Yes\", \"DeviceProtection\": \"No\", \"TechSupport\": \"No\", \"StreamingTV\": \"No\", \"StreamingMovies\": \"No\", \"Contract\": \"Month-to-month\", \"PaperlessBilling\": \"Yes\", \"PaymentMethod\": \"Electronic check\", \"MonthlyCharges\": 29.85, \"TotalCharges\": 29.85}"
```

**Sample Output:**
```json
{
  "churn_prediction": 1,
  "churn_probability": 0.68,
  "message": "Customer is likely to churn."
}
```

---

## Project 2: Video Game Sales Prediction API

Predicts global video game sales (in millions) using a **RandomForestRegressor** pipeline (with `OneHotEncoder` and `StandardScaler`).

### Directory Structure
```
videogame_sales_prediction/
├── Dockerfile
├── requirements.txt
├── train.py
└── main.py
```

### Build & Run Commands

```cmd
cd c:\Users\ganes\Desktop\churn-prediction\videogame_sales_prediction

:: 1. Build the Docker image (automatically trains and packages the model)
docker build -t videogame-api .

:: 2. Run the Docker container
docker run -d --name videogame-container -p 8001:8001 videogame-api
```

### Interactive API Docs
- Swagger UI: [http://localhost:8001/docs](http://localhost:8001/docs)
- ReDoc: [http://localhost:8001/redoc](http://localhost:8001/redoc)

### Test the Endpoint
```cmd
curl -X POST "http://localhost:8001/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"Platform\": \"Wii\", \"Year\": 2006, \"Genre\": \"Sports\", \"Publisher\": \"Nintendo\", \"NA_Sales\": 41.49, \"EU_Sales\": 29.02, \"JP_Sales\": 3.77, \"Other_Sales\": 8.46}"
```

**Sample Output:**
```json
{
  "predicted_global_sales": 82.74,
  "message": "Predicted global sales: 82.74M units"
}
```
