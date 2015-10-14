#!env python 

# Takes two csv files as input. Looks at all the columns. If columns have the same name,
# takes all the data in those columns and runs Mann Whitney U test on those two sets of data.
# Outputs a .csv file with calculated pvalues 

import sys
import csv
from statlib.stats import *

def readData(csvFileName):
    # read sample from csv file to detect its dialect
    try: 
        fin = open(csvFileName, "rt")
        header = fin.readline()
    except:
        print "Cannot open input file"
        print csvFileName
        exit(0)

    fin.close()

    csvDialectSniffer = csv.Sniffer()
    dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')
    fin = open(csvFileName, "rt")
    csvReader = csv.DictReader(fin, dialect=dialect)
    
    fields = csvReader.fieldnames
    
    # read in the data
    data = {}
    for field in fields:
        data[field] = []
    
    for row in csvReader:
        for key in row.keys():
            data[key].append(row[key])
    fin.close()  
    return data    

def writeData(csvFileName, data):
    # Write field names (column headers) into the output csv
    fout = open(csvFileName, "w")
    
    for key in data.keys():
        if (key.find("dG")==-1):
            continue
        fout.write('"'+str(key)+'","'+str(data[key])+'"\n')
        
    fout.close()
    
def main():
    
    if (len(sys.argv) < 4):
        print "Takes two csv files as input. Looks at all the columns. If columns have the same name,"
        print "takes all the data in those columns and runs Mann Whitney U test on those two sets of data."
        print "Outputs a .csv file with calculated pvalues."
        print "example: python find_pvalues_for_matching_columns.py sensitive.csv resistant.csv pvalues.csv"
        exit(0)

    data1 = readData(sys.argv[1])
    data2 = readData(sys.argv[2])

    result = {}

    for key in data1.keys():
        if key not in data2:
            continue
        try:
            (U,p) = mannwhitneyu(data1[key],data2[key])
        except ValueError:
            p = "Unclear"
        result[key] = p
            
    writeData(sys.argv[3], result)

main()