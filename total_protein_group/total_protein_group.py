import sys

if (len(sys.argv) < 2):
	print "I take one file names as input, and one file name as output"
	print "Example: python total_protein_group.py total_proteins_GO.csv output.csv"
	exit(0)

# try open input file
try: 
	fin = open(sys.argv[1], "r")
	inputData = fin.readlines()
	fin.close()
except:
	print "Cannot open input file"
	print argv[1]
	exit(0)

# try open output file
try:
	fout = open(sys.argv[2], "w")
except:
	print "Cannot open output file"
	print argv[2]
	exit(0)

# create group lists
group1 = []
group2 = []
group3 = []
group4 = []
group5 = []
group6 = []
group7 = []
group8 = []

fout.write(inputData[0])

for ix in range(1, len(inputData)):

	# if has Plasma membrane -> first group
	if (inputData[ix].upper().find("PLASMA MEMBRANE") != -1):
		group1.append(inputData[ix])
		continue

	if (inputData[ix].upper().find("MITO") != -1):
		group2.append(inputData[ix])
		continue

	if (inputData[ix].upper().find("ENDO") != -1):
		group5.append(inputData[ix])
		continue

	if (inputData[ix].upper().find("NUCLE") != -1):
		group3.append(inputData[ix])
		continue

	if ((inputData[ix].upper().find("CYTO") != -1) 
		and (inputData[ix].upper().find("MEMBRANE")) ):
		group7.append(inputData[ix])
		continue

	if (inputData[ix].upper().find("CYTO") != -1):
		group4.append(inputData[ix])
		continue

	if (inputData[ix].upper().find("GOLGI") != -1):
		group6.append(inputData[ix])
		continue

	if (inputData[ix].upper().find("MEMBRANE") != -1):
		group1.append(inputData[ix])
		continue
	
	# Nothing matched -> the line goes to group 8
	group8.append(inputData[ix])

fout.write("\n")
fout.write("Group II: mito*")
fout.write("\n\n")

for line in group2:
	fout.write(line)


fout.write("\n")
fout.write("Group V: endo*")
fout.write("\n\n")

for line in group5:
	fout.write(line)


fout.write("\n")
fout.write("Group III: nucle*")
fout.write("\n\n")

for line in group3:
	fout.write(line)


fout.write("\n")
fout.write("Group VII: cyto* and membrane")
fout.write("\n\n")

for line in group7:
	fout.write(line)


fout.write("\n")
fout.write("Group IV: cyto*")
fout.write("\n\n")

for line in group4:
	fout.write(line)


fout.write("\n")
fout.write("Group VI: Golgi")
fout.write("\n\n")

for line in group6:
	fout.write(line)


fout.write("\n")
fout.write("Group I: membrane")
fout.write("\n\n")

for line in group1:
	fout.write(line)


fout.write("\n")
fout.write("Group VIII: Everything else")
fout.write("\n\n")

for line in group8:
	fout.write(line)

fout.close()