import json
import re
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Bengaluru_House_Data.csv"
MODEL_PATH = BASE_DIR / "house_price_model.joblib"
METRICS_PATH = BASE_DIR / "model_metrics.json"

def parse_sqft(value):
    """Convert values such as '1200', '2100 - 2850' into a numeric square-foot value."""
    if pd.isna(value):
        return np.nan
    text = str(value).strip().replace(",", "")
    numbers = re.findall(r"\d+(?:\.\d+)?", text)
    if not numbers:
        return np.nan
    values = [float(number) for number in numbers[:2]]
    return sum(values) / len(values)

def parse_bhk(value):
    if pd.isna(value):
        return np.nan
    match = re.search(r"\d+", str(value))
    return float(match.group()) if match else np.nan

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Dataset not found. Download the Bengaluru dataset, rename it "
            "'Bengaluru_House_Data.csv', and place it beside train_model.py."
        )

    df = pd.read_csv(DATA_PATH)
    required = {"location", "total_sqft", "size", "bath", "price"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing)}. "
            "Use the Bengaluru House Price dataset with columns location, "
            "total_sqft, size, bath and price."
        )

    data = df[["location", "total_sqft", "size", "bath", "price"]].copy()
    data["location"] = data["location"].astype("string").str.strip()
    data["total_sqft"] = data["total_sqft"].apply(parse_sqft)
    data["bhk"] = data["size"].apply(parse_bhk)
    data["bath"] = pd.to_numeric(data["bath"], errors="coerce")
    data["price"] = pd.to_numeric(data["price"], errors="coerce")

    data = data.drop(columns=["size"]).dropna()
    data = data[
        (data["location"] != "")
        & (data["total_sqft"] > 100)
        & (data["total_sqft"] < 50000)
        & (data["bhk"] >= 1)
        & (data["bath"] >= 1)
        & (data["price"] > 0)
    ].copy()

    # Keep locations with enough examples to make a useful category.
    location_counts = data["location"].value_counts()
    data = data[data["location"].isin(location_counts[location_counts >= 5].index)].copy()

    if len(data) < 50:
        raise ValueError(
            f"Only {len(data)} usable rows remain. Check that you downloaded the correct dataset."
        )

    features = ["location", "total_sqft", "bhk", "bath"]
    X = data[features]
    y = data["price"]

    categorical_features = ["location"]
    numeric_features = ["total_sqft", "bhk", "bath"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("location", Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]), categorical_features),
            ("numbers", Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
            ]), numeric_features),
        ]
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=250, random_state=42, min_samples_leaf=2, n_jobs=-1
        )),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
    metrics = {
        "model": "RandomForestRegressor",
        "test_rows": int(len(X_test)),
        "mae_lakh": round(float(mean_absolute_error(y_test, predictions)), 3),
        "rmse_lakh": round(rmse, 3),
        "r2_score": round(float(r2_score(y_test, predictions)), 4),
        "locations": sorted(data["location"].dropna().unique().tolist()),
    }

    joblib.dump(pipeline, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print("Model training completed.")
    print(f"Usable dataset rows: {len(data)}")
    print(f"MAE: {metrics['mae_lakh']} lakh")
    print(f"RMSE: {metrics['rmse_lakh']} lakh")
    print(f"R2 score: {metrics['r2_score']}")
    print(f"Saved model: {MODEL_PATH.name}")
    print(f"Saved metrics: {METRICS_PATH.name}")

if __name__ == "__main__":
    main()
