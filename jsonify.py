#!/usr/bin/env python3
import sys
import json

def main():
    d = logfileParser(sys.argv[1:])
    saveAsJSON("logdata.json", d)

def logfileParser(files):
    """
    Transforms log data contained in multiple files into a python
    dictionary format in the format:
    {
        "user id0":[{timestamp0, input0},...,{timestampN,inputN}],
        ...
        "user idN":[{timestamp0, input0},...,{timestampN,inputN}]
    }
    
    Keyword Arguments:
    files -- A single file name, or a list of files.
    """
    if type(files) is not list:
        return logfileParser([files])
    else:
        data = {}
        for filepath in files:
            with open(filepath, 'r') as f:
                for line in f:
                    user,logdata = lineParser(line)
                    if user not in data:
                        data[user] = []
                    data[user].append(logdata)
        return data

def lineParser(line):
    """
    Converts individual lines of log files into constituent components.
    Returns the user ID and an opject containing the timestamp and the 
    code written.

    Keyword Arguments:
    line -- String containing a single line from the log file
    """
    try:
        userDate,code = line.split(" > ", 1)
        date,time,tz,user = userDate.split(" ")
    except ValueError:
        print("Unable to split line: "+line)

    # Convert time to ISO8601 datetime string (assume all times UTC)
    datetimeString = '{0}T{1}z'.format(date, time[:-3])
    return user,{"timestamp":datetimeString,"input":code.strip()}
                
def saveAsJSON(filename, values):
    """
    Creates a file in JSON format from python dictionary object.

    Keyword Arguments:
    filename -- String containing the name of the file (includes filetype)
    values -- Dictionary object containing data to be written to file
    """
    with open(filename, "w") as output:
        output.write(
                json.dumps(
                    values, separators=(',',':')
                    )
                )

if __name__ == "__main__":
    main()
