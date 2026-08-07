import streamlit as st

st.set_page_config(
    page_title="Singapore HDB Smart Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🏠 HDB Smart Assistant")

    st.markdown("---")

    st.success("Capstone Project")

    st.write("Navigate using the pages below.")

    st.markdown("---")

    st.info(
        """
        **Official Sources**

        • Housing Development Board (HDB)

        • CPF Board
        """
    )

# ---------- Main Page ----------

st.title("🏠 Singapore HDB Smart Assistant")

st.caption("AI-powered guidance for first-time HDB buyers")

st.divider()

left, right = st.columns([2,1])

with left:

    st.header("Welcome")

    st.write(
        """
This application helps Singapore residents understand
the HDB resale purchasing process through interactive
tools and Artificial Intelligence.

The assistant provides:

- Eligibility checking

- CPF Housing Grant guidance

- Housing journey planning

- AI-powered question answering

using official government information.
"""
    )

with right:

    st.metric(
        "Government Sources",
        2
    )

    st.metric(
        "AI Enabled",
        "Yes"
    )

st.divider()

st.header("Project Features")

col1,col2=st.columns(2)

with col1:

    st.success("✅ Eligibility & Grant Advisor")

    st.write(
        """
Check your basic HDB eligibility
and estimate CPF Housing Grants.
"""
    )

with col2:

    st.success("🤖 AI Housing Advisor")

    st.write(
        """
Ask questions using official
HDB and CPF information.
"""
    )

st.divider()

st.header("Assignment Objectives")

st.markdown("""
✔ Interactive Streamlit Application

✔ Large Language Model (OpenAI)

✔ Government Knowledge Base

✔ Multiple User Use Cases

✔ AI-assisted Recommendations

✔ Data Visualisation

✔ GitHub Deployment

✔ Streamlit Community Cloud
""")

st.divider()

st.info(
"""
Select a page from the left sidebar to begin.

Next we'll build the **Eligibility & Grant Advisor**.
"""
)