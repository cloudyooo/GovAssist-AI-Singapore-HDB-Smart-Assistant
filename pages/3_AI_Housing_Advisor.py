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

- HDB flat eligibility
- Flat types and housing options
- Singles housing options
- HFE Letter
- CPF Housing Grants
- CPF usage for housing
- HDB resale flats
- HDB buying process

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
# HDB / CPF RAG Knowledge Base
# ==========================================================
#
# Information below is based on publicly available official
# HDB and CPF information.
#
# Each knowledge item contains:
#
# - keywords
# - content
# - source
# - source_url
#
# The RAG system retrieves relevant items before sending
# them to OpenAI GPT.
#
# ==========================================================

knowledge = {


    # ======================================================
    # HFE LETTER
    # ======================================================

    "hfe": {

        "keywords": [
            "hfe",
            "hfe letter",
            "flat eligibility",
            "housing eligibility",
            "housing loan",
            "eligible for hdb",
            "can i buy hdb"
        ],

        "content": """
The HDB Flat Eligibility (HFE) Letter provides an integrated
assessment of a household's housing and financing options.

The HFE assessment can inform applicants about matters such as:

- Eligibility to buy a new or resale HDB flat
- Eligibility for applicable CPF Housing Grants
- Eligibility for an HDB housing loan

Prospective buyers should obtain an HFE Letter for an official
assessment before committing to a flat purchase.
""",

        "source": "Housing & Development Board (HDB)",

        "source_url":
            "https://www.hdb.gov.sg/buying-a-flat/"
            "flat-grant-and-loan-eligibility"
    },


    # ======================================================
    # SINGLES - GENERAL ELIGIBILITY
    # ======================================================

    "single_eligibility": {

        "keywords": [
            "single",
            "singles",
            "unmarried",
            "single singapore citizen",
            "single citizen",
            "single sc",
            "35",
            "36",
            "37",
            "38",
            "39",
            "40",
            "single hdb",
            "single buy hdb",
            "single eligibility",
            "single flat"
        ],

        "content": """
For a Singapore Citizen buying a flat alone:

An unmarried or divorced Singapore Citizen generally needs
to be at least 35 years old to buy under the applicable
singles eligibility conditions.

A single applicant may potentially:

NEW FLAT
- Apply for a 2-room Flexi flat from HDB, subject to the
  applicable eligibility requirements.

RESALE FLAT
- Buy an eligible resale flat on the open market, subject
  to HDB's applicable eligibility conditions.

The exact options depend on matters such as:

- Citizenship
- Age
- Income
- Property ownership
- Flat classification
- Whether CPF Housing Grants are being used
- Other prevailing HDB conditions

Applicants should obtain an HFE Letter for an official
assessment of their housing, grant and loan eligibility.
""",

        "source": "HDB - Singles",

        "source_url":
            "https://www.hdb.gov.sg/buying-a-flat/"
            "flat-grant-and-loan-eligibility/singles"
    },


    # ======================================================
    # SINGLES - FLAT TYPES / SIZE
    # ======================================================

    "single_flat_options": {

        "keywords": [
            "flat size",
            "flat sizes",
            "flat type",
            "flat types",
            "what flat can i buy",
            "which flat can i buy",
            "what hdb can i buy",
            "what can i buy",
            "how many room",
            "room flat",
            "2 room",
            "2-room",
            "3 room",
            "3-room",
            "4 room",
            "4-room",
            "5 room",
            "5-room",
            "executive",
            "3gen",
            "single flat size",
            "single flat type",
            "single resale",
            "single bto",
            "single new flat"
        ],

        "content": """
HDB provides different housing options for eligible singles
buying on their own.

NEW FLATS

Eligible singles may apply for:

- 2-room Flexi flats

Eligible singles may apply for 2-room Flexi flats under the
Standard, Plus and Prime classifications, subject to the
applicable HDB eligibility requirements.

RESALE FLATS

For resale unclassified, Standard and Plus flats:

- Eligible singles may generally buy all flat types
  except 3Gen flats.

However, HDB notes that where the single applicant is applying
for CPF Housing Grants, the applicable resale flat option is
up to a 5-room flat.

For resale Prime flats:

- The applicable flat type for a single buying alone is
  generally a 2-room flat, subject to HDB's prevailing
  Prime flat eligibility requirements.

Therefore, the available flat size depends on whether the
applicant is buying:

1. A new flat
2. A resale Prime flat
3. A resale Standard, Plus or unclassified flat
4. With or without applicable CPF Housing Grants

Applicants should obtain an HFE Letter for an official
assessment before making a housing decision.
""",

        "source": "HDB - Singles",

        "source_url":
            "https://www.hdb.gov.sg/buying-a-flat/"
            "flat-grant-and-loan-eligibility/singles"
    },


    # ======================================================
    # STANDARD / PLUS / PRIME
    # ======================================================

    "flat_classification": {

        "keywords": [
            "standard",
            "plus",
            "prime",
            "standard flat",
            "plus flat",
            "prime flat",
            "classification",
            "flat classification",
            "standard plus prime"
        ],

        "content": """
HDB introduced the Standard, Plus and Prime housing framework.

For eligible singles:

NEW FLATS

Singles may apply for a 2-room Flexi flat under:

- Standard
- Plus
- Prime

RESALE FLATS

Singles may potentially buy:

- A 2-room Prime resale flat
- All flat types except 3Gen under Standard, Plus and
  existing unclassified resale flats

Different eligibility, subsidy and resale conditions may apply
depending on the flat classification.

Applicants should verify the applicable conditions with HDB.
""",

        "source": "HDB - Standard, Plus and Prime Housing Framework",

        "source_url":
            "https://www.hdb.gov.sg/buying-a-flat/"
            "bto-sbf-and-open-booking-of-flats/"
            "finding-a-new-flat/"
            "standard-plus-and-prime-housing-framework"
    },


    # ======================================================
    # SINGLES GRANT
    # ======================================================

    "single_resale_grant": {

        "keywords": [
            "single grant",
            "singles grant",
            "grant for single",
            "grant for singles",
            "resale grant",
            "cpf housing grant",
            "single cpf grant",
            "single resale grant",
            "how much grant",
            "grant amount",
            "40000",
            "25000"
        ],

        "content": """
Eligible first-timer Singapore Citizens buying a resale flat
on their own may qualify for the Singles Grant.

Based on current HDB information:

- $40,000 Singles Grant may apply for an eligible
  2- to 4-room resale flat.

- $25,000 Singles Grant may apply for an eligible
  5-room resale flat.

The applicant must satisfy the applicable HDB eligibility
conditions.

Eligible applicants may potentially also qualify for other
housing grants such as:

- Enhanced CPF Housing Grant (Singles)
- Proximity Housing Grant (Singles)

Each grant has its own eligibility requirements.

Applicants should use the HFE Letter for an official assessment
of the grants they may receive.
""",

        "source": "HDB - CPF Housing Grant for Singles Buying Resale Flats",

        "source_url":
            "https://www.hdb.gov.sg/buying-a-flat/"
            "flat-grant-and-loan-eligibility/singles/"
            "cpf-housing-grant"
    },


    # ======================================================
    # GENERAL GRANTS
    # ======================================================

    "grants": {

        "keywords": [
            "grant",
            "grants",
            "housing grant",
            "cpf grant",
            "cpf housing grant",
            "ehg",
            "phg",
            "enhanced cpf housing grant",
            "proximity housing grant",
            "housing grants"
        ],

        "content": """
Eligible HDB buyers may potentially qualify for CPF Housing
Grants depending on their applicant profile and the type of
flat being purchased.

Examples include:

- Enhanced CPF Housing Grant (EHG)
- CPF Housing Grant for eligible resale flat buyers
- Proximity Housing Grant (PHG)

Eligibility and grant amounts depend on the applicable HDB
conditions, such as:

- Household income
- Applicant profile
- First-timer status
- Flat type
- Family circumstances
- Proximity conditions

Applicants should obtain an HFE Letter for an official
assessment of applicable grants.
""",

        "source": "Housing & Development Board (HDB)",

        "source_url":
            "https://www.hdb.gov.sg/buying-a-flat/"
            "flat-grant-and-loan-eligibility"
    },


    # ======================================================
    # CPF - USING OA FOR HOUSING
    # ======================================================

    "cpf_housing": {

        "keywords": [
            "cpf",
            "cpf oa",
            "ordinary account",
            "oa savings",
            "cpf savings",
            "use cpf",
            "cpf housing",
            "cpf payment",
            "cpf loan",
            "downpayment",
            "monthly instalment",
            "housing payment"
        ],

        "content": """
CPF Ordinary Account (OA) savings may be used for eligible
housing-related payments.

Depending on the applicable CPF rules, OA savings may be used
for purposes such as:

- Purchasing an HDB flat
- Eligible downpayment
- Housing loan payments
- Eligible stamp and legal fees
- Home Protection Scheme premiums for applicable HDB flats

There are limits on how much CPF OA savings may be used for
a property.

The amount that can be used may depend on factors such as:

- Remaining lease of the property
- Property type
- Loan type
- Whether it is the first or a subsequent property

Applicants should check their applicable CPF housing usage
limits before committing to a purchase.
""",

        "source": "Central Provident Fund Board (CPFB) - Using CPF to Buy a Home",

        "source_url":
            "https://www.cpf.gov.sg/member/home-ownership/"
            "using-your-cpf-to-buy-a-home"
    },


    # ======================================================
    # CPF HOUSING USAGE LIMITS
    # ======================================================

    "cpf_usage_limits": {

        "keywords": [
            "cpf limit",
            "cpf limits",
            "housing limit",
            "housing limits",
            "how much cpf",
            "how much oa",
            "cpf usage",
            "cpf housing usage",
            "cpf calculator",
            "housing usage calculator"
        ],

        "content": """
The amount of CPF Ordinary Account savings that can be used
for a property purchase is subject to CPF housing rules.

The applicable amount may depend on factors including:

- Remaining lease of the property
- Type of property
- Loan type
- Whether the property is the buyer's first or subsequent
  property

CPF provides a Housing Usage Calculator that can help members
estimate the amount of OA savings that may be used for an
eligible property purchase.
""",

        "source": "Central Provident Fund Board (CPFB) - CPF Housing Usage",

        "source_url":
            "https://www.cpf.gov.sg/member/tools-and-services/"
            "calculators/cpf-housing-usage"
    },


    # ======================================================
    # GENERAL RESALE ELIGIBILITY
    # ======================================================

    "resale_eligibility": {

        "keywords": [
            "resale",
            "resale flat",
            "buy resale",
            "resale eligibility",
            "eligible resale",
            "resale hdb",
            "can i buy resale"
        ],

        "content": """
Eligibility to purchase an HDB resale flat depends on the
applicant's circumstances and the applicable HDB rules.

Relevant considerations may include:

- Citizenship
- Age
- Applicant or household type
- Flat classification
- Property ownership
- Whether CPF Housing Grants are being used
- Other prevailing HDB eligibility conditions

Singles aged 35 and above who are Singapore Citizens may
potentially purchase eligible resale flats on their own,
subject to the applicable HDB conditions.

An HFE Letter should be obtained for an official assessment.
""",

        "source": "Housing & Development Board (HDB)",

        "source_url":
            "https://www.hdb.gov.sg/buying-a-flat/"
            "flat-grant-and-loan-eligibility/singles"
    },


    # ======================================================
    # RESALE BUYING PROCESS
    # ======================================================

    "resale_process": {

        "keywords": [
            "resale process",
            "buying process",
            "buy resale",
            "buy resale flat",
            "resale steps",
            "purchase process",
            "how to buy",
            "steps to buy",
            "buy hdb resale"
        ],

        "content": """
The HDB resale purchasing journey generally includes:

1. Understand your eligibility and finances.
2. Obtain an HFE Letter.
3. Search for a suitable resale flat.
4. Negotiate with the seller.
5. Follow the applicable HDB resale procedures.
6. Complete the required resale application processes.
7. Complete the resale transaction.

Applicants should refer to HDB's current resale procedures
for the exact requirements and sequence.
""",

        "source": "Housing & Development Board (HDB)",

        "source_url":
            "https://www.hdb.gov.sg/residential/"
            "buying-a-flat/buying-procedure-for-resale-flats"
    }
}


