#!/usr/bin/env python
import sys
import argparse
import requests
import regex
import json
from jsonify import saveAsJSON

def main():
    parser = argparse.ArgumentParser(
        description="Commandline utility to take analyse the javascript used to"
            +" run the haskell MOOC  in order to find all help text enclosed in"
            +" the <code>[HELP TEXT]</code>."
            +" Dictionary object is written to a json object specified in the OUTPUT"
            +" argument",
        epilog="Written by Marcus Lancaster as part of an MSc Summer Project at"
            +" Glasgow University. Supervised by Jeremy Singer."
            )
    parser.add_argument("--web", help="If this flag is set the input file(s) will"
        +" instead be read as URL(s) and be downloaded and parsed if a connection"
        +" is available.")
    parser.add_argument("-i", "--input", nargs="+", required=True,
            help="The filepath(s) or URL(s) (if --web flag is set) to parse")
    parser.add_argument("-o", "--output", nargs=1, required=True,
            help="The output file PREFIX for the final parsed json file")
    args = parser.parse_args(sys.argv[1:])
    if args.web != None:
        pagesData = getTutorialPages(args.input)
    else:
        pagesData = {}
        for filepath in args.input:
            with open(filepath, "r") as page:
                pagesData[filepath.split("/")[-1].split(".")[0]] = page.read()

    dataDict = processPages(pagesData)
    saveAsJSON(args.output[0],dataDict)
    #print(dataDict)


def fetchTutorialPages(baseURL):
    res = requests.get(baseURL)
    tutURLS =  regex.findall('(?<=href=").*\/tutorial[0-9]{1,2}\.pages\.js', res.text)
    # remove "...tutorial1.pages.js" as not used in MOOC
    tutURLS = tutURLS[1:]
    for i,tutURL in enumerate(tutURLS):
        tutURLS[i] = regex.sub("\/blob", "", tutURL)
    return ["https://raw.githubusercontent.com"+url for url in tutURLS]

def getTutorialPages(urls):
    if urls == None:
        raise ValueError("No urls provided")
    elif type(urls) != list:
        return getTutorialPages([urls])
    else:
        tutHTML = []
        for url in urls:
            print("Downloading HTML for: "+url)
            tutHTML.append(requests.get(url).text)
        return tutHTML

def processPages(htmlList):
    helpTextDic = {}
    non_unique = []
    for tutNum in htmlList:
        objects = getLessonObjects(htmlList[tutNum])
        for index,jsonObj in enumerate(objects):
            helpText = codeTagScrape(jsonObj)
            if len(helpText) != 0:
                for val in helpText:
                    if val in helpTextDic:
                        helpTextDic.pop(val)
                        print("removing "+val+" as a duplicated was found in:"+tutNum)
                    elif val in non_unique:
                        print("duplicate already removed for "+val)
                    else:
                        helpTextDic[val] = {"tutorial":tutNum,"lesson":index}
    return helpTextDic


def getLessonObjects(htmlData):
    jsonObjects = regex.findall(r"\{(?:[^{}]|(?R))*\}", htmlData)
    objs = []
    for obj in jsonObjects:
        # if "lesson:" in obj:
        objs.append(regex.sub("(\s{2,}|\\\')", "", obj))
    # Remove all empty objects
    objs.remove("{}")
    return objs

def codeTagScrape(jsonObjStr):
    stopWords = ["help", "next", "prev", "start", "back", "context", "show",
            "undo", "step\d+", "erase", "reset", "wipe"]
    if jsonObjStr != "":
        helperText = regex.findall("<code>([^<>]*)</code>", jsonObjStr)
        for stopWord in stopWords:
            helperText = [text for text in helperText if not bool(regex.match(stopWord, text))]
        return helperText
    else:
        return None




if __name__ == "__main__":
    main()
