
import json
import sqlite3
from pathlib import Path
from datetime import datetime

import joblib
import pandas as pd
import streamlit as st


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "house_price_model.joblib"
METRICS_PATH = BASE_DIR / "model_metrics.json"
DATA_PATH = BASE_DIR / "Bengaluru_House_Data.csv"
DB_PATH = BASE_DIR / "predictions.db"

st.set_page_config(
    page_title="NESTORA AI | Property Intelligence",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# 2. CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp {
    background: #071512;
    color: #F4F5F1;
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #F5F4EE !important;
}

.brand {
    color: #C5A879;
    font-family: 'Playfair Display', serif;
    font-size: 34px;
    font-weight: 700;
    letter-spacing: 3px;
}

.eyebrow {
    color: #8AB9A9;
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: 700;
}

.hero {
    background: linear-gradient(110deg, #103D34, #09221D 70%, #102E28);
    border: 1px solid #28564B;
    padding: 45px;
    border-radius: 22px;
    margin: 20px 0 28px 0;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 48px;
    line-height: 1.15;
    color: #FFFFFF;
}

.hero-text {
    color: #C5D9D1;
    font-size: 16px;
    max-width: 650px;
    line-height: 1.8;
}

.panel {
    background: #10231F;
    border: 1px solid #25483F;
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 16px;
}

.metric-card {
    background: #10231F;
    border: 1px solid #25483F;
    border-radius: 15px;
    padding: 20px;
}

.metric-label {
    color: #A6BEB4;
    font-size: 13px;
}

.metric-value {
    color: #E4C697;
    font-size: 27px;
    font-weight: 700;
    margin-top: 7px;
}

.property-card {
    background: #10231F;
    border: 1px solid #25483F;
    border-radius: 15px;
    overflow: hidden;
    margin-bottom: 15px;
}

.property-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
}

.property-info {
    padding: 15px;
}

.property-price {
    color: #E4C697;
    font-size: 23px;
    font-weight: 700;
}

.property-name {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 600;
    margin-top: 5px;
}

.property-detail {
    color: #A9BDB5;
    font-size: 12px;
    margin-top: 9px;
}

div[data-testid="stForm"] {
    background: #10231F;
    border: 1px solid #31574C;
    padding: 24px;
    border-radius: 17px;
}

.stButton > button,
.stFormSubmitButton > button {
    background: #C5A879;
    color: #101B17;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    min-height: 43px;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #E2C99D;
    color: #101B17;
    border: none;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #172C26;
    border-color: #45675C;
}

label, .stMarkdown p {
    color: #D7E2DC;
}

hr {
    border-color: #29483F;
}

