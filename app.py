import streamlit as st
import pandas as pd
import joblib

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sophos Network Security Monitor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
}

.dashboard-title {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    font-size: 17px;
    color: #666;
    margin-bottom: 25px;
}

.status-normal {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    background-color: #e8f5e9;
    border: 2px solid #4caf50;
}

.status-anomaly {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    background-color: #ffebee;
    border: 2px solid #f44336;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODEL
# =========================================================

try:

    model = joblib.load("sophos_model.pkl")
    scaler = joblib.load("sophos_scaler.pkl")
    features = joblib.load("sophos_features.pkl")

except Exception as e:

    st.error("❌ Unable to load the machine learning model.")

    st.write("Error:", e)

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🛡️ System Control")

    st.write("### Upload Firewall Data")

    uploaded_file = st.file_uploader(
        "Select Sophos CSV file",
        type=["csv"]
    )

    st.divider()

    st.write("### About the System")

    st.info(
        """
        This system uses **Isolation Forest**
        to detect unusual network traffic
        from Sophos firewall data.

        The system uses **unsupervised machine
        learning**, therefore anomaly labels are
        not required.
        """
    )

    st.divider()

    st.write("**Model:** Isolation Forest")

    st.write("**Learning:** Unsupervised")

    st.write("**Data Source:** Sophos Firewall Logs")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-title">🛡️ Sophos Network Security Monitor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Machine Learning-Based Network Anomaly Detection System'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# WAIT FOR FILE
# =========================================================

if uploaded_file is None:

    st.info(
        "👈 Upload a Sophos firewall CSV file from the sidebar "
        "to start anomaly detection."
    )

    st.markdown("### How the system works")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 1️⃣ Upload")

        st.write(
            "Upload your Sophos firewall traffic CSV file."
        )

    with col2:

        st.markdown("### 2️⃣ Analyze")

        st.write(
            "The trained Isolation Forest model analyzes "
            "the network traffic."
        )

    with col3:

        st.markdown("### 3️⃣ Detect")

        st.write(
            "The system identifies normal and unusual "
            "network activities."
        )

    st.stop()


# =========================================================
# READ DATA
# =========================================================

try:

    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error("❌ Failed to read the CSV file.")

    st.write(e)

    st.stop()


# =========================================================
# DATA INFORMATION
# =========================================================

st.markdown(
    '<div class="section-title">📊 Network Traffic Overview</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Records",
        f"{len(df):,}"
    )


with col2:

    st.metric(
        "Total Columns",
        f"{len(df.columns):,}"
    )


with col3:

    st.metric(
        "Model Features",
        f"{len(features):,}"
    )


with col4:

    st.metric(
        "Detection Method",
        "Isolation Forest"
    )


# =========================================================
# CHECK FEATURES
# =========================================================

missing_features = [
    feature
    for feature in features
    if feature not in df.columns
]


if missing_features:

    st.error(
        "❌ The uploaded file does not contain all "
        "features required by the trained model."
    )

    st.write("Missing features:")

    st.write(missing_features)

    st.stop()


# =========================================================
# PREPARE DATA
# =========================================================

X = df[features].copy()

X = X.fillna(X.median())


# =========================================================
# SCALE DATA
# =========================================================

try:

    X_scaled = scaler.transform(X)

except Exception as e:

    st.error(
        "❌ Error while preprocessing the uploaded data."
    )

    st.write(e)

    st.stop()


# =========================================================
# MACHINE LEARNING PREDICTION
# =========================================================

predictions = model.predict(X_scaled)

anomaly_scores = model.decision_function(X_scaled)


# =========================================================
# ADD RESULTS
# =========================================================

df["Prediction"] = predictions

df["Status"] = df["Prediction"].map(
    {
        1: "Normal",
        -1: "Anomaly"
    }
)

df["Anomaly_Score"] = anomaly_scores


# =========================================================
# CALCULATE COUNTS
# =========================================================

total_records = len(df)

normal_count = (
    df["Status"] == "Normal"
).sum()

anomaly_count = (
    df["Status"] == "Anomaly"
).sum()


if total_records > 0:

    anomaly_percentage = (
        anomaly_count / total_records
    ) * 100

else:

    anomaly_percentage = 0


# =========================================================
# SECURITY STATUS
# =========================================================

st.markdown(
    '<div class="section-title">🚨 Security Status</div>',
    unsafe_allow_html=True
)


if anomaly_count > 0:

    st.markdown(
        f"""
        <div class="status-anomaly">
        🚨 ANOMALY DETECTED<br>
        <span style="font-size:16px;">
        {anomaly_count:,} unusual network records detected
        </span>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="status-normal">
        🟢 NO ANOMALY DETECTED<br>
        <span style="font-size:16px;">
        All analyzed network records appear normal
        </span>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MAIN METRICS
# =========================================================

st.markdown(
    '<div class="section-title">📈 Detection Summary</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Traffic",
        f"{total_records:,}"
    )


with col2:

    st.metric(
        "🟢 Normal",
        f"{normal_count:,}"
    )


with col3:

    st.metric(
        "🔴 Anomalies",
        f"{anomaly_count:,}"
    )


with col4:

    st.metric(
        "Anomaly Rate",
        f"{anomaly_percentage:.2f}%"
    )


# =========================================================
# CHART
# =========================================================

st.markdown(
    '<div class="section-title">📊 Normal vs Anomaly Traffic</div>',
    unsafe_allow_html=True
)


chart_data = pd.DataFrame(
    {
        "Traffic Status": [
            "Normal",
            "Anomaly"
        ],
        "Records": [
            normal_count,
            anomaly_count
        ]
    }
)

chart_data = chart_data.set_index(
    "Traffic Status"
)

st.bar_chart(chart_data)


# =========================================================
# ANOMALY RECORDS
# =========================================================

st.markdown(
    '<div class="section-title">🚨 Detected Anomalies</div>',
    unsafe_allow_html=True
)


anomalies = df[
    df["Status"] == "Anomaly"
]


if anomaly_count > 0:

    st.warning(
        f"⚠️ The model identified {anomaly_count:,} "
        "records as unusual."
    )

    st.dataframe(
        anomalies,
        use_container_width=True,
        height=400
    )

else:

    st.success(
        "🟢 No unusual network activity was detected."
    )


# =========================================================
# ALL RESULTS
# =========================================================

st.markdown(
    '<div class="section-title">📋 Complete Detection Results</div>',
    unsafe_allow_html=True
)


st.dataframe(
    df,
    use_container_width=True,
    height=400
)


# =========================================================
# DOWNLOAD
# =========================================================

st.markdown(
    '<div class="section-title">📥 Export Results</div>',
    unsafe_allow_html=True
)


results_csv = df.to_csv(
    index=False
)


st.download_button(
    label="⬇️ Download Anomaly Detection Results",
    data=results_csv,
    file_name="sophos_anomaly_results.csv",
    mime="text/csv"
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Sophos Network Security Monitor | "
    "Machine Learning: Isolation Forest | "
    "Unsupervised Anomaly Detection"
)
