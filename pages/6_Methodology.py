import streamlit as st

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Methodology",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 System Methodology")

st.markdown("""
This page explains the overall design, architecture, workflow
and AI methodology of the Singapore HDB Smart Assistant.
""")

st.divider()


# ==========================================================
# 1. Development Methodology
# ==========================================================

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

Each component was implemented and tested independently before
being integrated into the complete application.
""")

st.divider()


# ==========================================================
# 2. System Architecture
# ==========================================================

st.header("2️⃣ System Architecture")

st.write("""
The Singapore HDB Smart Assistant combines a rule-based
eligibility assessment system with an AI-powered housing advisor.

The AI Housing Advisor uses a basic keyword-based
Retrieval-Augmented Generation (RAG) architecture.
""")

st.code("""
+--------------------------+
|           User           |
+------------+-------------+
             |
             v
+--------------------------+
|   Streamlit Interface    |
+------------+-------------+
             |
       +-----+------+
       |            |
       v            v
+-------------+  +------------------+
| Eligibility |  | AI Housing       |
| & Grant     |  | Advisor          |
| Advisor     |  +--------+---------+
+------+------+           |
       |                  v
       |          +------------------+
       |          | Keyword Retrieval|
       |          +--------+---------+
       |                   |
       |                   v
       |          +------------------+
       |          | Local HDB / CPF  |
       |          | Knowledge Base   |
       |          +--------+---------+
       |                   |
       |                   v
       |          +------------------+
       |          |   OpenAI GPT     |
       |          +--------+---------+
       |                   |
       +---------+---------+
                 |
                 v
        +------------------+
        |  Session State   |
        +--------+---------+
                 |
                 v
        +------------------+
        |    Dashboard     |
        +------------------+
""")

st.divider()


# ==========================================================
# 3. Application Workflow
# ==========================================================

st.header("3️⃣ Application Workflow")

workflow = [
    "User enters personal and household information into the Eligibility & Grant Advisor.",

    "The rule-based eligibility engine performs an advisory eligibility and grant assessment.",

    "Assessment results are stored using Streamlit Session State.",

    "The Dashboard visualises the assessment results.",

    "The user can ask housing-related questions through the AI Housing Advisor.",

    "The RAG component uses keyword matching to retrieve relevant information from the local HDB/CPF knowledge base.",

    "The retrieved information is added to the AI prompt as supporting context.",

    "The retrieved context and user's question are sent to OpenAI GPT.",

    "OpenAI GPT generates a natural-language response based primarily on the retrieved information.",

    "Relevant eligibility information stored in Session State may also be provided to the AI to support more personalised responses.",

    "Users are encouraged to verify important information using official HDB and CPF sources."
]

for step in workflow:
    st.write("✅", step)

st.divider()


# ==========================================================
# 4. Data Sources
# ==========================================================

st.header("4️⃣ Data Sources")

st.success("""
Primary Official Sources

• Housing & Development Board (HDB)

• Central Provident Fund (CPF)

The housing information used in the application's knowledge base
is sourced from publicly available information on the official
HDB and CPF websites.
""")

st.write("""
The relevant housing information is stored within the application's
local knowledge base.

The current version does **not retrieve information live from the
HDB or CPF websites each time a user submits a question**.

Instead, information sourced from the official websites is stored
locally and retrieved by the RAG component when relevant to the
user's question.
""")

st.divider()


# ==========================================================
# 5. AI Design
# ==========================================================

st.header("5️⃣ AI Design")

st.write("""
The current AI Housing Advisor includes:

- OpenAI GPT-4.1-mini integration
- Basic Retrieval-Augmented Generation (RAG)
- Keyword-based knowledge retrieval
- Local knowledge base containing information sourced from
  official HDB and CPF websites
- Natural-language question answering
- Session-aware responses
- Rule-based eligibility and grant assessment
- Domain restriction to HDB and CPF housing-related topics
""")

st.divider()


# ==========================================================
# 6. Retrieval-Augmented Generation (RAG)
# ==========================================================

st.header("6️⃣ Retrieval-Augmented Generation (RAG)")

st.write("""
The AI Housing Advisor uses a **basic keyword-based
Retrieval-Augmented Generation (RAG)** approach.

RAG combines information retrieval with a Large Language Model
(LLM).

Instead of relying only on the language model's general knowledge,
the system first retrieves relevant information from the
application's local HDB/CPF knowledge base.
""")

st.subheader("How RAG Works")

rag_steps = [
    "The user submits an HDB or CPF housing-related question.",

    "The system analyses the question and performs keyword matching.",

    "Relevant information is retrieved from the local HDB/CPF knowledge base.",

    "The retrieved information is added to the AI system prompt as context.",

    "The retrieved context and user's question are sent to OpenAI GPT.",

    "The language model generates a natural-language response based primarily on the retrieved information.",

    "The chatbot displays the generated response together with the relevant knowledge source."
]

for step in rag_steps:
    st.write("🔹", step)

st.subheader("RAG Workflow")

st.code("""
Official HDB / CPF Websites
           |
           v
Information Sourced for
Local Knowledge Base
           |
           v
+-------------------------+
| User Housing Question   |
+------------+------------+
             |
             v
+-------------------------+
| Keyword-Based Retrieval |
+------------+------------+
             |
             v
+-------------------------+
| Local HDB / CPF         |
| Knowledge Base          |
+------------+------------+
             |
             v
