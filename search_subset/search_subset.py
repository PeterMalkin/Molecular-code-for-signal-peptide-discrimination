# This script takes one file name as input and a string to search for.
# Looks for a given string and copies all the lines that contain the
# given string to the output file

import sys

def Main():

	if (len(sys.argv) < 3):
		print 'I take two parameters from command line. An input file name and a string to look for.'
		print 'And a filename to output data to' 
		print 'Example: python search_subset.py RLM165-min1peptides-allfilters.csv "plasma membrane" plasma-membrane.csv'
		exit(0)


	try:
		infile = open(sys.argv[1], "r")
	except:
		print "Could not open input file: "+str(sys.argv[1])
		exit(0)

	inputData = infile.readlines()
	infile.close() 

	try:
		outfile = open(sys.argv[3], "wt")
	except:
		print "Could not open output file: "+str(sys.argv[3])
		exit(0)	

	if ( len(sys.argv[2])<1 ):
		print "The search string is too short"
		exit(0)

	searchString = sys.argv[2]

	# Copy the header line
	outfile.write(inputData[0])

	# Search for the presence of the string and copy those lines to the output
	for line in inputData:
		if ( line.upper().find(searchString.upper()) >= 0 ):
			outfile.write(line)

	outfile.close()
Main()