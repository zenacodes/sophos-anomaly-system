
import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SOPHOS | Anomaly Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "DASHBOARD"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* ================= GENERAL ================= */

.stApp {
    background: #080d18;
    color: #f1f5f9;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* ================= LOGIN ================= */

.login-wrapper {
    max-width: 560px;
    margin: 90px auto 0 auto;
    text-align: center;
}

.sophos-logo {
    font-size: 68px;
    font-weight: 900;
    letter-spacing: 7px;
    color: #ffffff;
    margin-bottom: 0;
}

.system-name {
    font-size: 25px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #22c55e;
    margin-top: 4px;
}

.login-description {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.7;
    margin: 22px auto 35px auto;
    max-width: 500px;
}

.login-box {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 30px;
    text-align: left;
}

.secure-access {
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #e2e8f0;
    margin-bottom: 20px;
}

/* ================= TOP NAV ================= */

.topbar {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 13px 20px;
    margin-bottom: 28px;
}

.brand {
    font-size: 21px;
    font-weight: 900;
    letter-spacing: 3px;
    color: #ffffff;
}

.brand-sub {
    color: #22c55e;
    font-size: 10px;
    letter-spacing: 1.5px;
}

/* ================= HERO ================= */

.hero {
    padding: 10px 0 25px 0;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 5px;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 14px;
}

/* ================= STATUS ================= */

.status-box {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 22px;
    margin: 10px 0 25px 0;
}

.status-label {
    color: #64748b;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 700;
}

.status-value {
    font-size: 26px;
    font-weight: 800;
    margin-top: 6px;
}

.status-description {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 5px;
}

/* ================= METRICS ================= */

.metric-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 20px;
    min-height: 125px;
}

.metric-label {
    color: #64748b;
    font-size: 11px;
    letter-spacing: 1.5px;
    font-weight: 700;
    text-transform: uppercase;
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    margin-top: 9px;
    color: #f8fafc;
}

.metric-note {
    color: #64748b;
    font-size: 11px;
    margin-top: 4px;
}

/* ================= SECTIONS ================= */

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #f8fafc;
    margin: 30px 0 12px 0;
}

/* ================= FOOTER ================= */

