# 🌦️ Weather Detection ML System

An end-to-end **Machine Learning–powered Weather Detection and Analysis Web Application** that fetches real-time weather data, performs intelligent analysis, and presents interactive visual insights. The project is built with a focus on **clean ML workflow, secure API handling, and cloud deployment**.

---

## 🚀 Project Overview

The **Weather Detection ML System** integrates real-time weather data using external APIs and applies machine learning techniques to analyze and predict weather trends. The application is deployed on **Streamlit Cloud**, providing an interactive and user-friendly interface.

This project demonstrates the complete lifecycle of an ML application — from data ingestion and preprocessing to model usage and production deployment.

---

## ✨ Key Features

* 🌍 Real-time weather data fetching using OpenWeather API
* 🧠 Machine Learning–based weather analysis & prediction
* 📊 Interactive data visualizations with Plotly
* 🔐 Secure API key management using environment variables
* ☁️ Cloud deployment on Streamlit
* ⚡ Clean, modular, and scalable codebase

---

## 🛠️ Tech Stack

* **Programming Language:** Python
* **Web Framework:** Streamlit
* **Machine Learning:** Scikit-learn
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly
* **API Integration:** OpenWeather API
* **Model Persistence:** Joblib
* **Deployment:** Streamlit Cloud
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
├── app.py                # Main Streamlit application
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── .streamlit/
    └── secrets.toml      # (Cloud only) API keys (not committed)
```

---

## 🔐 API Key Management (Important)

For security reasons, API keys are **NOT hardcoded** in the project.

The application reads API keys from environment variables:

```
WEATHER_API_KEYS
```

### ➤ Streamlit Cloud Setup

Add the following in **Streamlit → Manage App → Settings → Secrets**:

```toml
WEATHER_API_KEYS = "your_api_key_1,your_api_key_2"
```

✔ Supports multiple API keys (comma-separated)

---

## ▶️ How to Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/weather-detection-ml-system.git
cd weather-detection-ml-system
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Environment Variable

**Linux / macOS:**

```bash
export WEATHER_API_KEYS="your_api_key"
```

**Windows (PowerShell):**

```powershell
setx WEATHER_API_KEYS "your_api_key"
```

### 5️⃣ Run the App

```bash
streamlit run app.py
```

---

## 🌐 Live Demo

👉 **Live Application:** https://ktgu7ygaek7mfkkrrk62ad.streamlit.app/



## 📈 Future Enhancements

* Add deep learning–based forecasting
* Improve model accuracy with historical datasets
* Add location-based auto-detection
* Implement API rate-limit handling
* Enhance UI/UX with advanced filters

---

## 🧠 Learning Outcomes

* End-to-end ML application development
* Secure API integration best practices
* Data visualization for real-world datasets
* Cloud deployment using Streamlit
* Writing production-ready Python code

---

## 👤 Author

**Rishi Jain**
Aspiring Machine Learning Engineer | Python Developer

📌 LinkedIn: https://www.linkedin.com/in/rishi-jain-837b75312/

---

## ⭐ Support

If you find this project helpful, consider giving it a ⭐ on GitHub!

---

### 📜 License

This project is open-source and available under the **MIT License**.
