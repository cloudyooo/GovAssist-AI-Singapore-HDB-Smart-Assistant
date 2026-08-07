import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Applicant Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# Title
# ==========================================================

st.title("📊 Applicant Dashboard")

st.markdown("""
This dashboard summarises the results generated from the
**HDB Resale Eligibility & Grant Advisor**.
""")

st.divider()

# ==========================================================
# Check Session State
# ==========================================================

if "eligibility" not in st.session_state:

    st.warning("""
No assessment found.

Please complete the **Eligibility & Grant Advisor**
before viewing this dashboard.
""")

    st.stop()

# ==========================================================
# Retrieve Session Data
# ==========================================================

eligibility = st.session_state.get(
    "eligibility",
    "Unknown"
)

grant = st.session_state.get(
    "grant",
    0
)

ehg = st.session_state.get(
    "ehg",
    0
)

phg = st.session_state.get(
    "phg",
    0
)

household_income = st.session_state.get(
    "household_income",
    0
)

household_members = st.session_state.get(
    "household_members",
    0
)

applicant_type = st.session_state.get(
    "applicant_type",
    "Unknown"
)

number_of_applicants = st.session_state.get(
    "number_of_applicants",
    1
)

applicant1 = st.session_state.get(
    "applicant1",
    {}
)

applicant2 = st.session_state.get(
    "applicant2",
    None
)

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("Assessment Summary")

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.metric(
        "Eligibility",
        eligibility
    )

with k2:

    st.metric(
        "Estimated Total Grant",
        f"${grant:,}"
    )

with k3:

    st.metric(
        "Household Income",
        f"${household_income:,}"
    )

with k4:

    st.metric(
        "Household Members",
        household_members
    )

st.divider()

# ==========================================================
# Applicant Information
# ==========================================================

st.subheader("Applicant Information")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Applicant 1")

    st.write(
        f"**Age:** {applicant1.get('age','-')}"
    )

    st.write(
        f"**Citizenship:** {applicant1.get('citizenship','-')}"
    )

    st.write(
        f"**First-time Applicant:** {applicant1.get('first_timer','-')}"
    )

    st.write(
        f"**Current Residential Property:** {applicant1.get('housing','-')}"
    )

    st.write(
        f"**Distance to Parents / Child:** {applicant1.get('distance','-')}"
    )

with col2:

    if applicant2:

        st.markdown("### Applicant 2")

        st.write(
            f"**Age:** {applicant2.get('age','-')}"
        )

        st.write(
            f"**Citizenship:** {applicant2.get('citizenship','-')}"
        )

        st.write(
            f"**First-time Applicant:** {applicant2.get('first_timer','-')}"
        )

        st.write(
            f"**Current Residential Property:** {applicant2.get('housing','-')}"
        )

        st.write(
            f"**Distance to Parents / Child:** {applicant2.get('distance','-')}"
        )

    else:

        st.info("Only one applicant.")

        # ==========================================================
# Household Information
# ==========================================================

st.divider()

st.subheader("Household Information")

household_df = pd.DataFrame(
    {
        "Item": [
            "Applicant Type",
            "Number of Applicants",
            "Number of Household Members",
            "Average Gross Monthly Household Income",
            "Overall Eligibility"
        ],
        "Value": [
            applicant_type,
            number_of_applicants,
            household_members,
            f"${household_income:,}",
            eligibility
        ]
    }
)