# ==========================================================
# RAG - Text Normalisation
# ==========================================================

def normalise_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================================
# RAG - Retrieval Function
# ==========================================================

def retrieve_knowledge(question, max_results=4):

    question_lower = normalise_text(question)

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

            keyword_lower = normalise_text(keyword)

            # --------------------------------------------------
            # Strong score for exact phrase
            # --------------------------------------------------

            if keyword_lower in question_lower:
                score += 5

            # --------------------------------------------------
            # Score matching words
            # --------------------------------------------------

            keyword_words = set(
                re.findall(
                    r"\b[a-zA-Z0-9]+\b",
                    keyword_lower
                )
            )

            common_words = question_words.intersection(
                keyword_words
            )

            score += len(common_words)

        # ------------------------------------------------------
        # Extra relevance rules
        # ------------------------------------------------------

        # Singles question
        if any(
            word in question_lower
            for word in [
                "single",
                "unmarried"
            ]
        ):

            if topic in [
                "single_eligibility",
                "single_flat_options",
                "single_resale_grant"
            ]:
                score += 5

        # Flat size / option question
        if any(
            phrase in question_lower
            for phrase in [
                "flat size",
                "flat type",
                "what flat",
                "which flat",
                "what hdb",
                "what option",
                "options",
                "how many room",
                "room flat"
            ]
        ):

            if topic == "single_flat_options":
                score += 10

        # Grant question
        if "grant" in question_lower:

            if topic in [
                "single_resale_grant",
                "grants"
            ]:
                score += 8

        # CPF question
        if "cpf" in question_lower:

            if topic in [
                "cpf_housing",
                "cpf_usage_limits"
            ]:
                score += 8

        # Resale question
        if "resale" in question_lower:

            if topic in [
                "resale_eligibility",
                "resale_process",
                "single_flat_options",
                "single_resale_grant"
            ]:
                score += 5

        if score > 0:

            scored_results.append({

                "topic": topic,

                "score": score,

                "content": data["content"],

                "source": data["source"],

                "source_url": data["source_url"]
            })

    # ----------------------------------------------------------
    # Highest relevance first
    # ----------------------------------------------------------

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
TOPIC:
{result["topic"]}

