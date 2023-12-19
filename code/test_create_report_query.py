""""
This script uses pandasql (SQLite for pandas dataframes) to verify that create_report.sql is giving the desired
results.  It takes the three tables produced in synthesize_data.py as input, runs create_report.sql, and then prints
the results and outputs the results to ../output/results.csv
"""
import pandas as pd
from pandasql import sqldf
import joblib

members = joblib.load('../output/members.pkl')
eligibility_checks = joblib.load('../output/eligibility_checks.pkl')
enrollments = joblib.load('../output/enrollments.pkl')

with open('create_report.sql') as f:
    query = f.read()

results = sqldf(query)

results.to_csv('../output/results.csv', index=False)
