import streamlit as st
import pandas as pd
from inference import classify_text, predict_label

st.set_page_config(page_title="Classroom Interaction Analysis", layout="wide")

# ------------------- HEADER + CUSTOM CSS -------------------
st.markdown("""
<style>
.big-title {
    font-size: 50px;
    font-weight: 700;
    color: #2A4D69;
    text-align: center;
}
.sub-title {
    font-size: 20px;
    font-weight: 400;
    color: #4F6D7A;
    text-align: center;
    margin-top: -15px;
}
.section-title {
    font-size: 25px;
    font-weight: 600;
    color: #1F4E79;
    padding-top: 15px;
}
.box {
    padding: 20px;
    background-color: #F2F4F8;
    border-radius: 12px;
    margin-bottom: 20px;
}

/* -------- Purple heading for Preview of Uploaded File -------- */
.preview-title {
    font-size: 22px;
    font-weight: 600;
    color: #6A1B9A;      /* Purple */
    margin-top: 20px;
}

/* -------- Table header light-purple style -------- */
thead tr th {
    background-color: #E8DAEF !important;   /* Light purple */
    color: #4A235A !important;              /* Dark purple text */
    font-weight: 700 !important;
}

/* Rounded table */
table {
    border-radius: 12px !important;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🎓 Classroom Interaction Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Classroom Interaction Classification System</div><br>', unsafe_allow_html=True)

# ====================================================
# 🔷 SECTION 1 — Single Text Prediction
# ====================================================
st.markdown('<div class="section-title">📝 Single Sentence Classification</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)

    text = st.text_area("Enter a classroom utterance:", height=150)

    if st.button("Predict Label"):
        if text.strip() == "":
            st.warning("⚠️ Please enter some text.")
        else:
            label, confidence = classify_text(text)
            st.success(f"**Predicted Class:** {label}")
            st.info(f"**Confidence Score:** `{confidence:.4f}`")

    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# 🔷 SECTION 2 — Manual 5 Inputs
# ====================================================
st.markdown('<div class="section-title">🧪 Test Manual Inputs (5 Examples)</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)

    for i in range(5):
        st.markdown(f"#### Example {i+1}")
        col1, col2 = st.columns(2)

        role = col1.selectbox(f"Role {i+1}", ["Teacher", "Student"], key=f"role_{i}")
        utt = col2.text_input(f"Utterance {i+1}", key=f"utt_{i}")

        if utt:
            pred = predict_label(role, utt)
            st.write(f"🔮 Predicted Label: **{pred}**")

    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# 🔷 SECTION 3 — Excel Upload + Prediction (Updated)
# ====================================================
st.markdown('<div class="section-title">📂 Excel File Classification</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)

    excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if excel_file is not None:
        # read excel (ensure openpyxl installed in your environment)
        df = pd.read_excel(excel_file)

        # ---------- Styled Preview Title ----------
        st.markdown('<div class="preview-title">📄 Preview of Uploaded File</div>',
                    unsafe_allow_html=True)

        # Prepare a display DataFrame without the index column
        df_display = df.head().reset_index(drop=True)

        # ====================== CUSTOM STYLED TABLE ======================
        def style_table(df_in):
            styles = [
                # Header Style (Purple)
                {"selector": "thead th",
                 "props": [
                     ("background-color", "#E8DAEF"),
                     ("color", "#4A235A"),
                     ("font-weight", "700"),
                     ("font-size", "14px"),
                     ("padding", "6px")
                 ]},

                # Cell Style
                {"selector": "tbody td",
                 "props": [
                     ("background-color", "#FFFFFF"),
                     ("color", "#1B2631"),
                     ("padding", "6px"),
                     ("border-bottom", "1px solid #E5E7EB"),
                     ("font-size", "14px")
                 ]},

                # Hover Row Highlight
                {"selector": "tbody tr:hover td",
                 "props": [
                     ("background-color", "#F4ECF7"),
                     ("cursor", "pointer")
                 ]},

                # Cell Hover Highlight
                {"selector": "tbody td:hover",
                 "props": [
                     ("background-color", "#F0D9F6"),
                     ("cursor", "pointer")
                 ]},

                # Rounded Table Corners
                {"selector": "table",
                 "props": [
                     ("border-collapse", "separate"),
                     ("border-spacing", "0"),
                     ("border-radius", "10px"),
                     ("overflow", "hidden"),
                     ("box-shadow", "0px 3px 12px rgba(0,0,0,0.08)")
                 ]}
            ]

            # Build styler WITHOUT using hide_index() to remain compatible
            styler = (df_in.style
                      .set_table_styles(styles)
                      .set_properties(**{"text-align": "left"})
                      )
            return styler

        # Render the styled table (df_display has reset index so no index column shown)
        st.markdown(style_table(df_display).to_html(), unsafe_allow_html=True)

        # ====================== VALIDATION & PREDICTION ======================
        if "Role" not in df.columns or "Utterance" not in df.columns:
            st.error("❌ Excel must contain **'Role'** and **'Utterance'** columns!")
        else:
            if st.button("Run Excel Predictions"):
                st.info("🔍 Classifying all rows... Please wait.")

                try:
                    df["Predicted_Label"] = df.apply(
                        lambda row: predict_label(str(row["Role"]), str(row["Utterance"])),
                        axis=1
                    )
                except Exception as e:
                    st.error(f"⚠️ Error during prediction: {e}")
                else:
                    # Save output file
                    output_path = "classified_output.xlsx"
                    df.to_excel(output_path, index=False)

                    st.success("✅ Classification Completed!")

                    # Download button
                    st.download_button(
                        label="📥 Download Classified Excel",
                        data=open(output_path, "rb").read(),
                        file_name="classified_output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

    st.markdown('</div>', unsafe_allow_html=True)