INFORMATION:
{result["content"]}

OFFICIAL SOURCE:
{result["source"]}

OFFICIAL URL:
{result["source_url"]}
"""
        )

    return "\n\n---\n\n".join(
        context_parts
    )


# ==========================================================
# RAG - Build Source List
# ==========================================================

def build_source_list(retrieved_results):

    source_lines = []

    seen = set()

    for result in retrieved_results:

        source = result["source"]

        source_url = result["source_url"]

        source_key = (
            source,
            source_url
        )

        if source_key not in seen:

            seen.add(source_key)

            source_lines.append(
                f"- [{source}]({source_url})"
            )

    return "\n".join(source_lines)


# ==========================================================
# AI Response Function
# ==========================================================

def generate_response(question):

    # ======================================================
    # RAG STEP 1 - RETRIEVAL
    # ======================================================

    retrieved_results = retrieve_knowledge(
        question
    )

    if not retrieved_results:

        return """
I could not find sufficiently relevant information in my
HDB/CPF knowledge base for that question.

I currently provide guidance about:

- HDB flat eligibility
- Singles housing options
- HDB flat types
- HFE Letters
- CPF Housing Grants
- CPF usage for housing
- HDB resale flats
- HDB buying processes

Please ask a question related to HDB or CPF housing.
"""


    # ======================================================
    # RAG STEP 2 - AUGMENTATION
    # ======================================================

    retrieved_context = build_context(
        retrieved_results
    )


    system_prompt = f"""
