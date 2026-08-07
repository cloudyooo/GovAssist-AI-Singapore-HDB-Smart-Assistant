import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="HDB Resale Eligibility & Grant Advisor",
    page_icon="🏠",
    layout="wide"
)

# ==========================================================
# Title
# ==========================================================

st.title("🏠 HDB Resale Eligibility & Grant Advisor")

st.markdown("""
This tool provides an **advisory assessment** of your likely eligibility to purchase an **HDB resale flat** and estimates the **CPF Housing Grants** you may qualify for.

The assessment is based on publicly available HDB and CPF information and is intended for educational purposes only.

> **Note:** This is **not** an official HDB Flat Eligibility (HFE) assessment.
""")

st.divider()

# ==========================================================
# Applicant Type
# ==========================================================

st.header("Applicant Type")

applicant_type = st.selectbox(
    "Select Applicant Type",
    [
        "Single",
        "Married Couple",
        "Family",
        "Fiancé / Fiancée"
    ]
)

# ==========================================================
# Number of Applicants
# ==========================================================

if applicant_type == "Single":

    number_of_applicants = 1

    st.info(
        "Single applicants can only have one applicant."
    )

else:

    number_of_applicants = st.radio(
        "Number of Applicants",
        [1, 2],
        horizontal=True
    )

st.divider()

# ==========================================================
# Applicant Information
# ==========================================================

st.header("Applicant Information")

# ==========================================================
# Applicant 1
# ==========================================================

st.subheader("Applicant 1")

left1, right1 = st.columns(2)

with left1:

    age1 = st.number_input(
        "Age",
        min_value=21,
        max_value=100,
        value=30,
        key="age1"
    )

    citizenship1 = st.selectbox(
        "Citizenship",
        [
            "Singapore Citizen",
            "Singapore PR"
        ],
        key="citizenship1"
    )

with right1:

    first_timer1 = st.radio(
        "First-time Applicant",
        [
            "Yes",
            "No"
        ],
        key="first_timer1"
    )

    housing1 = st.selectbox(
        "Current Residential Property",
        [
            "No Residential Property",
            "Own HDB Flat",
            "Own Private Residential Property"
        ],
        key="housing1"
    )

    distance1 = st.selectbox(
        "Distance from Parents / Child",
        [
            "Within 4 km",
            "More than 4 km"
        ],
        key="distance1"
    )

# ==========================================================
# Applicant 2
# ==========================================================

if number_of_applicants == 2:

    st.divider()

    st.subheader("Applicant 2")

    left2, right2 = st.columns(2)

    with left2:

        age2 = st.number_input(
            "Age",
            min_value=21,
            max_value=100,
            value=30,
            key="age2"
        )

        citizenship2 = st.selectbox(
            "Citizenship",
            [
                "Singapore Citizen",
                "Singapore PR"
            ],
            key="citizenship2"
        )

    with right2:

        first_timer2 = st.radio(
            "First-time Applicant",
            [
                "Yes",
                "No"
            ],
            key="first_timer2"
        )

        housing2 = st.selectbox(
            "Current Residential Property",
            [
                "No Residential Property",
                "Own HDB Flat",
                "Own Private Residential Property"
            ],
            key="housing2"
        )

        distance2 = st.selectbox(
            "Distance from Parents / Child",
            [
                "Within 4 km",
                "More than 4 km"
            ],
            key="distance2"
        )

else:

    age2 = None
    citizenship2 = None
    first_timer2 = None
    housing2 = None
    distance2 = None

st.divider()

# ==========================================================
# Household Information
# ==========================================================

st.header("Household Information")

left, right = st.columns(2)

with left:

    household_income = st.number_input(
        "Average Gross Monthly Household Income ($)",
        min_value=0,
        max_value=50000,
        value=5000,
        step=100,
        help="Combined average gross monthly household income of all applicants."
    )

with right:

    household_members = st.number_input(
        "Number of Household Members",
        min_value=1,
        max_value=20,
        value=2,
        step=1
    )

st.divider()

# ==========================================================
# Build Applicant List
# ==========================================================

