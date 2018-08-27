import unittest
import log_to_tutorial_matcher

class TestLogToTutorialClass(unittest.TestCase):

    def testIdenticalMatch(self):
        helpDir={"Elephants":"Return This", "Giraffes":"Don't Return This"}
        testInput = {"timestamp":"doesn't matter","input":"Elephants"}
        self.assertEqual(
                log_to_tutorial_matcher.findSimilar(testInput,helpDir),
                "Return This"
                )

    def testSimilarMatch(self):
        helpDir={"Elephants":"Return This", "Giraffes":"Don't Return This"}
        testInput = {"timestamp":"doesn't matter","input":"lepants"}
        self.assertEqual(
                log_to_tutorial_matcher.findSimilar(testInput,helpDir),
                "Return This"
                )

    def testSimilarLogOutput(self):
        helpDir={"Elephants":"Return This", "Giraffes":"Don't Return This"}
        testInput = {"timestamp":"doesn't matter","input":"let {} in lepants"}
        self.assertEqual(
                log_to_tutorial_matcher.findSimilar(testInput,helpDir),
                "Return This"
                )
