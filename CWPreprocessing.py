"""
CWPreprocessing.py
------------------------------------------------------------
Purpose:
Clean and normalise raw student assessment CSV files and store
the processed results into a SQLite database.

Usage:
Run via menu.ipynb before any analysis or visualisation.

"""
import sqlite3
import pandas as pd


class CWPreprocessor:
    """Preprocess CW CSV files and write cleaned tables into SQLite."""

    def __init__(
        self,
        db_path,
        file_test_1,
        file_test_2,
        file_test_3,
        file_test_4,
        file_mock,
        file_rate,
        file_sum
):
        self.db_path = db_path
        self.file_test_1 = file_test_1
        self.file_test_2 = file_test_2
        self.file_test_3 = file_test_3
        self.file_test_4 = file_test_4
        self.file_mock = file_mock
        self.file_rate = file_rate
        self.file_sum = file_sum

    def read_csv(self, csv_path):
        """Read a CSV file."""
        return pd.read_csv(csv_path)


    def strip_column_names(self, df):
        """Strip spaces in column names to avoid KeyError caused by extra spaces."""
        df.columns = [str(c).strip() for c in df.columns]
        return df

    def apply_rename(self, df, rename_map):
        """Rename columns using a mapping dictionary."""
        df.rename(columns=rename_map, inplace=True)
        return df


    def clean_numeric_columns(self, df, columns):
        """
        Replace '-' with 0, then convert given columns to numeric safely.
        Any non-numeric values become 0.
        """
        df.replace("-", 0, inplace=True)
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df


    def keep_best_attempt(self, df):
        """
        Keep the highest Grade row per research_id.
        Assumes 'research_id' and 'Grade' exist.
        """
        df = df.sort_values("Grade", ascending=False)
        df = df.drop_duplicates(subset=["research_id"], keep="first")
        df = df.sort_index()
        return df


    def remove_redundant_columns(self, df, cols_to_drop):
        """Drop columns only if they exist (prevents KeyError)."""
        existing = [c for c in cols_to_drop if c in df.columns]
        if existing:
            df.drop(columns=existing, inplace=True)
        return df


    def normalise_grade_to_10000(self, df, grade_total):
        """Normalise Grade to 0-10000 scale."""
        df["Grade"] = (df["Grade"] * (10000 / grade_total)).round().astype("Int64")
        return df


    def scale_cols_to_100(self, df, cols):
        """Scale fractional question scores (0-1) to percentage 0-100."""
        existing = [c for c in cols if c in df.columns]
        if existing:
            df[existing] = (df[existing] * 100).round().astype("Int64")
        return df


    def scale_cols_to_10000(self, df, col_to_maxscore):
        """
        Scale fractional question scores (0-1) to 0-10000 using max score.
        Example: if question max score is 500, then multiply by 10000/500.
        """
        for col, max_score in col_to_maxscore.items():
            if col in df.columns:
                df[col] = (df[col] * (10000 / max_score)).round().astype("Int64")
        return df

    def check_required_columns(self, df, required, table_name):
        """Raise a clear error if required columns are missing."""
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise KeyError(
                f"[{table_name}] Missing columns: {missing}. Current columns: {list(df.columns)}"
            )

    def write_table(self, conn, df, table_name):
        """Write DataFrame to SQLite table (replace to avoid rerun errors)."""
        df.to_sql(table_name, conn, if_exists="replace", index=False)

    def preprocess_test_1(self):
        """Preprocess Formative Test 1 data and return cleaned DataFrame."""
        
        df_raw = self.read_csv(self.file_test_1)
        df = df_raw.copy()  
        self.strip_column_names(df)

        rename_map = {
            "research id": "research_id",
            "Started on": "Started_on",
            "Time taken": "Time_taken",
            "Grade/600": "Grade",
            "Q 1 /100": "Q1",
            "Q 2 /100": "Q2",
            "Q 3 /100": "Q3",
            "Q 4 /100": "Q4",
            "Q 5 /100": "Q5",
            "Q 6 /100": "Q6",
        }
        self.apply_rename(df, rename_map)
        self.check_required_columns(df, ["research_id", "Grade"], "Test_1")

        df = self.keep_best_attempt(df)
        df = self.remove_redundant_columns(df, ["State", "Time_taken"])

        cols_numeric = ["Grade", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
        self.clean_numeric_columns(df, cols_numeric)

        self.normalise_grade_to_10000(df, 600)
        self.scale_cols_to_100(df, ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"])
        return df

    def preprocess_test_2(self):
        df = self.read_csv(self.file_test_2)
        self.strip_column_names(df)

        rename_map = {
            "research id": "research_id",
            "Started on": "Started_on",
            "Time taken": "Time_taken",
            "Grade/700": "Grade",
            "Q 1 /100": "Q1",
            "Q 2 /100": "Q2",
            "Q 3 /100": "Q3",
            "Q 4 /200": "Q4",
            "Q 5 /100": "Q5",
            "Q 6 /100": "Q6",
        }
        self.apply_rename(df, rename_map)
        self.check_required_columns(df, ["research_id", "Grade"], "Test_2")

        df = self.keep_best_attempt(df)
        df = self.remove_redundant_columns(df, ["State", "Time_taken"])

        cols_numeric = ["Grade", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
        self.clean_numeric_columns(df, cols_numeric)

        self.normalise_grade_to_10000(df, 700)
        self.scale_cols_to_100(df, ["Q1", "Q2", "Q3", "Q5", "Q6"])
        self.scale_cols_to_10000(df, {"Q4": 200})
        return df

    def preprocess_test_3(self):
        df = self.read_csv(self.file_test_3)
        self.strip_column_names(df)

        rename_map = {
            "research id": "research_id",
            "Started on": "Started_on",
            "Time taken": "Time_taken",
            "Grade/600": "Grade",
            "Q 1 /100": "Q1",
            "Q 2 /100": "Q2",
            "Q 3 /100": "Q3",
            "Q 4 /100": "Q4",
            "Q 5 /100": "Q5",
            "Q 6 /100": "Q6",
        }
        self.apply_rename(df, rename_map)
        self.check_required_columns(df, ["research_id", "Grade"], "Test_3")

        df = self.keep_best_attempt(df)
        df = self.remove_redundant_columns(df, ["State", "Time_taken"])

        cols_numeric = ["Grade", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
        self.clean_numeric_columns(df, cols_numeric)

        self.normalise_grade_to_10000(df, 600)
        self.scale_cols_to_100(df, ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"])
        return df

    def preprocess_test_4(self):
        df = self.read_csv(self.file_test_4)
        self.strip_column_names(df)

        rename_map = {
            "research id": "research_id",
            "Started on": "Started_on",
            "Time taken": "Time_taken",
            "Grade/1000": "Grade",
            "Q 1 /500": "Q1",
            "Q 2 /500": "Q2",
        }
        self.apply_rename(df, rename_map)
        self.check_required_columns(df, ["research_id", "Grade"], "Test_4")

        df = self.keep_best_attempt(df)
        df = self.remove_redundant_columns(df, ["State", "Time_taken"])

        cols_numeric = ["Grade", "Q1", "Q2"]
        self.clean_numeric_columns(df, cols_numeric)

        self.normalise_grade_to_10000(df, 1000)
        self.scale_cols_to_10000(df, {"Q1": 500, "Q2": 500})
        return df

    def preprocess_mock_test(self):
        df = self.read_csv(self.file_mock)
        self.strip_column_names(df)

        rename_map = {
            "research id": "research_id",
            "Started on": "Started_on",
            "Time taken": "Time_taken",
            "Grade/10000": "Grade",
            "Q 1 /500": "Q1",
            "Q 2 /300": "Q2",
            "Q 3 /600": "Q3",
            "Q 4 /700": "Q4",
            "Q 5 /500": "Q5",
            "Q 6 /400": "Q6",
            "Q 7 /1000": "Q7",
            "Q 8 /2000": "Q8",
            "Q 9 /2000": "Q9",
            "Q 10 /2000": "Q10",
        }
        self.apply_rename(df, rename_map)
        self.check_required_columns(df, ["research_id", "Grade"], "Mock_Test")

        df = self.keep_best_attempt(df)
        df = self.remove_redundant_columns(df, ["State", "Time_taken"])

        cols_numeric = ["Grade", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]
        self.clean_numeric_columns(df, cols_numeric)

        df["Grade"] = df["Grade"].round().astype("Int64")

        self.scale_cols_to_10000(df, {"Q1": 500, "Q5": 500})
        self.scale_cols_to_10000(df, {"Q8": 2000, "Q9": 2000, "Q10": 2000})
        self.scale_cols_to_10000(df, {"Q2": 300, "Q3": 600, "Q4": 700, "Q6": 400, "Q7": 1000})
        return df

    def preprocess_student_rate(self):
        df = self.read_csv(self.file_rate)
        self.strip_column_names(df)
        df.fillna(0, inplace=True)
        return df

    def preprocess_sum_test(self):
        df = self.read_csv(self.file_sum)
        self.strip_column_names(df)

        rename_map = {
            "research id": "research_id",
            "Started on": "Started_on",
            "Time taken": "Time_taken",
            "Grade/10000": "Grade",
            "Q 1 /500": "Q1",
            "Q 2 /300": "Q2",
            "Q 3 /600": "Q3",
            "Q 4 /700": "Q4",
            "Q 5 /400": "Q5",
            "Q 6 /500": "Q6",
            "Q 7 /1500": "Q7",
            "Q 8 /1500": "Q8",
            "Q 9 /1500": "Q9",
            "Q 10 /1000": "Q10",
            "Q 11 /400": "Q11",
            "Q 12 /500": "Q12",
            "Q 13 /600": "Q13",
        }
        self.apply_rename(df, rename_map)
        self.check_required_columns(df, ["research_id", "Grade"], "Sum_Test")

        df = self.keep_best_attempt(df)
        df = self.remove_redundant_columns(df, ["State", "Time_taken"])

        cols_numeric = ["Grade", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9",
                        "Q10", "Q11", "Q12", "Q13"]
        self.clean_numeric_columns(df, cols_numeric)

        df["Grade"] = df["Grade"].round().astype("Int64")

        self.scale_cols_to_10000(df, {
            "Q1": 500, "Q2": 300, "Q3": 600, "Q4": 700, "Q5": 400,
            "Q6": 500, "Q7": 1500, "Q8": 1500, "Q9": 1500, "Q10": 1000,
            "Q11": 400, "Q12": 500, "Q13": 600
        })
        return df


    def run(self):
        """Run preprocessing and write all tables into SQLite database."""
        conn = sqlite3.connect(self.db_path)

        self.write_table(conn, self.preprocess_test_1(), "Test_1")
        self.write_table(conn, self.preprocess_test_2(), "Test_2")
        self.write_table(conn, self.preprocess_test_3(), "Test_3")
        self.write_table(conn, self.preprocess_test_4(), "Test_4")
        self.write_table(conn, self.preprocess_mock_test(), "Mock_Test")
        self.write_table(conn, self.preprocess_student_rate(), "Student_Rate")
        self.write_table(conn, self.preprocess_sum_test(), "Sum_Test")

        conn.close()
        print("Database written successfully:", self.db_path)


def main():
    pre = CWPreprocessor()
    pre.run()


if __name__ == "__main__":
    print("Run preprocessing from menu.ipynb")