import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="Sophos Network Anomaly Detection",
    page_icon="🛡️",
    layout="wide"
)

# Title
st.title("🛡️ Sophos Network Anomaly Detection System")
st.write(
    "Upload a Sophos firewall CSV file to detect unusual network activity."
)

# Load trained model and preprocessing files
try:
    model = joblib.load("sophos_model.pkl")
    scaler = joblib.load("sophos_scaler.pkl")
    features = joblib.load("sophos_features.pkl")

    st.success("Machine Learning model loaded successfully.")

except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()


# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Sophos Firewall CSV",
    type=["csv"]
)


if uploaded_file is not None:

    # Read CSV
    try:
        df = pd.read_csv(uploaded_file)

        st.success("CSV uploaded successfully!")

    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()


    # Basic information
    st.subheader("📊 Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Records",
            len(df)
        )

    with col2:
        st.metric(
            "Total Columns",
            len(df.columns)
        )


    # Preview
    st.subheader("🔍 Data Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


    # Check required features
    missing_features = [
        col for col in features
        if col not in df.columns
    ]


    if missing_features:

        st.error("❌ Some required features are missing from the uploaded CSV.")

        st.write("Missing features:")

        st.write(missing_features)

    else:

        # Select features used during training
        X = df[features].copy()

        # Handle missing values
        X = X.fillna(X.median())


        # Scale data
        X_scaled = scaler.transform(X)


        # Make predictions
        predictions = model.predict(X_scaled)


        # Add results
        df["Prediction"] = predictions

        df["Status"] = df["Prediction"].map({
            1: "Normal",
            -1: "Anomaly"
        })


        # Calculate anomaly score
        df["Anomaly_Score"] = model.decision_function(
            X_scaled
        )


        # Count results
        normal_count = (
            df["Status"] == "Normal"
        ).sum()

        anomaly_count = (
            df["Status"] == "Anomaly"
        ).sum()


        total_records = len(df)


        if total_records > 0:
            anomaly_percentage = (
                anomaly_count / total_records
            ) * 100
        else:
            anomaly_percentage = 0


        # Detection results
        st.subheader("🚨 Detection Results")


        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.metric(
                "Total Records",
                total_records
            )


        with col2:
            st.metric(
                "Normal",
                normal_count
            )


        with col3:
            st.metric(
                "Anomalies",
                anomaly_count
            )


        with col4:
            st.metric(
                "Anomaly %",
                f"{anomaly_percentage:.2f}%"
            )


        # Anomaly table
        st.subheader("🚨 Detected Anomalies")


        anomalies = df[
            df["Status"] == "Anomaly"
        ]


        if len(anomalies) > 0:

            st.warning(
                f"{len(anomalies)} unusual network records detected."
            )

            st.dataframe(
                anomalies,
                use_container_width=True
            )

        else:

            st.success(
                "No anomalies detected in the uploaded data."
            )


        # All results
        st.subheader("📋 All Detection Results")

        st.dataframe(
            df,
            use_container_width=True
        )


        # Download results
        results_csv = df.to_csv(
            index=False
        )


        st.download_button(
            label="⬇️ Download Detection Results",
            data=results_csv,
            file_name="sophos_anomaly_results.csv",
            mime="text/csv"
        )
