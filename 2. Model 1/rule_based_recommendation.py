
import streamlit as st

# -----------------------------
# LIC Policy Recommendation App (Detailed Rule-Based)
# -----------------------------
st.set_page_config(page_title="LIC Policy Recommender", layout="centered")
st.title("\U0001F4B8 LIC Policy Recommendation (Rule-Based)")
st.write("Answer the following questions to get the best suitable LIC plan for you.")

# -----------------------------
# User Inputs
# -----------------------------
age_group = st.selectbox("\U0001F466 What is your Age Group?", ["18-25", "26-35", "36-45", "46-60"])
income_group = st.selectbox("\U0001F4B0 What is your Annual Income Group?", ["<3L", "3L-6L", "6L-10L", "10L+"])
policy_term = st.selectbox("\u23F1\ufe0f What is your Preferred Policy Duration?", ["Short Term", "Long Term"])
priority = st.radio("\U0001F6E0\ufe0f What is your Priority?", ["Savings + Protection", "Protection only"])

# -----------------------------
# Rule-based Recommendation
# -----------------------------
def recommend_policy(age, income, term, priority):
    if priority == "Protection only":
        if term == "Short Term":
            return "Tech Term"
        else:
            return "Jeevan Umang"

    # Now handle Savings + Protection
    if priority == "Savings + Protection":
        if age == "18-25":
            if income == "<3L":
                return "Jeevan Lakshya" if term == "Short Term" else "Jeevan Umang"
            elif income == "3L-6L":
                return "Endowment Plan" if term == "Short Term" else "Jeevan Lakshya"
            elif income == "6L-10L":
                return "Endowment Plan" if term == "Short Term" else "Jeevan Lakshya"
            elif income == "10L+":
                return "Jeevan Lakshya" if term == "Short Term" else "Jeevan Umang"

        elif age == "26-35":
            if income == "<3L":
                return "Endowment Plan" if term == "Short Term" else "Jeevan Umang"
            elif income == "3L-6L":
                return "Jeevan Lakshya" if term == "Short Term" else "Jeevan Umang"
            elif income == "6L-10L":
                return "Endowment Plan" if term == "Short Term" else "Jeevan Lakshya"
            elif income == "10L+":
                return "Jeevan Lakshya" if term == "Short Term" else "Jeevan Umang"

        elif age == "36-45":
            if income == "<3L":
                return "Endowment Plan" if term == "Short Term" else "Jeevan Umang"
            elif income == "3L-6L":
                return "Jeevan Lakshya" if term == "Short Term" else "Jeevan Umang"
            elif income == "6L-10L":
                return "Endowment Plan" if term == "Short Term" else "Jeevan Lakshya"
            elif income == "10L+":
                return "Endowment Plan" if term == "Short Term" else "Jeevan Lakshya"

        elif age == "46-60":
            if income == "<3L":
                return "Endowment Plan" if term == "Short Term" else "Jeevan Umang"
            elif income == "3L-6L":
                return "Jeevan Lakshya" if term == "Short Term" else "Jeevan Umang"
            elif income == "6L-10L":
                return "Endowment Plan" if term == "Short Term" else "Jeevan Lakshya"
            elif income == "10L+":
                return "Endowment Plan" if term == "Short Term" else "Jeevan Umang"

    return "No suitable policy found."

# -----------------------------
# Show Recommendation
# -----------------------------
if st.button("Recommend Policy"):
    recommended = recommend_policy(age_group, income_group, policy_term, priority)
    st.subheader("\U0001F4DD Recommended LIC Policy:")
    st.success(recommended)

    st.markdown("---")
    st.subheader("\U0001F4C3 Basic Policy Info:")
    if recommended == "Jeevan Umang":
        st.markdown("- Whole life plan with survival benefit\n- Premium payment term less than policy term\n- Good for long-term savings and yearly income")
    elif recommended == "Jeevan Lakshya":
        st.markdown("- Endowment-based savings plan\n- Good for children's education or long-term goals\n- Annual bonus applicable")
    elif recommended == "Endowment Plan":
        st.markdown("- Savings + Life Cover\n- One-time maturity benefit\n- Suitable for medium risk appetite")
    elif recommended == "Tech Term":
        st.markdown("- Pure term insurance plan\n- Highest life cover at lowest premium\n- No maturity benefit")