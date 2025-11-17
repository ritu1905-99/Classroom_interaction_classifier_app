import streamlit as st

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Classroom Behaviour Analytics System",
    page_icon="🎓",
    layout="wide"
)
# st.sidebar.markdown("<div class='sidebar-title'>📚 Navigation</div>", unsafe_allow_html=True)

# ------------------------------------------------
# CUSTOM CSS FOR BETTER UI
# ------------------------------------------------
st.markdown("""
    <style>

        /* Remove default padding */
        .main {
            padding: 0rem 2rem;
        }

        /* Card styling */
        .info-card {
            background: #f3eaff;
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
            border-left: 6px solid #8b4cea;
        }

        /* Title styling */
        .title {
            font-size: 46px;
            font-weight: 700;
            text-align: center;
            margin-top: 10px;
            color: #333;
        }

        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #7b3fe0;
            margin-bottom: 35px;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #f5f0ff;
            padding-top: 20px;
        }
        
        .sidebar-title {
            font-size: 22px;
            font-weight: bold;
            color: #4b2ca0;
            padding-bottom: 15px;
            text-align: center;
        }
        
        /* Sidebar menu */
        .sidebar-link {
            padding: 10px 15px;
            margin: 6px 0;
            border-radius: 10px;
            color: #4b2ca0;
            font-size: 18px;
            font-weight: 500;
            text-decoration: none;
            display: block;
        }

        .sidebar-link:hover {
            background-color: #e2d4ff;
            color: #3b1b85;
        }

    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------

# st.sidebar.markdown("<a class='sidebar-link' href='/Home' target='_self'>🏠 Home</a>", unsafe_allow_html=True)
# st.sidebar.markdown("<a class='sidebar-link' href='/app' target='_self'>📊 Model Prediction</a>", unsafe_allow_html=True)
# st.sidebar.markdown("<a class='sidebar-link' href='/PNR_IDIR_Analysis' target='_self'>📈 PNR & IDIR Analysis</a>", unsafe_allow_html=True)

# ------------------------------------------------
# MAIN CONTENT
# ------------------------------------------------
st.markdown("<div class='title'>🎓 Classroom Behaviour Analytics System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered System for Classroom Transcript Understanding</div>", unsafe_allow_html=True)

# ------------------------------------------------
# PROJECT OVERVIEW CARD
# ------------------------------------------------
st.markdown("<div class='info-card'>", unsafe_allow_html=True)

st.markdown("""
### 📘 **Project Overview**

This system uses **state-of-the-art NLP** to analyze classroom transcripts and understand teaching–learning behaviour.

---

#### 🔍 **Core Features**
- 📌 **Classify utterances** — Lecture, Question, Instruction, Response  
- 🤝 **Identify student–teacher interaction patterns**
- 📊 **Compute engagement metrics** — **PNR**, **IDIR**
- 🧠 **Generate insights** about classroom dynamics
- 🔮 Provide analytics using **ML / NLP models**

---

#### 🎯 **Project Goals**
- Enhance classroom understanding  
- Improve teacher feedback  
- Support automated transcript analysis  
""")

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown("### ")
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center>Made in 2025</center>", unsafe_allow_html=True)