You are GovAssist AI, a Singapore HDB Housing Advisor.

You use Retrieval-Augmented Generation (RAG).

Relevant information has already been retrieved from the
application's curated HDB/CPF knowledge base.

============================================================
RETRIEVED HDB / CPF KNOWLEDGE
============================================================

{retrieved_context}

============================================================

INSTRUCTIONS

1. Answer the user's question primarily using the retrieved
   information above.

2. Do not invent HDB eligibility rules, grant amounts,
   flat types, CPF rules or housing policies that are not
   supported by the retrieved information.

3. If the user provides personal details such as:

   - Age
   - Citizenship
   - Single / married status
   - Household income
   - First-timer status
   - Property ownership

   use those details together with the retrieved information.

4. If the user asks:

   "What options do I have?"
   "What flat can I buy?"
   "What flat size can I buy?"

   clearly explain the relevant options separately.

   Where supported by the retrieved information, organise
   the answer into:

   NEW FLAT OPTIONS
   RESALE FLAT OPTIONS
   POSSIBLE GRANTS
   CPF / FINANCING
   NEXT STEP

5. Clearly distinguish between:

   - New flats
   - Resale flats
   - Standard flats
   - Plus flats
   - Prime flats

   whenever this distinction is relevant.

6. Do not tell the user that they are definitely eligible
   unless the retrieved information supports a definitive
   conclusion.

   Use wording such as:

   "Based on the information provided..."

   "You may generally..."

   "Subject to HDB's eligibility conditions..."

7. Explain that the HFE Letter provides the official
   assessment where relevant.

8. If the retrieved information is insufficient to answer
   part of the question, say so rather than guessing.

9. Only answer questions related to:

   - HDB housing
   - CPF housing
   - HFE Letter
   - Housing grants
   - HDB eligibility
   - Flat types
   - HDB resale flats
   - HDB buying process
   - Singapore public housing

