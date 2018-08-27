import unittest
import anon

class AnonifyTestClass(unittest.TestCase):

    def testAnonifySingleFile(self):
        data = anon.main(["testData/fakeIPAddresses1.log"])
        for line in data:
            splitLine = line.split(" ")
            anonID = splitLine[3]
            expectID = splitLine[5]
            self.assertEqual(anonID, expectID)

    def testAnonifyMultiFile(self):
        data = anon.main(["testData/fakeIPAddresses1.log","testData/fakeIPAddresses2.log"])
        for line in data:
            splitLine = line.split(" ")
            anonID = splitLine[3]
            expectID = splitLine[5]
            self.assertEqual(anonID, expectID)
