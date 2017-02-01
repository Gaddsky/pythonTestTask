#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import sys
import logging

# search testing path in command-line arguments
for arg in sys.argv:
    if os.path.isdir(arg):
        base_dir_name = arg
        break
    else:
        base_dir_name = os.getcwd()  # default folder - current working folder


def main():
    """Main function where tests are run"""

    from tests import testFileOperations
    from tests import testFileAttributes

    logging_setup()

    loader = unittest.TestLoader()

    suite = loader.loadTestsFromModule(testFileOperations)
    suite.addTests(loader.loadTestsFromModule(testFileAttributes))

    runner = CustomTextTestRunner(verbosity=2)
    result = runner.run(suite)
    write_results_to_log(result)


def logging_setup():
    """Logging setup

    Two levels of logging are used:
        1. Usual log, if no additional arguments in the command line
        2. Debug log, if "--debug" argument is in the command line
    In the usual log case only errors and short summary are written in the logfile. Debug log uses more verbose log.
    Two handlers are used:
        1. Stream handler with log level INFO for output in console
        2. File handler with log level INFO (usual log) or DEBUG (debug log)
    """
    message_format = '%(asctime)s %(levelname)s %(message)s'  # Log message format
    if '--debug' in sys.argv:  # "--debug" command line argument, log level is set to DEBUG
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO  # usual log, log level is set to INFO

    stream_handler = logging.StreamHandler()  # Stream handler, log level is INFO
    stream_handler.setLevel(logging.INFO)

    logging.basicConfig(level=log_level,
                        format=message_format,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler(os.path.join(os.getcwd(), "log.txt"), mode='w'),
                                  stream_handler]
                        )


def write_results_to_log(result):
    """Writes results in the end of testing to the log file in the sorted order"""

    for i in sorted(result.test_results, key=lambda description: description[0].shortDescription()):
        logging.info('{:.<60}'.format(i[0].shortDescription()) + i[1])


class CustomTestResult(unittest.TestResult):
    """Overrides unittest.TestResult for custom test report"""
    test_results = []

    def addSuccess(self, test):  # Called when the test passed
        self.test_results.append((test, "Success"))
        logging.debug("Test passed\n")

    def addFailure(self, test, err):  # Called when the test failed
        self.test_results.append((test, "Failed"))
        logging.error(test.shortDescription() + "\n" + str(err))
        logging.debug("Test failed\n")


class CustomTextTestRunner(unittest.TextTestRunner):
    """Overrides unittest.TextTestRunner; returns CustomTestResult instance"""
    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)


if __name__ == "__main__":
    main()
