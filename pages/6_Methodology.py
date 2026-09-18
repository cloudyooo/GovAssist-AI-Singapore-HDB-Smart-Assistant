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
- OpenAI GPT
- Retrieval-Augmented Generation (RAG)

Each page was implemented and tested independently before integration.
""")

st.divider()

# ----------------------------------------------------
# System Architecture
# ----------------------------------------------------

st.header("2️⃣ System Architecture")

st.code("""
+----------------------+
|        User          |
+----------+-----------+
           |
           v
+----------------------+
| Streamlit Interface  |
+----------+-----------+
           |
     +-----+------+
     |            |
     v            v
Eligibility    AI Housing
& Grant        Advisor
Advisor           |
     |            v
     |      Knowledge Retrieval
     |            |
     |            v
     |      HDB / CPF Knowledge
     |            |
     |            v
     |       OpenAI GPT
     |            |
     +------+-----+
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
    "User enters personal information into the Eligibility & Grant Advisor.",
    "The rule-based eligibility engine performs an advisory assessment.",
    "Assessment results are stored in Streamlit Session State.",
    "The Dashboard visualises the assessment results.",
    "The user can ask housing-related questions through the AI Housing Advisor.",
    "The RAG component retrieves relevant information from the local HDB/CPF knowledge base.",
    "The retrieved information is provided as context to the OpenAI language model.",
    "OpenAI GPT generates a response based on the retrieved information and relevant session data.",
    "Users are encouraged to verify important information using official HDB and CPF sources."
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

The application's local knowledge base is curated using publicly
available HDB and CPF information for educational purposes.
""")

st.divider()

# ----------------------------------------------------
# AI Design
# ----------------------------------------------------

st.header("5️⃣ AI Design")

st.write("""
Current Version

• OpenAI GPT integration

• Retrieval-Augmented Generation (RAG)

• Keyword-based knowledge retrieval

• Curated local HDB/CPF knowledge base

• Session-aware responses

• Rule-based eligibility and grant assessment

• Natural language question answering


Future Version

• Semantic retrieval using embeddings and vector search

• Automated retrieval of updated official HDB and CPF information

• Expanded government knowledge base

• Improved source citation and document retrieval
""")

st.divider()

# ----------------------------------------------------
# RAG Architecture
# ----------------------------------------------------

st.header("6️⃣ Retrieval-Augmented Generation (RAG)")

st.write("""
The AI Housing Advisor uses a basic keyword-based
Retrieval-Augmented Generation (RAG) approach.

When a user submits a housing question:

1. The system analyses the user's question.

2. Keyword matching is used to retrieve relevant information
   from the local HDB/CPF knowledge base.

3. The retrieved information is added to the AI prompt as context.

4. The question and retrieved context are sent to OpenAI GPT.

5. GPT generates a natural-language response based primarily on
   the retrieved information.

This approach helps ground AI responses in the project's curated
housing knowledge rather than relying solely on the language
model's general knowledge.
""")

st.code("""
User Question
      |
      v
Keyword Retrieval
      |
      v
Local HDB / CPF Knowledge Base
      |
      v
Relevant Context
      |
      v
OpenAI GPT
      |
      v
Generated Housing Response
""")

st.divider()

# ----------------------------------------------------
# Technologies
# ----------------------------------------------------

st.header("7️⃣ Technologies")

tech = {
    "Programming Language": "Python",
    "Framework": "Streamlit",
    "Charts": "Plotly",
    "Data Processing": "Pandas",
    "AI / LLM": "OpenAI GPT",
    "RAG Retrieval": "Keyword-based retrieval",
    "Knowledge Base": "Curated HDB / CPF information",
    "IDE": "Visual Studio Code",
    "Version Control": "Git & GitHub"
}

for key, value in tech.items():
    st.write(f"**{key}:** {value}")

st.divider()

# ----------------------------------------------------
# Limitations
# ----------------------------------------------------

st.header("8️⃣ Current Limitations")

st.warning("""
• Eligibility assessments are advisory only.

• Grant estimation is simplified for demonstration purposes.

• The RAG system currently uses keyword-based retrieval rather
  than semantic vector search.

• The knowledge base is manually curated and does not automatically
  retrieve live updates from HDB or CPF.

• AI-generated responses may still contain errors or incomplete
  information.

• Users should verify important information with official HDB
  and CPF sources.
""")

st.divider()

# ----------------------------------------------------
# Future Enhancements
# ----------------------------------------------------

st.header("9️⃣ Future Enhancements")

future = [
    "Implement semantic search using embeddings and a vector database.",
    "Automatically retrieve updated HDB and CPF information.",
    "Expand the knowledge base with additional official documents.",
    "Improve source citation and traceability.",
    "Generate downloadable PDF reports.",
    "Support additional Singapore government services.",
    "Add voice interaction."
]

for item in future:
    st.write("🚀", item)

st.divider()

# ----------------------------------------------------
# Conclusion
# ----------------------------------------------------

st.header("🔟 Conclusion")

st.info("""
The Singapore HDB Smart Assistant demonstrates how rule-based
decision support, Retrieval-Augmented Generation (RAG) and Large
Language Models (LLMs) can be combined to improve access to
housing-related information.

The Eligibility & Grant Advisor provides rule-based assessments,
while the AI Housing Advisor retrieves relevant information from
a curated HDB/CPF knowledge base and uses OpenAI GPT to generate
natural-language responses.

The system is intended for educational purposes and complements,
rather than replaces, official government services.
""")

st.caption(
    "Singapore HDB Smart Assistant | AI Bootcamp Capstone Project"
)
