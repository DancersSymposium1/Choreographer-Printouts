"""
This script was created for use by Dancers' Symposium at Carnegie Mellon University.

This script reads a CSV file containing piece rankings for dancers
and prints out files for each piece with the audition number and gender
of each interested dancer.

Please change the DANCER_FILE variable to the name of the file to be read
and also modify HEADERS and ENDING_COLUMNS if the csv file format changes.

The headers expected on the CSV file are in the HEADERS array, followed by a column
per dance piece, followed by the ENDING_COLUMNS array.

Printouts will be printed to the audition_printouts folder. Please clear out this
folder or rename any previous folders before running this script.

This script will also print out any lines of the csv file that have an integrity
error in it (duplicate dance names, duplicate or missing audition numbers,
duplicate rankings, skipped rankings).

NOTE: Any dancer rows that have errors will NOT be included in the printouts. You should
fix these errors and run the script again if you'd like them to be included.

Contact Karin for any questions!

author: Karin Tsai (ktsai11@gmail.com)
created: August 2014

---

RUNNING INSTRUCTIONS:

- Open Terminal
- Navigate to the choreographer_printouts folder, where this file is
  (for example, "cd /Users/ktsai11/Desktop/DS/choreographer_printouts")
- Delete any files in the audition_printouts folder ("rm audition_printouts/*")
- Change the DANCER_FILE variable below to whatever file you want to read. Make
  sure that file is also in the choreographer_printouts folder.
- Type and execute "python print_audition_sheets.py" in Terminal

"""

DANCER_FILE = 'DANCER_RANKINGS_2014.csv'
PRINTOUT_PATH = 'audition_printouts/'

HEADERS = ['date', 'first', 'last', 'id', 'gender', 'num_pieces']
ENDING_COLUMNS = ['agreement']

if __name__ == '__main__':
    dancer_ranking_file = open(DANCER_FILE, 'rU')

    # create map of pieces to dancers
    dancer_map = {}
    dancer_ids = {}
    for i, line in enumerate(dancer_ranking_file):
        if i == 0: # this is the header line
            # parse piece names from header
            columns = line.strip().split(',')
            DANCE_NAMES = columns[len(HEADERS):-len(ENDING_COLUMNS)]
            duplicates = set([d for d in DANCE_NAMES if DANCE_NAMES.count(d) > 1])
            if duplicates:
                print 'Duplicate dance names: %s' % ', '.join(list(duplicates))
                exit()
            continue

        columns = line.strip().split(',')
        _id = columns[HEADERS.index('id')]
        gender = columns[HEADERS.index('gender')]

        # integrity checks
        if not _id:
            print 'No audition number: %s' % line
            continue

        _id = int(_id)

        if _id in dancer_ids:
            print 'Duplicate audition number (%d):\n%s%s' % (_id, line, dancer_ids[_id])
            continue

        rankings = set()
        dance_indices = []
        preferences = columns[len(HEADERS):-len(ENDING_COLUMNS)]
        error = False
        for dance_index, ranking in enumerate(preferences):
            if ranking:
                ranking = int(ranking)
                if ranking in rankings:
                    print 'Duplicate ranking (%d): %s' % (ranking, line)
                    error = True
                rankings.add(ranking)
                dance_indices.append(dance_index)

        for ranking in range(1, len(rankings)):
            if ranking not in rankings:
                print 'Skipped ranking (%d): %s' % (ranking, line)
                error = True

        # add to dancer map if checks pass
        if not error:
            for dance_index in dance_indices:
                dancer_map.setdefault(DANCE_NAMES[dance_index], []).append((_id, gender))
            dancer_ids[_id] = line

    dancer_ranking_file.close()

    # print files
    for dance_name, dancers in dancer_map.iteritems():
        f = open(PRINTOUT_PATH + '%s.txt' % dance_name, 'w+')
        print >> f, '********************'
        print >> f, dance_name
        print >> f, '********************'
        sorted_dancers = sorted(dancers, key=lambda (d, _): d)
        for (dancer_id, gender) in sorted_dancers:
            print >> f, dancer_id, gender
        f.close()
