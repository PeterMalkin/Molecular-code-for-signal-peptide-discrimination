#!/bin/pyhon

import sys

def main():

	if (len(sys.argv) < 2):
		print "Gime we a filename as input and I will count lines that are mentioned at least twice or more"
		print "Example: python count.py list.txt"
		exit(0)

	try:
		infile = open(sys.argv[1], "r")
	except:
		return
	
	filedata = infile.readlines()	

	count = 0
	datalist = []

	for line in filedata:
		datalist.append(line.strip())

	doublestripleslist = []
	for line in filedata:
		if ( datalist.count(line.strip()) > 1 ):
			if ( line.strip() not in doublestripleslist ):
				doublestripleslist.append(line.strip())

	for l in doublestripleslist:
		print l

	infile.close()

	print "The total number of repeated accessions is: "+str(len(doublestripleslist))

main()