st.dataframe(
    household_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# Housing Grant Summary
# ==========================================================

st.divider()

st.subheader("Estimated Housing Grant")

grant_df = pd.DataFrame(
    {
        "Grant Type": [
            "Enhanced CPF Housing Grant (EHG)",
            "Proximity Housing Grant (PHG)",
            "Estimated Total Grant"
        ],
        "Amount ($)": [
            ehg,
            phg,
            grant
        ]
    }
)

st.dataframe(
    grant_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# Grant Metrics
# ==========================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Enhanced CPF Housing Grant",
        f"${ehg:,}"
    )

with c2:

    st.metric(
        "Proximity Housing Grant",
        f"${phg:,}"
    )

with c3:

    st.metric(
        "Estimated Total Grant",
        f"${grant:,}"
    )

    # ==========================================================
# Visualisations
# ==========================================================

st.divider()

st.subheader("Housing Grant Breakdown")

fig = px.bar(
    grant_df,
    x="Grant Type",
    y="Amount ($)",
    text="Amount ($)",
    color="Grant Type",
    title="Estimated Housing Grant Breakdown"
)

fig.update_layout(
    height=450,
    showlegend=False,
    xaxis_title="Grant Type",
    yaxis_title="Estimated Amount ($)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# Income vs Grant
# ==========================================================

comparison_df = pd.DataFrame(
    {
        "Category": [
            "Average Household Income",
            "Estimated Total Grant"
        ],
        "Amount": [
            household_income,
            grant
        ]
    }
)

comparison_fig = px.bar(
    comparison_df,
    x="Category",
    y="Amount",
    text="Amount",
    color="Category",
    title="Average Household Income vs Estimated Housing Grant"
)

comparison_fig.update_layout(
    height=450,
    showlegend=False
)

st.plotly_chart(
    comparison_fig,
    use_container_width=True
)

# ==========================================================
# Grant Composition
# ==========================================================

pie_df = pd.DataFrame(
    {
        "Grant": [
            "Enhanced CPF Housing Grant",
            "Proximity Housing Grant"
        ],
        "Amount": [
            ehg,
            phg
        ]
    }
)

if grant > 0:

    pie = px.pie(
        pie_df,
        names="Grant",
        values="Amount",
        hole=0.45,
        title="Composition of Estimated Housing Grant"
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )
else:

    st.info(
        "No housing grant is currently estimated based on the information provided."
    )

    # ==========================================================
# Recommendation
# ==========================================================

st.divider()

st.subheader("Recommended Next Steps")

if "Eligible" in eligibility:

    st.success("""
### Based on your assessment

Your household appears to be **likely eligible** to purchase an HDB resale flat.

Recommended next steps:

1. Apply for an HDB Flat Eligibility (HFE) Letter.
2. Review your CPF Ordinary Account savings.
3. Search for suitable resale flats.
4. Request an HDB valuation.
5. Submit the resale application.
6. Complete the resale transaction.
""")

else:

    st.warning("""
### Your household may not currently satisfy one or more eligibility requirements.

Please review:

- Citizenship requirements
- Minimum age requirements
- Property ownership rules
- Applicant eligibility scheme

Refer to the official HDB website before making any housing decisions.
""")

# ==========================================================
# Assessment Summary
# ==========================================================

st.divider()

st.subheader("Assessment Summary")

summary = f"""
HDB RESALE ELIGIBILITY & GRANT ADVISOR

Overall Eligibility
-------------------
{eligibility}

Applicant Type
--------------
{applicant_type}

Number of Applicants
--------------------
{number_of_applicants}

Number of Household Members
---------------------------
{household_members}

Average Gross Monthly Household Income
--------------------------------------
${household_income:,}

Applicant 1
-----------
Age: {applicant1.get('age','-')}
Citizenship: {applicant1.get('citizenship','-')}
First-time Applicant: {applicant1.get('first_timer','-')}
Current Residential Property: {applicant1.get('housing','-')}
Distance to Parents / Child: {applicant1.get('distance','-')}
"""

if applicant2:

    summary += f"""

Applicant 2
-----------
Age: {applicant2.get('age','-')}
Citizenship: {applicant2.get('citizenship','-')}
First-time Applicant: {applicant2.get('first_timer','-')}
Current Residential Property: {applicant2.get('housing','-')}
Distance to Parents / Child: {applicant2.get('distance','-')}
"""

summary += f"""

Estimated Grants
----------------
Enhanced CPF Housing Grant (EHG): ${ehg:,}
Proximity Housing Grant (PHG): ${phg:,}

Estimated Total Grant
---------------------
${grant:,}
"""

st.text(summary)

# ==========================================================
# Download Report
# ==========================================================

st.download_button(
    label="📄 Download Assessment Report",
    data=summary,
    file_name="HDB_Eligibility_Assessment.txt",
    mime="text/plain"
)

# ==========================================================
# Disclaimer
# ==========================================================

st.divider()

st.info("""
### Disclaimer

This dashboard is generated from the information entered in the **HDB Resale Eligibility & Grant Advisor**.

The assessment is intended for educational purposes only and **does not replace an official HDB Flat Eligibility (HFE) assessment**.

Eligibility rules, CPF Housing Grants and HDB policies may change over time.

Please refer to the official HDB and CPF websites before making any housing decisions.
""")