import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

# ==========================================================
# Environment / OpenAI
# ==========================================================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ==========================================================
# Page Configuration
# ==========================================================

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

This assistant uses **Retrieval-Augmented Generation (RAG)**
to retrieve relevant HDB/CPF knowledge before generating
an AI response.
""")

st.divider()

# ==========================================================
# Session State
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# HDB / CPF Knowledge Base
# ==========================================================
#
# This is a curated local knowledge base based on
# publicly available HDB and CPF information.
#
# The RAG retrieval function searches this knowledge base
# before sending relevant information to the LLM.
#

knowledge = {

    "hfe": {
        "keywords": [
            "hfe",
            "hfe letter",
            "flat eligibility",
            "housing loan"
        ],

        "content": """
The HDB Flat Eligibility (HFE) Letter provides an integrated
assessment of a household's eligibility to:

- Buy an HDB flat
- Receive CPF Housing Grants
- Obtain an HDB housing loan

Prospective flat buyers should obtain an HFE Letter before
committing to an HDB flat purchase.
""",

        "source": "Housing & Development Board (HDB)"
    },

    "grant": {
        "keywords": [
            "grant",
            "grants",
            "housing grant",
            "cpf grant",
            "ehg",
            "phg",
            "enhanced cpf housing grant",
            "proximity housing grant"
        ],

        "content": """
Eligible HDB resale flat buyers may qualify for CPF Housing
Grants.

Examples include:

- Enhanced CPF Housing Grant (EHG)
- Proximity Housing Grant (PHG)

Actual eligibility and grant amounts depend on factors such
as household income, applicant profile and prevailing
HDB/CPF conditions.
""",

        "source": "HDB / Central Provident Fund (CPF)"
    },

    "cpf": {
        "keywords": [
            "cpf",
            "ordinary account",
            "cpf oa",
            "cpf savings",
            "finance",
            "financing"
        ],

        "content": """
CPF Ordinary Account savings may be used to finance the
purchase of an HDB resale flat, subject to prevailing CPF
and HDB rules.

CPF savings may potentially be used for eligible housing
payments, including housing loan repayments, subject to
applicable conditions.
""",

        "source": "Central Provident Fund (CPF)"
    },

    "single": {
        "keywords": [
            "single",
            "singles",
            "unmarried",
            "35",
            "36",
            "single singapore citizen",
            "single citizen"
        ],

        "content": """
Singapore Citizens who are single and at least 35 years old
may generally purchase an HDB resale flat under the
applicable eligibility scheme, subject to prevailing HDB
conditions.

Other eligibility requirements may still apply, including
citizenship, property ownership and other HDB requirements.
""",

        "source": "Housing & Development Board (HDB)"
    },

    "eligibility": {
        "keywords": [
            "eligible",
            "eligibility",
            "qualify",
            "qualification",
            "can i buy",
            "allowed to buy",
            "buy hdb"
        ],

        "content": """
Eligibility to purchase an HDB resale flat depends on
several factors.

These may include:

- Citizenship
- Age
- Family nucleus
- Applicant type
- Ownership of other residential property
- Other prevailing HDB requirements

An HFE assessment should be used for an official
determination.
""",

        "source": "Housing & Development Board (HDB)"
    },

    "resale": {
        "keywords": [
            "resale",
            "resale process",
            "buy resale",
            "buying process",
            "purchase process",
            "steps",
            "buy flat"
        ],

        "content": """
The HDB resale purchasing journey generally involves:

1. Obtain an HFE Letter.
2. Search for a suitable resale flat.
3. Negotiate with the seller and follow the required
   resale procedures.
4. Complete the required valuation and resale application
   processes.
5. Complete the resale transaction.

The exact process should be verified using current HDB
guidance.
""",

        "source": "Housing & Development Board (HDB)"
    }
}

# ==========================================================
# RAG - Retrieval Function
# ==========================================================

def retrieve_knowledge(question, max_results=3):

    question_lower = question.lower()

    question_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            question_lower
        )
    )

    scored_results = []

    for topic, data in knowledge.items():

        score = 0

        for keyword in data["keywords"]:

            keyword_lower = keyword.lower()

            # Higher score for complete phrase match
            if keyword_lower in question_lower:
                score += 3

            # Additional score for individual word matches
            keyword_words = set(
                re.findall(
                    r"\b[a-zA-Z0-9]+\b",
                    keyword_lower
                )
            )

            score += len(
                question_words.intersection(keyword_words)
            )

        if score > 0:

            scored_results.append({
                "topic": topic,
                "score": score,
                "content": data["content"],
                "source": data["source"]
            })

    # Sort highest relevance first
    scored_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_results[:max_results]


# ==========================================================
# RAG - Build Retrieved Context
# ==========================================================

def build_context(retrieved_results):

    if not retrieved_results:
        return ""

    context_parts = []

    for result in retrieved_results:

        context_parts.append(
            f"""
