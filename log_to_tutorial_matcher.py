#!/usr/bin/env python

import json
import re
from datetime import datetime
from difflib import SequenceMatcher

def main():
    logData = json.loads(open("2016-MOOC-logdata.json","r").read())
    tutorialsData = json.loads(open("tutorialHelpText.json", "r").read())
    data = []
    for userData in logData["420"]:
        if findSimilar(userData, tutorialsData) != None:
            userData["exercise"] = tutorialsData[findSimilar(userData,tutorialsData)]
            data.append(userData)
    data.sort(key=lambda x: datetime.strptime(x["timestamp"],"%Y-%m-%dT%H:%M:%S.%f%z"))
    return data

def findSimilar(userInput, helpData):
    """
    Method to find the closest matching help text to a user's input (or in our case
    the server log data)

    This is done using the Sequence matching you can read more details about the method
    here: https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.

    we can adjust the minimum similarity by increasing the ratio cut of value.
    Here 0.6 is used as a baseline as it is stated in the python docs that this
    is a reasonable estimate for similar strings
    """
    helpList = list(helpData.keys())
    userInput = re.sub("let {.*} in ", "", userInput["input"])
    maxInd = []
    for text in helpList:
        maxInd.append(SequenceMatcher(None, userInput, text).ratio())
    if max(maxInd) >= 0.6:
        return helpData[helpList[maxInd.index(max(maxInd))]]

if __name__ == "__main__":
    main()
