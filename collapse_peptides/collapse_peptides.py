# Accepts a csv file as input. Collapses all records for one Accession #,
# Adds a column with the number of peptides being collapsed into one 
# accession number's record

import sys
import csv

def main():

	if (len(sys.argv) < 3):
		print "I take two file names as parameters. One to read from, one to write to"
		print "Example: python collapse_peptides.py RLM165-min1peptides-allfilters-GO.csv output.csv"
		exit(0)

	# read sample from csv file to detect its dialect
	try: 
		f = open(sys.argv[1], "rt")
		header = f.readline()
	except:
		print "Cannot open input file"
		print argv[1]
		exit(0)

	f.close()

	# Read in data and count the number of peptides for each accession #
	csvDialectSniffer = csv.Sniffer()
	dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')

	f = open(sys.argv[1], "rt")
	csvReader = csv.DictReader(f, dialect=dialect)

	fields = csvReader.fieldnames

	# Check the input data has valid info
	if ( 	not "Accession" in fields
		or not "Avg Peptide Ratio" in fields
		or not "# Peptide Ratio" in fields 
		or not "Peptide" in fields ):
		print "The input data is incomplete"
		print "Missing one of the crucial columns"
		print "Make sure you have Peptide, Accession, # Peptide Ratio and Avg Peptide Ratio" 
		exit(0)

	data = {}

	for row in csvReader:
		accession = row["Accession"]
		if ( accession in data ):
			data[ accession ]["# of peptides"] += 1
			data[ accession ]["Avg Peptide Ratio"] = float(data[ accession ]["Avg Peptide Ratio"]) + float(row["Avg Peptide Ratio"])
			data[ accession ]["# Peptide Ratio"] = int(data[ accession ]["# Peptide Ratio"]) + int(row["# Peptide Ratio"])
		else:
			data[ accession ] = row
			data[ accession ]["# of peptides"] = 1

	f.close()

	# Remove the peptides column if there is one
	try:
		fields.remove("Peptide")
	except:
		print "Warning, no Peptide column found in the input file"

	fields.append("# of peptides")

	# Average the values for the field "Avg Peptide Ratio"
	for key in data.keys():
		data[key]["Avg Peptide Ratio"] = float(data[key]["Avg Peptide Ratio"]) / float(data[key]["# of peptides"])

	# Output resulting data into csv
	f = open(sys.argv[2], "w")
	csvWriter = csv.DictWriter(f, dialect=dialect, fieldnames=fields, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
	csvWriter.writerow(dict((fn,fn) for fn in fields))

	accessionsWritten = set()

	for key in data.keys():
		if ( "Peptide" in data[key] ):
			del data[key]["Peptide"]
		csvWriter.writerow(data[key])
	
	f.close()

main()
