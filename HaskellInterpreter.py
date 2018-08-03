import pexpect

class HaskellInterpreter:

    def __init__(self):
        self._shell = pexpect.spawnu("ghci")
        self._prelude = "Prelude System.Timeout> "
        self.__init_shell__()

    def __init_shell__(self):
        self._shell.expect("Prelude>")
        self._shell.sendline("import System.Timeout")
        self._shell.expect("Prelude System.Timeout>")

    def runLine(self, code):
        self._shell.sendline("timeout 2000000 (return $! "+code+")")
        self._shell.readline()
        self._shell.expect(self._prelude)
        return self._shell.before
