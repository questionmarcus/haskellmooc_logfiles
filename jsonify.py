#!/usr/bin/env python3
import sys
import argparse
import json
from datetime import datetime,timedelta
from requests import get

from log_to_tutorial_matcher import findSimilar
from tutorial_scraper import processPages,webLoadPageData
from HaskellInterpreter import HaskellInterpreter

def main():
    parser = argparse.ArgumentParser(
        description="Commandline utility to take server log files and convert"
            +"them to json files. Expects files to be in the format."
            +" <date:yyyy-mm-dd> <time:hh-MM-ss.ms> <timezone> <userID> > <user input>"
            +" Returns 2 files: <PREFIX>-logdata.json and <PREFIX>-UserSessions.json,"
            +" the prefix for which is set with the -o flag.",
        epilog="Written by Marcus Lancaster as part of an MSc Summer Project at"
            +" Glasgow University. Supervised by Jeremy Singer."
            )
    parser.add_argument("--web", action="store_true", help="If this flag is set"
            +" the input file(s) will instead be read as URL(s) and be downloaded"
            +" and parsed if a connection is available.")
    parser.add_argument("-i", "--input", nargs="+", required=True,
            help="The filepath(s) or URL(s) (if --web flag is set) to parse")
    parser.add_argument("-o", "--output", nargs=1, required=True,
            help="The output file PREFIX for the final parsed json file")
    parser.add_argument("--tut-data", nargs=1, required=True,
            help="The filepath to the data containing the tutorial help text"
            +" returned by the tutorial_scraper.py utility. RUN THE TUTORIAL"
            +"_SCRAPER UTILITY BEFORE THIS")
    args = parser.parse_args(sys.argv[1:])
    if args.web == True:
        d = webParse(args.input)
    else:
        d = logfileParser(args.input)
    d = getCodeErrors(d)
    d = getExercise(d)
    US = userSessions(d)
    saveAsJSON(args.output[0]+"-logdata.json", d)
    saveAsJSON(args.output[0]+"-UserSessions.json", US)

def webParse(urls):
    """
    Transforms log data contained sourced from data hosted online
    into a python dictionary format in the format:
    {
        "user id0":[{timestamp0, input0},...,{timestampN,inputN}],
        ...
        "user idN":[{timestamp0, input0},...,{timestampN,inputN}]
    }

    dictionaries are then sorted based on their timestamp

    Keyword Arguments:
    urls -- A single url, or a list of urls.
    """
    if type(urls) is not list:
        return webParse([urls])
    else:
        data = {}
        for url in urls:
            response = get(url)
            for line in response.text.split("\n")[:-1]:
                user,logdata = lineParser(line)
                if user not in data:
                    data[user] = []
                data[user].append(logdata)
        for user in data:
            sortData(data[user])
        return data

def logfileParser(files):
    """
    Transforms log data contained in multiple files into a python
    dictionary format in the format:
    {
        "user id0":[{timestamp0, input0},...,{timestampN,inputN}],
        ...
        "user idN":[{timestamp0, input0},...,{timestampN,inputN}]
    }

    dictionaries are then sorted based on their timestamp

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
        for user in data:
            sortData(data[user])
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
        # Create List of timestamps as datetime objects, which are already sorted
        timestamps = []
        for obj in data[user]:
            # timestamp strings in ISO format
            timestamps.append(datetime.strptime(
                obj['timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z"
                ))

        # Create variables needed
        sessStart = currTime = prevTime = None
        n = 0
        sessions = []
        session = {}

        # Go through every timestamp in order of appearance
        for time in timestamps:
            currTime = time
            if not sessStart:
                # if session start not define, (at start of data) define it
                sessStart = currTime
            if prevTime:
                # Once there are two times to compare, calc inter event time
                IET = currTime - prevTime # IET (Inter Event Time)
                if IET > timedelta(0,60*max_pause_length):
                    # if IET > 10 minutes (600 seconds)
                   sessTime = prevTime - sessStart
                   session['start'] = sessStart.isoformat()[:-6]+".000000+0000"
                   session['end'] = prevTime.isoformat()[:-6]+".000000+0000"
                   session['inputs'] = n
                   session['duration (s)'] = (prevTime - sessStart).total_seconds()
                   sessStart = currTime
                   n = 1
                   sessions.append(session)
                   session = {}
                else:
                    n += 1
            prevTime = currTime
        # Once last input is record, define this as end of the session
        session['start'] = sessStart.isoformat()[:-6]+".000000+0000"
        session['end'] = prevTime.isoformat()[:-6]+".000000+0000"
        session['inputs'] = n
        session['duration (s)'] = (prevTime - sessStart).total_seconds()
        sessions.append(session)

        # Add session to dict
        userSessions[user] = sessions
    return userSessions

def sortData(userLogData):
    """
    Method that takes list of dictionary objects and sorts the list based
    on the "timestamp" value of that object.

    Keywords: userLogData --- list of objects containing a "timestamp" key-value
        pair.
    """
    return userLogData.sort(
            key=lambda x: datetime.strptime(x["timestamp"],"%Y-%m-%dT%H:%M:%S.%f%z")
            )

def getCodeErrors(data):
    logData = data.copy()
    for index,user in enumerate(logData):
        print("----------PROCESSING FOR USER "+user+"------------")
        shell = HaskellInterpreter()
        for data in logData[user]:
            output = shell.runLine(data['input'])
            if "Nothing" in output:
                data["error"] = "Timeout"
            elif "Just" not in output:
                data["error"]= output
            else:
                data["error"] = None
        shell.endProcess()
    return logData

def getExercise(data):
    logData = data.copy()
    helpText = json.loads(open("tutorialHelpText.json", "r").read())
    for index,user in enumerate(logData):
        for log in logData[user]:
            log["exercise"] = findSimilar(log, helpText)
    return logData

if __name__ == "__main__":
    main()
