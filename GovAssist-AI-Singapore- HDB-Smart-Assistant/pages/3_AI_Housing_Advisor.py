import streamlit as st

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

st.set_page_config(
    page_title="AI Housing Advisor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Housing Advisor")

st.markdown("""
Ask questions about:

- HDB Resale Eligibility
- HFE Letter
- CPF Housing Grants
- Buying Process
- Housing Schemes

This assistant provides educational guidance based on publicly available HDB and CPF information.
""")

st.divider()

# ----------------------------------------------------
# Session State
# ----------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------
# Knowledge Base
# ----------------------------------------------------

knowledge = {

    "hfe":
    """The HDB Flat Eligibility (HFE) Letter is an integrated assessment that
helps determine your eligibility to buy a flat, CPF Housing Grants and HDB housing loan eligibility.""",

    "grant":
    """Eligible buyers may qualify for grants such as the Enhanced CPF Housing Grant (EHG)
and the Proximity Housing Grant (PHG), depending on their circumstances.""",

    "cpf":
    """CPF Ordinary Account savings may be used to finance an HDB resale flat,
subject to CPF and HDB rules.""",

    "single":
    """Singles who are Singapore Citizens and at least 35 years old may generally
purchase an HDB resale flat, subject to prevailing HDB eligibility conditions.""",

    "eligibility":
    """Eligibility depends on factors such as citizenship, age,
family nucleus and ownership of private property.""",

    "resale":
    """The HDB resale process generally includes:

1. Apply for an HFE Letter

2. Search for a resale flat

3. Request valuation

4. Submit resale application

5. Complete the transaction."""
}

# ----------------------------------------------------
# Response Function
# ----------------------------------------------------

def generate_response(question):

    system_prompt = """
    You are GovAssist AI, a Singapore HDB Housing Advisor.

    Answer only questions related to:

    - HDB
    - CPF Housing
    - HFE Letter
    - HDB Grants
    - HDB Eligibility
    - Buying or Selling HDB Flats
    - Singapore Housing Policies

    If the user asks something unrelated,
    politely explain that you only answer HDB and CPF housing questions.

    Always recommend users verify important information with the official
    HDB and CPF websites.
    """

    if "eligibility" in st.session_state:

        system_prompt += f"""

The user's latest eligibility assessment:

Eligibility:
{st.session_state.get("eligibility")}

Estimated Grant:
${st.session_state.get("grant",0):,}

Monthly Income:
${st.session_state.get("income",0):,}
"""

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role":"system",
                    "content":system_prompt
                },

                {
                    "role":"user",
                    "content":question
                }

            ],

            temperature=0.3

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"❌ OpenAI Error:\n\n{e}"

    # ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:

    st.header("💡 Suggested Questions")

    suggested_questions = [
        "What is an HFE Letter?",
        "Am I eligible to buy a resale flat?",
        "What CPF Housing Grants are available?",
        "Can a single buy an HDB resale flat?",
        "Explain the HDB resale process."
    ]

    for question in suggested_questions:
        if st.button(question, use_container_width=True):

            # Save user question
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            # Generate response
            response = generate_response(question)

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.success("🟢 AI Status: OpenAI Connected")

# ----------------------------------------------------
# Display Chat History
# ----------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------------------------------
# Chat Input
# ----------------------------------------------------

prompt = st.chat_input("Ask a question about HDB or CPF...")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate assistant response
    answer = generate_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# ----------------------------------------------------
# Official References
# ----------------------------------------------------

st.divider()

with st.expander("📚 Official References"):

    st.markdown("""
This chatbot is designed for educational purposes and references publicly
available information from:

- Housing & Development Board (HDB)
- Central Provident Fund (CPF)

Please verify all eligibility requirements and housing grants using the
official government websites.

**HDB:** https://www.hdb.gov.sg

**CPF:** https://www.cpf.gov.sg/member
""")

st.success(
    "OpenAI is connected. Responses are generated dynamically."
)