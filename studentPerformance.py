"""
studentPerformance.py
------------------------------------------------------------
Purpose:
Analyse a student's absolute and relative performance for a
selected assessment and visualise the results.

Usage:
Run from menu.ipynb with a database path, student ID and test name.

"""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect to database and load the selected assessment table
def student_performance(db_path, student_id, test_name):
    """Analyse and visualise a student's performance for a given test."""

    conn = sqlite3.connect(db_path)

    df_test = pd.read_sql_query(
        f"SELECT * FROM {test_name}",
        conn
    )

    # 2. Locate the target student record and validate student_id
    df_student = df_test[df_test['research_id'] == student_id]

    if df_student.empty:
        print("Student ID not found in this test.")
        conn.close()
        return
    
    # 3. Detect question columns (Q1, Q2, ...) and compute absolute/relative scores
    question_cols = [col for col in df_test.columns if col.startswith('Q')]

    absolute_scores = df_student[question_cols].iloc[0]
    average_scores = df_test[question_cols].mean()
    relative_scores = absolute_scores - average_scores

    # 4. Visualise absolute performance
    plt.figure()
    absolute_scores.plot(kind='bar')
    plt.xlabel('Question')
    plt.ylabel('Score (%)')
    plt.title(f'Absolute Performance – Student {student_id} ({test_name})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 5. Visualise relative performance
    plt.figure()
    relative_scores.plot(kind='bar')
    plt.axhline(0)
    plt.xlabel('Question')
    plt.ylabel('Score Difference')
    plt.title(f'Relative Performance – Student {student_id} vs Average ({test_name})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 6. Close database connection
    conn.close()

if __name__ == "__main__":
    print("Run this module from menu.ipynb.")