from time import strptime, mktime
from datetime import datetime
import csv

## convert the time stamp to epoch
def dateTimeToEpoch(date, time):
    ## make a timestamp
    value = ' '.join([date, time])
    timestamp = strptime(value, '%Y-%m-%d %H:%M:%S')
    ## get the epoch
    epoch = mktime(timestamp)
    ## return the epoch
    return(epoch)

## convert epoch to date
def epochToDateTime(epoch):
    timestamp = datetime.fromtimestamp(epoch)
    string = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    ## return the formated time
    return(string)

## check if we need to write to disk
## if user sessions are getting stale
def checkHashTable(hash_table, time_out, epoch, out_file):
    ## we need to get a sorted list of times inserted
    sorted_list = sorted(hash_table, key= lambda x: hash_table[x][0])
    ## if we use python3.5+, all dicts are ordered
    for key in sorted_list:
        ip = key
        first_epoch, last_epoch, request_count = hash_table[key]
        ## get the change in time
        delta_time = epoch - last_epoch
        ## check if change in time 
        if delta_time > time_out:
            ## remove the key from the hash table
            hash_table.pop(key)
            ## let's get the delta epoch
            ## convert decimal to int
            ## increment for 1 since we have granularity
            ## of 1
            delta_epoch = int(last_epoch - first_epoch) + 1
            ## let's get the dates formatted properly
            first_date = epochToDateTime(first_epoch)
            last_date = epochToDateTime(last_epoch)
            ## write to csv file
            out_file.writerow([ip, first_date, last_date, delta_epoch, request_count])


## analyze the data stream and sort out
## hash table = {key : (first_epoch, last_epoch, request_count)}
def analyzeStream(in_stream, out_file, time_out, indices):
    ## use a moving hash table
    hash_table = {}
    ## get some indices
    ip_index = indices[0]
    date_index = indices[1]
    time_index = indices[2]
    ## loop through the input stream
    for line in in_stream:
        ## we only need the ip and date information
        ## since the problem doesn't ask for
        ## unique web pages
        ip = line[ip_index]
        ## convert date time to epoch for easier comparison
        ## deals with midnight calculations
        epoch = dateTimeToEpoch(line[date_index], line[time_index])
        ## check if we have the key
        if ip in hash_table:
            first_epoch, last_epoch, request_count  = hash_table[ip]
            delta_time = epoch - last_epoch
            ## if we are still in a user session
            if delta_time <= time_out:
                ## increase the requested web pages
                ## by one
                hash_table[ip] = (first_epoch, epoch, request_count+1)
        ## if we don't have the key, add it
        else:
            ## add to the hash table
            hash_table[ip] = (epoch, epoch, 1)
        ## run the hash table check function to prune
        ## the hash table and write to disk
        checkHashTable(hash_table, time_out, epoch, out_file)
    ## write to disk anything left over
    ## trigger a flush to disk by reporting an epoch with
    ## time_out
    checkHashTable(hash_table, time_out, epoch+time_out+1, out_file)