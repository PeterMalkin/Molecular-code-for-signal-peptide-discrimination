#!env python 

# Accepts a csv file as input. For each row adds columns that contain signal sequences
# prepended with "A" in a pattern AAAAX and XAAAA

import sys
import csv

# The length of the parent subsequence
ParentSubsequnceLength = 9
TotalLengthOfSubsequences = 19

# From a given sequence, take last keepLastN aminoacids and prepend it with A such that
# the resulting sequence is of length TotalLengthOfSubsequences
def prependSubsequence(sequence, keepLastN, totalLengthOfSubsequences):
    result = ""
    if ( len(sequence) < keepLastN ):
        return result
    subsequence = sequence[-keepLastN:]    
    for ix in range(0,totalLengthOfSubsequences-len(subsequence)):
        result+="A"
    return result+subsequence

# From a given sequence, take last keepFirstN aminoacids and postpend it with A such that
# the resulting sequence is of length TotalLengthOfSubsequences
def postpendSubsequence(sequence, keepFirstN, totalLengthOfSubsequences):
    result = ""
    if ( len(sequence) < keepFirstN ):
        return result
    subsequence = sequence[:keepFirstN]
    result = subsequence
    for ix in range(len(subsequence),totalLengthOfSubsequences):
        result+="A"
    return result

def main():

    if (len(sys.argv) < 3):
        print "I take two csv file names as parameters. One to read from, one to write to"
        print "Example: python prepended_short_subsequences.py parent_19aa_MS_typeII_TMDs.csv output.csv"
        exit(0)

    # read sample from csv file to detect its dialect
    try: 
        fin = open(sys.argv[1], "rt")
        header = fin.readline()
    except:
        print "Cannot open input file"
        print sys.argv[1]
        exit(0)

    fin.close()

    # Read in data and count the number of peptides for each accession #
    csvDialectSniffer = csv.Sniffer()
    dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')

    fin = open(sys.argv[1], "rt")
    csvReader = csv.DictReader(fin, dialect=dialect)

    fields = csvReader.fieldnames

    # Check the input data has valid info
    if (   not "Accession" in fields
        or not "Avg Ratio" in fields
        or not "parent sequence" in fields ):
        print "The input data is incomplete"
        print "Missing one of the crucial columns"
        print "Make sure you have Accession, Avg Ratio and parent sequence  columns" 
        exit(0)

    # read in the data
    data = []
    for row in csvReader:
        data.append(row)
    fin.close()  

    # Create fields (column headers) for output data
    x_sequence = "XXXXXXXXXXXXXXXXXXX"

    # Add fields for prepended sequences from the back of the parent sequence
    for addFieldIx in range(1,ParentSubsequnceLength+1):
        addFieldName = prependSubsequence(x_sequence, addFieldIx, TotalLengthOfSubsequences)
        fields.append(addFieldName)

    # Add fields for postpended sequences from the beginning of the parent sequence
    for addFieldIx in range(1,ParentSubsequnceLength+1):
        addFieldName = postpendSubsequence(x_sequence, addFieldIx, TotalLengthOfSubsequences)
        fields.append(addFieldName)

    # Process the data
    for row in data:
        sequence = row["parent sequence"]
        
        # form prepended subsequences
        for subsequenceLengtIx in range(1,ParentSubsequnceLength+1):
            fieldName = prependSubsequence(x_sequence, subsequenceLengtIx, TotalLengthOfSubsequences)
            row[fieldName] = prependSubsequence(sequence, subsequenceLengtIx, TotalLengthOfSubsequences)

        # form postpended subsequences
        for subsequenceLengtIx in range(1,ParentSubsequnceLength+1):
            fieldName = postpendSubsequence(x_sequence, subsequenceLengtIx, TotalLengthOfSubsequences)
            row[fieldName] = postpendSubsequence(sequence, subsequenceLengtIx, TotalLengthOfSubsequences)


    # Write field names (column headers) into the output csv
    fout = open(sys.argv[2], "w")
    csvWriter = csv.DictWriter(fout, dialect=dialect, fieldnames=fields, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
    csvWriter.writerow(dict((fn,fn) for fn in fields))
        
    # Write data to output
    for row in data:
        csvWriter.writerow(row)    
        
    fout.close()

main()