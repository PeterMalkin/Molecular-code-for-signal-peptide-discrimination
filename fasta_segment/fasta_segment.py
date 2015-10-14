import sys
import re
import csv

def Main():

	if (len(sys.argv) < 3):
		print 'Give me two files. One - your csv with data, and one more - list of all fastas'
		print 'Example: python fasta_segment.py .csv uniprot_typeII_human_SA_spec.csv type_II_signal_anchor_FASTA.txt'
		exit(0)

	fastaData = {}
	fastaline = ""
	fastaacc  = ""

	with open(sys.argv[2], "r") as infile:
		for line in infile:
			match = re.match(r"\>sp\|([A-Z0-9]+)\|", line)	
			if (match != None):
				if ( len(fastaacc) > 0 and len(fastaline) > 0 ):
					fastaData[fastaacc] = fastaline
				fastaacc = match.group(1)
				fastaline = ""
			else:
				fastaline += line.strip()

	fastaData[fastaacc] = fastaline

	# read sample from csv file to detect its dialect
	with open(sys.argv[1], "rt") as f:
		header = f.readline()

	csvDialectSniffer = csv.Sniffer()
	dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')

	f = open(sys.argv[1], "rt")

	csvReader = csv.DictReader(f, dialect=dialect)

	outFileName = "output.csv"
	if (len(sys.argv)>3):
		outFileName = sys.argv[3]

	fields = csvReader.fieldnames
	fields = fields + ["Sequence"]

	csvWriter = csv.DictWriter( open(outFileName,'w'), dialect=dialect, delimiter='\t', quotechar='"', fieldnames=fields, escapechar='\\', quoting=csv.QUOTE_ALL )
	csvWriter.writerow(dict((fn,fn) for fn in fields))

	for row in csvReader:
		From = int(row["from"])
		From -= 1
		To = int(row["to"])
		seq = fastaData[row["Accession"]]
		if ( (len(seq) >= To > From >= 0) ):
			row["Sequence"] = seq[From:To]
		else:
			row["Sequence"] = ""
			print "Warning: Not found sequence for "+str(row["Accession"])
		csvWriter.writerow(row)

	f.close()



Main()