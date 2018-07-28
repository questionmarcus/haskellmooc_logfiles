#!/usr/bin/env python
import sys
import requests
import regex
import json

def main():
    args = sys.argv[1:]
    if args[0] == "--web":
        if len(args) == 1:
            repoFolder = "https://github.com/wimvanderbauwhede/haskelltutorials/tree/master/static/js"
            tutorialURLS = fetchTutorialPages(repoFolder)
            pagesData = getTutorialPages(tutorialURLS)
        else:
            pagesData = getTutorialPages(args)
    else:
        pagesData = []
        for filepath in args:
            with open(filepath, "r") as page:
                pagesData.append("".join(page.readlines()))

    print(processPages(pagesData))


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
    for tutNum,page in enumerate(htmlList):
        objects = getLessonObjects(page)
        helpTextDic["tutorial"+str(tutNum+1)] = []
        for jsonObj in objects:
            helpText = codeTagScrape(jsonObj)
            if len(helpText) != 0:
                helpTextDic["tutorial"+str(tutNum+1)].append(helpText)
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
    stopWords = ["help", "next", "prev", "start", "back", "context", "show", "undo", "step\d+"]
    if jsonObjStr != "":
        helperText = regex.findall("<code>([^<>]*)</code>", jsonObjStr)
        for stopWord in stopWords:
            helperText = [text for text in helperText if not bool(regex.match(stopWord, text))]
#            if any([bool(regex.match(stopWord,text)) for text in helperText]):
#                helperText.remove(stopWord)
        return helperText
    else:
        return None




if __name__ == "__main__":
    main()
