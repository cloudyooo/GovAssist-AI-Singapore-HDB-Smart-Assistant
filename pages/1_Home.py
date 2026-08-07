import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main-header{
    font-size:42px;
    font-weight:bold;
    color:#C62828;
}

.sub-header{
    font-size:22px;
    color:#444444;
}

.feature-card{
    background-color:#F8F9FA;
    padding:20px;
    border-radius:10px;
    border:1px solid #DDDDDD;
    min-height:170px;
}

.footer{
    text-align:center;
    color:grey;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Hero Section
# -----------------------------
st.set_page_config(
    page_title="Singapore HDB Smart Assistant",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Singapore HDB Smart Assistant")


st.markdown(
'<p class="sub-header">AI-powered guidance for first-time HDB resale buyers</p>',
unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Introduction
# -----------------------------

left,right = st.columns([2,1])

with left:

    st.markdown("""
### Welcome

Buying an HDB resale flat involves many decisions.

This application helps Singapore residents understand:

- HDB eligibility
- CPF Housing Grants
- HDB resale procedures
- Required documents
- Next steps
- Government resources

The information is based on official HDB and CPF references.
""")

with right:

    st.info("""
### Official Sources

🏠 Housing & Development Board

💰 Central Provident Fund Board

AI responses will be generated using official information.
""")

# -----------------------------
# Statistics
# -----------------------------

st.divider()

col1,col2,col3 = st.columns(3)

col1.metric("Government Sources","2")
col2.metric("AI Enabled","Yes")
col3.metric("Platform","Streamlit")

# -----------------------------
# Features
# -----------------------------

st.divider()

st.header("Application Features")

c1,c2 = st.columns(2)

with c1:

    st.markdown("""
<div class="feature-card">

## ✅ Eligibility & Grant Advisor

Check:

- HDB eligibility

- CPF Housing Grant estimate

- Recommended next steps

</div>
""", unsafe_allow_html=True)

with c2:

    st.markdown("""
<div class="feature-card">

## 🤖 AI Housing Advisor

Ask questions like:

• Can I buy a resale flat?

• What is an HFE Letter?

• What grants am I eligible for?

</div>
""", unsafe_allow_html=True)

c3,c4 = st.columns(2)

with c3:

    st.markdown("""
<div class="feature-card">

## 📊 Dashboard

Visualise

- Eligibility

- Income

- Estimated grants

- User summary

</div>
""", unsafe_allow_html=True)

with c4:

    st.markdown("""
<div class="feature-card">

## 📚 Methodology

Learn

- AI architecture

- Data sources

- Technologies

- RAG workflow

</div>
""", unsafe_allow_html=True)


# -----------------------------
# Quick Navigation
# -----------------------------

st.divider()

st.header("Getting Started")

st.write("""
Use the navigation menu on the left.

Recommended order:

1. Eligibility & Grant Advisor

2. AI Housing Advisor

3. Dashboard

4. About Us

5. Methodology
""")

# -----------------------------
# Disclaimer
# -----------------------------

st.divider()

st.warning("""
Disclaimer

This application is developed for educational purposes as part of a Capstone Project.

Eligibility and grant estimates are advisory only.

Please verify all information with the official HDB and CPF websites.
""")

# -----------------------------
# Footer
# -----------------------------

st.markdown(
"""
<hr>
<p class="footer">
Singapore HDB Smart Assistant • Capstone Project • AI Bootcamp
</p>
""",
unsafe_allow_html=True
)