10. If the question is unrelated to HDB or CPF housing,
    explain that this assistant focuses on HDB and CPF
    housing topics.

11. Keep the response educational and easy to understand.

12. Do not create fake official URLs.

13. Important eligibility, grant and financial information
    should be verified through the official HDB or CPF
    websites.
"""


    # ======================================================
    # Session-Aware Personalisation
    # ======================================================

    if "eligibility" in st.session_state:

        system_prompt += f"""

============================================================
USER'S EXISTING ELIGIBILITY ASSESSMENT
============================================================

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

============================================================

Use this information only when relevant to the user's
housing question.

Do not treat the application's advisory eligibility result
as an official HDB determination.
"""


    # ======================================================
    # RAG STEP 3 - GENERATION
    # ======================================================

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


        answer = (
            response
            .choices[0]
            .message
            .content
        )


        # ==================================================
        # Add Official Retrieved References
        # ==================================================

        source_text = build_source_list(
            retrieved_results
        )


        answer += f"""

---

### 📚 Official References Retrieved

{source_text}

*The answer above is generated using information retrieved
from the application's HDB/CPF knowledge base. Please verify
important eligibility, grant and financial information using
the official HDB or CPF websites.*
"""


        return answer


    except Exception as e:

        return (
            "❌ OpenAI Error:\n\n"
            f"{e}"
        )


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.header(
        "💡 Suggested Questions"
    )

    suggested_questions = [

        "I am a single Singapore Citizen aged 36. What HDB flat options do I have?",

        "I am single and 36. What flat size can I buy?",

        "What is an HFE Letter?",

        "What CPF Housing Grants can a single receive?",

        "Can a single buy a 4-room resale flat?",

        "Can a single buy a 5-room resale flat?",

        "Can I use CPF to buy an HDB flat?",

        "How much CPF can I use for housing?",

        "Explain the HDB resale buying process."
    ]


    for question in suggested_questions:

        if st.button(
            question,
            use_container_width=True
        ):

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })


            response = generate_response(
                question
            )


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
        "📚 RAG Status: HDB / CPF Knowledge Retrieval Enabled"
    )


    st.caption(
        "RAG uses a curated local knowledge base "
        "sourced from official HDB and CPF information."
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
    "Ask about HDB flats, grants, CPF or eligibility..."
)


if prompt:

    # ------------------------------------------------------
    # Display user question
    # ------------------------------------------------------

    with st.chat_message(
        "user"
    ):

        st.markdown(
            prompt
        )


    # ------------------------------------------------------
    # Save user message
    # ------------------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })


    # ------------------------------------------------------
    # Generate RAG response
    # ------------------------------------------------------

    answer = generate_response(
        prompt
    )


    # ------------------------------------------------------
    # Display AI response
    # ------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            answer
        )


    # ------------------------------------------------------
    # Save AI response
    # ------------------------------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# ==========================================================
# Official References
# ==========================================================

st.divider()

with st.expander(
    "📚 Official Government References"
):

    st.markdown("""
The knowledge base used by this chatbot is based on publicly
available information from official Singapore government
sources.

### Housing & Development Board (HDB)

- [HDB Homepage](https://www.hdb.gov.sg/homepage)

- [HDB - Singles](https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/singles)

- [HDB - CPF Housing Grant for Singles](https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/singles/cpf-housing-grant)

- [HDB - Standard, Plus and Prime Housing Framework](https://www.hdb.gov.sg/buying-a-flat/bto-sbf-and-open-booking-of-flats/finding-a-new-flat/standard-plus-and-prime-housing-framework)


### Central Provident Fund Board (CPFB)

- [CPF Member Homepage](https://www.cpf.gov.sg/member)

- [CPF - Using Your CPF to Buy a Home](https://www.cpf.gov.sg/member/home-ownership/using-your-cpf-to-buy-a-home)

- [CPF Housing Usage Calculator](https://www.cpf.gov.sg/member/tools-and-services/calculators/cpf-housing-usage)


### Important

This chatbot is an educational prototype.

Eligibility, housing grants, flat availability and financial
rules may change. Users should obtain an HFE Letter and verify
important information using official HDB and CPF services.
""")


# ==========================================================
# Footer
# ==========================================================

st.success(
    "🤖 OpenAI GPT-4.1-mini connected | "
    "📚 Keyword-based RAG enabled | "
    "🏠 HDB / CPF knowledge base enabled"
)

st.caption(
    "GovAssist AI – Singapore HDB Smart Assistant | "
    "Educational Capstone Project"
)
