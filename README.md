# 🏡 NESTORA AI – House Price Prediction System

### AI-Powered Real Estate Price Estimation Using Machine Learning

NESTORA AI is a machine learning-based house price prediction system that estimates residential property prices in Bengaluru, India. Built using Python, Scikit-learn, and Streamlit, the application allows users to enter property details and receive estimated house prices through an interactive web interface.

The project combines data preprocessing, machine learning, model evaluation, and database integration to create a practical real estate price estimation application.

---

## 🚀 Project Overview

Buying or selling a house involves understanding property prices based on several factors, such as location, total area, number of bedrooms, and bathrooms.

NESTORA AI addresses this problem using a trained machine learning model that analyzes historical Bengaluru housing data and predicts an estimated property price based on user inputs.

### Main Objectives

- Analyze Bengaluru housing data.
- Clean and preprocess real estate information.
- Train a machine learning model for price prediction.
- Build an interactive Streamlit web application.
- Store prediction history using SQLite.
- Present model evaluation results through a dashboard.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🏠 House Price Prediction | Estimates property prices based on user inputs. |
| 📍 Location-Based Input | Allows users to select a property location. |
| 📐 Property Details | Accepts area, BHK, and bathroom information. |
| 🤖 Machine Learning | Uses a trained Random Forest model. |
| 📊 Dashboard | Displays model performance information. |
| 🕒 Prediction History | Stores previous predictions in SQLite. |
| 📥 CSV Export | Allows users to download prediction history. |
| 💻 Interactive Interface | Provides a Streamlit-based user experience. |

---

## 🧠 Machine Learning Model

The project uses a **Random Forest Regressor** to estimate house prices.

### Machine Learning Workflow

1. Load the Bengaluru housing dataset.
2. Explore and understand the dataset.
3. Handle missing and inconsistent values.
4. Clean and preprocess the data.
5. Prepare input features and target values.
6. Split the dataset into training and testing sets.
7. Train the Random Forest model.
8. Evaluate model performance.
9. Save the trained model for application use.

### Model Evaluation

The model was evaluated using three standard regression metrics.

| Metric | Result |
|---|---:|
| Mean Absolute Error (MAE) | 31.19 Lakhs |
| Root Mean Squared Error (RMSE) | 90.717 Lakhs |
| R² Score | 0.5885 |

**Note:** These results are from the current training run. Predictions are estimates based on the available dataset and should not be treated as official property valuations.

---

## 📂 Dataset Information

**Dataset:** Bengaluru House Data

The dataset contains historical residential property information for Bengaluru.

- Original dataset records: 13,320
- Usable records after preprocessing: 11,713
- Dataset format: CSV
- File name: `Bengaluru_House_Data.csv`

### Important Features

- Location
- Total square feet
- Number of bedrooms (BHK)
- Number of bathrooms
- Property price

The dataset is cleaned and processed before model training.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning |
| Random Forest | Price prediction model |
| Streamlit | Web application |
| SQLite | Prediction history database |
| Joblib | Saving and loading the trained model |
| Git & GitHub | Version control and project hosting |

---

## 📁 Project Structure

```text
NESTORA-AI-House-Price-Prediction/
│
├── app.py
│
├── train_model.py
│
├── database.py
│
├── Bengaluru_House_Data.csv
│
├── house_price_model.joblib
│
├── model_metrics.json
│
├── requirements.txt
│
├── DATASET_INSTRUCTIONS.txt
│
├── README.md
│
└── .gitignore
```

### File Description

| File | Description |
|---|---|
| `app.py` | Main Streamlit application |
| `train_model.py` | Data preprocessing, model training, and evaluation |
| `database.py` | SQLite database operations |
| `Bengaluru_House_Data.csv` | Housing dataset |
| `house_price_model.joblib` | Trained machine learning model |
| `model_metrics.json` | Saved model evaluation metrics |
| `requirements.txt` | Required Python libraries |
| `DATASET_INSTRUCTIONS.txt` | Dataset information and instructions |
| `.gitignore` | Files excluded from Git tracking |

---

## ⚙️ Installation and Setup

Follow these steps to run NESTORA AI on your local computer.

### 1. Clone the Repository

```bash
git clone https://github.com/meganadhreddy/NESTORA-AI-House-Price-Prediction.git
```

### 2. Open the Project Folder

```bash
cd NESTORA-AI-House-Price-Prediction
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

---

## 🔄 Model Training

To train the machine learning model again using the dataset, run:

```bash
python train_model.py
```

After successful training, the model and evaluation metrics are saved as:

```text
house_price_model.joblib
model_metrics.json
```

The Streamlit application uses the saved model for predictions.

---

## 🗄️ Database Integration

NESTORA AI uses SQLite to maintain a history of previous house price predictions.

The database functionality is handled by `database.py`.

It supports:

- Creating the prediction history table.
- Saving prediction records.
- Retrieving previous predictions.
- Displaying prediction history.
- Exporting history as a CSV file.

The database file is created locally when the application runs.

---

## 🎯 Expected Application Workflow

```text
User Opens Application
          |
          v
Enters Property Details
          |
          v
Machine Learning Model
          |
          v
Predicted House Price
          |
          v
Save Prediction in SQLite
          |
          v
View Prediction History
```

---

## 🔮 Future Improvements

The project can be extended with the following features:

- Integrate real-time property listings.
- Add interactive maps for property locations.
- Experiment with advanced machine learning algorithms.
- Improve prediction accuracy through feature engineering.
- Add user authentication and personalized dashboards.
- Deploy the application to a cloud platform.
- Support additional cities and housing markets.

---

## 👨‍💻 Project Information

**Project Name:** NESTORA AI – House Price Prediction System

**Domain:** Artificial Intelligence and Machine Learning

**Application Type:** Machine Learning Web Application

**Programming Language:** Python

**Framework:** Streamlit

**Repository:** [NESTORA AI – GitHub](https://github.com/meganadhreddy/NESTORA-AI-House-Price-Prediction)

---

## ⭐ Conclusion

NESTORA AI demonstrates how machine learning can be applied to real-world real estate problems. By combining data preprocessing, Random Forest regression, Streamlit, and SQLite, the project provides an interactive platform for estimating residential property prices.

The project also demonstrates practical skills in Python programming, data analysis, machine learning model development, database integration, and application development.

**Built with Python, Machine Learning, and Streamlit.** 🏡