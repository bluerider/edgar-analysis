import csv

## create a simple file 
def outFile(file):
    out_stream = open(file, 'w')
    out_file = csv.writer(out_stream, delimiter=',', quotechar='"')
    return(out_file)