.footer {
    text-align: center;
    color: #81968C;
    font-size: 12px;
    padding: 30px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD MODEL AND DATA
# ==========================================

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_metrics():
    if METRICS_PATH.exists():
        with open(METRICS_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


@st.cache_data
def load_locations():
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        locations = (
            df["location"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )
        return sorted([x for x in locations if x])

    return ["Whitefield", "Electronic City", "Sarjapur Road"]


model = load_model()
metrics = load_metrics()
locations = load_locations()


# ==========================================
# 4. DATABASE
# ==========================================

def create_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            area REAL,
            bhk INTEGER,
            bathrooms INTEGER,
            predicted_price REAL,
            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_prediction(location, area, bhk, bathrooms, price):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (location, area, bhk, bathrooms, predicted_price, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        location,
        area,
        bhk,
        bathrooms,
        price,
        datetime.now().strftime("%d-%m-%Y %I:%M %p")
    ))

    connection.commit()
    connection.close()


def get_history():
    connection = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY id DESC",
        connection
    )

    connection.close()
    return df


create_database()


# ==========================================
# 5. NAVIGATION
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

nav1, nav2, nav3, nav4 = st.columns([2, 1, 1, 1])

with nav1:
    st.markdown('<div class="brand">NESTORA.</div>', unsafe_allow_html=True)
    st.caption("AI PROPERTY INTELLIGENCE")

with nav2:
    if st.button("Home", width="stretch"):
        st.session_state.page = "Home"

with nav3:
    if st.button("Dashboard", width="stretch"):
        st.session_state.page = "Dashboard"

with nav4:
    if st.button("History", width="stretch"):
        st.session_state.page = "History"

st.markdown("---")


# ==========================================
# 6. HOME PAGE
# ==========================================

if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">INTELLIGENT REAL ESTATE PLATFORM</div>
        <div class="hero-title">
            Find your place.<br>
            Understand its value.
        </div>
        <p class="hero-text">
            Explore properties and discover estimated house values
            using machine learning and real estate data from Bengaluru.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Explore Properties")
    st.caption("Example property styles. These cards are visual examples, not live listings.")

    property_data = [
        {
            "name": "Contemporary Villa",
            "location": "Whitefield",
            "price": "₹1.25 Cr",
            "details": "3 BHK  •  1800 Sq.ft",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=900"
        },
        {
            "name": "Modern Family Home",
            "location": "Sarjapur Road",
            "price": "₹95 Lakh",
            "details": "3 BHK  •  1450 Sq.ft",
            "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=900"
        },
        {
            "name": "Luxury Residence",
            "location": "Electronic City",
            "price": "₹78 Lakh",
            "details": "2 BHK  •  1250 Sq.ft",
            "image": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=900"
        }
    ]

    columns = st.columns(3)

    for column, item in zip(columns, property_data):
        with column:
            st.markdown(f"""
            <div class="property-card">
                <img src="{item['image']}">
                <div class="property-info">
                    <div class="property-price">{item['price']}</div>
                    <div class="property-name">{item['name']}</div>
                    <div class="property-detail">
                        {item['location']}<br>
                        {item['details']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("## Find Your Property Value")

    st.markdown("""
    <div class="panel">
        <h3>AI Property Valuation</h3>
        <p>Enter your property details to estimate its market value.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Price Prediction", width="stretch"):
        st.session_state.page = "Dashboard"
        st.rerun()

    st.markdown("## Why NESTORA AI?")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">AI</div>
            <div class="metric-label">Machine learning valuation</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">Data</div>
            <div class="metric-label">Bengaluru property dataset</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">History</div>
            <div class="metric-label">Saved prediction records</div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 7. PRICE PREDICTION DASHBOARD
# ==========================================

elif st.session_state.page == "Dashboard":

    st.markdown("""
    <div class="eyebrow">NESTORA INTELLIGENCE / VALUATION</div>
    <h1>Property Valuation Dashboard</h1>
    <p style="color:#A9BDB5">
        Estimate your Bengaluru property's value with our Random Forest model.
    </p>
    """, unsafe_allow_html=True)

    if model is None:
        st.error("Trained model not found. Please run: python train_model.py")
    else:

        left, right = st.columns([1.2, 0.8], gap="large")

        with left:
            st.markdown("### Enter Property Details")

            with st.form("prediction_form"):

                location = st.selectbox(
                    "Property Location",
                    options=locations
                )

                area = st.number_input(
                    "Area (square feet)",
                    min_value=100.0,
                    max_value=50000.0,
                    value=1200.0,
                    step=50.0
                )

                col1, col2 = st.columns(2)

                with col1:
                    bhk = st.number_input(
                        "Bedrooms (BHK)",
                        min_value=1,
                        max_value=20,
                        value=2,
                        step=1
                    )

                with col2:
                    bathrooms = st.number_input(
                        "Bathrooms",
                        min_value=1,
                        max_value=20,
                        value=2,
                        step=1
                    )

                submitted = st.form_submit_button(
                    "Predict Property Price",
                    width="stretch"
                )

            if submitted:
                input_data = pd.DataFrame([{
                    "location": location,
                    "total_sqft": area,
                    "bhk": bhk,
                    "bath": bathrooms
                }])

                try:
                    predicted_price = float(model.predict(input_data)[0])

                    if predicted_price <= 0:
                        st.error("The model returned an invalid price.")
                    else:
                        save_prediction(
                            location,
                            area,
                            bhk,
                            bathrooms,
                            predicted_price
                        )

                        st.session_state.latest_prediction = {
                            "price": predicted_price,
                            "location": location,
                            "area": area,
                            "bhk": bhk,
                            "bath": bathrooms
                        }

                except Exception as error:
                    st.error(f"Prediction failed: {error}")

        with right:
            st.markdown("### Valuation Result")

            result = st.session_state.get("latest_prediction")

            if result:
                price = result["price"]

                st.markdown(f"""
                <div class="hero">
                    <div class="eyebrow">ESTIMATED PROPERTY VALUE</div>
                    <div class="hero-title" style="font-size:39px">
                        ₹ {price:,.2f} Lakh
                    </div>
                    <p class="hero-text">
                        Estimated value for {result['location']}.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### Property Summary")

                st.markdown(f"""
                <div class="panel">
                    <p>📍 Location: <b>{result['location']}</b></p>
                    <p>📐 Area: <b>{result['area']:,.0f} sq.ft</b></p>
                    <p>🛏️ Bedrooms: <b>{result['bhk']} BHK</b></p>
                    <p>🚿 Bathrooms: <b>{result['bath']}</b></p>
                    <p>💰 Price per sq.ft: <b>₹{price * 100000 / result['area']:,.0f}</b></p>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.info("Enter your property details and click Predict Property Price.")

    st.markdown("---")
    st.markdown("### Model Performance")

    if metrics:
        m1, m2, m3 = st.columns(3)

        with m1:
            st.metric("MAE", f"{metrics.get('mae_lakh', 0)} Lakh")

        with m2:
            st.metric("RMSE", f"{metrics.get('rmse_lakh', 0)} Lakh")

        with m3:
            st.metric("R² Score", metrics.get("r2_score", "N/A"))

    st.caption(
        "Predictions are estimates based on historical training data, "
        "not official property valuations or guaranteed selling prices."
    )


# ==========================================
# 8. PREDICTION HISTORY
# ==========================================

elif st.session_state.page == "History":

    st.markdown("""
    <div class="eyebrow">YOUR PROPERTY ACTIVITY</div>
    <h1>Prediction History</h1>
    <p style="color:#A9BDB5">
        Review your previously saved property valuations.
    </p>
    """, unsafe_allow_html=True)

    history = get_history()

    if history.empty:
        st.info("No predictions saved yet. Make your first prediction.")

    else:
        st.metric("Total Predictions", len(history))

        st.dataframe(
            history,
            width="stretch",
            hide_index=True
        )

        csv_data = history.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Prediction History",
            data=csv_data,
            file_name="nestora_prediction_history.csv",
            mime="text/csv"
        )


# ==========================================
# 9. FOOTER
# ==========================================

st.markdown("""
<div class="footer">
    NESTORA AI · PROPERTY INTELLIGENCE PLATFORM<br>
    Built with Python · Streamlit · Machine Learning
</div>
""", unsafe_allow_html=True)
