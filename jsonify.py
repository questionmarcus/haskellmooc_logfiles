#!/usr/bin/env python3
import sys
import json

def main():
    d = logfileParser(sys.argv[1:])
    saveAsJSON("logdata.json", d)

def logfileParser(files):
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
    try:
        userDate,code = line.split(" > ", 1)
        date,time,tz,user = userDate.split(" ")
    except ValueError:
        print("Unable to split line: "+line)

    # Convert time to ISO8601 datetime string (assume all times UTC)
    datetimeString = '{0}T{1}z'.format(date, time[:-3])
    return user,{"timestamp":datetimeString,"input":code.strip()}
                
def saveAsJSON(filename, values):
    with open(filename, "w") as output:
        output.write(
                json.dumps(
                    values, separators=(',',':')
                    )
                )

if __name__ == "__main__":
    main()
