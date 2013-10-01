import sys
import csv
import numpy
from statlib.stats import *
from scipy.stats import *

def readRatiosByAccessionNumber(csvFileName):
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
    
    accessionFieldName = ""
    for f in fields:
        if ( f.find("Accession") != -1 ):
            accessionFieldName = f
            break

    # read in the data
    data = {}
    
    if (accessionFieldName == ""):
        return data
    
    for row in csvReader:
        if ( row[accessionFieldName] not in data ):
            data[row[accessionFieldName]] = []
        data[row[accessionFieldName]].append(row)

    fin.close()  
    return data, accessionFieldName

def readRatios(csvFileName):
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

    ratioFieldName = ""
    for f in fields:
        if ( f.find("Ratio") != -1 ):
            ratioFieldName = f
            break

    # read in the data
    data = []
    
    if (ratioFieldName == ""):
        return data
    
    for row in csvReader:
        for key in row.keys():
            data.append(float(row[ratioFieldName]))
    fin.close()  
    return data, ratioFieldName


def writeData(csvFileName, data):
    # Write field names (column headers) into the output csv
    fout = open(csvFileName, "w")
    
    fields = []
    for key in data[0].keys():
        fields.append(key)
    fields=sorted(fields)
    csvWriter = csv.DictWriter(fout, fieldnames=fields, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
    csvWriter.writerow(dict((fn,fn) for fn in fields))
        
    # Write data to output
    for row in data:
        csvWriter.writerow(row)    
        
    fout.close()    

def main():
    
    if (len(sys.argv) < 2):
        print ""
        print "Takes a csv file as input. Looks for all peptides" 
        print "that constitute each accession number, "
        print "gets median of peptides Ratios per accession number"
        print  "and calculates two tailed p-value using t-test"
        print "for two independednt samples of scores "
        print "(peptides in accession number vs all peptides)" 
        print "assuming equal population variance."
        print " Outputs a .csv file with calculated pvalues."
        print ""
        print "example: "
        print "python avg-ratio-pvalue-accession-num.py 091611-RLM-217-Peptide-Quant.csv"
        exit(0)

    if (len(sys.argv) == 3 ):
        outputFileName = sys.argv[2]
    else:
        outputFileName = "output.csv"

    ratios, ratioFieldName = readRatios(sys.argv[1])
    medianRatio = numpy.median(ratios)
    fullData, accessionFieldName = readRatiosByAccessionNumber(sys.argv[1])

    result = []

    for accession in fullData:
        currentRatios = []
        for accData in fullData[accession]:
            currentRatios.append(float(accData[ratioFieldName]))
        currentMedianRatio = numpy.median(currentRatios)
        currentMeanRatio = numpy.mean(currentRatios)

        t,p = stats.ttest_ind(ratios, currentRatios)

        out = {}
        out["Accession"] = accession
        out["Median"] = currentMedianRatio
        out["Mean"] = currentMeanRatio
        out["P-Value"] = p
        out["Number of peptides"] = len(currentRatios)
        result.append(out)

    writeData(outputFileName, result)

main()