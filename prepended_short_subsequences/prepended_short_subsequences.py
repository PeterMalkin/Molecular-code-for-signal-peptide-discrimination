#!env python 

# Accepts a csv file as input. For each row adds columns that contain signal sequences
# prepended with "A" in a pattern AAAAX and XAAAA, then goes to http://dgpred.cbr.su.se/
# and looks up hydrophobicity, the fills the next field with the result

import sys
import csv
import re
import itertools
import mimetools
import mimetypes
import urllib2

# The length of the parent subsequence
ParentSubsequnceLength = 9
TotalLengthOfSubsequences = 19

class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return
  
    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return
  
    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
        parts = []
        part_boundary = '--' + self.boundary
      
        # Add the form fields
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
            ]
            for name, value in self.form_fields
            )
      
        # Add the files to upload
        parts.extend(
            [ part_boundary,
              'Content-Disposition: file; name="%s"; filename="%s"' % \
                 (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
            ]
            for field_name, filename, content_type, body in self.files
            )
      
        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)

def getDG(sequence):

    url = 'http://dgpred.cbr.su.se/results.php?program=TMpred'

    req = urllib2.Request( url )

    req.add_header('Host', 'dgpred.cbr.su.se')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Language', 'en-us,en;q=0.5')
    req.add_header('Accept-Encoding', '')
    req.add_header('Referer', 'http://dgpred.cbr.su.se/index.php?p=TMpred')
    req.add_header('Connection', 'keep-alive')

    # Create the form with two fields
    form = MultiPartForm()
    form.add_field('seq', sequence)
    form.add_field('with_length', "on")

    data = str(form)

    req.add_header('Content-length', len(data))
    req.add_header('Content-type', form.get_content_type())
    req.add_data(data)

    html_page= ""
    try:
        r = urllib2.urlopen(req)
        html_page = r.read()
        html_page = html_page.split("\n")
    except urllib2.URLError:
        print "Network error!"

    # Parse the answer
    result = "NaN"

    for line in html_page:
        if (line.find(sequence)!=-1):
            match = re.match(".+"+sequence+"</td><td>\&nbsp\;</td><td>([0-9\-\.]+).*", line)
            if match != None:
                result = match.group(1)
            
    return result

# From a given sequence, take last keepLastN aminoacids and prepend it with A such that
# the resulting sequence is of length TotalLengthOfSubsequences
def prependSubsequence(sequence, keepLastN, totalLengthOfSubsequences):
    result = ""
    if ( len(sequence) < keepLastN ):
        return result
    subsequence = sequence[-keepLastN:]    
    for ix in range(0,totalLengthOfSubsequences-len(subsequence)):
        result+="A"
    return result+subsequence

# From a given sequence, take last keepFirstN aminoacids and postpend it with A such that
# the resulting sequence is of length TotalLengthOfSubsequences
def postpendSubsequence(sequence, keepFirstN, totalLengthOfSubsequences):
    result = ""
    if ( len(sequence) < keepFirstN ):
        return result
    subsequence = sequence[:keepFirstN]
    result = subsequence
    for ix in range(len(subsequence),totalLengthOfSubsequences):
        result+="A"
    return result

def main():

    if (len(sys.argv) < 3):
        print "I take two csv file names as parameters. One to read from, one to write to"
        print "Example: python prepended_short_subsequences.py parent_19aa_MS_typeII_TMDs.csv output.csv"
        exit(0)

    # read sample from csv file to detect its dialect
    try: 
        fin = open(sys.argv[1], "rt")
        header = fin.readline()
    except:
        print "Cannot open input file"
        print sys.argv[1]
        exit(0)

    fin.close()

    # Read in data and count the number of peptides for each accession #
    csvDialectSniffer = csv.Sniffer()
    dialect = csvDialectSniffer.sniff(header, delimiters=' ,\t')

    fin = open(sys.argv[1], "rt")
    csvReader = csv.DictReader(fin, dialect=dialect)

    fields = csvReader.fieldnames

    # Check the input data has valid info
    if (   not "Accession" in fields
        or not "Avg Ratio" in fields
        or not "parent sequence" in fields ):
        print "The input data is incomplete"
        print "Missing one of the crucial columns"
        print "Make sure you have Accession, Avg Ratio and parent sequence  columns" 
        exit(0)

    # read in the data
    data = []
    for row in csvReader:
        data.append(row)
    fin.close()  

    # Create fields (column headers) for output data
    x_sequence = "XXXXXXXXXXXXXXXXXXX"

    # Add fields for prepended sequences from the back of the parent sequence
    for addFieldIx in range(1,ParentSubsequnceLength+1):
        addFieldName = prependSubsequence(x_sequence, addFieldIx, TotalLengthOfSubsequences)
        fields.append(addFieldName)
        fields.append("dG("+addFieldName+")")

    # Add fields for postpended sequences from the beginning of the parent sequence
    for addFieldIx in range(1,ParentSubsequnceLength+1):
        addFieldName = postpendSubsequence(x_sequence, addFieldIx, TotalLengthOfSubsequences)
        fields.append(addFieldName)
        fields.append("dG("+addFieldName+")")

    # Process the data
    totalItems = len(data) * 2 * ParentSubsequnceLength
    print "Processing the data. Total items: " + str( totalItems )
    currentItem = 0
    
    for row in data:
        sequence = row["parent sequence"]
        
        # form prepended subsequences
        for subsequenceLengtIx in range(1,ParentSubsequnceLength+1):
            fieldName = prependSubsequence(x_sequence, subsequenceLengtIx, TotalLengthOfSubsequences)
            row[fieldName] = prependSubsequence(sequence, subsequenceLengtIx, TotalLengthOfSubsequences)
            dGFieldName = "dG("+fieldName+")"
            row[dGFieldName] = getDG(row[fieldName])
            currentItem+=1
            print str(row[fieldName]) + " " + str(row[dGFieldName]) + " "  + " [ " +str(currentItem)+ " / " +str(totalItems)+ " ]"

        # form postpended subsequences
        for subsequenceLengtIx in range(1,ParentSubsequnceLength+1):
            fieldName = postpendSubsequence(x_sequence, subsequenceLengtIx, TotalLengthOfSubsequences)
            row[fieldName] = postpendSubsequence(sequence, subsequenceLengtIx, TotalLengthOfSubsequences)
            dGFieldName = "dG("+fieldName+")"
            row[dGFieldName] = getDG(row[fieldName])
            currentItem+=1
            print str(row[fieldName]) + " " + str(row[dGFieldName]) + " "  + " [ " +str(currentItem)+ " / " +str(totalItems)+ " ]"

    print "Done"
    
    # Write field names (column headers) into the output csv
    fout = open(sys.argv[2], "w")
    csvWriter = csv.DictWriter(fout, dialect=dialect, fieldnames=fields, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
    csvWriter.writerow(dict((fn,fn) for fn in fields))
        
    # Write data to output
    for row in data:
        csvWriter.writerow(row)    
        
    fout.close()

main()