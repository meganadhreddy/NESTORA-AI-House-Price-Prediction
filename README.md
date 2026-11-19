# House Price Prediction System

A Bengaluru house-price estimation project using Python, Pandas, Scikit-learn,
Streamlit and SQLite.

## 1. Files

- `app.py` — Streamlit web application
- `train_model.py` — cleans the dataset, trains and evaluates the model
- `database.py` — creates the SQLite prediction-history table
- `requirements.txt` — Python dependencies
- `Bengaluru_House_Data.csv` — dataset file you download separately
- `house_price_model.joblib` — generated after training
- `model_metrics.json` — generated after training
- `predictions.db` — generated when the app runs

## 2. Dataset

Use the Bengaluru House Price dataset whose CSV includes these columns:
`location`, `total_sqft`, `size`, `bath`, and `price`.

Save the downloaded CSV in this same folder with the exact filename:
`Bengaluru_House_Data.csv`.

Do not use a different dataset without adapting `train_model.py`.

## 3. Install dependencies

Activate your virtual environment, then run:

```bash
python -m pip install -r requirements.txt
```

## 4. Train the machine-learning model

```bash
python train_model.py
```

Training creates `house_price_model.joblib` and `model_metrics.json`.

## 5. Run the Streamlit application

```bash
python -m streamlit run app.py
```

Streamlit will show a local address, usually `http://localhost:8501`.

## 6. Notes

- The model predicts price in lakh rupees, based on the dataset's `price` column.
- Predictions are estimates and should not be treated as official property valuations.
- The training script reports MAE, RMSE and R-squared on a held-out test set.
- The database stores predictions made in the app.
