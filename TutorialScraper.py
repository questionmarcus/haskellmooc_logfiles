#!/usr/bin/env python

import requests
import regex
import json

def main():
    repoFolder = "https://github.com/wimvanderbauwhede/haskelltutorials/tree/master/static/js"
    tutorialURLS = fetchTutorialPages(repoFolder)
    pagesData = getTutorialPages(tutorialURLS)
    for page in pagesData:
        print(getLessonObjects(page))


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

def getLessonObjects(htmlData):
    jsonObjects = regex.findall(r"\{(?:[^{}]|(?R))*\}", htmlData)
    objs = []
    for obj in jsonObjects:
        # if "lesson:" in obj:
        objs.append(regex.sub("(\s{2,}|\\\')", "", obj))
    return objs


if __name__ == "__main__":
    main()