applicants = [
    {
        "name": "Applicant 1",
        "age": age1,
        "citizenship": citizenship1,
        "first_timer": first_timer1,
        "housing": housing1,
        "distance": distance1,
    }
]

if number_of_applicants == 2:
    applicants.append(
        {
            "name": "Applicant 2",
            "age": age2,
            "citizenship": citizenship2,
            "first_timer": first_timer2,
            "housing": housing2,
            "distance": distance2,
        }
    )

# ==========================================================
# Eligibility Assessment
# ==========================================================

eligible = True
reasons = []

# ----------------------------------------------------------
# Citizenship Requirement
# ----------------------------------------------------------

citizen_found = any(
    applicant["citizenship"] == "Singapore Citizen"
    for applicant in applicants
)

if not citizen_found:
    eligible = False
    reasons.append(
        "At least one applicant must be a Singapore Citizen."
    )

# ----------------------------------------------------------
# Age Requirement
# ----------------------------------------------------------

if applicant_type == "Single":

    if age1 < 35:
        eligible = False
        reasons.append(
            "Single applicants must be at least 35 years old."
        )

else:

    for applicant in applicants:

        if applicant["age"] < 21:
            eligible = False
            reasons.append(
                f'{applicant["name"]} must be at least 21 years old.'
            )

# ----------------------------------------------------------
# Residential Property Ownership
# ----------------------------------------------------------

for applicant in applicants:

    if applicant["housing"] == "Own Private Residential Property":

        eligible = False

        reasons.append(
            f'{applicant["name"]} currently owns a private residential property.'
        )

# ----------------------------------------------------------
# HDB Ownership Advisory
# ----------------------------------------------------------

for applicant in applicants:

    if applicant["housing"] == "Own HDB Flat":

        reasons.append(
            f'{applicant["name"]} currently owns an HDB flat. Existing HDB ownership may affect eligibility and disposal requirements.'
        )

# ----------------------------------------------------------
# First-timer Assessment
# ----------------------------------------------------------

all_first_timer = all(
    applicant["first_timer"] == "Yes"
    for applicant in applicants
)

# ==========================================================
# Enhanced CPF Housing Grant (Advisory)
# ==========================================================

ehg = 0

if eligible and all_first_timer:

    if household_income <= 1500:
        ehg = 80000

    elif household_income <= 2500:
        ehg = 70000

    elif household_income <= 3500:
        ehg = 60000

    elif household_income <= 4500:
        ehg = 50000

    elif household_income <= 5500:
        ehg = 40000

    elif household_income <= 6500:
        ehg = 30000

    elif household_income <= 7500:
        ehg = 20000

    elif household_income <= 8500:
        ehg = 10000

# ==========================================================
# Proximity Housing Grant (Advisory)
# ==========================================================

phg = 0

near_parent = any(
    applicant["distance"] == "Within 4 km"
    for applicant in applicants
)

if near_parent:

    if applicant_type == "Single":
        phg = 10000
    else:
        phg = 20000

total_grant = ehg + phg

# ==========================================================
# Check Eligibility
# ==========================================================

