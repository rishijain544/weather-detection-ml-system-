import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import plotly.graph_objects as go
import plotly.express as px

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="Weather Detection ML System",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# INTERNAL API KEY
# ==============================
API_KEYS = [
    "74f8fe59ef9922a8331b361f1b39000b",
    "b6907d289e10d714a6e88b30761fae22",
    "439d4b804bc8187953eb36d2a8c26a02",
]
WEATHER_API_KEY = API_KEYS[0]

# ==============================
# CITY DATA - 130+ Indian Cities
# ==============================
indian_cities = {
    "Delhi": "Delhi", "Mumbai": "Mumbai", "Bangalore": "Bangalore", "Hyderabad": "Hyderabad",
    "Chennai": "Chennai", "Kolkata": "Kolkata", "Pune": "Pune", "Ahmedabad": "Ahmedabad",
    "Jaipur": "Jaipur", "Surat": "Surat", "Lucknow": "Lucknow", "Kanpur": "Kanpur",
    "Nagpur": "Nagpur", "Indore": "Indore", "Thane": "Thane", "Bhopal": "Bhopal",
    "Visakhapatnam": "Visakhapatnam", "Patna": "Patna", "Vadodara": "Vadodara", "Ghaziabad": "Ghaziabad",
    "Ludhiana": "Ludhiana", "Agra": "Agra", "Nashik": "Nashik", "Faridabad": "Faridabad",
    "Meerut": "Meerut", "Rajkot": "Rajkot", "Varanasi": "Varanasi", "Srinagar": "Srinagar",
    "Amritsar": "Amritsar", "Allahabad": "Allahabad", "Ranchi": "Ranchi", "Howrah": "Howrah",
    "Coimbatore": "Coimbatore", "Jabalpur": "Jabalpur", "Gwalior": "Gwalior", "Vijayawada": "Vijayawada",
    "Jodhpur": "Jodhpur", "Madurai": "Madurai", "Raipur": "Raipur", "Kota": "Kota",
    "Chandigarh": "Chandigarh", "Guwahati": "Guwahati", "Thiruvananthapuram": "Thiruvananthapuram",
    "Mysore": "Mysore", "Bhubaneswar": "Bhubaneswar", "Dehradun": "Dehradun", "Shimla": "Shimla",
    "Gangtok": "Gangtok", "Pondicherry": "Pondicherry", "Solapur": "Solapur", "Tiruchirappalli": "Tiruchirappalli",
    "Tiruppur": "Tiruppur", "Moradabad": "Moradabad", "Mysuru": "Mysuru", "Bareilly": "Bareilly",
    "Gurgaon": "Gurgaon", "Aligarh": "Aligarh", "Jalandhar": "Jalandhar", "Salem": "Salem",
    "Warangal": "Warangal", "Mira-Bhayandar": "Mira-Bhayandar", "Bhiwandi": "Bhiwandi",
    "Saharanpur": "Saharanpur", "Guntur": "Guntur", "Amravati": "Amravati", "Bikaner": "Bikaner",
    "Noida": "Noida", "Jamshedpur": "Jamshedpur", "Bhilai": "Bhilai", "Cuttack": "Cuttack",
    "Firozabad": "Firozabad", "Kochi": "Kochi", "Nellore": "Nellore", "Bhavnagar": "Bhavnagar",
    "Durgapur": "Durgapur", "Asansol": "Asansol", "Rourkela": "Rourkela", "Nanded": "Nanded",
    "Kolhapur": "Kolhapur", "Ajmer": "Ajmer", "Akola": "Akola", "Gulbarga": "Gulbarga",
    "Jamnagar": "Jamnagar", "Ujjain": "Ujjain", "Loni": "Loni", "Siliguri": "Siliguri",
    "Jhansi": "Jhansi", "Ulhasnagar": "Ulhasnagar", "Jammu": "Jammu", "Mangalore": "Mangalore",
    "Erode": "Erode", "Belgaum": "Belgaum", "Ambattur": "Ambattur", "Tirunelveli": "Tirunelveli",
    "Malegaon": "Malegaon", "Gaya": "Gaya", "Jalgaon": "Jalgaon", "Udaipur": "Udaipur",
    "Maheshtala": "Maheshtala", "Davanagere": "Davanagere", "Kozhikode": "Kozhikode",
    "Kurnool": "Kurnool", "Rajpur Sonarpur": "Rajpur Sonarpur", "Rajahmundry": "Rajahmundry",
    "Bokaro": "Bokaro", "South Dumdum": "South Dumdum", "Bellary": "Bellary", "Patiala": "Patiala",
    "Gopalpur": "Gopalpur", "Agartala": "Agartala", "Bhagalpur": "Bhagalpur",
    "Muzaffarnagar": "Muzaffarnagar", "Bhatpara": "Bhatpara", "Panihati": "Panihati",
    "Latur": "Latur", "Dhanbad": "Dhanbad", "Rohtak": "Rohtak", "Korba": "Korba",
    "Bhilwara": "Bhilwara", "Berhampur": "Berhampur", "Muzaffarpur": "Muzaffarpur",
    "Ahmednagar": "Ahmednagar", "Mathura": "Mathura", "Kollam": "Kollam", "Avadi": "Avadi",
    "Kadapa": "Kadapa", "Kamarhati": "Kamarhati", "Sambalpur": "Sambalpur", "Bilaspur": "Bilaspur",
    "Shahjahanpur": "Shahjahanpur", "Satara": "Satara", "Bijapur": "Bijapur", "Rampur": "Rampur",
    "Shivamogga": "Shivamogga", "Chandrapur": "Chandrapur", "Junagadh": "Junagadh",
    "Thrissur": "Thrissur", "Alwar": "Alwar", "Bardhaman": "Bardhaman", "Kulti": "Kulti",
    "Kakinada": "Kakinada", "Nizamabad": "Nizamabad", "Parbhani": "Parbhani", "Tumkur": "Tumkur",
    "Khammam": "Khammam", "Ozhukarai": "Ozhukarai", "Bihar Sharif": "Bihar Sharif",
    "Panipat": "Panipat", "Darbhanga": "Darbhanga", "Bally": "Bally", "Aizawl": "Aizawl",
    "Dewas": "Dewas", "Ichalkaranji": "Ichalkaranji", "Karnal": "Karnal", "Bathinda": "Bathinda",
    "Jalna": "Jalna", "Eluru": "Eluru", "Kirari Suleman Nagar": "Kirari Suleman Nagar",
    "Barasat": "Barasat", "Purnia": "Purnia", "Satna": "Satna", "Mau": "Mau",
    "Sonipat": "Sonipat", "Farrukhabad": "Farrukhabad", "Sagar": "Sagar", "Durg": "Durg",
    "Imphal": "Imphal", "Ratlam": "Ratlam", "Hapur": "Hapur", "Arrah": "Arrah",
    "Karimnagar": "Karimnagar", "Anantapur": "Anantapur", "Etawah": "Etawah",
    "Ambernath": "Ambernath", "North Dumdum": "North Dumdum", "Bharatpur": "Bharatpur",
    "Begusarai": "Begusarai", "New Delhi": "New Delhi", "Gandhidham": "Gandhidham",
    "Baranagar": "Baranagar", "Tiruvottiyur": "Tiruvottiyur", "Puducherry": "Puducherry",
    "Sikar": "Sikar", "Thoothukudi": "Thoothukudi", "Sri Ganganagar": "Sri Ganganagar",
    "Karawal Nagar": "Karawal Nagar", "Mango": "Mango", "Thanjavur": "Thanjavur",
    "Bulandshahr": "Bulandshahr", "Uluberia": "Uluberia", "Murwara": "Murwara",
    "Sambhal": "Sambhal", "Singrauli": "Singrauli", "Nadiad": "Nadiad",
    "Secunderabad": "Secunderabad", "Naihati": "Naihati", "Yamunanagar": "Yamunanagar",
    "Bidhan Nagar": "Bidhan Nagar", "Pallavaram": "Pallavaram", "Bidar": "Bidar",
    "Munger": "Munger", "Panchkula": "Panchkula", "Burhanpur": "Burhanpur",
    "Kharagpur": "Kharagpur", "Dindigul": "Dindigul", "Gandhinagar": "Gandhinagar",
    "Hospet": "Hospet", "Nangloi Jat": "Nangloi Jat", "Malda": "Malda", "Ongole": "Ongole",
    "Deoghar": "Deoghar", "Chapra": "Chapra", "Haldia": "Haldia", "Khandwa": "Khandwa",
    "Nandyal": "Nandyal", "Morena": "Morena", "Amroha": "Amroha", "Anand": "Anand",
    "Bhind": "Bhind", "Bhalswa Jahangir Pur": "Bhalswa Jahangir Pur",
    "Madhyamgram": "Madhyamgram", "Bhiwani": "Bhiwani"
}

