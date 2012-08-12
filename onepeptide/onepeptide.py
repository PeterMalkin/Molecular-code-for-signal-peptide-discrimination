# Accepts a csv file. Outputs only the lines 
# that belong to accession numbers occur only once. 

import sys
import csv

def main():

	if (len(sys.argv) < 3):
		print "This script reads in a csv file. It outputs only the lines"
		print "that belong to accession numbers occur only once. "
		print "Example: python onepeptide.py RLM288-all-ratios.csv output.csv"
		exit(0)

	# Read file into memory

	data = []

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
		data.append(row)
	f.close()

	# Count the number of times each accession number is present in a file
	accessions = {}
	for row in data:
		if ( row["Accession"] in accessions.keys() ):
			accessions[ row["Accession"] ] += 1
		else:
			accessions[ row["Accession"] ] = 1

        uniqueAccessions = []
	for key in accessions.keys():
		if ( accessions[key] == 1 ):
			uniqueAccessions.append(key)

	# Output the data for accession number that are present in both files
	csvWriter = csv.DictWriter(open(sys.argv[2],'w'), dialect=dialect, fieldnames=fields, delimiter='\t', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
	csvWriter.writerow(dict((fn,fn) for fn in fields))

	for row in data:
		if ( row["Accession"] in uniqueAccessions ):
			csvWriter.writerow( row )

	f.close()

main()
