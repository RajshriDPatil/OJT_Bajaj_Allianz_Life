
# 📊 Insurance Benefit Term Recommendation System – OJT Project

This repository contains the complete work done during my internship at **Bajaj Allianz Life Insurance**, focused on building a rule-based recommendation system using both Python and R.

---

## 🧭 Objective

To develop a system that recommends the most suitable **Benefit Term** or **Policy Term** based on customer demographic and financial profiles, using synthetic datasets modeled on real-life insurance behavior.

---

## 📁 Repository Structure

| Folder Name        | Description |
|--------------------|-------------|
| `1. Data & EDA/`    | Synthetic dataset generation (`.ipynb`) and Exploratory Data Analysis |
| `2. Model 1/`       | Manual rule-based model using if-else logic (Python Streamlit app + LIC dataset) |
| `3. Model 2/`       | Apriori-based model with Tkinter GUI (Python) |
| `4. Model 3/`       | Apriori-based model with Streamlit interface (Python) |
| `5. Model 4/`       | R Shiny implementation of Apriori + fallback logic |
| `report/`           | Final OJT report (`OJT Report.docx`) |
| `references/`       | Academic papers and supporting notes |

---

## ⚙️ Technologies Used

- **Python**: `pandas`, `mlxtend`, `streamlit`, `seaborn`, `tkinter`, `faker`
- **R**: `shiny`, `arules`, `dplyr`
- **Data Mining**: Association Rule Mining (Apriori Algorithm)
- **Visualization**: Matplotlib, Seaborn, Shiny plots

---

## 🧪 How to Run

### 🔹 Python Models (Model 1, 2, 3 & 4)
1. Install required packages:
   ```bash
   pip install pandas mlxtend streamlit seaborn
   ```

2. Run Streamlit model (Model 1):
   ```bash
   streamlit run rule_based_recommendation.py
   ```

3. Run Tkinter GUI (Model 2):
   ```bash
   python Tkinter_policy_recommender.py
   ```
4. Run Tkinter GUI (Model 3):
   ```bash
   streamlit run Streamlit_policy_recommendation.py
      ```

5 🔹 R Shiny App (Model 4)
1. Open `app.R` in RStudio
2. Click **Run App**

---

## 📌 Key Highlights

- 4 models built using different interfaces: Streamlit, Tkinter, and Shiny
- Uses Apriori algorithm for pattern discovery
- Fully synthetic data based on real insurance product logic
- Interactive visualizations and recommendations
- Reusable structure and extendable framework

---

## 📎 Credits & Acknowledgements

- Internship at **Bajaj Allianz Life Insurance**
- Mentored by: *Mr. Kulkarni Mukund Gopal – B06*
- Academic guidance: Department of Statistics, SPPU
- Association Rule concepts: [GeeksforGeeks - Association Rule Mining](https://www.geeksforgeeks.org/association-rule/)
- Research inspiration from included PDFs (`ref 1.pdf`, `ref 2.pdf`)

---

## 📄 License

This repository is for academic and learning purposes only. All datasets are synthetic and do not reflect real customer information.
