# Accepts a two csv files as input. Outputs only the lines 
# that are unique to file one. 

import sys
import csv

def main():

	if (len(sys.argv) < 3):
		print "This script reads a csv file and outputs lines with the accession"
		print "numbers that are unique to the first file."
		print "Example: python merge.py input1.csv input2.csv output.csv"
		exit(0)

	# Read file 1 into memory

	data1 = {}

	# read sample from csv file to detect its dialect
	try: 
		f = open(sys.argv[1], "rt")
		header = f.readline()
	except:
		print "Cannot open input file", sys.argv[2]
		exit(0)

	f.close()

	csvDialectSniffer = csv.Sniffer()
	dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')

	f = open(sys.argv[1], "rt")
	csvReader = csv.DictReader(f, dialect=dialect)
	fields = csvReader.fieldnames
	for row in csvReader:
		data1[row["Accession"]] = row
	f.close()

	# Read file 2 into memory

	data2 = {}

	# read sample from csv file to detect its dialect
	try: 
		f = open(sys.argv[2], "rt")
		header = f.readline()
	except:
		print "Cannot open input file", sys.argv[2]
		exit(0)

	f.close()

	csvDialectSniffer = csv.Sniffer()
	dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')

	f = open(sys.argv[2], "rt")
	csvReader = csv.DictReader(f, dialect=dialect)
	for row in csvReader:
		data2[row["Accession"]] = row
	f.close()

	# Make a list of accesssion that are present in both files
	accessions1 = []
	for key in data1:
		accessions1.append(data1[key]["Accession"])
	
	accessions2 = []
	for key in data2:
		accessions2.append(data2[key]["Accession"])

	uniqueAccessions = []

	for acc in accessions1:
		if ( acc in accessions2 ):
			uniqueAccessions.append(acc)

	# Output the data for accession number that are present in both files
	csvWriter = csv.DictWriter(open(sys.argv[3],'w'), dialect=dialect, fieldnames=fields, delimiter='\t', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
	csvWriter.writerow(dict((fn,fn) for fn in fields))

	for acc in uniqueAccessions:
		csvWriter.writerow( data1[acc] )

	f.close()

main()
