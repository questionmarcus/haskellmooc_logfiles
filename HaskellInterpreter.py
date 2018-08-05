import pexpect
from re import sub

class HaskellInterpreter:
    """
    This class acts as proxy for running Haskell code in from python.

    It works by creating an instance of the haskell interactive compiler (ghci)
    which can then run lines of input which this class will then capture the output
    of and return it.

    The instance of ghci that is run involves using the System.Timeout library
    so that infinite loops are not run.

     - In the case that the code ran successfully the return will be "Just" followed
        by the output.
     - When the code times out it will return "Nothing".
     - When an error is encountered, it will return the entire error message from
        ghci.

    """

    def __init__(self):
        self._shell = pexpect.spawnu("ghci")
        self._prelude = "Prelude System.Timeout> "
        self.__init_shell__()

    def __init_shell__(self):
        self._shell.expect("Prelude>")
        self._shell.sendline("import System.Timeout")
        self._shell.expect("Prelude System.Timeout>")

    def runLine(self, code):
        """
        This method passes on the line of input to the ghci and returns the shell's
        output
        """
        print("Processing: "+code)
        self._shell.sendline("timeout 2000000 (return $! "+code+")")
        self._shell.readline()
        try:
            self._shell.expect(self._prelude,timeout=5)
        except pexpect.TIMEOUT:
            self._shell.sendcontrol("c")
            self._shell.expect(self._prelude)
            return "Timeout"
        return sub("(\\x1b|\\r|\\n|\[.{1,2}m|\[\?1.{3})", "",self._shell.before)

    def endProcess(self):
        self._shell.kill(0)
