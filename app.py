import streamlit as st
import pandas as pd
import joblib

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Sophos Security Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

body {
    background-color: #0b1120;
}

.stApp {
    background-color: #0b1120;
    color: #e5e7eb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Header */

.header {
    padding: 10px 0 25px 0;
}

.header h1 {
    font-size: 34px;
    margin-bottom: 3px;
    color: #f8fafc;
}

.header p {
    color: #94a3b8;
    font-size: 15px;
}

/* Cards */

.card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 22px;
    min-height: 125px;
}

.card-title {
    color: #94a3b8;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.card-value {
    color: #f8fafc;
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}

.card-description {
    color: #64748b;
    font-size: 12px;
    margin-top: 4px;
}

/* Threat panel */

.threat-panel {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 25px;
    margin: 10px 0 25px 0;
}

.threat-title {
    color: #94a3b8;
    font-size: 12px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.threat-status {
    font-size: 28px;
    font-weight: 700;
    margin-top: 8px;
}

.threat-message {
    color: #94a3b8;
    margin-top: 7px;
    font-size: 14px;
}

/* Section titles */

.section {
    color: #f8fafc;
    font-size: 20px;
    font-weight: 600;
    margin: 30px 0 12px 0;
}

/* Info */

.info-panel {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 20px;
}

/* Footer */

.footer {
    text-align: center;
    color: #64748b;
    padding-top: 30px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# LOAD MODEL
# ==========================================================

try:

    model = joblib.load("sophos_model.pkl")
    scaler = joblib.load("sophos_scaler.pkl")
    features = joblib.load("sophos_features.pkl")

except Exception as e:

    st.error("Machine learning model could not be loaded.")
    st.code(str(e))
    st.stop()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("## 🛡️ Security Center")

    st.caption("Sophos Network Intelligence")

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload firewall traffic",
        type=["csv"]
    )

    st.divider()

    st.markdown("### Detection Engine")

    st.write("**Algorithm**")
    st.write("Isolation Forest")

    st.write("**Learning Type**")
    st.write("Unsupervised Learning")

    st.write("**Purpose**")
    st.write("Network anomaly detection")

    st.divider()

    st.caption("Security Analytics Platform")


# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class="header">

<h1>🛡️ Sophos Security Intelligence</h1>

<p>
Network traffic monitoring, behavioral analysis and
machine-learning-based anomaly detection
</p>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# NO FILE
# ==========================================================

if uploaded_file is None:

    st.markdown("""
    <div class="info-panel">

    <h3>Security Monitoring Console</h3>

    <p style="color:#94a3b8;">
    Upload a Sophos firewall traffic dataset to initiate
    behavioral analysis and identify network activity that
    deviates from the learned baseline.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section">Detection Workflow</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="card">

        <div class="card-title">01 — Ingestion</div>

        <div style="font-size:22px;margin-top:10px;">
        📂 Traffic Data
        </div>

        <div class="card-description">
        Import Sophos firewall traffic records.
        </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="card">

        <div class="card-title">02 — Analysis</div>

        <div style="font-size:22px;margin-top:10px;">
        🧠 Behavioral Model
        </div>

        <div class="card-description">
        Analyze network behavior using machine learning.
        </div>

        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="card">

        <div class="card-title">03 — Detection</div>

        <div style="font-size:22px;margin-top:10px;">
        🚨 Security Events
        </div>

        <div class="card-description">
        Identify traffic patterns that appear unusual.
        </div>

        </div>
        """, unsafe_allow_html=True)

    st.stop()


# ==========================================================
# READ DATA
# ==========================================================

try:

    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error("Unable to read the uploaded CSV.")
    st.code(str(e))
    st.stop()


# ==========================================================
# CHECK FEATURES
# ==========================================================

missing_features = [
    feature
    for feature in features
    if feature not in df.columns
]

if missing_features:

    st.error("The uploaded dataset is incompatible with the trained model.")

    st.write("Missing model features:")

    for feature in missing_features:
        st.write(f"• {feature}")

    st.stop()


# ==========================================================
# PREPROCESSING
# ==========================================================

X = df[features].copy()

X = X.fillna(X.median())

try:

    X_scaled = scaler.transform(X)

except Exception as e:

    st.error("Data preprocessing failed.")
    st.code(str(e))
    st.stop()


# ==========================================================
# PREDICTION
# ==========================================================

predictions = model.predict(X_scaled)

scores = model.decision_function(X_scaled)

df["Status"] = predictions.map({
    1: "NORMAL",
    -1: "ANOMALY"
})

df["Anomaly_Score"] = scores


# ==========================================================
# STATISTICS
# ==========================================================

total = len(df)

normal = (df["Status"] == "NORMAL").sum()

anomaly = (df["Status"] == "ANOMALY").sum()

if total > 0:
    anomaly_rate = anomaly / total * 100
else:
    anomaly_rate = 0


# ==========================================================
# THREAT LEVEL
# ==========================================================

if anomaly_rate == 0:

    threat_level = "LOW"
    threat_color = "#22c55e"
    threat_message = "No anomalous traffic detected in the analyzed dataset."

elif anomaly_rate < 5:

    threat_level = "GUARDED"
    threat_color = "#eab308"
    threat_message = "Limited unusual network activity detected."

elif anomaly_rate < 10:

    threat_level = "ELEVATED"
    threat_color = "#f97316"
    threat_message = "An increased level of unusual network activity was detected."

else:

    threat_level = "HIGH"
    threat_color = "#ef4444"
    threat_message = "Significant anomalous network activity requires investigation."


# ==========================================================
# THREAT STATUS
# ==========================================================

st.markdown(f"""
<div class="threat-panel">

<div class="threat-title">
CURRENT SECURITY POSTURE
</div>

<div class="threat-status" style="color:{threat_color};">
● {threat_level}
</div>

<div class="threat-message">
{threat_message}
</div>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# KPI CARDS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(f"""
    <div class="card">

    <div class="card-title">
    Traffic Monitored
    </div>

    <div class="card-value">
    {total:,}
    </div>

    <div class="card-description">
    Network records analyzed
    </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown(f"""
    <div class="card">

    <div class="card-title">
    Normal Traffic
    </div>

    <div class="card-value" style="color:#22c55e;">
    {normal:,}
    </div>

    <div class="card-description">
    Expected behavioral patterns
    </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown(f"""
    <div class="card">

    <div class="card-title">
    Anomalies
    </div>

    <div class="card-value" style="color:#ef4444;">
    {anomaly:,}
    </div>

    <div class="card-description">
    Unusual behavioral patterns
    </div>

    </div>
    """, unsafe_allow_html=True)


with col4:

    st.markdown(f"""
    <div class="card">

    <div class="card-title">
    Anomaly Rate
    </div>

    <div class="card-value">
    {anomaly_rate:.2f}%
    </div>

    <div class="card-description">
    Percentage of traffic classified as unusual
    </div>

    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# TRAFFIC ANALYSIS
# ==========================================================

st.markdown(
    '<div class="section">Traffic Behavior Analysis</div>',
    unsafe_allow_html=True
)

chart_data = pd.DataFrame({
    "Status": ["NORMAL", "ANOMALY"],
    "Records": [normal, anomaly]
})

st.bar_chart(
    chart_data.set_index("Status")
)


# ==========================================================
# ANOMALY SCORE
# ==========================================================

st.markdown(
    '<div class="section">Anomaly Score Distribution</div>',
    unsafe_allow_html=True
)

score_data = pd.DataFrame({
    "Anomaly Score": df["Anomaly_Score"]
})

st.line_chart(score_data)


# ==========================================================
# SECURITY EVENTS
# ==========================================================

st.markdown(
    '<div class="section">Detected Security Events</div>',
    unsafe_allow_html=True
)

anomalies = df[df["Status"] == "ANOMALY"].copy()


if len(anomalies) > 0:

    st.warning(
        f"{len(anomalies):,} anomalous traffic records identified."
    )

    st.dataframe(
        anomalies,
        use_container_width=True,
        height=420
    )

else:

    st.success(
        "No anomalous traffic records were identified."
    )


# ==========================================================
# COMPLETE RESULTS
# ==========================================================

with st.expander("View Complete Traffic Analysis"):

    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )


# ==========================================================
# DOWNLOAD
# ==========================================================

st.markdown(
    '<div class="section">Export Security Report</div>',
    unsafe_allow_html=True
)

csv = df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Detection Report",
    data=csv,
    file_name="sophos_security_detection_report.csv",
    mime="text/csv"
)


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""
<div class="footer">

Sophos Security Intelligence Platform
&nbsp; • &nbsp;
Isolation Forest
&nbsp; • &nbsp;
Unsupervised Network Anomaly Detection

</div>
""", unsafe_allow_html=True)
