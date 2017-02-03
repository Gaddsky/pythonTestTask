#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import uuid
import unittest
import logging

from pythonTestTask import base_dir_name


class TestFileOperations(unittest.TestCase):
    """File operations"""

    dirname = os.path.join(base_dir_name, "test-" + str(uuid.uuid4()))

    @classmethod
    def setUpClass(cls):
        os.mkdir(cls.dirname)
        logging.debug("Starting test group: " + str(TestFileOperations.__doc__.split('\n', 1)[0]))
        logging.debug("Test folder " + cls.dirname + "\n")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dirname)

    def test_create_file(self):
        """TC001 Create a file

        The test verifies possibility to create a new file

        Steps:
            1. Generate a random filename
            2. Create a file
            3. Check if a file with the filename created in Step 1 exists

        Expected results:
            The file was created
        """
        logging.debug("Starting test: " + str(self.test_create_file.__doc__.split('\n', 1)[0]))

        # generating a filename
        filename = "new_file-" + str(uuid.uuid4())
        logging.debug("New file name: " + os.path.join(self.dirname, filename))

        # file creating
        open(os.path.join(self.dirname, filename), mode='x').close()
        logging.debug("File created: " + str(os.path.isfile(os.path.join(self.dirname, filename))))

        # check if a file was created
        self.assertTrue(os.path.isfile(os.path.join(self.dirname, filename)))

    def test_delete_file(self):
        """TC002 Delete an existing file

        The test verifies possibility to delete an existing file

        Steps:
            1. Create a new file
            2. Check that the file has been created
            3. Delete the file
            4. Check that the file has been deleted

        Expected results:
            The created file is absent in the folder's file list (has been deleted)
        """
        logging.debug("Starting test: " + str(self.test_delete_file.__doc__.split('\n', 1)[0]))

        # file creating
        filename = "new_file-" + str(uuid.uuid4())
        logging.debug("New file name: " + os.path.join(self.dirname, filename))
        open(os.path.join(self.dirname, filename), mode='x').close()

        # check assert, that this file has been really created
        logging.debug("File created: " + str(os.path.isfile(os.path.join(self.dirname, filename))))
        self.assertTrue(os.path.isfile(os.path.join(self.dirname, filename)), "File was not created!!!")

        # delete file
        os.remove(os.path.join(self.dirname, filename))
        logging.debug("File exists after deleting: " + str(os.path.isfile(os.path.join(self.dirname, filename))))

        # check the file is absent in the folder's file list
        self.assertNotIn(filename, os.listdir(self.dirname))

    def test_delete_not_existing_file(self):
        """TC003 Delete not existing file

        The test verifies that an attempt to delete not existing file rises an exception

        Steps:
            1. Generate a name of not existing file
            2. Try to delete file with the name from Step 1

        Expected results:
            Rising exception "FileNotFoundError"
        """
        logging.debug("Starting test: " + str(self.test_delete_not_existing_file.__doc__.split('\n', 1)[0]))

        # creating filename
        filename = "not-exist-file" + str(uuid.uuid4())
        logging.debug("Not exist file name: " + os.path.join(self.dirname, filename))
        logging.debug("File exists: " + str(os.path.isfile(os.path.join(self.dirname, filename))))

        # try to delete non existing file
        with self.assertRaises(FileNotFoundError):
            os.remove(os.path.join(self.dirname, filename))

    def test_write_to_file(self):
        """TC004 Write to a file

        The test verifies correctness of writing to a file

        Steps:
            1. Prepare a randomly generated string
            2. Create a file containing the string from Step 1
            3. Read the file content
            4. Compare the file content and the string from Step 1

        Expected results:
            The file content and the string from Step 1 are equal
        """

        logging.debug("Starting test: " + str(self.test_write_to_file.__doc__.split('\n', 1)[0]))

        # prepare the string
        string = str(uuid.uuid4())
        logging.debug("Expected string: " + string)

        # prepare the filename
        filename = "wright_to_file-" + str(uuid.uuid4())
        logging.debug("New file name: " + os.path.join(self.dirname, filename))

        # create a file containing the string
        with open(os.path.join(self.dirname, filename), mode='w') as file:
            file.write(string)
        logging.debug("File exist: " + str(os.path.isfile(os.path.join(self.dirname, filename))))

        # read the file content and compare with the initial string
        read_string = open(os.path.join(self.dirname, filename), mode='r').read()
        logging.debug("Read string: " + read_string)
        self.assertEqual(string, read_string)

    def test_file_renaming(self):
        """TC005 Rename a file

        The test verifies correctness of a file renaming

        Steps:
            1. Prepare a randomly generated string
            2. Prepare an initial filename and a new filename
            3. Create a file with the initial filename from Step 2 and containing the string from Step 1
            4. Rename file from the initial name to the new name from Step 2
            5. Read the content of the file with the new name
            6. Compare the read file content and the string from Step 1

        Expected results:
            Content of the file from Step 5 and the string from Step 1 are equal
        """

        logging.debug("Starting test: " + str(self.test_file_renaming.__doc__.split('\n', 1)[0]))

        # prepare the string
        string = str(uuid.uuid4())
        logging.debug("Expected string: " + string)

        # prepare the file names
        initial_name = "initial_name-" + str(uuid.uuid4())
        new_name = "new_name-" + str(uuid.uuid4())
        logging.debug("Initial filename: " + os.path.join(self.dirname, initial_name))
        logging.debug("New filename: " + os.path.join(self.dirname, new_name))

        # create the initial file
        with open(os.path.join(self.dirname, initial_name), mode='w') as file:
            file.write(string)
        logging.debug("File with the initial name exists: " + str(os.path.isfile(os.path.join(self.dirname, initial_name))))
        logging.debug("File with the new name exists: " + str(os.path.isfile(os.path.join(self.dirname, new_name))))

        # rename the file
        os.rename(os.path.join(self.dirname, initial_name), os.path.join(self.dirname, new_name))
        logging.debug(
            "File with the initial name after renaming exist: "
            + str(os.path.isfile(os.path.join(self.dirname, initial_name))))
        logging.debug("File with the new name after renaming exist: "
                      + str(os.path.isfile(os.path.join(self.dirname, new_name))))

        # check that the content of the file with the new name and the generated string are equal
        read_string = open(os.path.join(self.dirname, new_name), mode='r').read()
        logging.debug("Read string: " + read_string)
        self.assertEqual(string, read_string)


if __name__ == '__main__':
    unittest.main()
