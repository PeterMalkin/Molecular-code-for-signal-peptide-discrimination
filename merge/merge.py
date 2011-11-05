# Accepts a two csv files as input. Outputs only the lines from file one 
# that have accession numbers from file two. 

import sys
import csv

def main():

	if (len(sys.argv) < 3):
		print "This script reads a csv file and outputs only the lines with the accession"
		print "numbers that are present in the second file."
		print "If accession number is present in both files, all the data from both files"
		print "is copied to the output file"
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

	mutualAccessions = []

	for acc in accessions1:
		if ( acc in accessions2 ):
			mutualAccessions.append(acc)

	# Get the field names ready
	if ("Avg Peptide Ratio" in fields):
		fields.remove("Avg Peptide Ratio")
		fields.append("Avg Peptide Ratio 1")
		fields.append("Avg Peptide Ratio 2")

	if ("# Peptide Ratio" in fields):
		fields.remove("# Peptide Ratio")
		fields.append("# Peptide Ratio 1")
		fields.append("# Peptide Ratio 2")

	if ("# of peptides" in fields):
		fields.remove("# of peptides")
		fields.append("# of peptides 1")
		fields.append("# of peptides 2")

	# Output the data for accession number that are present in both files
	csvWriter = csv.DictWriter(open(sys.argv[3],'w'), dialect=dialect, fieldnames=fields, delimiter='\t', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
	csvWriter.writerow(dict((fn,fn) for fn in fields))

	data = []

	for acc in mutualAccessions:
		out = {}
		out["Accession"] = acc
		for key in data1[acc]:
			newKey = key
			if ( key.lower() == "avg peptide ratio" ):
				newKey = "Avg Peptide Ratio 1"
			if ( key.lower() == "# peptide ratio".lower() ):
				newKey = "# Peptide Ratio 1"
			if ( key.lower() == "# of peptides".lower() ):
				newKey = "# of peptides 1"
			out[newKey] = data1[acc][key]
		for key in data2[acc]:
			newKey = key
			if ( key.lower() == "avg peptide ratio" ):
				newKey = "Avg Peptide Ratio 2"
			if ( key.lower() == "# peptide ratio".lower() ):
				newKey = "# Peptide Ratio 2"
			if ( key.lower() == "# of peptides".lower() ):
				newKey = "# of peptides 2"
			out[newKey] = data2[acc][key]
		data.append(out)

	for row in data:
		csvWriter.writerow(row)

	f.close()




main()
