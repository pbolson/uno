"""
This script generates synthetic data using the Faker package to develop and test a SQL report creation query.
It takes no input. It outputs the 3 tables of the assumed data model as pickled pandas dataframes and as CSVs:
1. ../output/members.pkl                 ../output/members.csv
2. ../output/eligibility_checks.pkl      ../output/eligibility_checks.csv
3. ../output/enrollments.pkl             ../output/enrollments.pkl

The assumption for the data model is that the there is a 1-to-1 mapping from member to eligibility_checks to
enrollments.  Where the size of members > eligibility_checks > enrollments.
"""

import pandas as pd
from faker import Faker
from datetime import timedelta
import joblib
import numpy as np

# Set seeds for reproducibility
Faker.seed(1)
np.random.seed(1)

# Set number of members to reflect total amount in example in question
nbr_members = 3640

fake = Faker('en_US')

# Generate the member table.
members = []
for i in range(nbr_members):
    member_id = i + 1
    member_dt = fake.date_between(start_date='-4y', end_date='today')
    eligibility_check_dt = member_dt + timedelta(days=30)
    enrollment_dt = eligibility_check_dt + timedelta(days=45)
    name = fake.name()
    first_name = name.split()[0]
    last_name = name.split()[1]
    email = fake.ascii_email()
    phone_nbr = fake.phone_number()
    address = fake.address().split('\n')
    # Null out bad addresses returned by Faker
    try:
        street = address[0]
        city = address[1].split(',')[0]
        state = address[1].split(',')[1].split()[0]
        zip_code = str(address[1].split(',')[1].split()[1])
    except:
        street = ''
        city = ''
        state = ''
        zip_code = ''

    members.append([member_id, member_dt, eligibility_check_dt, enrollment_dt, first_name, last_name, email, phone_nbr, street, city, state, zip_code])


members = pd.DataFrame(members, columns=['member_id', 'member_dt', 'eligibility_check_dt', 'enrollment_dt', 'first_name', 'last_name', 'email', 'phone_nbr', 'street', 'city', 'state', 'zip_code'])

# Randomly null out last names to reflect example data
members['last_name'] = members['last_name'].mask(np.random.random(members['last_name'].shape) < .01)

# Create eligibility_checks and enrollments tables by sampling from members table based on ratios from example table.
eligibility_checks = members[['member_id', 'eligibility_check_dt', 'enrollment_dt']].sample(frac=.8, random_state=1)
enrollments = eligibility_checks[['member_id', 'enrollment_dt']].sample(frac=.5, random_state=1)

# Finalize tales by dropping unneeded columns
members = members.drop(columns=['eligibility_check_dt', 'enrollment_dt'])
eligibility_checks = eligibility_checks.drop(columns=['enrollment_dt'])

# Save tables as pickled dataframes and CSVs
joblib.dump(members, '../output/members.pkl')
joblib.dump(eligibility_checks, '../output/eligibility_checks.pkl')
joblib.dump(enrollments, '../output/enrollments.pkl')

members.to_csv('../output/members.csv', index=False)
eligibility_checks.to_csv('../output/eligibility_checks.csv', index=False)
enrollments.to_csv('../output/enrollments.csv', index=False)