if st.button(
    "🔍 Check My Eligibility",
    use_container_width=True,
    key="check_eligibility"
):

    st.divider()

    # =====================================================
    # Overall Result
    # =====================================================

    if eligible:

        st.success(
            "🎉 Based on the information provided, your household is likely eligible to purchase an HDB resale flat."
        )

    else:

        st.error(
            "⚠ Your household may not meet one or more eligibility requirements."
        )

    # =====================================================
    # Eligibility Checklist
    # =====================================================

    st.subheader("Eligibility Checklist")

    checklist = []

    checklist.append((
        "At least one Singapore Citizen",
        citizen_found
    ))

    if applicant_type == "Single":

        age_ok = age1 >= 35

    else:

        age_ok = all(
            applicant["age"] >= 21
            for applicant in applicants
        )

    checklist.append((
        "Minimum age requirement",
        age_ok
    ))

    no_private_property = all(
        applicant["housing"] != "Own Private Residential Property"
        for applicant in applicants
    )

    checklist.append((
        "No applicant owns private residential property",
        no_private_property
    ))

    checklist.append((
        "All applicants are first-timers",
        all_first_timer
    ))

    for item, status in checklist:

        if status:
            st.success(f"✅ {item}")
        else:
            st.error(f"❌ {item}")

    # =====================================================
    # Reasons
    # =====================================================

    if reasons:

        st.divider()

        st.subheader("Assessment Notes")

        for reason in reasons:
            st.write(f"• {reason}")

    st.divider()

    # =====================================================
    # Recommended Flat Types (Advisory)
    # =====================================================

    st.subheader("Recommended HDB Resale Flat Types")

    if applicant_type == "Single":

        recommended = [
            "2-Room Flexi",
            "3-Room",
            "4-Room"
        ]

    else:

        if household_members <= 2:

            recommended = [
                "3-Room",
                "4-Room"
            ]

        elif household_members <= 4:

            recommended = [
                "4-Room",
                "5-Room"
            ]

        else:

            recommended = [
                "5-Room",
                "Executive Apartment / Executive Maisonette (Resale)"
            ]

    st.info(
        "These are suggested resale flat sizes based on your household size. "
        "They are recommendations only and are not HDB eligibility restrictions."
    )

    flat_df = pd.DataFrame({
        "Recommended Flat Types": recommended
    })

    st.table(flat_df)

    st.divider()

    # =====================================================
    # KPI Cards
    # =====================================================

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:

        st.metric(
            "Eligibility",
            "Likely Eligible" if eligible else "Likely Not Eligible"
        )

    with kpi2:

        st.metric(
            "Estimated Total Housing Grant",
            f"${total_grant:,}"
        )

    with kpi3:

        st.metric(
            "Average Household Income",
            f"${household_income:,}"
        )

    st.divider()

    # =====================================================
    # Grant Breakdown
    # =====================================================

    st.subheader("Estimated Housing Grant Breakdown")

    grant_df = pd.DataFrame({

        "Grant": [
            "Enhanced CPF Housing Grant",
            "Proximity Housing Grant"
        ],

        "Amount": [
            ehg,
            phg
        ]

    })

    st.dataframe(
        grant_df,
        use_container_width=True,
        hide_index=True
    )

        # =====================================================
    # Grant Breakdown Chart
    # =====================================================

    fig = px.bar(
        grant_df,
        x="Grant",
        y="Amount",
        text="Amount",
        title="Estimated Housing Grant Breakdown"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Grant Type",
        yaxis_title="Grant Amount ($)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # Income vs Estimated Grant
    # =====================================================

    comparison_df = pd.DataFrame({
        "Category": [
            "Average Household Income",
            "Estimated Housing Grant"
        ],
        "Amount": [
            household_income,
            total_grant
        ]
    })

    comparison_fig = px.pie(
        comparison_df,
        names="Category",
        values="Amount",
        hole=0.45,
        title="Income Compared with Estimated Housing Grant"
    )

    st.plotly_chart(
        comparison_fig,
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # Recommended Next Steps
    # =====================================================

    st.subheader("Recommended Next Steps")

    if eligible:

        st.success("""
1. Apply for an **HDB Flat Eligibility (HFE) Letter**.

2. Confirm your CPF Housing Grant eligibility.

3. Search for suitable HDB resale flats.

4. Request a valuation from HDB.

5. Submit the resale application.

6. Complete the resale transaction.
""")

    else:

        st.warning("""
Please review the assessment notes above.

Consider:

- Reviewing HDB eligibility requirements.
- Reviewing ownership of any residential property.
- Reviewing citizenship and age requirements.
- Applying for an HFE assessment through HDB for an official determination.
""")

    st.divider()

    # =====================================================
    # Assessment Summary
    # =====================================================

    st.subheader("Assessment Summary")

    summary = f"""
Applicant Type: {applicant_type}

Number of Applicants: {number_of_applicants}

Applicant 1
-----------
Age: {age1}
Citizenship: {citizenship1}
First-time Applicant: {first_timer1}
Current Residential Property: {housing1}
Distance from Parents / Child: {distance1}
"""

    if number_of_applicants == 2:

        summary += f"""

Applicant 2
-----------
Age: {age2}
Citizenship: {citizenship2}
First-time Applicant: {first_timer2}
Current Residential Property: {housing2}
Distance from Parents / Child: {distance2}
"""

    summary += f"""

Household Information
---------------------
Average Gross Monthly Household Income: ${household_income:,}

Number of Household Members: {household_members}

Estimated Enhanced CPF Housing Grant: ${ehg:,}

Estimated Proximity Housing Grant: ${phg:,}

Estimated Total Housing Grant: ${total_grant:,}

Overall Assessment:
{"Likely Eligible" if eligible else "Likely Not Eligible"}
"""

    st.text(summary)

    st.download_button(
        label="📄 Download Assessment Report",
        data=summary,
        file_name="HDB_Eligibility_Report.txt",
        mime="text/plain"
    )

        # =====================================================
    # Save Results to Session State
    # =====================================================

    st.session_state["eligibility"] = (
        "Likely Eligible" if eligible else "Likely Not Eligible"
    )

    st.session_state["grant"] = total_grant
    st.session_state["ehg"] = ehg
    st.session_state["phg"] = phg

    st.session_state["household_income"] = household_income
    st.session_state["household_members"] = household_members

    st.session_state["applicant_type"] = applicant_type
    st.session_state["number_of_applicants"] = number_of_applicants

    st.session_state["applicant1"] = {
        "age": age1,
        "citizenship": citizenship1,
        "first_timer": first_timer1,
        "housing": housing1,
        "distance": distance1
    }

    if number_of_applicants == 2:

        st.session_state["applicant2"] = {
            "age": age2,
            "citizenship": citizenship2,
            "first_timer": first_timer2,
            "housing": housing2,
            "distance": distance2
        }

    else:

        st.session_state["applicant2"] = None

    # =====================================================
    # Disclaimer
    # =====================================================

    st.divider()

    st.warning("""
### Disclaimer

This advisory tool is intended for educational purposes only.

The results are **not an official HDB Flat Eligibility (HFE) assessment** and should not be relied upon as a final determination of eligibility.

Eligibility requirements, housing grants, income ceilings, property ownership rules, and resale policies are subject to prevailing HDB and CPF regulations.

Please verify your eligibility and grant entitlement through the official HDB HFE application before making any housing decisions.
""")

    # ==========================================================
# Housing Grant Estimation (Advisory)
# ==========================================================

ehg = 0
phg = 0

# ----------------------------------------------------------
# Enhanced CPF Housing Grant (EHG)
# Advisory only
# ----------------------------------------------------------

if eligible and all_first_timer:

    # Families / Joint Applicants
    if applicant_type != "Single":

        if household_income <= 1500:
            ehg = 80000
        elif household_income <= 2500:
            ehg = 70000
        elif household_income <= 3500:
            ehg = 60000
        elif household_income <= 4500:
            ehg = 50000
        elif household_income <= 5500:
            ehg = 40000
        elif household_income <= 6500:
            ehg = 30000
        elif household_income <= 7500:
            ehg = 20000
        elif household_income <= 8500:
            ehg = 10000
        else:
            ehg = 0

    # Singles
    else:

        if household_income <= 1500:
            ehg = 40000
        elif household_income <= 2500:
            ehg = 35000
        elif household_income <= 3500:
            ehg = 30000
        elif household_income <= 4500:
            ehg = 25000
        elif household_income <= 5500:
            ehg = 20000
        elif household_income <= 6500:
            ehg = 15000
        elif household_income <= 7500:
            ehg = 10000
        else:
            ehg = 0

# ----------------------------------------------------------
# Proximity Housing Grant (PHG)
# ----------------------------------------------------------

near_parent = any(
    applicant["distance"] == "Within 4 km"
    for applicant in applicants
)

if near_parent:

    if applicant_type == "Single":
        phg = 10000
    else:
        phg = 20000

# ----------------------------------------------------------
# Total Estimated Grant
# ----------------------------------------------------------

total_grant = ehg + phg