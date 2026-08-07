import streamlit as st

st.set_page_config(
    page_title="Methodology",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 System Methodology")

st.markdown("""
This page explains the overall design, architecture and workflow of the
Singapore HDB Smart Assistant.
""")

st.divider()

# ----------------------------------------------------
# Development Methodology
# ----------------------------------------------------

st.header("1️⃣ Development Methodology")

st.write("""
The project follows an iterative software development approach.

The application was developed incrementally using:

- Python
- Streamlit
- Pandas
- Plotly
- OpenAI (future integration)

Each page was implemented and tested independently before integration.
""")

st.divider()

# ----------------------------------------------------
# System Architecture
# ----------------------------------------------------

st.header("2️⃣ System Architecture")

st.code("""
+----------------------+
|      User            |
+----------+-----------+
           |
           v
+----------------------+
| Streamlit Interface  |
+----------+-----------+
           |
           +-------------------+
           |                   |
           v                   v
Eligibility Engine       AI Housing Advisor
           |                   |
           +----------+--------+
                      |
                      v
                Session State
                      |
                      v
                 Dashboard
""")

st.divider()

# ----------------------------------------------------
# Workflow
# ----------------------------------------------------

st.header("3️⃣ Application Workflow")

workflow = [
    "User enters personal information.",
    "Eligibility & Grant Advisor performs an advisory assessment.",
    "Results are stored in Streamlit Session State.",
    "Dashboard visualises the assessment.",
    "AI Housing Advisor provides personalised responses.",
    "Users are encouraged to verify information using the official HDB and CPF websites."
]

for step in workflow:
    st.write("✅", step)

st.divider()

# ----------------------------------------------------
# Data Sources
# ----------------------------------------------------

st.header("4️⃣ Data Sources")

st.success("""
Primary References

• Housing & Development Board (HDB)

• Central Provident Fund (CPF)

The application references publicly available government information
to support educational guidance.
""")

st.divider()

# ----------------------------------------------------
# AI Design
# ----------------------------------------------------

st.header("5️⃣ AI Design")

st.write("""
Current Version

• Rule-based knowledge retrieval

• Keyword matching

• Session-aware responses

Future Version

• OpenAI GPT integration

• Retrieval-Augmented Generation (RAG)

• Official document retrieval

• Natural language understanding
""")

st.divider()

# ----------------------------------------------------
# Technologies
# ----------------------------------------------------

st.header("6️⃣ Technologies")

tech = {
    "Programming Language": "Python",
    "Framework": "Streamlit",
    "Charts": "Plotly",
    "Data": "Pandas",
    "AI": "OpenAI (planned integration)",
    "IDE": "Visual Studio Code",
    "Version Control": "Git & GitHub"
}

for key, value in tech.items():
    st.write(f"**{key}:** {value}")

st.divider()

# ----------------------------------------------------
# Limitations
# ----------------------------------------------------

st.header("7️⃣ Current Limitations")

st.warning("""
• Eligibility assessment is advisory only.

• Grant estimation is simplified for demonstration purposes.

• AI currently uses a built-in knowledge base.

• Users should verify all information with HDB and CPF.
""")

st.divider()

# ----------------------------------------------------
# Future Enhancements
# ----------------------------------------------------

st.header("8️⃣ Future Enhancements")

future = [
    "Integrate OpenAI GPT.",
    "Use Retrieval-Augmented Generation (RAG).",
    "Automatically retrieve HDB and CPF updates.",
    "Generate downloadable PDF reports.",
    "Support multiple government services.",
    "Add voice interaction."
]

for item in future:
    st.write("🚀", item)

st.divider()

# ----------------------------------------------------
# Conclusion
# ----------------------------------------------------

st.header("9️⃣ Conclusion")

st.info("""
The Singapore HDB Smart Assistant demonstrates how AI can enhance access
to public information by providing users with personalised guidance,
interactive dashboards and conversational assistance.

The system is intended for educational purposes and complements,
rather than replaces, official government services.
""")

st.caption("Singapore HDB Smart Assistant | AI Bootcamp Capstone Project")