+-------------------------+
| Relevant Context        |
| Retrieved               |
+------------+------------+
             |
             v
+-------------------------+
| Retrieved Context +     |
| User Question           |
+------------+------------+
             |
             v
+-------------------------+
| OpenAI GPT-4.1-mini     |
+------------+------------+
             |
             v
+-------------------------+
| Generated Response      |
+-------------------------+
""")

st.info("""
The current RAG implementation uses keyword matching rather
than embeddings or vector similarity search.

This provides a simple and explainable RAG implementation
for the current prototype.
""")

st.divider()


# ==========================================================
# 7. Rule-Based Eligibility & Grant Advisor
# ==========================================================

st.header("7️⃣ Rule-Based Eligibility & Grant Advisor")

st.write("""
The Eligibility & Grant Advisor operates alongside the
RAG-based AI Housing Advisor.

It uses predefined Python rules to perform an advisory
assessment based on user inputs such as:

- Citizenship
- Age
- Applicant type
- Household composition
- Household income
- Property ownership
- Proximity to parents or children

The results can be stored in Streamlit Session State and
shared with other parts of the application.
""")

st.code("""
User Information
       |
       v
Rule-Based Conditions
       |
       v
Eligibility Assessment
       |
       v
Grant Estimation
       |
       v
Streamlit Session State
       |
       +---------------------+
       |                     |
       v                     v
   Dashboard          AI Housing Advisor
""")

st.divider()


# ==========================================================
# 8. Large Language Model (LLM)
# ==========================================================

st.header("8️⃣ Large Language Model (LLM)")

st.write("""
The AI Housing Advisor integrates OpenAI GPT-4.1-mini
to generate conversational responses.

The LLM acts as the **generation component** of the RAG
architecture.

Relevant HDB/CPF information is retrieved first and supplied
to the language model as context before the response is
generated.
""")

st.code("""
Retrieved HDB / CPF Context
            +
       User Question
            |
            v
   OpenAI GPT-4.1-mini
            |
            v
Natural-Language Response
""")

st.divider()


# ==========================================================
# 9. Session-Aware Responses
# ==========================================================

st.header("9️⃣ Session-Aware Responses")

st.write("""
Streamlit Session State is used to share relevant information
between different components of the application.

For example, after a user completes the Eligibility & Grant
Advisor, information such as the eligibility result, estimated
grant and household income can be stored in Session State.

The AI Housing Advisor can use this information when relevant
to the user's housing question.
""")

st.code("""
Eligibility & Grant Advisor
           |
           v
    Session State
           |
           v
   AI Housing Advisor
           |
           v
Context-Aware AI Response
""")

st.divider()


# ==========================================================
# 10. Technologies
# ==========================================================

st.header("🔟 Technologies")

tech = {
    "Programming Language": "Python",
    "Web Framework": "Streamlit",
    "Data Processing": "Pandas",
    "Data Visualisation": "Plotly",
    "Large Language Model": "OpenAI GPT-4.1-mini",
    "AI Architecture": "Retrieval-Augmented Generation (RAG)",
    "Retrieval Method": "Keyword-based retrieval",
    "Knowledge Base": "Locally stored HDB / CPF information",
    "State Management": "Streamlit Session State",
    "IDE": "Visual Studio Code",
    "Version Control": "Git & GitHub"
}

for key, value in tech.items():
    st.write(f"**{key}:** {value}")

st.divider()


# ==========================================================
# 11. Current Limitations
# ==========================================================

st.header("1️⃣1️⃣ Current Limitations")

st.warning("""
• Eligibility assessments are advisory only.

• Grant estimation is simplified for demonstration purposes.

• The RAG system currently uses keyword-based retrieval rather
  than semantic vector search.

• HDB and CPF information is stored locally and is not retrieved
  live from the official websites for every question.

• The local knowledge base must be manually updated when relevant
  government information changes.

• AI-generated responses may be incomplete if the retrieved
  information is insufficient.

• Users should verify important housing, eligibility and financial
  information through official HDB and CPF channels.

• Implement live retrieval from official HDB and CPF sources.
""")

st.divider()


# ==========================================================
# 12. Future Enhancements
# ==========================================================

st.header("1️⃣2️⃣ Future Enhancements")

future = [
    "Expand the knowledge base with additional official government information.",

    "Support additional Singapore government services.",

    "Add voice-based interaction."
]

for item in future:
    st.write("🚀", item)

st.divider()


# ==========================================================
# 13. Conclusion
# ==========================================================

st.header("1️⃣3️⃣ Conclusion")

st.info("""
The Singapore HDB Smart Assistant demonstrates how rule-based
decision support, Retrieval-Augmented Generation (RAG) and
Large Language Models (LLMs) can be combined within a Streamlit
application to provide housing-related educational guidance.

The Eligibility & Grant Advisor uses predefined rules to provide
an advisory eligibility and grant assessment.

The AI Housing Advisor uses keyword-based retrieval to identify
relevant information from a local knowledge base containing
housing information sourced from official HDB and CPF websites.

The retrieved information is provided to OpenAI GPT-4.1-mini
as context before the model generates a natural-language response.

The current prototype therefore combines rule-based assessment,
keyword-based RAG, OpenAI GPT and Streamlit Session State.

The system is intended for educational purposes and complements,
rather than replaces, official government services.
""")

st.caption(
    "Singapore HDB Smart Assistant | AI Bootcamp Capstone Project"
)
