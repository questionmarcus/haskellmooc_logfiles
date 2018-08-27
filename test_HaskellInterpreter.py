import unittest
import HaskellInterpreter

class HaskellInterpreterTestClass(unittest.TestCase):
    
    def testHaskellMaths(self):
        shell = HaskellInterpreter.HaskellInterpreter()
        shellOut = shell.runLine("2+2")
        shell.endProcess()
        self.assertEqual(shellOut, "Just 4")

    def testHaskellPrint(self):
        shell = HaskellInterpreter.HaskellInterpreter()
        shellOut = shell.runLine('\"Hello, World\"')
        shell.endProcess()
        self.assertEqual(shellOut, 'Just "Hello, World"')

    def testFailOutputCapture(self):
        shell = HaskellInterpreter.HaskellInterpreter()
        shellOut = shell.runLine('sum "test"')
        shell.endProcess()
        self.assertTrue("No instance for (Num Char) arising from a use of ‘sum’" in shellOut)

    def testTimeoutForInfiniteLoop(self):
        shell = HaskellInterpreter.HaskellInterpreter()
        shellOut = shell.runLine('let answer = answer * answer in answer')
        shell.endProcess()
        self.assertEqual(shellOut, "Nothing")
