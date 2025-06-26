
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

st.set_page_config(page_title="Insurance Benefit Term Recommender", layout="centered")
st.title("📊 Insurance Benefit Term Recommendation using Apriori")
st.warning("If you have large data (like 1.5 lakh rows), please clean or sample it first to avoid memory errors.")

# File upload
uploaded_file = st.file_uploader("📁 Upload your insurance dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Data uploaded successfully!")

    # Clean input data to reduce unique values
    for col in ['Premium_Term', 'Gender', 'Income', 'Occupation', 'Marital_Status', 'Location', 'Children',
                'Benefit_Term']:
        df[col] = df[col].astype(str).str.strip().str.lower()
        df[col] = df[col].fillna("unknown")

     #Optional: Sampling for quick testing (remove for full data)
    if len(df) > 25000:
        df = df.sample(n=90000, random_state=42)

    # Show first few rows
    st.subheader("🔍 Sample of Uploaded Data")
    st.dataframe(df.head())

    # standardize column names to avoid key errors
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Check required columns
    required_cols = ["premium_term", "gender", "income", "occupation", "marital_status", "location", "children",
                     "benefit_term"]

    if not all(col in df.columns for col in required_cols):
        st.error(f"❌ Required columns missing in data. Please ensure your CSV file includes: {', '.join(required_cols)}")
    if True:
        for col in required_cols:
            df[col] = df[col].astype(str).str.strip().str.lower().fillna("unknown")

    #eda section
            # 👇 Optional EDA Section (button-based)
        if st.button("📊 Perform EDA"):
           st.header("🔍 Exploratory Data Analysis")

           try:
                fig1, ax1 = plt.subplots()
                df['premium_term'].value_counts().sort_index().plot(kind='bar', ax=ax1, color='skyblue')
                ax1.set_title("Premium Term Distribution")
                st.pyplot(fig1)
                top_premium = df['premium_term'].value_counts().idxmax()
                st.markdown(f"📌 Most common premium term: **{top_premium} years**")

                fig2, ax2 = plt.subplots()
                df['benefit_term'].value_counts().sort_index().plot(kind='bar', ax=ax2, color='salmon')
                ax2.set_title("Benefit Term Distribution")
                st.pyplot(fig2)
                top_benefit = df['benefit_term'].value_counts().idxmax()
                st.markdown(f"📌 Most chosen benefit term: **{top_benefit} years**")

                fig3, ax3 = plt.subplots()
                df['income'].value_counts().plot(kind='bar', ax=ax3, color='orange')
                ax3.set_title("Income Group Distribution")
                st.pyplot(fig3)
                top_income = df['income'].value_counts().idxmax()
                st.markdown(f"📌 Most common income group: **{top_income}**")

                fig4, ax4 = plt.subplots()
                df['gender'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax4)
                ax4.set_title("Gender Split")
                ax4.set_ylabel("")
                st.pyplot(fig4)

                gender_counts = df['gender'].value_counts()
                if gender_counts.get('male', 0) > gender_counts.get('female', 0):
                    st.markdown("📌 Majority of policyholders are **male**.")
                elif gender_counts.get('female', 0) > gender_counts.get('male', 0):
                    st.markdown("📌 Majority of policyholders are **female**.")
                else:
                    st.markdown("📌 Gender distribution is **balanced**.")

                st.subheader("Premium Term vs Benefit Term Table")
                st.dataframe(pd.crosstab(df['premium_term'], df['benefit_term']))

           except Exception as e:
                st.error(f"⚠️ EDA error: {e}")

    # labeling
    if True:
        # Convert to string labels
        df['premium_label'] = 'premium_' + df['premium_term'].astype(str)
        df['income_label'] = 'income_' + df['income']
        df['benefit_label'] = 'benefit_' + df['benefit_term'].astype(str)
        df['gender_label'] = 'gender_' + df['gender']
        df['occupation_label'] = 'occupation_' + df['occupation']
        df['marital_label'] = 'marital_' + df['marital_status']

        # Use fewer features to reduce memory load
        labeled_cols = ['premium_label', 'income_label', 'benefit_label', 'gender_label', 'occupation_label',
                        'marital_label']
        transactions = df[labeled_cols].values.tolist()

        # Encode transactions
        te = TransactionEncoder()
        try:
            te_ary = te.fit(transactions).transform(transactions)
            df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

            # Apriori Algorithm
            frequent_itemsets = apriori(df_encoded, min_support=0.0001, use_colnames=True)
            rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)

            # Filter rules: Premium → Benefit
            benefit_rules = rules[
                rules['antecedents'].apply(lambda x: any(i.startswith("premium_") for i in x)) &
                rules['consequents'].apply(lambda x: any(i.startswith("benefit_") for i in x))
                ]

            # Recommendation Section
            st.subheader("🎯 Get Benefit Term Recommendation")

            # User Inputs
            age = st.selectbox("Select Age Group", ["18-25", "26-35", "36-45", "46-60"])
            gender = st.selectbox("Select Gender", ["Male", "Female"])
            income = st.selectbox("Select Income Group", ["<3l", "3-6l", "6-10l", "10l+"])
            occupation = st.selectbox("Select Occupation",
                                      ["teacher", "engineer", "farmer", "clerk", "business owner", "self-employed"])
            marital = st.selectbox("Select Marital Status", ["single", "married", "widowed"])
            premium_term = st.selectbox("Select Premium Term", sorted(df['premium_term'].unique()))

            # selected_premium = st.selectbox("Select Premium Term", sorted(df['premium_term'].astype(str).unique()))
            # Format inputs as set
            input_set = {
                f"premium_{premium_term}",
                f"income_{income}",
                f"gender_{gender.lower()}",
                f"occupation_{occupation.lower()}",
                f"marital_{marital.lower()}"
            }

            if not benefit_rules.empty:
                matched = benefit_rules[
                    benefit_rules['antecedents'].apply(lambda x: input_set.issubset(x))
                ].sort_values(by='confidence', ascending=False)

                if not matched.empty:
                    st.success("✅ Top Recommended Benefit Terms:")
                    for i, row in matched.head(3).iterrows():
                        term = list(row['consequents'])[0].replace("benefit_", "")
                        # confidence = row.get('confidence', None)
                        # if confidence is not None:
                        # st.markdown(f"- {term} years (Confidence: {confidence:.2f})")
                        # else:
                        st.markdown(f"- {term} years")
                else:
                    st.warning("No matching rules found for selected premium term.")
            else:
                st.warning("No benefit rules were generated. Try increasing dataset size or lowering thresholds.")

        except MemoryError:
            st.error("⚠️ Dataset is too large for memory. Try reducing size or number of features.")
