#!/usr/bin/env python

import json
import re
from difflib import SequenceMatcher

def main():
    logData = json.loads(open("2016-MOOC-logdata.json","r").read())
    tutorialsData = json.loads(open("tutorialHelpText.json", "r").read())
    for userData in logData["0"]:
        if findSimilar(userData, tutorialsData) != None:
            print(str(tutorialsData[findSimilar(userData, tutorialsData)])+" time: "+userData['timestamp'])

def findSimilar(userInput, helpData):
    helpList = list(helpData.keys())
    userInput = re.sub("let {.*} in ", "", userInput["input"])
    maxInd = []
    for text in helpList:
        maxInd.append(SequenceMatcher(None, userInput, text).ratio())
    if max(maxInd) >= 0.6:
        return helpList[maxInd.index(max(maxInd))]

if __name__ == "__main__":
    main()
