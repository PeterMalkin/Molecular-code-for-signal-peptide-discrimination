# Accepts two files as input. One should contain Accession #,
# in column number two. The other should contain Accession # 
# in first column and GO_compartment data corresponding to Acc#
# in column number 5

import sys
import csv

import usefulgo


def main():

	if (len(sys.argv) < 3):
		print "I take two file names as input, and one file name as output"
		print "Example: python add_go_compartment.py RLM165-min1peptides-allfilters.csv UsefulGO.csv output.csv"
		exit(0)

	# load UsefulGO data
	ugo = usefulgo.UsefulGoData()
	ugo.loadFile(sys.argv[2])

	# read sample from csv file to detect its dialect
	try: 
		f = open(sys.argv[1], "rt")
		header = f.readline()
	except:
		print "Cannot open input file"
		print argv[1]
		exit(0)

	f.close()

	csvDialectSniffer = csv.Sniffer()
	dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')

	f = open(sys.argv[1], "rt")

	csvReader = csv.DictReader(f, dialect=dialect)

	fields = csvReader.fieldnames
	fields = fields + ["GO_Compartment"]

	csvWriter = csv.DictWriter(open(sys.argv[3],'w'), dialect=dialect, fieldnames=fields, delimiter='\t', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
	csvWriter.writerow(dict((fn,fn) for fn in fields))

	for row in csvReader:
		GO_Compartment = ugo.getGOCompartmentByAccession(row["Accession"])
		if (GO_Compartment != None):
			row["GO_Compartment"] = GO_Compartment
		else:
			row["GO_Compartment"] = "None"
			print "Warning: Not found GO_Compartment for "+str(row["Accession"])
		csvWriter.writerow(row)

	f.close()

main()