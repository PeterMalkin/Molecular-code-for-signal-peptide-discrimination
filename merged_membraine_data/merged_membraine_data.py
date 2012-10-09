import sys
import re
import csv


def main():

    # Populate lists of accession numbers
    Mitochondrial = loadAccessionNumbersList("Mitochondrial.csv")
    multiTM = loadAccessionNumbersList("multiTM.csv")
    signal_peptide = loadAccessionNumbersList("signal_peptide.csv")
    typeIII = loadAccessionNumbersList("typeIII.csv")
    typeII = loadAccessionNumbersList("typeII.csv")

    experiment1 = loadExperimentData("Experiment_1_normalized_ratios.csv")
    experiment2 = loadExperimentData("Experiment_2_normalized_ratios.csv")
    experiment3 = loadExperimentData("Experiment_3_normalized_ratios.csv")
    
    Accessions = listUniqueAccessions(experiment1, experiment2, experiment3)
    if (Accessions == None):
        print "Experiment files contain no data, or the format is wrong. I need: Accession, Description, Avg Norm Ratio"
        exit(0)

    Merged_result = {}
    for acc in Accessions:
        merged_row={}
        merged_row["Accession"]=acc
        
        if (acc in experiment1):
            merged_row["Description"]=experiment1[acc]["Description"]
            merged_row["Experiment 1"]=experiment1[acc]["Norm Avg Ratio"]

        if (acc in experiment2):
            merged_row["Description"]=experiment2[acc]["Description"]
            merged_row["Experiment 2"]=experiment2[acc]["Norm Avg Ratio"]

        if (acc in experiment3):
            merged_row["Description"]=experiment3[acc]["Description"]
            merged_row["Experiment 3"]=experiment3[acc]["Norm Avg Ratio"]
            
        if (acc in Mitochondrial):
            merged_row["Mitochondrial?"]="1"            
        if (acc in multiTM):
            merged_row["Multi TM?"]="1"
        if (acc in signal_peptide):
            merged_row["Signal Peptide?"]="1"
        if (acc in typeIII):
            merged_row["Type III?"]="1"
        if (acc in typeII):
            merged_row["Type II?"]="1"

        Merged_result[acc]=merged_row
            
    # Write data out
    dialect = sniffDialect("Experiment_3_normalized_ratios.csv")
    merged_fields = [ "Accession", "Description", "Experiment 1", "Experiment 2", "Experiment 3", "Mitochondrial?", "Signal Peptide?", "Type II?", "Type III?", "Multi TM?" ]
    csvWriter = csv.DictWriter(open("merged_membraine_data.csv","w"), dialect=dialect, fieldnames=merged_fields)
    csvWriter.writerow(dict((fn,fn) for fn in merged_fields))
    
    for key in Merged_result:
        csvWriter.writerow(Merged_result[key])

def listUniqueAccessions(experiment1, experiment2, experiment3):
    Accessions = []
    for row in experiment1:
        if (row not in Accessions):
            Accessions.append(row)
    for row in experiment2:
        if (row not in Accessions):
            Accessions.append(row)
    for row in experiment3:
        if (row not in Accessions):
            Accessions.append(row)
    return Accessions
    
def loadExperimentData(filename):

    result = {}
    dialect = sniffDialect(filename)

    try:
        f = open(filename, "r")
        csvReader = csv.DictReader(f, dialect=dialect)
        fields = csvReader.fieldnames
        accessionNumberFieldName = fields[0]
    except:
        print "Could not read data from file "+filename
        f.close()
        return result

    for row in csvReader:
        if ( len(str(row[accessionNumberFieldName])) <= 0 ):
            continue
        result[row[accessionNumberFieldName]] = row
        
    f.close()
    return result        
        
def loadAccessionNumbersList(filename):
    result = []
    dialect = sniffDialect(filename)
    f = open(filename, "r")
    csvReader = csv.DictReader(f, dialect=dialect)
    fields = csvReader.fieldnames
    accessionNumberFieldName = fields[0]
    for row in csvReader:
        result.append(row[accessionNumberFieldName])
    f.close()
    return result

def sniffDialect(filename):
    try:
        f = open(filename, "r")
    except:
        print "Cannot find a file "+filename
        return None
    
    header = f.readline()
    f.close()
    csvDialectSniffer = csv.Sniffer()
    dialect = csvDialectSniffer.sniff(header)
    return dialect

main()