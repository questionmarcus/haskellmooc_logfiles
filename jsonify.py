#!/usr/bin/env python3
import sys
import json
import datetime

def main():
    d = logfileParser(sys.argv[1:])
    saveAsJSON("logdata.json", d)
    US = userSessions(d)
    saveAsJSON("UserSessions.json", US)

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
    datetimeString = '{0}T{1}+0000'.format(date, time)
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

def userSessions(data, max_pause_length=10):
    """
    Creates a Python Dictionary object that seperates inputs into sessions
    where the user took a break no longer than the [max_pause_length] minutes

    Keyword Arguments:
    logdata -- Values to break into sessions
    max_pause_length -- Maximum time between inputs (in minutes) before new
    input is start of new session. Optional, defaults to 10 minutes.
    """
    userSessions = {}
    for user in data:
        timestamps = []
        for obj in data[user]:
            timestamps.append(datetime.datetime.strptime(
                obj['timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z"
                ))
        sessStart = currTime = prevTime = None
        n = 0
        sessions = []
        session = {}
        for time in sorted(timestamps):
            currTime = time
            if not sessStart:
                sessStart = currTime
            if prevTime:
                IET = currTime - prevTime # IET (Inter Event Time)
                if IET > datetime.timedelta(0,60*max_pause_length):
                    # if IET > 10 minutes (600 seconds)
                   sessTime = prevTime - sessStart
                   session['start'] = sessStart.isoformat()
                   session['end'] = prevTime.isoformat()
                   session['inputs'] = n
                   session['duration (s)'] = (prevTime - sessStart).total_seconds()
                   sessStart = currTime
                   n = 1
                   sessions.append(session)
                   session = {}
                else:
                    n += 1
            prevTime = currTime
        session['Start'] = sessStart.isoformat()
        session['End'] = prevTime.isoformat()
        session['Inputs'] = n
        session['duration (s)'] = (prevTime - sessStart).total_seconds()
        sessions.append(session)
        userSessions[user] = sessions
    return userSessions


if __name__ == "__main__":
    main()
