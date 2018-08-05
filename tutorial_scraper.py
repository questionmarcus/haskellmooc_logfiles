#!/usr/bin/env python
import sys
import argparse
import requests
import regex
import json

def main():
    from jsonify import saveAsJSON
    parser = argparse.ArgumentParser(
        description="Commandline utility to take analyse the javascript used to"
            +" run the haskell MOOC  in order to find all help text enclosed in"
            +" the <code>[HELP TEXT]</code>."
            +" Dictionary object is written to a json object specified in the OUTPUT"
            +" argument",
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
    args = parser.parse_args(sys.argv[1:])

    if args.web == True:
        pagesData = webLoadPageData(args.input)
    else:
        pagesData = fileLoadPageData(args.input)

    dataDict = processPages(pagesData)
    saveAsJSON(args.output[0],dataDict)
    #print(dataDict)

def fetchTutorialPages(baseURL):
    """
    Method to scrape a base github url to find all urls containing the filename:
    ".../tutorial__.pages.js" and then return the urls for those files

    only tested for: "github.com/wimvanderbauwhede/haskelltutorials/tree/master/static/js"
    """
    res = requests.get(baseURL)
    tutURLS =  regex.findall('(?<=href=").*\/tutorial[0-9]{1,2}\.pages\.js', res.text)
    # remove "...tutorial1.pages.js" as not used in MOOC
    tutURLS = tutURLS[1:]
    for i,tutURL in enumerate(tutURLS):
        tutURLS[i] = regex.sub("\/blob", "", tutURL)
    return ["https://raw.githubusercontent.com"+url for url in tutURLS]

def webLoadPageData(urls):
    """
    Method to gather a dictionary of tutorial javascript files with the key
    being the tutorial number and the value being the raw text from the javascript
    file.

    This method is to be used when grabbing data from the web rather than locally

    keywords urls --- list of urls to grab raw javascript from
    """
    pagesData = {}
    for url in urls:
        pagesData[url.split("/")[-1].split(".")[0]] = requests.get(url).text
    return pagesData

def fileLoadPageData(filepaths):
    """
    Method to gather a dictionary of tutorial javascript files with the key
    being the tutorial number and the value being the raw text from the javascript
    file.

    This method is to be used when grabbing data from local files

    keywords filepaths --- list of filepaths to read data from
    """
    pagesData = {}
    for filepath in filepaths:
        with open(filepath, "r") as page:
            pagesData[filepath.split("/")[-1].split(".")[0]] = page.read()
    return pagesData

def processPages(htmlList):
    """
    Method which carries out the parsing methods on a dictoriary like collection
    or output of the ____LoadPageData() method.

    returns an dictionary with keys representing text contained in <code> tags
    and values being objects with the tutorial and lesson values to indicate location
    within the MOOC
    """
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
    """
    Method that will find all javascript objects from within the ...pages.js 
    files and returns a list of non-empty objects from each file.
    """
    jsonObjects = regex.findall(r"\{(?:[^{}]|(?R))*\}", htmlData)
    objs = []
    for obj in jsonObjects:
        # remove all empty space and \' characters
        objs.append(regex.sub("(\s{2,}|\\\')", "", obj))
    # Remove all empty objects
    objs.remove("{}")
    return objs

def codeTagScrape(jsonObjStr):
    """
    strips tag values from json objects and removes any words which are listed
    in the stopWords list.

    returns a list of text within <code> tags for each object passed to it.
    """
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
