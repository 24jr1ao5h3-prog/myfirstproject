import streamlit as st
import requests
import time
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Eswar Currency Converter",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS - FUTURISTIC ANIMATIONS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Orbitron', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(0, 255, 255, 0.12), transparent 25%),
        radial-gradient(circle at 90% 80%, rgba(150, 0, 255, 0.15), transparent 25%),
        linear-gradient(135deg, #020617, #07111f, #030712);
    color: white;
}

/* Animated background */
.stApp::before {
    content: "";
    position: fixed;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: rgba(0, 255, 255, 0.05);
    filter: blur(80px);
    top: 5%;
    left: 5%;
    animation: float1 8s ease-in-out infinite;
    z-index: -1;
}

.stApp::after {
    content: "";
    position: fixed;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: rgba(160, 0, 255, 0.05);
    filter: blur(90px);
    bottom: 5%;
    right: 5%;
    animation: float2 10s ease-in-out infinite;
    z-index: -1;
}

@keyframes float1 {
    0%,100% { transform: translate(0,0); }
    50% { transform: translate(100px,60px); }
}

@keyframes float2 {
    0%,100% { transform: translate(0,0); }
    50% { transform: translate(-100px,-70px); }
}

/* Main title */
.title {
    text-align: center;
    font-size: 45px;
    font-weight: 800;
    letter-spacing: 4px;
    margin-top: 15px;
    background: linear-gradient(90deg, #00ffff, #ffffff, #a855f7, #00ffff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleGlow 4s linear infinite;
}

@keyframes titleGlow {
    0% { background-position: 0% center; }
    100% { background-position: 300% center; }
}

.subtitle {
    text-align: center;
    color: #8ea7c7;
    font-size: 14px;
    letter-spacing: 2px;
    margin-bottom: 35px;
}

/* Converter card */
.converter-card {
    max-width: 950px;
    margin: auto;
    padding: 35px;
    border-radius: 28px;
    background: rgba(8, 20, 38, 0.78);
    border: 1px solid rgba(0, 255, 255, 0.35);
    box-shadow:
        0 0 25px rgba(0,255,255,0.12),
        inset 0 0 30px rgba(0,255,255,0.025);
    backdrop-filter: blur(20px);
    animation: cardAppear 1s ease-out;
}

@keyframes cardAppear {
    from {
        opacity: 0;
        transform: translateY(30px) scale(0.97);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* Input labels */
label {
    color: #bdefff !important;
    font-weight: 600 !important;
}

/* Text input / number input */
div[data-baseweb="input"] {
    border-radius: 14px !important;
    border: 1px solid rgba(0,255,255,0.3) !important;
    background: rgba(0,0,0,0.25) !important;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border: 1px solid rgba(0,255,255,0.3) !important;
    background: rgba(0,0,0,0.25) !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(0,255,255,0.5);
    background: linear-gradient(135deg, #063d52, #15215c);
    color: white;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 13px;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow:
        0 0 15px rgba(0,255,255,0.5),
        0 0 35px rgba(120,0,255,0.2);
    border-color: #00ffff;
}

/* Result */
.result-box {
    margin-top: 30px;
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    background: linear-gradient(
        135deg,
        rgba(0,255,255,0.08),
        rgba(130,0,255,0.12)
    );
    border: 1px solid rgba(0,255,255,0.4);
    box-shadow: 0 0 35px rgba(0,255,255,0.1);
    animation: resultPulse 2s ease-in-out infinite alternate;
}

@keyframes resultPulse {
    from {
        box-shadow: 0 0 15px rgba(0,255,255,0.08);
    }
    to {
        box-shadow: 0 0 35px rgba(0,255,255,0.22);
    }
}

.result-label {
    color: #91a8c4;
    font-size: 13px;
    letter-spacing: 2px;
}

.result-value {
    font-size: 42px;
    font-weight: 800;
    color: #00ffff;
    text-shadow: 0 0 20px rgba(0,255,255,0.5);
    margin-top: 10px;
}

/* Stats */
.stat-card {
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
    transition: 0.3s;
}

.stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(0,255,255,0.4);
}

.stat-title {
    color: #8196b0;
    font-size: 12px;
}

.stat-value {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
    margin-top: 8px;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 40px;
    color: #5f738e;
    font-size: 11px;
    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# CURRENCY DATA
# ============================================================

currencies = {
    "USD": "🇺🇸 US Dollar",
    "INR": "🇮🇳 Indian Rupee",
    "EUR": "🇪🇺 Euro",
    "GBP": "🇬🇧 British Pound",
    "JPY": "🇯🇵 Japanese Yen",
    "AUD": "🇦🇺 Australian Dollar",
    "CAD": "🇨🇦 Canadian Dollar",
    "CHF": "🇨🇭 Swiss Franc",
    "CNY": "🇨🇳 Chinese Yuan",
    "SGD": "🇸🇬 Singapore Dollar",
    "AED": "🇦🇪 UAE Dirham",
    "SAR": "🇸🇦 Saudi Riyal",
    "KRW": "🇰🇷 South Korean Won",
    "NZD": "🇳🇿 New Zealand Dollar",
    "ZAR": "🇿🇦 South African Rand"
}

# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="title">💱 Eswar CURRENCY CONVERTER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">REAL-TIME • FAST • SMART • FUTURISTIC</div>',
    unsafe_allow_html=True
)

# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

# ============================================================
# CONVERTER
# ============================================================

st.markdown('<div class="converter-card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2.2, 1, 2.2])

with col1:
    amount = st.number_input(
        "💰 Amount",
        min_value=0.01,
        value=100.00,
        step=1.00
    )

    from_currency = st.selectbox(
        "FROM",
        list(currencies.keys()),
        format_func=lambda x: currencies[x],
        index=0
    )

with col2:
    st.write("")
    st.write("")
    
    if st.button("⇄ SWAP"):
        st.session_state.swap = True

with col3:
    to_currency = st.selectbox(
        "TO",
        list(currencies.keys()),
        format_func=lambda x: currencies[x],
        index=1
    )

st.write("")

convert = st.button("⚡ CONVERT CURRENCY", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# CONVERSION
# ============================================================

if convert:

    if from_currency == to_currency:
        rate = 1
        converted = amount

    else:
        try:
            url = (
                f"https://api.frankfurter.app/latest"
                f"?amount={amount}"
                f"&from={from_currency}"
                f"&to={to_currency}"
            )

            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                converted = data["rates"][to_currency]
                rate = converted / amount

            else:
                st.error("⚠️ Currency API request failed.")
                st.stop()

        except requests.exceptions.RequestException:
            st.error("⚠️ Unable to connect to the currency service.")
            st.stop()

    st.session_state.result = converted

    # Add history
    st.session_state.history.insert(
        0,
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "result": converted,
            "rate": rate
        }
    )

    # Keep latest 5
    st.session_state.history = st.session_state.history[:5]

# ============================================================
# RESULT
# ============================================================

if st.session_state.result is not None:

    converted = st.session_state.result

    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-label">CONVERSION RESULT</div>
            <div class="result-value">
                {converted:,.2f} {to_currency}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Stats
    if st.session_state.history:

        latest = st.session_state.history[0]

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-title">EXCHANGE RATE</div>
                    <div class="stat-value">
                        1 {latest['from']} = {latest['rate']:.4f} {latest['to']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-title">CONVERTED</div>
                    <div class="stat-value">
                        {latest['result']:,.2f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-title">UPDATED</div>
                    <div class="stat-value">
                        {latest['time']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ============================================================
# HISTORY
# ============================================================

if st.session_state.history:

    st.markdown("### 📊 Recent Conversions")

    for item in st.session_state.history:

        st.markdown(
            f"""
            <div style="
                padding:14px;
                margin:8px 0;
                border-radius:14px;
                background:rgba(255,255,255,0.025);
                border:1px solid rgba(255,255,255,0.07);
            ">
                <b>{item['amount']:,.2f} {item['from']}</b>
                &nbsp; → &nbsp;
                <b>{item['result']:,.2f} {item['to']}</b>
                <span style="float:right;color:#7187a2;">
                    {item['time']}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ESWAR CURRENCY CONVERTER • LIVE EXCHANGE RATES • STREAMLIT
    </div>
    """,
    unsafe_allow_html=True
)