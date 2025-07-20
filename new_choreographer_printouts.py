import pandas as pd

NUM_PIECES = 19 #not including tap
PREF_FILE = 'prefs_2pm.csv'

df = pd.read_csv(PREF_FILE)
pieces = ["A - Alex & Alisa (Beginner)", "B - Karina (Beginner)", "C - Jillian (Beginner)", "E - Caroline", "F - Nina & Lily",
          "G - Sydney","H - Tyler & Kina", "I - Alex", "J - Suzy", "K - Juliann", "L - Tiffany", "M - Vera",
          "N - Stanley", "O - Zachary", "P - Paige", "Q - Camille", "R - Jianing & Lydia", "S - Helen", "T -  Valia"]

df = df.rename(columns={"Timestamp":"t",
                   "Email Address":"e",
                   "Audition Number":"id",
                   "First Name":"fn",
                   "Last Name":"ln",
                   "How many pieces would you like to be in?":"np"})

for piece in pieces:
    print("-----",piece,"-----")

    first_placers = df[df["Rankings [1]"]==piece]["id"].tolist()

    interested = []
    for i in range(2,NUM_PIECES+1):
        interested+=df[df[f'Rankings [{i}]']==piece]["id"].tolist()

    interested = set(interested)
        
    for first_placer in first_placers:
        print(f'{first_placer}*')
    for other in interested:
        print(other)