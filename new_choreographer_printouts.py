import pandas as pd

'''
Use Case:
    Run this program 3 times:
        - after makeup auditions
        - during 10am auditions
        - during 1pm auditions
    Copy-and-paste outputs into each choreographer's "Dancers who preffed you" Google Doc
    They need this info before auditions can continue

PREF_FILE formatting: **subject to change each semester, but this was Spring 2025 formatting
    Follows the columns from the "Dancer Prefs" Google Form
    Timestamp,Email Address,Audition Number,First Name,Last Name,How many pieces would you like to be in?, Rankings [1 thru 19, inclusive]

    Because the Rankings are dropdown options with the list of available pieces, all entries in the Rankings columns are strings matching the "pieces" list below

Requirements:
    - On the form, choreographers must pref their own piece first (for the matching code later down the line). These prefs have been removed from the spreadsheet before downloading the csv.
        FUTURE NOTE: make this program able to run assuming that choreographers preffed their own pieces first. Could use "choreographers" list and just check membership. Shift all indices down by 1.
    
    - Audition numbers must be unique
        Can't have two different people with the same audition number. This happens at least once per semester.
    
    - Number of pieces must be <4 for non-choreographers
        Available options limit responses to 1-4 desired pieces, inclusive. However, 4 is only an option for choreographers
        FUTURE NOTE: add this check into the choreographer check anyway
    
    - Must not have gaps between rankings
        e.g. can't have Rankings [1] = "piece1", Rankings [2] = "", Rankings [3] = "piece3" <-- no ranking for piece 2
        Shouldn't matter for this code, but better to catch this error now before final matching
    
    - Must not repeat Rankings
        e.g. can't have Rankings [1] = "piece1", Rankings [2] = "piece1"
        Same stipulation as above
    
    - Number of Rankings must be >= Number of desired pieces
        e.g. If you want to be in 3 pieces, you can't just rank one piece
        Same stipulation as above
'''

# UPDATE VARIABLES HERE
NUM_PIECES = 19 #not including tap
PREF_FILE = 'prefs_2pm.csv'
pieces = ["A - Alex & Alisa (Beginner)", "B - Karina (Beginner)", "C - Jillian (Beginner)", "E - Caroline", "F - Nina & Lily",
          "G - Sydney","H - Tyler & Kina", "I - Alex", "J - Suzy", "K - Juliann", "L - Tiffany", "M - Vera",
          "N - Stanley", "O - Zachary", "P - Paige", "Q - Camille", "R - Jianing & Lydia", "S - Helen", "T -  Valia"]
# BELOW SHOULD NOT NEED TO BE UPDATED

df = pd.read_csv(PREF_FILE)

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
        
    # put a * by the numbers of people who ranked that particular piece as their #1 choice
    for first_placer in first_placers:
        print(f'{first_placer}*')
    for other in interested:
        print(other)