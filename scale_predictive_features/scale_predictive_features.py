import csv
import nltk
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

features_table = {}
labels_table = []
accession_numbers = []

def _load_data():
    filename = "signal_peptide_features_table.csv" 
    # read sample from csv file to detect its dialect
    try: 
        f = open(filename, "rt")
        header = f.readline()
    except:
        print "Cannot open input file", filename
        exit(0)

    f.close()

    csvDialectSniffer = csv.Sniffer()
    dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')

    f = open(filename, "rt")
    csvReader = csv.DictReader(f, dialect=dialect)
    fields = csvReader.fieldnames
    for row in csvReader:
        accession_numbers.append(row["accession"])
        labels_table.append((row["accession"],row["sensitivity label"]))
        features_table[row["accession"]] = {}
        for field in fields:
            if ("min" in field) or ("max" in field):
                features_table[row["accession"]][field] = float(row[field])
        pass
    f.close()

def get_label(accession):
    if ((accession, "sensitive") in labels_table):
        return "sensitive"
    return "not sensitive"

def get_features(accession):
    #ToDo: potentially introduce cross features here
    return (features_table[accession], get_label(accession))

def train_naive_bayes():
    featuresets = []
    for a in accession_numbers:
        featuresets.append(get_features(a))
     
    classifier = nltk.NaiveBayesClassifier.train(featuresets)
    return classifier

def Main():
    _load_data()
    c = train_naive_bayes()
    c.show_most_informative_features(150)


if __name__ == "__main__":
    Main()
