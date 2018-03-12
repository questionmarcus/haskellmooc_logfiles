#!/usr/bin/python 

# sessions.py
# Jeremy Singer
# 12 Mar 2018

# analyse logfiles, remove IP
# addresses and replace with integer IDs

####from __future__ import statistics
import glob  # for filename wildcards
import datetime
import sys

# dictionary of IP addresses
ips = {}
anonId = 0

# list of txt log files to process
##infiles = glob.glob('../logfiles_2016/*.log')

infiles = []
infiles.append(sys.argv[1])

for infile in infiles:
    #print "analysing file %s" % (infile)
    with open(infile, 'r') as f:
        # the first element of each line is the timestamp
        # in the form '2016-09-21' i.e. YYYY-MM-DD
        for line in f:
            if line.startswith('20'):
                date = line.split(' ')[0]
                time = line.split(' ')[1]
                ipaddress = (line.split(' ')[3])[:-1]  # remove last char
                # store data based on IP address
                if ipaddress not in ips:
                    ips[ipaddress] = anonId
                    anonId = anonId +1
                print (line.replace(ipaddress, str(ips[ipaddress]) + " ")),
