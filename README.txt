# 🏘️ PrimeEstate AI: Luxury Real Estate Valuator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**PrimeEstate AI** is a premium SaaS-style dashboard that provides professional-grade property appraisals using Machine Learning. It bridges the gap between raw data and luxury user experience.

## ✨ Key Features
* **Algorithmic Appraisal:** Uses a refined Linear Regression model trained on the California Housing Dataset.
* **Bento-Grid UX:** A modern, glassmorphic interface designed for clarity and a "premium" feel.
* **Explainable AI (XAI):** Provides a dynamic "Valuation Breakdown" to explain the factors (Location, Size, Layout) driving the price.
* **Market Sentiment Engine:** Real-time logic that determines if a local market is **RISING** or **COOLING**.
* **Geographic Intelligence:** Automatically maps 30+ major California cities to their exact coordinates for model precision.

## 🚀 Technical Architecture
The system follows a standard ML pipeline:
1.  **Preprocessing:** Feature scaling using `StandardScaler` to handle multivariate input ranges.
2.  **Inference:** A `Scikit-Learn` regression engine calculates the baseline market value.
3.  **UI/UX:** A custom-styled `Streamlit` frontend using CSS injection for glassmorphism and responsive typography.vv

![image alt](https://github.com/rehan-hash/PrimeEstate-AI/blob/main/preview1.png?raw=true)
![image alt](https://github.com/rehan-hash/PrimeEstate-AI/blob/main/preview2.png?raw=true)
      
## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/rehan-hash/primeestate-ai.git](https://github.com/rehan-hash/primeestate-ai.git)
   cd primeestate-ai