Topic:
{result["topic"]}

Information:
{result["content"]}

Source:
{result["source"]}
"""
        )

    return "\n---\n".join(context_parts)


# ==========================================================
# AI Response Function
# ==========================================================

def generate_response(question):

    # ------------------------------------------------------
    # RAG STEP 1 - RETRIEVAL
    # ------------------------------------------------------

    retrieved_results = retrieve_knowledge(question)

    # If no relevant HDB/CPF knowledge is found
    if not retrieved_results:

        return """
I could not find relevant information in my HDB/CPF
knowledge base for that question.

I currently provide guidance about:

- HDB housing
- CPF housing
- HFE Letters
- Housing grants
- HDB eligibility
- HDB resale purchases

Please ask a question related to HDB or CPF housing.
"""

    # ------------------------------------------------------
    # RAG STEP 2 - AUGMENTATION
    # ------------------------------------------------------

    retrieved_context = build_context(
        retrieved_results
    )

    system_prompt = f"""
You are GovAssist AI, a Singapore HDB Housing Advisor.

You use Retrieval-Augmented Generation (RAG).

Relevant information has been retrieved from the
application's HDB/CPF knowledge base.

====================================================
RETRIEVED KNOWLEDGE
====================================================

{retrieved_context}

====================================================

INSTRUCTIONS:

1. Answer the user's question primarily using the
   retrieved knowledge above.

2. Do not invent HDB eligibility requirements,
   grant amounts or housing policies that are not
   supported by the retrieved information.

3. If the retrieved information is insufficient,
   clearly explain that more information is required.

4. Only answer questions related to:

   - HDB
   - CPF Housing
   - HFE Letter
   - HDB Grants
   - HDB Eligibility
   - Buying or Selling HDB Flats
   - Singapore Housing Policies

5. If the user asks about unrelated topics such as
   IRAS income tax, healthcare or unrelated government
   services, explain that this assistant only covers
   HDB and CPF housing topics.

6. Important eligibility and financial information
   should always be verified through official HDB
   and CPF channels.

7. Keep answers clear, educational and concise.
"""

    # ------------------------------------------------------
    # Session-Aware Personalisation
    # ------------------------------------------------------

    if "eligibility" in st.session_state:

        system_prompt += f"""

====================================================
USER'S ELIGIBILITY ASSESSMENT
====================================================

Eligibility:
{st.session_state.get("eligibility")}

Estimated Grant:
${st.session_state.get("grant", 0):,}

Average Household Income:
${st.session_state.get("household_income", 0):,}

Applicant Type:
{st.session_state.get("applicant_type", "Not available")}

Household Members:
{st.session_state.get("household_members", "Not available")}

Use this information only when relevant to the
user's housing question.
"""

    # ------------------------------------------------------
    # RAG STEP 3 - GENERATION
    # ------------------------------------------------------

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": question
                }

            ],

            temperature=0.2

        )

        answer = response.choices[0].message.content

        # --------------------------------------------------
        # Add Retrieved Knowledge Sources
        # --------------------------------------------------

        sources = sorted(
            set(
                result["source"]
                for result in retrieved_results
            )
        )

        source_text = "\n".join(
            f"- {source}"
            for source in sources
        )

        answer += f"""

---

**Knowledge Sources Retrieved**

{source_text}

*Please verify important eligibility and financial
information through the official HDB or CPF website.*
"""

        return answer

    except Exception as e:

        return f"❌ OpenAI Error:\n\n{e}"


# ==========================================================
# Sidebar
# ==========================================================

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

        if st.button(
            question,
            use_container_width=True
        ):

            # Save user question
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            # Generate RAG response
            response = generate_response(question)

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.success(
        "🟢 AI Status: OpenAI Connected"
    )

    st.info(
        "📚 RAG Status: Knowledge Retrieval Enabled"
    )


# ==========================================================
# Display Chat History
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==========================================================
# Chat Input
# ==========================================================

prompt = st.chat_input(
    "Ask a question about HDB or CPF..."
)

if prompt:

    # Display user question
    with st.chat_message("user"):

        st.markdown(prompt)

    # Save user question
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate RAG response
    answer = generate_response(prompt)

    # Display assistant response
    with st.chat_message("assistant"):

        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# ==========================================================
# Official References
# ==========================================================

st.divider()

with st.expander(
    "📚 Official References"
):

    st.markdown("""
This chatbot is designed for educational purposes.

The local knowledge base is based on publicly available
information from:

- Housing & Development Board (HDB)
- Central Provident Fund (CPF)

Important eligibility requirements, housing grants and
financial information should be verified using the
official government websites.

**HDB:** https://www.hdb.gov.sg

**CPF:** https://www.cpf.gov.sg/member
""")


# ==========================================================
# Footer
# ==========================================================

st.success(
    "OpenAI is connected. "
    "RAG retrieval is enabled using the local HDB/CPF "
    "knowledge base."
)
