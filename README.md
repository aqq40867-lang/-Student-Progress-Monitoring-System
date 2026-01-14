# -Student-Progress-Monitoring-System

## Overview
This project implements a **student performance management and analysis system**
using **Python, Pandas, SQLite, and Matplotlib**.

It processes raw assessment CSV files, stores cleaned and normalised results
in a relational database, and provides analytical tools to evaluate both
individual student performance and cohort-level trends.

The system follows a modular, database-driven design and is suitable for
educational data analysis and reporting.

---

## Key Features

- **Data Preprocessing Pipeline**
  - Cleans raw CSV assessment data
  - Handles missing and invalid values safely
  - Keeps the best attempt per student
  - Normalises grades to a unified 0–10000 scale

- **Relational Database Storage**
  - SQLite database with one table per assessment
  - Consistent schema across all tables
  - Enables efficient querying and reuse across analyses

- **Student Performance Analysis**
  - Absolute performance by question
  - Relative performance compared to cohort average
  - Cross-assessment grade comparison

- **Underperforming Student Detection**
  - Identifies students performing below the cohort average
  - Considers both summative performance and formative engagement
  - Highlights weakest formative assessment per student

- **Visual Analytics**
  - Clear bar-chart visualisations using Matplotlib
  - Supports both individual and cohort-level insights

---

## Project Structure

├── menu.ipynb # Main entry point (user interface)
├── CWPreprocessing.py # Data cleaning & database creation
├── studentPerformance.py # Per-student performance analysis
├── testResults.py # Cross-assessment result summary
├── underperformingStudent.py # Underperforming student detection
├── CWDatabase.db # SQLite database (generated locally)
└── data/ # Raw assessment CSV files

---

## Technologies Used

- **Python 3**
- **Pandas** – data manipulation and cleaning
- **SQLite3** – relational data storage
- **Matplotlib** – data visualisation
- **Jupyter Notebook** – interactive execution

---

## How to Run

1. Place all raw assessment CSV files in the `data/` directory  
2. Open `menu.ipynb`
3. Run the preprocessing step to generate the SQLite database
4. Use the menu options to:
   - View a student’s results across assessments
   - Analyse question-level performance
   - Identify underperforming students

---

## Design Principles

- Modular and single-responsibility Python modules
- Defensive data cleaning to prevent runtime errors
- Database-first architecture for scalable analysis
- Reproducible results with consistent grading normalisation

---

## Notes

- The SQLite database is generated locally from raw CSV files  
- Raw data files are not included in the repository  
