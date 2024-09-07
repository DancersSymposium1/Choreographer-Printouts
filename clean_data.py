'''
Author: Sophia Holland (sophiaho@andrew.cmu.edu or the.sophia.holland@gmail.com)
Created: August 2024

This script should allow us to detect any potential errors people made when filling out their dance pref forms
as quickly as possible. 
Errors should be clearly printed so that we can confirm the necessary changes with the people involved.
'''

import pandas as pd
import numpy as np

DANCER_FILE = 'test_sheet.csv'


print("\n\n##################### checking data #######################\n")
df = pd.read_csv(DANCER_FILE,delimiter=",")

# Headings are based on Google Forms automatic headings; might change year by year
df.rename({'Timestamp':'timestamp',
           'Email Address':'email',
           'First Name':'first',
           'Last Name':'last',
           'Audition Number':'id',
           'What pronouns do you use? (collecting to pass along to your choreographers once you are placed in a piece)':'pronouns',
           'How many dances would you like to be in?':'num_dances'},
           axis=1,inplace=True)


# Check 1: no unusual blanks
no_blanks_subset = df[["email","first","last",
                       "id","num_dances"]]
has_nan = no_blanks_subset.isna().any().any()

if(has_nan):
  
  print("\n\n====Error: missing necessary data====\n\n")
  non_problem_rows = no_blanks_subset.dropna(inplace=False)

  ind = 0
  for row in non_problem_rows.index:
    if ind!=row:
      print("\n---Row ",ind," ---\n",no_blanks_subset.iloc[ind],"\n")
      ind = row
    ind+=1

# Check 2: no repeat emails or IDs
if(df["email"].duplicated().any()):
  print("\n====Error: duplicate email====\n")
  print(df[df["id"].duplicated()])

if(df["id"].duplicated().any()):
  print("\n====Error: duplicate dancer audition number====\n")
  print(df[df["id"].duplicated()])


# Check 3: dance preferences are valid, including:
#    - num_dances ranked <= num of dances preffed
#    - no duplicate rankings
#    - no skipped rankings
#    - choreographers preffed their own pieces

num_dances_total = len(df.columns)-7

for row in df.index:
  row_data = df.loc[row]
  num_preffed = list((row_data[7:]).isna()).count(False)
  if(row_data.num_dances > num_preffed):
    print("\n====Error: Not enough dances preffed====\n")
    print(row_data,"\n")

  correct_rankings = [i for i in range(1,num_preffed+1)]
  user_rankings = list((row_data[7:]))
  if(set(correct_rankings) ^ set(user_rankings) != set()):
    print("\n====Error! Duplicate or invalid rankings====\n")
    print(row_data,"\n")
