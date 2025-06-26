
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import pandas as pd
import datetime
import os

# Load rules
rules = pd.read_csv("filtered_rules.csv")

def extract_premium(antecedent_str):
    items = antecedent_str.strip("{}").replace("'", "").split(", ")
    for item in items:
        if item.startswith("Premium_"):
            return item.replace("Premium_", "")
    return None

rules['Premium_Term'] = rules['antecedents'].apply(extract_premium)

def recommendation_gui_scrollable():
    root = tk.Tk()
    style = Style("superhero")
    root.title("PolicyMatch - Smart Life Insurance Recommender")
    root.geometry("900x650")
    root.resizable(True, True)

    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ttk.Label(scroll_frame, text="🛡️ PolicyMatch: Smart Life Insurance Recommender",
              font=("Segoe UI", 15, "bold")).pack(pady=10)

    fields = {
        "Premium Term (years)": [5, 7, 8, 10, 15, 20, 25, 30, 40],
        "Gender": ["Male", "Female"],
        "Income Group": ["<3L", "3–6L", "6–10L", "10L+"],
        "Occupation": ["Farmer", "Clerk", "Business Owner", "Teacher", "Self-employed", "Engineer"],
        "Marital Status": ["Single", "Married", "Widowed"],
        "Location": ["Urban", "Semi-urban", "Rural"],
        "Children": ["Yes", "No"]
    }
    inputs = {}

    for label, options in fields.items():
        ttk.Label(scroll_frame, text=label + ":", font=("Segoe UI", 11)).pack(anchor="w", pady=2)
        cb = ttk.Combobox(scroll_frame, values=options)
        cb.pack(fill="x", pady=2)
        inputs[label] = cb

    use_lift = tk.BooleanVar()
    ttk.Checkbutton(scroll_frame, text="Use Lift instead of Confidence", variable=use_lift).pack(pady=5)

    output_text = tk.Text(scroll_frame, height=12, width=110, font=("Consolas", 10))
    output_text.pack(pady=10)

    def get_recommendations():
        output_text.delete("1.0", tk.END)
        filters = []

        premium_val = inputs["Premium Term (years)"].get()
        if not premium_val:
            output_text.insert(tk.END, "⚠️ Please select a Premium Term.\n")
            return
        filters.append(f"Premium_{premium_val}")

        for label, cb in inputs.items():
            if label != "Premium Term (years)" and cb.get():
                filters.append(f"{label.replace(' ', '_').replace('(', '').replace(')', '')}_{cb.get()}")

        matched_rules = rules[rules['antecedents'].apply(lambda x: any(f in x for f in filters))]
        sort_metric = 'lift' if use_lift.get() else 'confidence'
        matched_rules = matched_rules.sort_values(by=sort_metric, ascending=False)

        os.makedirs("logs", exist_ok=True)
        with open("logs/recommendation_log.csv", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp},{'|'.join(filters)}\n")

        if matched_rules.empty:
            output_text.insert(tk.END, "❌ No matching recommendations found.\n")
        else:
            output_text.insert(tk.END, f"✅ Top 3 Recommendations (sorted by {sort_metric}):\n\n")
            for i, (_, row) in enumerate(matched_rules.head(3).iterrows(), 1):
                rule_text = (
                    f"{i}. If {set(eval(row['antecedents']))} → Then {set(eval(row['consequents']))}\n"
                    f"   Confidence: {row['confidence']:.2f}, Lift: {row['lift']:.2f}\n"
                    f"   Explanation: Based on similar customer profiles, this benefit is preferred.\n\n"
                )
                output_text.insert(tk.END, rule_text)

    ttk.Button(scroll_frame, text="Get Recommendations", command=get_recommendations).pack(pady=15)

    root.mainloop()

recommendation_gui_scrollable()
