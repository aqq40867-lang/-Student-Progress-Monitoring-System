"""
testResults.py
------------------------------------------------------------
Purpose:
Retrieve and display all assessment results for a given student
from the SQLite database.

Usage:
Run from menu.ipynb with a database path and student ID.

"""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def fetch_all_results(db_path, student_id):
    """Retrieve all grades for a student and visualise them using a bar chart."""
    
    # 1) Connect to database
    conn = sqlite3.connect(db_path)

    # 2) Get all table names in the database
    tables = pd.read_sql_query(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;",
        conn
    )["name"].tolist()

    results = []
    for t in tables:
        if t not in ["Test_1", "Test_2", "Test_3", "Test_4", "Mock_Test", "Sum_Test"]:
            continue

        df = pd.read_sql_query(
            f"SELECT research_id, Grade FROM {t} WHERE research_id = ?",
            conn,
            params=(student_id,)
        )
        if len(df) > 0:
            results.append({"Assessment": t, "Grade": float(df.loc[0, "Grade"])})
    # 3) Close database connection
    conn.close()

    # 4) Handle case where student has no results
    if not results:
        print("No results found for student:", student_id)
        return
    
    # 6) Display results table
    df_out = pd.DataFrame(results).sort_values("Assessment")
    print(df_out.to_string(index=False))

    # 7) Visualise results
    plt.figure()
    plt.bar(df_out["Assessment"], df_out["Grade"])
    plt.xlabel("Assessment")
    plt.ylabel("Grade")
    plt.title(f"Student {student_id} Performance Across Assessments")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Run this module from menu.ipynb.")