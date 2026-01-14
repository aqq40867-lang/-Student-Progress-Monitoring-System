"""
underperformingStudent.py
------------------------------------------------------------
Purpose:
Identify underperforming students based on summative and
formative assessment results and visualise their performance.

Usage:
Run from menu.ipynb with a database path.

"""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def find_underperforming_students(db_path):
    conn = sqlite3.connect(db_path)

    # 1) Summative table
    df_sum = pd.read_sql_query("SELECT research_id, Grade FROM Sum_Test", conn)
    df_sum = df_sum.dropna(subset=["research_id", "Grade"]).copy()

    # 2) Formative tables (include Mock_Test as stated)
    formative_tables = ["Test_1", "Test_2", "Test_3", "Test_4", "Mock_Test"]
    formative_results = []

    for table in formative_tables:
        df = pd.read_sql_query(f"SELECT research_id, Grade FROM {table}", conn)
        df["Test"] = table
        formative_results.append(df)

    df_formative = pd.concat(formative_results, ignore_index=True)
    df_formative = df_formative.dropna(subset=["research_id", "Grade"]).copy()

    # 3) Grade > 0 counts as an attempt
    df_attempts = df_formative[df_formative["Grade"] > 0].groupby("research_id").size().reset_index(name="Attempts")

    # 4) Lowest formative grade
    df_attended = df_formative[df_formative["Grade"] > 0].copy()
    df_low = df_attended.sort_values(["research_id", "Grade", "Test"]).groupby("research_id").first().reset_index()
    df_low = df_low.rename(columns={"Grade": "Lowest_Formative_Grade", "Test": "Lowest_Formative_Test"})

    # 5) Underperforming definition
    sum_average = df_sum["Grade"].mean()
    df_under = df_sum[df_sum["Grade"] < sum_average].copy()
    df_under = df_under.sort_values(by="Grade", ascending=True)
    df_under = df_under.rename(columns={"Grade": "Summative_Grade"})

    # 6) Merge: add attempts + lowest formative info
    df_result = pd.merge(df_under, df_attempts, on="research_id", how="left")
    df_result = pd.merge(df_result, df_low, on="research_id", how="left")

    # 7) Filter inactive students
    df_result["Attempts"] = df_result["Attempts"].fillna(0).astype(int)
    df_result = df_result[df_result["Attempts"] >= 3].copy()

    if df_result.empty:
        print("No underperforming students found (after inactive filter).")
        conn.close()
        return

    # 8) Display results
    cols = ["research_id", "Summative_Grade", "Lowest_Formative_Grade", "Lowest_Formative_Test", "Attempts"]
    print(df_result[cols].to_string(index=False))

    # 9) Visualisation
    plt.figure(figsize=(14, 6))

    x = list(range(len(df_result)))
    summ = df_result["Summative_Grade"]
    lowf = df_result["Lowest_Formative_Grade"].fillna(0)

    plt.bar([i - 0.2 for i in x], summ, width=0.4, label="Summative Grade")
    plt.bar([i + 0.2 for i in x], lowf, width=0.4, label="Lowest Formative Grade", alpha=0.7)

    labels = df_result["research_id"].astype(str).tolist()
    step = max(1, len(labels) // 10)
    plt.xticks(x[::step], labels[::step], rotation=45, ha="right")

    plt.xlabel("Student ID")
    plt.ylabel("Grade")
    plt.title("Underperforming Students: Summative vs Lowest Formative Grade")
    plt.legend()
    plt.tight_layout()
    plt.show()

    conn.close()
if __name__ == "__main__":
    print("Run this module from menu.ipynb.")