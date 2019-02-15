import csv

## ingest the data
## only job is to generate a
## file output byte stream
## asynchronously
def ingestData(file):
    ## open the file
    in_stream = open(file, "r")
    ## parse as a csv file
    csv_stream = csv.reader(in_stream, delimiter=',', quotechar='"')
    ## we need to get the headers
    header = next(csv_stream)
    ## make the header all lower case to avoid case issues
    header = [field.lower() for field in header]
    return(csv_stream, header)

## parse the header to
## get the needed values
## takes a list of strings as terms
## takes a header which is a list of strings
## returns a list of indices in the same order
## as terms
def parseHeader(header, terms):
    ## we only want the indices of these terms
    indices = [header.index(term) for term in terms]
    ## return the dictionary
    return(indices)
    
    
## get the inactivty period time
def getInactivityPeriod(file):
    ## need to convert string to int
    inactivity_period_time = int(open(file, "r").read())
    return(inactivity_period_time)
    
 