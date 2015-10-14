#Reads in UsefulGO data and gives access to it

import re

class UsefulGORecord:
#-----------------------
# Represents UsefulGO data
# Accession	NumGoTerms	GO_Function	GO_Process	GO_Compartment
	Accession = ""
	NumGoTerms = ""
	GO_Function = ""
	GO_Process = ""
	GO_Compartment = ""
#-----------------------

class UsefulGoData:
#-----------------------
# Container for all the UsefulGO data with accessors

	data = {}

	def __init__(self):
		data = {}

	# load data from a file
	def loadFile(self,filename):

		if ( len(filename) < 1 ):
			return

		self.data = {}

		try:
			file = open(filename, "r")
		except:
			print "Could not open file with UsefulGO data "+filename
			return

		for line in file:
			match = re.match('"([A-Z0-9]{6})",([0-9]*?),"(.*?)","(.*?)","(.*?)",*(.*)', line)
			if (match==None):
				continue

			dataPiece = UsefulGORecord()

			dataPiece.Accession = match.group(1)
			dataPiece.NumGoTerms = match.group(2)
			dataPiece.GO_Function = match.group(3)
			dataPiece.GO_Process = match.group(4)
			dataPiece.GO_Compartment = match.group(5)
			dataPiece.extra	= match.group(6)

			self.data[dataPiece.Accession] = dataPiece

		file.close()

	def getByAccession(self, Accession):
		try:
			return self.data[Accession]
		except:
			return None

	def getGOCompartmentByAccession(self, Accession):
		try:
			return self.getByAccession(Accession).GO_Compartment
		except:
	        	return None
#-----------------------
