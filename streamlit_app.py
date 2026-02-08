import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from torus import MultiPhaseTorus

st.set_page_config(
    page_title="Toroidal Anomaly Detector",
    layout="wide"
)

st.title("Toroidal Anomaly Detector")
st.markdown("Phase-space based telemetry anomaly detection")

uploaded = st.file_uploader(
    "Upload CSV telemetry file",
    type=["csv"]
)

if uploaded:
    df = pd.read_csv(uploaded)

    st.subheader("Data preview")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    selected_cols = st.multiselect(
        "Select numeric telemetry channels",
        numeric_cols,
        default=numeric_cols[:3]
    )

    if st.button("Run analysis") and selected_cols:
        torus = MultiPhaseTorus()
        results = []

        for i, row in df[selected_cols].iterrows():
            x = row.values.astype(float)
            r = torus.step(x)
            if r:
                r["step"] = i
                results.append(r)

        if results:
            res_df = pd.DataFrame(results)

            st.subheader("State table")
            st.dataframe(res_df)

            st.subheader("Anomaly score dynamics")
            fig, ax = plt.subplots()
            ax.plot(res_df["step"], res_df["anomaly_score"])
            ax.axhline(6.0, linestyle="--", label="threshold")
            ax.set_xlabel("step")
            ax.set_ylabel("anomaly_score")
            ax.legend()
            st.pyplot(fig)

            st.subheader("Unstable states")
            st.dataframe(res_df[res_df["state"] == "unstable"])
