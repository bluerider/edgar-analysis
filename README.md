# Table of Contents
1. [Challenge](README.md#challenge)
2. [Implementation details](README.md#implementation-details)
3. [Input files](README.md#input-file)
4. [Output file](README.md#output-file)
5. [Running the test suite](README.md#test-suite)
6. [Run the program](README.md#run-the-program)

# Challenge

Parse the EDGAR weblogs and determine how long users spend on Edgar during a visit and how many documents user requests during their sessions.


# Implementation details

Webblogs to read are placed in `input/log.csv`. 

In addition, the tunable for session inactivity should be tuned as an integer in `input/inactivity_period.txt`

Sessionized analysis is outputted to `output/sessionization.txt`

Streaming reads are parsed and read into an unordered hash table. After every read, a hash table pruner and flusher is called which determines if a session has expired based on changes in time. It prunes the hash table and writes to disk.

## Input file

### `log.csv`

The SEC provides weblogs stretching back years and is [regularly updated, although with a six month delay](https://www.sec.gov/dera/data/edgar-log-file-data-set.html). 

For the purposes of this challenge, below are the data fields you'll want to pay attention to from the SEC weblogs:

* `ip`: identifies the IP address of the device requesting the data. While the SEC anonymizes the last three digits, it uses a consistent formula that allows you to assume that any two `ip` fields with the duplicate values are referring to the same IP address
* `date`: date of the request (yyyy-mm-dd) 
* `time`:  time of the request (hh:mm:ss)
* `cik`: SEC Central Index Key
* `accession`: SEC document accession number
* `extention`: Value that helps determine the document being requested

There are other fields that can be found in the weblogs. For the purposes of this challenge, your program can ignore those other fields.

Unlike other weblogs that contain the actual http web request, the SEC's files use a different but deterministic convention. For the purposes of this challenge, you can assume the combination of `cik`, `accession` and `extention` fields uniquely identifies a single web page document request. Don't assume any particular format for any of those three fields (e.g., the fields can consist of numbers, letters, hyphens, periods and other characters)

The first line of `log.csv` will be a header denoting the names of the fields in each web request. Each field is separated by a comma. Your program should only use this header to determine the order in which the fields will appear in the rest of the other lines in the same file.

### `inactivity_period.txt`
This file will hold a single integer value denoting the period of inactivity (in seconds) that your program should use to identify a user session. The value will range from 1 to 86,400 (i.e., one second to 24 hours)

## Output file

Once your program identifies the start and end of a session, it should gather the following fields and write them out to a line in the output file, `sessionization.txt`. The fields on each line must be separated by a `,`:

* IP address of the user exactly as found in `log.csv`
* date and time of the first webpage request in the session (yyyy-mm-dd hh:mm:ss)
* date and time of the last webpage request in the session (yyyy-mm-dd hh:mm:ss)
* duration of the session in seconds
* count of webpage requests during the session

If your program is able to detect multiple user sessions ending at the same time, it should write the results to the `sessionization.txt` output file in the same order as the user's first request for that session appeared in the input `log.csv` file.

## Test Suite

Run the test-suite with `test/run_tests.sh`. Due to path issues, please `chdir` before running `run_tests.sh`

## Run the program
Create `input/log.csv` and `input/inactivity_period.txt` and run with `./run.sh`
