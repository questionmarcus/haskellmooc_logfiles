#!/usr/bin/env python

import unittest

import test_anon
import test_HaskellInterpreter
import test_jsonify
import test_log_to_tutorial

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_anon))
suite.addTests(loader.loadTestsFromModule(test_HaskellInterpreter))
suite.addTests(loader.loadTestsFromModule(test_jsonify))
suite.addTests(loader.loadTestsFromModule(test_log_to_tutorial))

runner = unittest.TextTestRunner()
result = runner.run(suite)