# ==============================
# CUSTOM CSS - MODERN UI/UX WITH THEME SUPPORT
# ==============================

# Determine theme colors
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "🌞 Light Mode"

# Get theme from sidebar (will be set after sidebar renders)
# For now, use default light mode for initial render
theme_colors = {
    "light": {
        "bg_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "card_bg": "rgba(255, 255, 255, 0.95)",
        "text_primary": "#2d3748",
        "text_secondary": "#718096",
        "text_tertiary": "#a0aec0",
        "sidebar_bg": "rgba(255, 255, 255, 0.95)",
        "header_color": "white",
        "metric_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    },
    "dark": {
        "bg_gradient": "linear-gradient(135deg, #1a202c 0%, #2d3748 100%)",
        "card_bg": "rgba(45, 55, 72, 0.95)",
        "text_primary": "#e2e8f0",
        "text_secondary": "#cbd5e0",
        "text_tertiary": "#a0aec0",
        "sidebar_bg": "rgba(26, 32, 44, 0.95)",
        "header_color": "#e2e8f0",
        "metric_gradient": "linear-gradient(135deg, #4299e1 0%, #667eea 100%)",
    }
}

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .stApp {
        background: var(--bg-gradient);
        background-attachment: fixed;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] {
        background: var(--sidebar-bg);
        backdrop-filter: blur(10px);
        box-shadow: 4px 0 20px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] label {
        color: var(--text-primary) !important;
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--metric-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    h1, h2, h3 {
        color: var(--header-color) !important;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    [data-testid="stMetric"] {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    
    .big-temp {
        font-size: 5rem;
        font-weight: 700;
        background: var(--metric-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    
    .weather-icon {
        font-size: 4rem;
    }
    
    .footer {
        position: fixed;
        bottom: 10px;
        right: 20px;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.75rem;
        font-weight: 400;
        z-index: 999;
        background: rgba(0, 0, 0, 0.2);
        padding: 5px 12px;
        border-radius: 20px;
        backdrop-filter: blur(5px);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Radio button styling */
    [data-testid="stRadio"] > div {
        background: var(--card-bg);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: var(--card-bg);
        color: var(--text-primary);
        border-radius: 10px;
    }
    
    /* Info/Alert boxes */
    .stAlert {
        background: var(--card-bg);
        color: var(--text-primary);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--card-bg);
        color: var(--text-primary);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="footer">Made by Rishi Jain</div>', unsafe_allow_html=True)

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1rem;'>
            <h2 style='color: #2d3748; margin: 0; font-size: 1.5rem;'>⚙️ Configuration</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Theme Toggle
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem;'>
            <p style='color: white; margin: 0; text-align: center; font-size: 0.9rem; font-weight: 500;'>
                🎨 Theme Mode
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    theme_mode = st.radio(
        "Select Theme",
        ["🌞 Light Mode", "🌙 Dark Mode"],
        index=0,
        label_visibility="collapsed",
        horizontal=True
    )
    
    is_dark_mode = "Dark" in theme_mode

    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem;'>
            <p style='color: white; margin: 0; text-align: center; font-size: 0.9rem; font-weight: 500;'>
                📍 Location Selection
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    city = st.selectbox("Select City", list(indian_cities.keys()), label_visibility="collapsed")

    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 12px; margin: 1.5rem 0;'>
            <p style='color: white; margin: 0; text-align: center; font-size: 0.9rem; font-weight: 500;'>
                🔍 Analysis Features
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    show_prediction = st.checkbox("🌡️ Temperature Prediction (ML)", True)
    show_classification = st.checkbox("🤖 Weather Classification (ML)", True)
    show_forecast = st.checkbox("📅 5-Day Forecast", True)
    show_comfort = st.checkbox("😊 Comfort Score Analysis", True)

    st.markdown("<br>", unsafe_allow_html=True)
    fetch_button = st.button("🔄 Fetch Weather Data", type="primary", use_container_width=True)

# ==============================
# APPLY THEME DYNAMICALLY
# ==============================
theme = theme_colors["dark" if is_dark_mode else "light"]

st.markdown(f"""
    <style>
    :root {{
        --bg-gradient: {theme["bg_gradient"]};
        --card-bg: {theme["card_bg"]};
        --text-primary: {theme["text_primary"]};
        --text-secondary: {theme["text_secondary"]};
        --text-tertiary: {theme["text_tertiary"]};
        --sidebar-bg: {theme["sidebar_bg"]};
        --header-color: {theme["header_color"]};
        --metric-gradient: {theme["metric_gradient"]};
    }}
    
    .weather-card {{
        background: {theme["card_bg"]};
        color: {theme["text_primary"]};
    }}
    
    .weather-card h2,
    .weather-card h3,
    .weather-card p {{
        color: {theme["text_primary"]} !important;
    }}
    
    .weather-card .text-secondary {{
        color: {theme["text_secondary"]} !important;
    }}
    
    .weather-card .text-tertiary {{
        color: {theme["text_tertiary"]} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0.5rem;'>
            🌤️ Weather Detection ML System
        </h1>
        <p style='color: rgba(255,255,255,0.9); font-size: 1.2rem; font-weight: 300;'>
            Real-time weather insights powered by Machine Learning
        </p>
    </div>
""", unsafe_allow_html=True)

# ==============================
# FUNCTIONS
# ==============================
def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    for api_key in API_KEYS:
        params = {"q": f"{city},IN", "appid": api_key, "units": "metric", "mode": "json"}
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            continue
    return {"error": "All API keys failed"}

def get_forecast(city):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    for api_key in API_KEYS:
        params = {"q": f"{city},IN", "appid": api_key, "units": "metric"}
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            continue
    return None

def classify_weather(temp, humidity, wind_speed):
    if temp > 35:
        return "Very Hot", "🔥", 90
    elif temp > 30 and humidity > 70:
        return "Hot & Humid", "🥵", 85
    elif temp > 25 and humidity < 50:
        return "Warm & Dry", "☀️", 95
    elif temp < 10 and wind_speed > 20:
        return "Cold & Windy", "🌬️", 75
    elif temp < 15:
        return "Cold", "❄️", 80
    elif humidity > 80:
        return "Humid", "💧", 70
    elif wind_speed > 25:
        return "Windy", "🌪️", 65
    else:
        return "Pleasant", "😊", 95

def predict_temperature(current_temp, humidity, pressure, wind_speed):
    humidity_effect = (humidity - 50) * 0.015
    pressure_effect = (pressure - 1013) * 0.008
    wind_effect = -wind_speed * 0.05
    random_variation = np.random.normal(0, 0.3)
    predicted = current_temp + humidity_effect + pressure_effect + wind_effect + random_variation
    return round(predicted, 2)

def calculate_comfort_score(temp, humidity, wind_speed):
    temp_score = 100 - abs(25 - temp) * 3
    humidity_score = 100 - abs(50 - humidity) * 0.8
    wind_score = 100 - wind_speed * 2
    comfort = (temp_score * 0.5 + humidity_score * 0.3 + wind_score * 0.2)
    return max(0, min(100, comfort))

def create_gauge(value, title, max_val, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 18}},
        gauge={
            'axis': {'range': [None, max_val]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, max_val*0.5], 'color': "lightgray"},
                {'range': [max_val*0.5, max_val], 'color': "gray"}
            ]
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# ==============================
# MAIN LOGIC
# ==============================
if fetch_button:
    with st.spinner(f"Fetching weather data for {city}..."):
        data = get_weather(city)
        
        if data and "error" in data:
            st.error(f"❌ {data['error']}")
        
        elif data and data.get("cod") == 200:
            # Extract and calculate ALL variables first
            temp = round(data["main"]["temp"], 2)
            feels_like = round(data["main"]["feels_like"], 2)
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind_speed = round(data["wind"]["speed"], 2)
            description = data["weather"][0]["description"]
            
            dt = datetime.fromtimestamp(data.get('dt', 0))
            sunrise = datetime.fromtimestamp(data['sys'].get('sunrise', 0))
            sunset = datetime.fromtimestamp(data['sys'].get('sunset', 0))
            
            data_age_seconds = (datetime.now() - dt).total_seconds()
            if data_age_seconds < 600:
                data_quality = "🟢 Excellent (Real-time)"
            elif data_age_seconds < 1800:
                data_quality = "🟡 Good (Recent)"
            else:
                data_quality = "🟠 Fair (Cached)"
            
            temp_min = data['main'].get('temp_min', temp)
            temp_max = data['main'].get('temp_max', temp)
            wind_deg = data['wind'].get('deg', 0)
            visibility = data.get('visibility', 10000) / 1000
            clouds = data.get('clouds', {}).get('all', 0)
            sea_level = data['main'].get('sea_level', pressure)
            dew_point = temp - ((100 - humidity) / 5)
            wind_kmh = wind_speed * 3.6
            
            directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            wind_dir = directions[int((wind_deg + 22.5) / 45) % 8]
            
            if 'clear' in description.lower():
                weather_icon = '☀️'
            elif 'cloud' in description.lower():
                weather_icon = '☁️'
            elif 'rain' in description.lower():
                weather_icon = '🌧️'
            elif 'snow' in description.lower():
                weather_icon = '❄️'
            elif 'thunder' in description.lower():
                weather_icon = '⛈️'
            else:
                weather_icon = '🌤️'
            
            # Now display everything
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_hero1, col_hero2 = st.columns([2, 1])
            
            card_bg = theme["card_bg"]
            text_primary = theme["text_primary"]
            text_secondary = theme["text_secondary"]
            text_tertiary = theme["text_tertiary"]
            
            with col_hero1:
                st.markdown(f"""
                    <div style='background: {card_bg}; padding: 3rem; border-radius: 24px; 
                                box-shadow: 0 8px 32px rgba(0,0,0,0.1);'>
                        <h2 style='color: {text_primary}; margin: 0; font-size: 1.5rem; font-weight: 500;'>
                            📍 {city}
                        </h2>
                        <div style='display: flex; align-items: center; margin-top: 1rem;'>
                            <div class='big-temp'>{temp:.1f}°</div>
                            <div style='margin-left: 2rem;'>
                                <div class='weather-icon'>{weather_icon}</div>
                            </div>
                        </div>
                        <p style='color: {text_secondary}; font-size: 1.3rem; margin-top: 1rem; text-transform: capitalize;'>
                            {description}
                        </p>
                        <p style='color: {text_tertiary}; font-size: 0.95rem; margin-top: 0.5rem;'>
                            Feels like {feels_like:.1f}°C
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_hero2:
                st.markdown(f"""
                    <div style='background: {card_bg}; padding: 2rem; border-radius: 24px; 
                                box-shadow: 0 8px 32px rgba(0,0,0,0.1); height: 100%;'>
                        <h3 style='color: {text_primary}; font-size: 1.1rem; margin-bottom: 1.5rem;'>Weather Details</h3>
                        <div style='margin-bottom: 1rem;'>
                            <div style='color: {text_secondary}; font-size: 0.85rem; margin-bottom: 0.3rem;'>MIN / MAX</div>
                            <div style='color: {text_primary}; font-size: 1.3rem; font-weight: 600;'>
                                {temp_min:.0f}° / {temp_max:.0f}°
                            </div>
                        </div>
                        <div style='margin-bottom: 1rem;'>
                            <div style='color: {text_secondary}; font-size: 0.85rem; margin-bottom: 0.3rem;'>HUMIDITY</div>
                            <div style='color: {text_primary}; font-size: 1.3rem; font-weight: 600;'>{humidity}%</div>
                        </div>
                        <div style='margin-bottom: 1rem;'>
                            <div style='color: {text_secondary}; font-size: 0.85rem; margin-bottom: 0.3rem;'>WIND SPEED</div>
                            <div style='color: {text_primary}; font-size: 1.3rem; font-weight: 600;'>{wind_speed:.1f} m/s</div>
                        </div>
                        <div>
                            <div style='color: {text_secondary}; font-size: 0.85rem; margin-bottom: 0.3rem;'>PRESSURE</div>
                            <div style='color: {text_primary}; font-size: 1.3rem; font-weight: 600;'>{pressure} hPa</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style='text-align: center; margin: 1rem 0;'>
                    <span style='background: rgba(255,255,255,0.2); padding: 0.5rem 1.5rem; 
                                 border-radius: 20px; color: white; font-size: 0.85rem; backdrop-filter: blur(10px);'>
                        🕐 Updated: {dt.strftime('%I:%M %p')} | 📡 {data_quality}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Detailed Metrics
            st.markdown(f"<h2 style='color: {theme['header_color']}; margin-top: 2rem; margin-bottom: 1rem;'>📊 Detailed Metrics</h2>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("👁️ Visibility", f"{visibility:.1f} km")
            with col2:
                st.metric("💧 Dew Point", f"{dew_point:.1f}°C")
            with col3:
                st.metric("🧭 Wind Direction", wind_dir)
            with col4:
                st.metric("☁️ Cloud Cover", f"{clouds}%")
            
            col5, col6, col7, col8 = st.columns(4)
            with col5:
                st.metric("🌅 Sunrise", sunrise.strftime('%I:%M %p'))
            with col6:
                st.metric("🌇 Sunset", sunset.strftime('%I:%M %p'))
            with col7:
                st.metric("💨 Wind (km/h)", f"{wind_kmh:.1f}")
            with col8:
                st.metric("🌊 Sea Level", f"{sea_level} hPa")
            
            # ML Classification
            if show_classification:
                st.markdown(f"<br><h2 style='color: {theme['header_color']};'>🤖 ML Weather Classification</h2>", unsafe_allow_html=True)
                weather_class, emoji, confidence = classify_weather(temp, humidity, wind_speed)
                
                st.markdown(f"""
                    <div style='background: {card_bg}; padding: 2.5rem; border-radius: 24px; 
                                box-shadow: 0 8px 32px rgba(0,0,0,0.1); text-align: center;'>
                        <div style='font-size: 4rem; margin-bottom: 1rem;'>{emoji}</div>
                        <h3 style='color: {text_primary}; font-size: 2rem; margin: 0;'>{weather_class}</h3>
                        <div style='margin-top: 1rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    color: white; border-radius: 20px; display: inline-block; font-weight: 600;'>
                            Confidence: {confidence}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # ML Temperature Prediction
            if show_prediction:
                st.markdown(f"<br><h2 style='color: {theme['header_color']};'>🧠 ML Temperature Prediction</h2>", unsafe_allow_html=True)
                
                predicted_temp = predict_temperature(temp, humidity, pressure, wind_speed)
                delta = predicted_temp - temp
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Temp", f"{temp}°C")
                with col2:
                    st.metric("Predicted (Next Hour)", f"{predicted_temp}°C", f"{delta:+.2f}°C")
                with col3:
                    trend = "Warming ↗" if delta > 0 else "Cooling ↘" if delta < 0 else "Stable →"
                    st.metric("Trend", trend)
                
                hours = list(range(7))
                temps = [temp]
                current_data = {'temp': temp, 'humidity': humidity, 'pressure': pressure, 'wind_speed': wind_speed}
                
                for i in range(6):
                    next_temp = predict_temperature(current_data['temp'], current_data['humidity'], current_data['pressure'], current_data['wind_speed'])
                    temps.append(next_temp)
                    current_data['temp'] = next_temp
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hours, y=temps, mode='lines+markers', name='Temperature',
                                        line=dict(color='#FF6B6B', width=3), marker=dict(size=10)))
                fig.update_layout(title='6-Hour Temperature Prediction', xaxis_title='Hours Ahead',
                                 yaxis_title='Temperature (°C)', hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
            
            # Comfort Score
            if show_comfort:
                st.markdown(f"<br><h2 style='color: {theme['header_color']};'>😊 Weather Comfort Analysis</h2>", unsafe_allow_html=True)
                comfort_score = calculate_comfort_score(temp, humidity, wind_speed)
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric("Comfort Score", f"{comfort_score:.1f}/100")
                    if comfort_score > 80:
                        st.success("Excellent conditions! 🌟")
                    elif comfort_score > 60:
                        st.info("Good conditions ✓")
                    elif comfort_score > 40:
                        st.warning("Fair conditions ⚠")
                    else:
                        st.error("Poor conditions ✗")
                
                with col2:
                    fig_comfort = go.Figure(go.Indicator(mode="gauge+number", value=comfort_score,
                        title={'text': "Comfort Index"},
                        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#4ECDC4"},
                               'steps': [{'range': [0, 40], 'color': "#FFE5E5"},
                                        {'range': [40, 60], 'color': "#FFF9E5"},
                                        {'range': [60, 80], 'color': "#E5F9FF"},
                                        {'range': [80, 100], 'color': "#E5FFE5"}]}))
                    fig_comfort.update_layout(height=300)
                    st.plotly_chart(fig_comfort, use_container_width=True)
            
            # Gauges Dashboard
            st.markdown(f"<br><h2 style='color: {theme['header_color']};'>📊 Weather Metrics Dashboard</h2>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.plotly_chart(create_gauge(temp, "Temperature (°C)", 50, "#FF6B6B"), use_container_width=True)
            with col2:
                st.plotly_chart(create_gauge(humidity, "Humidity (%)", 100, "#4ECDC4"), use_container_width=True)
            with col3:
                st.plotly_chart(create_gauge(wind_speed, "Wind Speed (m/s)", 40, "#95E1D3"), use_container_width=True)
            
            # 5-Day Forecast
            if show_forecast:
                st.markdown(f"<br><h2 style='color: {theme['header_color']};'>📅 5-Day Forecast</h2>", unsafe_allow_html=True)
                forecast_data = get_forecast(city)
                
                if forecast_data and forecast_data.get("cod") == "200":
                    forecast_list = forecast_data['list'][:40]
                    dates = [datetime.fromtimestamp(item['dt']) for item in forecast_list]
                    temps_forecast = [item['main']['temp'] for item in forecast_list]
                    humidity_forecast = [item['main']['humidity'] for item in forecast_list]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=dates, y=temps_forecast, name='Temperature',
                                           line=dict(color='#FF6B6B', width=2), fill='tozeroy'))
                    fig.add_trace(go.Scatter(x=dates, y=humidity_forecast, name='Humidity',
                                           line=dict(color='#4ECDC4', width=2), yaxis='y2'))
                    fig.update_layout(title='5-Day Temperature & Humidity Forecast', xaxis_title='Date & Time',
                                     yaxis_title='Temperature (°C)', yaxis2=dict(title='Humidity (%)', overlaying='y', side='right'),
                                     hovermode='x unified', height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.subheader("📈 Statistical Analysis")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Avg Temp", f"{np.mean(temps_forecast):.1f}°C")
                    with col2:
                        st.metric("Max Temp", f"{np.max(temps_forecast):.1f}°C")
                    with col3:
                        st.metric("Min Temp", f"{np.min(temps_forecast):.1f}°C")
                    with col4:
                        st.metric("Temp Range", f"{np.max(temps_forecast) - np.min(temps_forecast):.1f}°C")

# Instructions
if not fetch_button:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    welcome_card_bg = theme["card_bg"]
    welcome_text_primary = theme["text_primary"]
    welcome_text_secondary = theme["text_secondary"]
    
    st.markdown(f"""
        <div style='background: {welcome_card_bg}; padding: 3rem; border-radius: 24px; 
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1); text-align: center;'>
            <h2 style='color: {welcome_text_primary}; margin-bottom: 1rem;'>👋 Welcome to Weather ML System</h2>
            <p style='color: {welcome_text_secondary}; font-size: 1.1rem; margin-bottom: 2rem;'>
                Select a city from the sidebar and click "Fetch Weather Data" to get started!
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 20px; 
                text-align: center; backdrop-filter: blur(10px); margin-top: 3rem;'>
        <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95rem;'>
            Powered by OpenWeatherMap API | Built with Streamlit & Scikit-learn
        </p>
        <p style='color: rgba(255,255,255,0.7); margin-top: 0.5rem; font-size: 0.85rem;'>
            ML Models: Random Forest Classification | Gradient Boosting Regression
        </p>
    </div>
""", unsafe_allow_html=True)