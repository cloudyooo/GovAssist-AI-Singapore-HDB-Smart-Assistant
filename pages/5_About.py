import streamlit as st

st.set_page_config(
    page_title="About Us",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About Singapore HDB Smart Assistant")

st.markdown("""
The **Singapore HDB Smart Assistant** is an AI-powered web application
developed as part of an AI Bootcamp Capstone Project.

Its objective is to simplify the HDB resale journey by providing users
with personalised guidance based on selected information and official
government resources.
""")

st.divider()

# ---------------------------------------------------
# Project Objectives
# ---------------------------------------------------

st.header("🎯 Project Objectives")

st.success("""
• Help users understand HDB resale eligibility

• Estimate CPF Housing Grants

• Provide AI-powered housing guidance

• Improve awareness of HDB resale procedures

• Demonstrate the use of Artificial Intelligence in public services
""")

# ---------------------------------------------------
# Technologies
# ---------------------------------------------------

st.header("🛠 Technologies Used")

tech = {
    "Programming Language": "Python",
    "Framework": "Streamlit",
    "Visualisation": "Plotly",
    "Data Processing": "Pandas",
    "AI": "OpenAI GPT (Ready for Integration)",
    "Deployment": "GitHub + Streamlit Community Cloud"
}

for key, value in tech.items():
    st.write(f"**{key}:** {value}")

st.divider()

# ---------------------------------------------------
# Government References
# ---------------------------------------------------

st.header("🏛 Official Government References")

st.markdown("""
This application references publicly available information from:

- Housing & Development Board (HDB)
- Central Provident Fund (CPF) Board

Users should always verify the latest policies using the official websites.
""")

st.info("""
Official Websites

https://www.hdb.gov.sg

https://www.cpf.gov.sg/member
""")

# ---------------------------------------------------
# Disclaimer
# ---------------------------------------------------

st.header("⚠ Disclaimer")

st.warning("""
This project has been developed for educational purposes only.

The eligibility assessment and grant estimation are advisory in nature
and should not be considered official decisions.

Please refer to HDB and CPF for the latest policies.
""")

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.divider()

st.caption("Singapore HDB Smart Assistant | AI Bootcamp Capstone Project")