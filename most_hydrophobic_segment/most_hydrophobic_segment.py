import sys
import csv

def hydrophobic_value(sequence, hydrophobicity_scale_map):
    result = 0.0
    for letter in sequence:
        result += hydrophobicity_scale_map[letter]
    return result

def maximum_hydrophobic_sequence(sequence, hydrophobicity_scale_map, minimum_window_size = 9):
    max_seq = ""
    max_value = -10000.0

    if (len(sequence)<=minimum_window_size):
        return max_seq,max_value

    for window_size in range(minimum_window_size, len(sequence)+1):
        for window_start in range(0,len(sequence)+1-window_size):
            window_end = window_start + window_size
            seq = sequence[window_start:window_end]
            value = hydrophobic_value(seq, hydrophobicity_scale_map)
            if (value > max_value):
                max_seq = seq
                max_value = value

    return max_seq,max_value


def check_input():
    if (len(sys.argv) < 3):
        print "I take two csv files as parameters. One should contain the hydrophobicity table, the second one - a list of sequences"
        print "Example: python most_hydrophobic_segment.py RLM165-min1peptides-allfilters-GO.csv output.csv"
        exit(0)

def read_hydrophobicity_table(fname):
    # read sample from csv file to detect its dialect
    try:
        f = open(fname, "rt")
        header = f.readline()
    except:
        print "Cannot open input file"
        print fname
        exit(0)
    f.close()

    # Read in data and count the number of peptides for each accession #
    csvDialectSniffer = csv.Sniffer()
    dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')

    f = open(fname, "rt")
    csvReader = csv.DictReader(f, dialect=dialect)

    fields = csvReader.fieldnames
    # Check the input data has valid info
    if (not "AA" in fields
        or not "HValue" in fields):
        print "The input data is incomplete"
        print "Missing one of the crucial columns"
        print "Make sure your "+fname+" file has AA and HValue columns"
        exit(0)

    data = {}

    for row in csvReader:
        data[row["AA"]] = float(row["HValue"])

    f.close()

    return data

def find_maximum_hydrophobic_sequence(fname, hydrophobicity_scale_map):
    # read sample from csv file to detect its dialect
    try:
        fin = open(fname, "rt")
        header = fin.readline()
    except:
        print "Cannot open input file"
        print fname
        exit(0)
    fin.close()

    # Read in data and count the number of peptides for each accession #
    csvDialectSniffer = csv.Sniffer()
    dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')

    fin = open(fname, "rt")
    csvReader = csv.DictReader(fin, dialect=dialect)

    fields = csvReader.fieldnames
    # Check the input data has valid info
    if (not "Accession" in fields
        or not "Sequence" in fields):
        print "The input data is incomplete"
        print "Missing one of the crucial columns"
        print "Make sure your "+fname+" file has Accession and Sequence columns"
        exit(0)

    # Output the data for accession number that are present in both files
    fields = ("Accession","MaxSequence","MaxValue")
    csvWriter = csv.DictWriter(open("output.csv",'w'), dialect=dialect, fieldnames=fields, delimiter='\t', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
    csvWriter.writerow(dict((fn,fn) for fn in fields))

    for row in csvReader:
        Accession = row["Accession"]
        Sequence = row["Sequence"]
        seq,val = maximum_hydrophobic_sequence(Sequence, hydrophobicity_scale_map)
        row_to_write = {}
        row_to_write["Accession"] = Accession
        row_to_write["MaxSequence"] = seq
        row_to_write["MaxValue"] = val
        csvWriter.writerow( row_to_write )

    fin.close()

def Main():
    check_input()

    hydrophobicity_table_filename = sys.argv[1]
    sequence_data_filename = sys.argv[2]

    hydrophobicity_table = read_hydrophobicity_table(hydrophobicity_table_filename)
    find_maximum_hydrophobic_sequence(sequence_data_filename, hydrophobicity_table)

if __name__ == "__main__":
    Main()