import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.markdown("""
<style>

/* Color the AG-Grid (st.dataframe) header */
[data-testid="stDataFrame"] .ag-header {
    background-color: #E6D7FF !important;   /* light purple */
    color: #4A148C !important;              /* deep purple text */
    font-weight: 800 !important;
    font-size: 15px !important;
}

/* Apply purple color to each header cell */
[data-testid="stDataFrame"] .ag-header-cell-label {
    color: #4A148C !important;
    justify-content: center !important;
}

/* Center header text */
[data-testid="stDataFrame"] .ag-header-cell {
    text-align: center !important;
}

/* Center all table content */
[data-testid="stDataFrame"] .ag-cell {
    justify-content: center !important;
    text-align: center !important;
    font-size: 14px !important;
}

/* Hover row highlight */
[data-testid="stDataFrame"] .ag-row-hover {
    background-color: #F3E8FF !important;
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="PNR-IDIR Analysis", layout="wide")

# ------------------- CSS OVERRIDE FOR STREAMLIT TABLES -------------------
st.markdown("""
<style>
/* Light Purple Header for ALL Streamlit tables */
thead tr th {
    background-color: #E6D7FF !important;
    color: #4A235A !important;
    font-weight: 700 !important;
    text-align: center !important;
    border-bottom: 2px solid #B795D7 !important;
}

/* Center table content */
tbody tr td {
    text-align: center !important;
}

/* Hover highlight */
tbody tr:hover {
    background-color: #F3E8FF !important;
}

/* Section Heading */
.section-title {
    font-size: 30px;
    font-weight: 700;
    color: #6A1B9A;
    padding-bottom: 8px;
}
.sub-heading {
    font-size: 22px;
    font-weight: 600;
    color: #8E44AD;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)


# ------------------- PAGE TITLE -------------------
st.markdown('<div class="section-title">📊 PNR–IDIR Classroom Interaction Analysis</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("📥 Upload your Speaker Excel File", type=["xlsx"])

if uploaded is not None:

    df = pd.read_excel(uploaded)
    df.index = df.index + 1

    st.markdown('<div class="sub-heading">📄 Preview of Uploaded File</div>', unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

    # ------------------- FORMULA DISPLAY -------------------
    st.markdown("""
    ### 📘 Computation Formulas
    - **PNR = Response / Instruction**  
    - **IDIR = (Response + Question) / (Lecture + Instruction)**  
    """)

    # ------------------- COMPUTE -------------------
    df["pnr"] = df["Response"] / df["Instruction"]
    df["idir"] = (df["Response"] + df["Question"]) / (df["Lecture"] + df["Instruction"])

    # ------------------- SHOW MAX/MIN BEFORE GRAPH -------------------
    max_pnr = df["pnr"].max()
    min_pnr = df["pnr"].min()
    max_idir = df["idir"].max()
    min_idir = df["idir"].min()

    st.markdown('<div class="sub-heading">📌 PNR–IDIR Range Summary</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔼 Max PNR", f"{max_pnr:.3f}")
    col2.metric("🔽 Min PNR", f"{min_pnr:.3f}")
    col3.metric("🔼 Max IDIR", f"{max_idir:.3f}")
    col4.metric("🔽 Min IDIR", f"{min_idir:.3f}")

    # ------------------- CALCULATED TABLE -------------------
    st.markdown('<div class="sub-heading">🧮 Computed PNR and IDIR Values</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    # ------------------- QUADRANT -------------------
    def assign_quadrant(row):
        if row["pnr"] >= 1 and row["idir"] >= 1:
            return "Q1"
        elif row["pnr"] < 1 and row["idir"] >= 1:
            return "Q2"
        elif row["pnr"] < 1 and row["idir"] < 1:
            return "Q3"
        else:
            return "Q4"

    df["Quadrant"] = df.apply(assign_quadrant, axis=1)

    # ------------------- INTERACTIVE GRAPH -------------------
    st.markdown('<div class="sub-heading">📈 Interactive PNR–IDIR Visualization</div>', unsafe_allow_html=True)

    fig = px.scatter(
        df,
        x="pnr",
        y="idir",
        color="Quadrant",
        text="Speakers",
        hover_data={
            "pnr": ':.3f',
            "idir": ':.3f',
            "Speakers": True,
            "Quadrant": True
        }
    )

    # FORCE AXIS RANGE & TICKS
    fig.update_xaxes(range=[0, 2], dtick=0.1, title="PNR (0–2 scale)")
    fig.update_yaxes(range=[0, 2], dtick=0.1, title="IDIR (0–2 scale)")

    # Clean layout
    fig.update_layout(
        height=550,
        template="plotly_white",
        title_x=0.5,
        margin=dict(l=30, r=30, t=40, b=20),
        font=dict(size=13)
    )

    # Threshold lines
    fig.add_vline(x=1, line_dash="dash", line_color="purple")
    fig.add_hline(y=1, line_dash="dash", line_color="purple")

    # Speaker label positioning
    fig.update_traces(textposition="top center")

    st.plotly_chart(fig, use_container_width=True)

    # ------------------- QUADRANT TABLE -------------------
    st.markdown('<div class="sub-heading">📊 Speakers per Quadrant</div>', unsafe_allow_html=True)

    quad_table = df.groupby("Quadrant")["Speakers"].apply(list).reset_index()
    st.dataframe(quad_table, use_container_width=True)

else:
    st.info("📥 Please upload an Excel file to begin.")

