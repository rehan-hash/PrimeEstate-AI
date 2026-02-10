import streamlit as st
import pickle
import numpy as np
import pandas as pd
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="PrimeEstate AI | Luxury Valuations", layout="centered")

# --- LOAD ASSETS ---
@st.cache_resource
def load_assets():
    model = pickle.load(open('house_model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    return model, scaler

model, scaler = load_assets()

# --- LUXURY CITY DATABASE (Expanded) ---
locations = {
  "San Francisco": (37.77, -122.42),
    "Palo Alto": (37.44, -122.14),
    "Mountain View": (37.38, -122.08),
    "Cupertino": (37.32, -122.03),
    "San Jose": (37.33, -121.89),
    "Oakland": (37.80, -122.27),
    "Berkeley": (37.87, -122.27),
    "Walnut Creek": (37.91, -122.06),
    "Woodside": (37.42, -122.25),
    "Los Altos": (37.38, -122.11),

    # --- Southern California Coastal & Luxury ---
    "Beverly Hills": (34.07, -118.40),
    "Bel Air": (34.08, -118.44),
    "Malibu": (34.02, -118.77),
    "Santa Monica": (34.01, -118.49),
    "Pacific Palisades": (34.04, -118.52),
    "Newport Beach": (33.61, -117.92),
    "Laguna Beach": (33.54, -117.78),
    "Manhattan Beach": (33.88, -118.41),
    "Santa Barbara": (34.42, -119.69),
    "Montecito": (34.43, -119.63),
    "San Diego": (32.71, -117.16),
    "La Jolla": (32.83, -117.27),
    "Coronado": (32.68, -117.17),

    # --- Major Cities & Inland Wealth ---
    "Los Angeles": (34.05, -118.24),
    "Pasadena": (34.14, -118.14),
    "Irvine": (33.68, -117.79),
    "Sacramento": (38.58, -121.49),
    "Palm Springs": (33.83, -116.54),
    "Fresno": (36.74, -119.77),
    "Riverside": (33.95, -117.39),
    "Anaheim": (33.83, -117.91),
    "Temecula": (33.49, -117.14),
    "Yorba Linda": (33.88, -117.77)
}

# --- LUXURY CSS INJECTION ---
st.markdown("""
    <style>
    /* Dark Premium Gradient Background */
    .stApp {
        background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
    }



    /* Custom Header Style */
    .luxury-header {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    /* Result Glow Card */
    .result-card {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid #3b82f6;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
    }

    .price-text {
        font-size: 4rem;
        font-weight: 900;
        color: #60a5fa;
        margin: 0;
    }

    /* Elegant Button */
    div.stButton > button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        width: 100%;
        border-radius: 12px;
        height: 55px;
        font-weight: bold;
        border: none;
        transition: 0.3s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
    
    /* 1. Global Root Font Size (Affects everything) */
    html, body, [class*="css"] {
        font-size: 1.15rem !important; /* Increases all text by ~15% */
    }

    /* 2. Target Specific Widget Labels (Bedrooms, Bathrooms, etc.) */
    .stWidgetLabel p {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin-bottom: 10px !important;
    }

    /* 3. Increase Input Box Text (The numbers and dropdowns) */
    input {
        font-size: 1.2rem !important;
    }

    /* 4. Increase Radio Button Text */
    div[data-baseweb="radio"] div {
        font-size: 1.1rem !important;
    }

    /* 5. Pricing Text (Make it even bolder) */
    .price-text {
        font-size: 4.5rem !important; /* Massive price display */
        font-weight: 900;
    }

    /* 6. Section Headers */
    h3 {
        font-size: 1.8rem !important;
        margin-top: 20px !important;
    }

    </style>
""", unsafe_allow_html=True)

# --- APP LAYOUT ---
st.markdown('<h1 class="luxury-header">PrimeEstate AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; opacity:0.6; margin-bottom:30px;"> Algorithmic Real Estate Valuation</p>', unsafe_allow_html=True)

# Main centered column
col_left, col_mid, col_right = st.columns([0.1, 1, 0.1])

with col_mid:
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    
    with st.form("luxury_prediction_form"):
        st.write("### 💎 Property Details")
        
        sqft = st.number_input("Living Area (Sq Ft)", 500, 15000, 2500)
        
        c1, c2 = st.columns(2)
        with c1:
            bhk = st.radio("Bedrooms", [1, 2, 3, 4, 5, 6], index=2, horizontal=True)
        with c2:
            bath = st.radio("Bathrooms", [1, 2, 3, 4, 5], index=1, horizontal=True)
        
        st.markdown("---")
        st.write("### 📍 Location Context")
        selected_city = st.selectbox("Market Region", sorted(locations.keys()))
        
        st.write("")
        submit = st.form_submit_button("GENERATE VALUATION")

    # --- PREDICTION & SENTIMENT LOGIC ---
    if submit:
        with st.spinner("Analyzing neighborhood metrics..."):
            time.sleep(1.5) # The "expensive" delay
            
            # 1. Fetch Location Coords
            lat, lon = locations[selected_city]
            
            # 2. Build Feature Array (California Model Order)
            # [MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Lat, Long]
            features = np.array([[5.5, 20, sqft/250, bhk, 1500, 3.2, lat, lon]])
            
            # 3. Model Inference
            scaled = scaler.transform(features)
            prediction = model.predict(scaled)[0]
            final_price = abs(prediction * 100000)

            # 4. Dynamic Sentiment Logic
            benchmark = 350000 # California Luxury Baseline
            if final_price > benchmark:
                status, delta, color = "RISING", "High Demand", "normal"
            else:
                status, delta, color = "COOLING", "Low Demand", "inverse"

            # 5. Display Result
            st.markdown(f"""
                <div class="result-card">
                    <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.7rem; opacity:0.7;">Market Valuation</p>
                    <div class="price-text">${final_price:,.0f}</div>
                    <p style="opacity:0.5;">Verified for {selected_city}, CA</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Smart Metrics
            st.write("")
            m1, m2 = st.columns(2)
            m1.metric("Price per SqFt", f"${final_price/sqft:,.2f}")
            m2.metric("Market Sentiment", status, delta=delta, delta_color=color)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; opacity:0.3; font-size:0.8rem;'>PrimeEstate AI © 2026</p>", unsafe_allow_html=True)  