.footer {
    text-align: center;
    color: #475569;
    font-size: 11px;
    padding-top: 35px;
    letter-spacing: 0.5px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOGIN FUNCTION
# ============================================================

def login_page():

    st.markdown("""
    <div class="login-wrapper">

     
       
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    st.markdown(
        '<div class="secure-access">🔐 SECURE ACCESS</div>',
        unsafe_allow_html=True
    )

    username = st.text_input(
        "USERNAME",
        placeholder="Enter username"
    )

    password = st.text_input(
        "PASSWORD",
        type="password",
        placeholder="Enter password"
    )

    if st.button(
        "SIGN IN  →",
        use_container_width=True
    ):

        # Temporary login credentials
        # Change these later using Streamlit Secrets.

        if username == "admin" and password == "sophos123":

            st.session_state.authenticated = True

            st.rerun()

        else:

            st.error(
                "Access denied. Invalid username or password."
            )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="footer">AUTHORIZED SECURITY PERSONNEL ONLY</div>',
        unsafe_allow_html=True
    )


# ============================================================
# SHOW LOGIN
# ============================================================

if not st.session_state.authenticated:

    login_page()

    st.stop()


# ============================================================
# LOAD MODEL
# ============================================================

try:

    model = joblib.load("sophos_model.pkl")
    scaler = joblib.load("sophos_scaler.pkl")
    features = joblib.load("sophos_features.pkl")

except Exception as e:

    st.error("Machine learning model could not be loaded.")

    st.code(str(e))

    st.stop()


# ============================================================
# TOP NAVIGATION
# ============================================================

st.markdown("""
<div class="topbar">

<span class="brand">🛡️ SOPHOS</span>

&nbsp;&nbsp;

<span class="brand-sub">
ANOMALY DETECTION SYSTEM
</span>

</div>
""", unsafe_allow_html=True)


nav1, nav2, nav3, nav4, nav5 = st.columns(
    [1, 1, 1, 1, 1]
)


with nav1:

    if st.button("DASHBOARD", use_container_width=True):
        st.session_state.page = "DASHBOARD"


with nav2:

    if st.button("TRAFFIC", use_container_width=True):
        st.session_state.page = "TRAFFIC"


with nav3:

    if st.button("ANOMALIES", use_container_width=True):
        st.session_state.page = "ANOMALIES"


with nav4:

    if st.button("ANALYTICS", use_container_width=True):
        st.session_state.page = "ANALYTICS"


with nav5:

    if st.button("REPORTS", use_container_width=True):
        st.session_state.page = "REPORTS"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## SOPHOS")

    st.caption("ANOMALY DETECTION SYSTEM")

    st.divider()

    uploaded_file = st.file_uploader(
        "UPLOAD FIREWALL DATA",
        type=["csv"]
    )

    st.divider()

    st.write("SYSTEM")

    st.write("● ML ENGINE ONLINE")

    st.write("● DETECTION READY")

    st.divider()

    if st.button("LOG OUT", use_container_width=True):

        st.session_state.authenticated = False

        st.rerun()


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
Network Security Intelligence
</div>

<div class="hero-subtitle">
Behavioral analysis and machine-learning-based anomaly detection
for Sophos firewall traffic.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# WAIT FOR DATA
# ============================================================

if uploaded_file is None:

    st.markdown("""
    <div class="status-box">

    <div class="status-label">
    SYSTEM STATUS
    </div>

    <div class="status-value" style="color:#22c55e;">
    ● READY FOR ANALYSIS
    </div>

    <div class="status-description">
    Upload a Sophos firewall CSV dataset from the sidebar
    to begin network behavior analysis.
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Security Monitoring</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="metric-card">

        <div class="metric-label">
        DATA INGESTION
        </div>

        <div class="metric-number">
        📂
        </div>

        <div class="metric-note">
        Import Sophos firewall traffic
        </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="metric-card">

        <div class="metric-label">
        BEHAVIORAL ANALYSIS
        </div>

        <div class="metric-number">
        🧠
        </div>

        <div class="metric-note">
        Isolation Forest detection engine
        </div>

        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="metric-card">

        <div class="metric-label">
        SECURITY DETECTION
        </div>

        <div class="metric-number">
        🚨
        </div>

        <div class="metric-note">
        Identify unusual network behavior
        </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
    SOPHOS ANOMALY DETECTION SYSTEM
    • UNSUPERVISED MACHINE LEARNING
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ============================================================
# READ CSV
# ============================================================

try:

    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error("Unable to read the uploaded CSV file.")

    st.code(str(e))

    st.stop()


# ============================================================
# CHECK FEATURES
# ============================================================

missing_features = [
    feature
    for feature in features
    if feature not in df.columns
]

if missing_features:

    st.error(
        "The uploaded dataset is incompatible with the trained model."
    )

    st.write("Missing features:")

    st.write(missing_features)

    st.stop()


# ============================================================
# PREPROCESS DATA
# ============================================================

X = df[features].copy()

X = X.fillna(X.median())


try:

    X_scaled = scaler.transform(X)

except Exception as e:

    st.error("Preprocessing failed.")

    st.code(str(e))

    st.stop()


# ============================================================
# ANOMALY DETECTION
# ============================================================

predictions = model.predict(X_scaled)

scores = model.decision_function(X_scaled)


df["Status"] = pd.Series(predictions).map({
    1: "NORMAL",
    -1: "ANOMALY"
}).values


df["Anomaly_Score"] = scores


# ============================================================
# STATISTICS
# ============================================================

total = len(df)

normal = (df["Status"] == "NORMAL").sum()

anomalies = (df["Status"] == "ANOMALY").sum()

if total > 0:

    anomaly_rate = anomalies / total * 100

else:

    anomaly_rate = 0


# ============================================================
# THREAT LEVEL
# ============================================================

if anomaly_rate == 0:

    level = "LOW"
    symbol = "●"
    message = "No anomalous traffic detected."

elif anomaly_rate < 5:

    level = "GUARDED"
    symbol = "●"
    message = "Limited unusual activity detected."

elif anomaly_rate < 10:

    level = "ELEVATED"
    symbol = "●"
    message = "Increased unusual network activity detected."

else:

    level = "HIGH"
    symbol = "●"
    message = "Significant anomalous activity requires investigation."


if level == "LOW":
    level_color = "#22c55e"

elif level == "GUARDED":
    level_color = "#eab308"

elif level == "ELEVATED":
    level_color = "#f97316"

else:
    level_color = "#ef4444"


# ============================================================
# SECURITY STATUS
# ============================================================

st.markdown(f"""
<div class="status-box">

<div class="status-label">
CURRENT SECURITY POSTURE
</div>

<div class="status-value" style="color:{level_color};">
{symbol} {level}
</div>

<div class="status-description">
{message}
&nbsp;&nbsp;|&nbsp;&nbsp;
{anomalies:,} anomalous records identified from {total:,} analyzed.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# KPI DASHBOARD
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-label">
    TRAFFIC MONITORED
    </div>

    <div class="metric-number">
    {total:,}
    </div>

    <div class="metric-note">
    Records analyzed
    </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-label">
    NORMAL TRAFFIC
    </div>

    <div class="metric-number" style="color:#22c55e;">
    {normal:,}
    </div>

    <div class="metric-note">
    Expected behavior
    </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-label">
    ANOMALIES
    </div>

    <div class="metric-number" style="color:#ef4444;">
    {anomalies:,}
    </div>

    <div class="metric-note">
    Unusual behavior
    </div>

    </div>
    """, unsafe_allow_html=True)


with col4:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-label">
    ANOMALY RATE
    </div>

    <div class="metric-number">
    {anomaly_rate:.2f}%
    </div>

    <div class="metric-note">
    Current detection rate
    </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "DASHBOARD":

    st.markdown(
        '<div class="section-title">Network Behavior Overview</div>',
        unsafe_allow_html=True
    )

    chart_data = pd.DataFrame({
        "Status": ["NORMAL", "ANOMALY"],
        "Records": [normal, anomalies]
    })

    st.bar_chart(
        chart_data.set_index("Status")
    )

    st.markdown(
        '<div class="section-title">Recent Security Events</div>',
        unsafe_allow_html=True
    )

    recent = df[df["Status"] == "ANOMALY"].head(10)

    if len(recent) > 0:

        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No security events detected."
        )


# ============================================================
# TRAFFIC PAGE
# ============================================================

elif st.session_state.page == "TRAFFIC":

    st.markdown(
        '<div class="section-title">Traffic Intelligence</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Overview of the network traffic records processed by the system."
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=550,
        hide_index=True
    )


# ============================================================
# ANOMALIES PAGE
# ============================================================

elif st.session_state.page == "ANOMALIES":

    st.markdown(
        '<div class="section-title">Detected Anomalies</div>',
        unsafe_allow_html=True
    )

    anomaly_data = df[
        df["Status"] == "ANOMALY"
    ].copy()

    if len(anomaly_data) > 0:

        st.error(
            f"{len(anomaly_data):,} anomalous records require attention."
        )

        st.dataframe(
            anomaly_data,
            use_container_width=True,
            height=550,
            hide_index=True
        )

    else:

        st.success(
            "No anomalous network behavior detected."
        )


# ============================================================
# ANALYTICS PAGE
# ============================================================

elif st.session_state.page == "ANALYTICS":

    st.markdown(
        '<div class="section-title">Behavioral Analytics</div>',
        unsafe_allow_html=True
    )

    st.write("Anomaly score distribution")

    st.line_chart(
        df["Anomaly_Score"]
    )

    st.write("Normal vs anomalous traffic")

    analytics = pd.DataFrame({
        "NORMAL": [normal],
        "ANOMALY": [anomalies]
    })

    st.bar_chart(
        analytics
    )

    st.markdown(
        '<div class="section-title">Detection Statistics</div>',
        unsafe_allow_html=True
    )

    stats = pd.DataFrame({
        "Metric": [
            "Total Records",
            "Normal Records",
            "Anomalous Records",
            "Anomaly Rate"
        ],
        "Value": [
            total,
            normal,
            anomalies,
            f"{anomaly_rate:.2f}%"
        ]
    })

    st.table(stats)


# ============================================================
# REPORTS PAGE
# ============================================================

elif st.session_state.page == "REPORTS":

    st.markdown(
        '<div class="section-title">Security Reports</div>',
        unsafe_allow_html=True
    )

    report = df.copy()

    report_csv = report.to_csv(
        index=False
    )

    st.download_button(
        label="⬇️ DOWNLOAD SECURITY REPORT",
        data=report_csv,
        file_name="sophos_security_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown(
        '<div class="section-title">Report Summary</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"""
        **Analysis completed**

        - Total traffic records: **{total:,}**
        - Normal records: **{normal:,}**
        - Anomalous records: **{anomalies:,}**
        - Anomaly rate: **{anomaly_rate:.2f}%**
        - Threat level: **{level}**
        - Detection algorithm: **Isolation Forest**
        - Learning approach: **Unsupervised Machine Learning**
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

SOPHOS ANOMALY DETECTION SYSTEM
&nbsp; • &nbsp;
NETWORK SECURITY INTELLIGENCE
&nbsp; • &nbsp;
ISOLATION FOREST

</div>
""", unsafe_allow_html=True)

