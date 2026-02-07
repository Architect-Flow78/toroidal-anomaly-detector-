# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from torus import MultiPhaseTorus

st.set_page_config(page_title="Toroidal Anomaly Detector", layout="wide")

st.title("🌀 Toroidal Anomaly Detector")
st.markdown("**Новая математика потока: СУЩЕСТВУЮ → ТВОРЕЦ / ЖЕРТВА**")

uploaded = st.file_uploader("Загрузите CSV с телеметрией", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.subheader("Предпросмотр данных")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    selected_cols = st.multiselect(
        "Выберите числовые каналы телеметрии",
        numeric_cols,
        default=numeric_cols[:3]
    )

    if st.button("▶ RUN (СУЩЕСТВУЮ)") and selected_cols:
        torus = MultiPhaseTorus()
        results = []

        for i, row in df[selected_cols].iterrows():
            x = row.values.astype(float)
            r = torus.step(x)
            if r:
                r["time"] = i
                results.append(r)

        res_df = pd.DataFrame(results)

        st.subheader("📋 Таблица состояний")
        st.dataframe(res_df)

        st.subheader("📈 Динамика аномальности")
        fig, ax = plt.subplots()
        ax.plot(res_df["time"], res_df["anomaly_score"])
        ax.axhline(6.0, linestyle="--")
        ax.set_xlabel("time")
        ax.set_ylabel("anomaly_score")
        st.pyplot(fig)

        st.subheader("🔴 Зоны ЖЕРТВЫ")
        st.dataframe(res_df[res_df["mode"] == "ЖЕРТВА"])

