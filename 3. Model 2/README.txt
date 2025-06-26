
📝 Life Insurance Recommendation System - Final Submission

📁 Folder Structure:
---------------------
Insurance_Recommender_Project/
├── Tkinter_policy_recommender.py        ← Final GUI App (.py)
├── filtered_rules.csv                             ← Rules file used by the GUI
├── Tkinter_policy_recommender.ipynb ← Full project notebook
├── Demographic_Combinations.csv              ← Demographic combination dataset
├── README.txt                                      ← Project instructions

📌 Model Overview:
---------------------
This Model uses the Apriori algorithm to recommend life insurance benefit terms
based on user demographics and premium terms. It is designed for real-world usability,
handling all combinations of realistic customer inputs through a synthetic dataset.

👤 User Inputs:
- Premium Term
- Gender
- Income Group
- Occupation
- Marital Status
- Location
- Children Status

🔎 Output:
- Top 3 recommended Benefit Terms
- Confidence and Lift of each rule
- Explanation of each recommendation
- Stored logs of user input for review


▶️ How to Run the App:
-----------------------
1. If using Python:
   - Run `insurance_recommender_gui_scrollable.py` with Python 3.10+ installed.
   - Ensure `filtered_rules.csv` is in the same folder.

2. If using a notebook:
   - Open `OJT_Project_Final_With_GUI_From_Notebook.ipynb` in Jupyter
   - Run all cells to generate the rules and launch the GUI.

📦 Notes:
---------
- The GUI is built using `tkinter` and styled with `ttkbootstrap` ("superhero" theme).
- Rules are generated using `mlxtend`'s Apriori algorithm.
- Logs are saved automatically in the `logs/` folder on each recommendation.

👩‍💻 Developer:
---------------
Name: RAJSHRI DURVAS PATIL  
Project: LIC Smart Life Insurance Policy Recommender  
Internship / OJT Submission

🎉 All the best!
