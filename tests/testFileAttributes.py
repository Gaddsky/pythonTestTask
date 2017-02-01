#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import shutil
import uuid
import stat
import subprocess
import logging

from pythonTestTask import base_dir_name


class TestFileAttributes(unittest.TestCase):
    """File attributes operations"""

    dirname = os.path.join(base_dir_name, "test-" + str(uuid.uuid4()))  # folder to run tests

    @classmethod
    def setUpClass(cls):
        os.mkdir(cls.dirname)
        logging.debug("Starting test group: " + str(TestFileAttributes.__doc__.split('\n', 1)[0]))
        logging.debug("Test folder " + cls.dirname + "\n")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dirname)

    def test_executable_bit_not_set(self):
        """TC101 Run a file with the executable bit not set

        The test verifies, that it's not possible to run a file with the executable bit not set

        Steps:
            1. Create a file containing a shell-script
            2. Change permissions of the file: the current user is the file owner, the executable bit is not set
            3. Check possibility to run the script with os.access()
            4. Try to run the script

        Expected results:
            1. os.access() from Step 3 return False
            2. The attempt to run the script rises the "PermissionError" exception
        """

        logging.debug("Starting test: " + str(self.test_executable_bit_not_set.__doc__.split('\n', 1)[0]))

        # generate the filename
        filename = "no_exec_file-" + str(uuid.uuid4())
        logging.debug("New file name: " + os.path.join(self.dirname, filename))

        # prepare the file for the test
        with open(os.path.join(self.dirname, filename), mode='w') as file:
            file.write("#!/bin/sh\necho test")
        logging.debug("File created: " + str(os.path.isfile(os.path.join(self.dirname, filename))))

        # make the current user the owner of the file (it affects to possibility to run the script)
        # the executable bit is not set
        os.chmod(os.path.join(self.dirname, filename), stat.S_IRUSR)
        logging.debug("File is executable: " + str(os.access(os.path.join(self.dirname, filename), os.X_OK)))

        # check result with os.access()
        self.assertFalse(os.access(os.path.join(self.dirname, filename), os.X_OK))
        # check that an attempt to run the script rises the exception
        with self.assertRaises(PermissionError):
            subprocess.Popen(os.path.join(self.dirname, filename))

    def test_set_executable_bit(self):
        """TC102 Run a file with executable bit set

        The test verifies possibility to run a file with the executable bit set

        Steps:
            1. Prepare a randomly generated string
            2. Create a file containing a shell-script, which writes the string from Step 1 to the console 
            3. Change the file permissions: the current user is the file owner, the executable bit is set
            4. Run the script
            5. Read the output of the script

        Expected results:
            The output of the shell-script from Step 2 and the string from Step 1 are equal
        """
        logging.debug("Starting test: " + str(self.test_set_executable_bit.__doc__.split('\n', 1)[0]))

        # generating the string
        string = str(uuid.uuid4())
        logging.debug("Expected string: " + string)

        # generating the filename
        filename = "exec_file-" + str(uuid.uuid4())
        logging.debug("New file name: " + os.path.join(self.dirname, filename))

        # prepare the file for the test
        with open(os.path.join(self.dirname, filename), mode='w') as file:
            file.write("#!/bin/sh\necho " + string)

        # make the current user the owner of the file (it affects to possibility to run the script)
        # and set the executable bit
        os.chmod(os.path.join(self.dirname, filename), stat.S_IXUSR | stat.S_IRUSR)
        logging.debug("File executable: " + str(os.access(os.path.join(self.dirname, filename), os.X_OK)))

        # read the output of the run script
        # 'output' variable contains newline-symbol, it needs to be deleted with strip()
        output = os.popen(os.path.join(self.dirname, filename)).read().strip()
        logging.debug("Output string: " + str(output))

        # check that the output of the run script and the generated string are equal
        self.assertEqual(string, output)

    def test_has_not_write_permission(self):
        """TC103 Write to a file without write permissions

        The test verifies that it's not possible to write to a file without write permission

        Steps:
            1. Create a new file
            2. Change permissions of the file: the current user has the permission to read, not to write
            3. Write to the file

        Expected results:
            The attempt to write to the file rises the exception "PermissionError"
        """
        logging.debug("Starting test: " + str(self.test_has_not_write_permission.__doc__.split('\n', 1)[0]))

        # generate the filename
        filename = "write_file-" + str(uuid.uuid4())
        logging.debug("New file name: " + os.path.join(self.dirname, filename))

        # create the file with the generated filename
        open(os.path.join(self.dirname, filename), mode='x').close()
        logging.debug("File created: " + str(os.path.isfile(os.path.join(self.dirname, filename))))

        # give the current user permission to read, not to write
        os.chmod(os.path.join(self.dirname, filename), stat.S_IRUSR)
        logging.debug("File has the write permission: " + str(os.access(os.path.join(self.dirname, filename), os.W_OK)))

        # try to write in the file
        with self.assertRaises(PermissionError):
            with open(os.path.join(self.dirname, filename), mode='w') as file:
                file.write(str(uuid.uuid4()))

    def test_has_not_read_permission(self):
        """TC104 Read from a file without read permissions

        The test verifies that it's not possible to read from a file without the read permission

        Steps:
            1. Create a new file with a some content
            2. Change permissions of the file: the current user has the permission to write, not to read
            3. Read the file

        Expected results:
            Attempt to read from the file rises the exception "PermissionError"
        """
        logging.debug("Starting test: " + str(self.test_has_not_read_permission.__doc__.split('\n', 1)[0]))

        # generate the filename
        filename = "read_file-" + str(uuid.uuid4())
        logging.debug("New file name: " + os.path.join(self.dirname, filename))

        # create the file with the generated filename
        with open(os.path.join(self.dirname, filename), mode='w') as file:
            file.write(str(uuid.uuid4()))
        logging.debug("File was created: " + str(os.path.isfile(os.path.join(self.dirname, filename))))

        # give the current user the permission to write, not to read
        os.chmod(os.path.join(self.dirname, filename), stat.S_IWUSR)
        logging.debug("File has the read permission: " + str(os.access(os.path.join(self.dirname, filename), os.R_OK)))

        # try to read from the file
        with self.assertRaises(PermissionError):
            with open(os.path.join(self.dirname, filename), mode='r') as file:
                file.read()
