import unittest
import jsonify
import json

class JsonifyTestClass(unittest.TestCase):

    def testWebParse(self):
        # Use URL from this project, known number of entries (100)
        baseURL = "https://raw.githubusercontent.com/questionmarcus/"
        URL = "haskellmooc_logfiles/master/testData/2018_testData.log"
        # Load web data
        webData = jsonify.webParse(baseURL+URL)
        # Get nEntries, NOT LEN(data) as data is returned as dic
        # This would calculate the number of users not the number of lines
        nEntries = 0
        for user in webData:
            nEntries += len(webData[user])
        self.assertEqual(nEntries, 100)

    def testFileParse(self):
        filename = "testData/2018_testData.log"

        parsedData = jsonify.logfileParser(filename)
        nEntries = 0
        for user in parsedData :
            nEntries += len(parsedData[user])
        self.assertEqual(nEntries, 100)

    def testLineParser(self):
        testVals = [
                u'2016-09-22 16:06:06.970086 UTC 241 > let {f x  =  x+1;add3num x y z = x+y+z}',
                u'2016-09-29 21:13:59.597184 UTC 1683 > reverse "hello"',
                u'2016-09-27 15:32:24.006764 UTC 1367 > let {answer  =  42;double  =  answer * 2 } in double'
]
        expectedOut = [
                ("241",{"timestamp":"2016-09-22T16:06:06.970086+0000","input":'let {f x  =  x+1;add3num x y z = x+y+z}'}),
                ("1683",{"timestamp":"2016-09-29T21:13:59.597184+0000","input":'reverse "hello"'}),
                ("1367",{"timestamp":"2016-09-27T15:32:24.006764+0000","input":'let {answer  =  42;double  =  answer * 2 } in double'})
                ]
        for i in range(len(testVals)):
            self.assertEqual(jsonify.lineParser(testVals[i]),expectedOut[i])

    def testSortdata(self):
        testVals = [
                {"timestamp":"2016-08-08T00:00:00.000000+0000","input":"5"},
                {"timestamp":"2016-03-21T13:00:00.000000+0000","input":"2"},
                {"timestamp":"2016-07-08T00:00:00.000000+0000","input":"4"},
                {"timestamp":"2016-05-08T00:00:00.000000+0000","input":"3"},
                {"timestamp":"2017-07-08T00:00:00.000000+0000","input":"6"},
                {"timestamp":"2017-12-08T00:00:00.000000+0000","input":"9"},
                {"timestamp":"2016-03-21T12:05:00.000000+0000","input":"0"},
                {"timestamp":"2017-08-08T00:00:00.000000+0000","input":"7"},
                {"timestamp":"2016-03-21T12:06:00.000000+0000","input":"1"},
                {"timestamp":"2017-11-08T00:00:00.000000+0000","input":"8"},
                ]
        # Sort the list
        jsonify.sortData(testVals)
        for i in range(10):
            self.assertEqual(testVals[i]["input"], str(i))

    def testExportJSON(self):
        exportString = "testData/exportedFile.json"
        testData = {"0":[1,2,3],"1":["more data"],"2":["a","b"]}
        jsonify.saveAsJSON(exportString,testData)
        with open("testData/exportedFile.json", "r") as f:
            self.assertEqual(json.load(f), testData)

    def testUserSessions(self):
        self.maxDiff = None
        testData = {
                "0": [
                    {"timestamp":"2016-10-08T12:00:00.000000+0000","input":"session 1"},
                    {"timestamp":"2016-10-08T12:03:00.000000+0000","input":"session 1"},
                    {"timestamp":"2016-10-08T12:12:59.000000+0000","input":"session 1"},
                    {"timestamp":"2016-10-08T12:52:59.000000+0000","input":"session 2"},
                    ],
                "1": [
                    {"timestamp":"2016-10-08T15:00:00.000000+0000","input":"session 1"}
                    ]
                }
        expectedOut = {
                "0": [
                    {
                        "start":"2016-10-08T12:00:00.000000+0000",
                        "end":"2016-10-08T12:12:59.000000+0000",
                        "inputs":3,
                        "duration (s)":779.0
                    },
                    {
                        "start":"2016-10-08T12:52:59.000000+0000",
                        "end":"2016-10-08T12:52:59.000000+0000",
                        "inputs":1,
                        "duration (s)":0.0
                    },
                    ],
                "1": [
                    {
                        "start":"2016-10-08T15:00:00.000000+0000",
                        "end":"2016-10-08T15:00:00.000000+0000",
                        "inputs":1,
                        "duration (s)":0.0
                        }
                    ]
                }
        self.assertEqual(jsonify.userSessions(testData),expectedOut)

