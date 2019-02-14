## Insight Problem - Edgar Analytics
## Solution uses hash tables (dictionaries)
## we use python since python has a well
## optimized dictionary for integers

import sys
from python import export, ingest, utils

## main insertion function
def main(log_file, inactivity_period_file, output_file):
    ## generate the ingestion stream
    in_stream, header = ingest.ingestData(log_file)
    ## get the indices for the header
    indices = ingest.parseHeader(header, ["ip", "date", "time", "cik", "accession", "extention"])
    ## get the inactivity period time
    time_out= ingest.getInactivityPeriod(inactivity_period_file)
    ## get an output file
    out_file = export.outFile(output_file)
    ## run the analyzer
    utils.analyzeStream(in_stream, out_file, time_out, indices)
    
if __name__ == "__main__":
    ## run the main insertion function
    log_csv = sys.argv[1]
    inactivity_period_file = sys.argv[2]
    output_file = sys.argv[3]
    main(log_csv, inactivity_period_file, output_file)
