import unittest
import shutil
import os
import logging
import uuid

from pythonTestTask import base_dir_name


class TestNfs4Acl(unittest.TestCase):
    """NFSv4 ACL operations tests"""

    dirname = os.path.join(base_dir_name, "test-" + str(uuid.uuid4()))  # folder to run tests

    @classmethod
    def setUpClass(cls):
        os.mkdir(cls.dirname)
        logging.debug("Starting test group: " + str(TestNfs4Acl.__doc__.split('\n', 1)[0]))
        logging.debug("Test folder " + cls.dirname + "\n")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dirname)

    def test_deny_read_permission(self):
        """TC201 NFSv4 ACL: deny reading a file to its owner

        This test verifies that a user cannot read a file without the read permission

        Steps:
            1. Create a new file with some content
            2. Change permissions of the file: deny reading the file to the current user
            3. Try to read the file

        Expected results:
            Attempt to read the file rises the exception "PermissionError"
        """
        logging.debug("Starting test: " + str(self.test_deny_read_permission.__doc__.split('\n', 1)[0]))

        # generate the string
        string = str(uuid.uuid4())
        logging.debug("Expected string: " + string)

        # generate the filename
        filename = "not_read_file-" + str(uuid.uuid4())
        logging.debug("New file name: " + os.path.join(self.dirname, filename))

        # prepare the file for the test
        with open(os.path.join(self.dirname, filename), mode='w') as file:
            file.write(string)

        logging.debug("ACL for a file before changing permissions:\n"
                      + str(os.popen("nfs4_getfacl " + os.path.join(self.dirname, filename)).read().strip()))

        # change NFSv4 ACL permission to deny reading to the file owner
        os.system("nfs4_setfacl -a D::OWNER@:R " + os.path.join(self.dirname, filename))

        logging.debug("ACL for a file after changing permissions:\n"
                      + str(os.popen("nfs4_getfacl " + os.path.join(self.dirname, filename)).read().strip()))

        # try to read the file
        with self.assertRaises(PermissionError):
            with open(os.path.join(self.dirname, filename), mode='r') as file:
                file.read()

    def test_deny_write_permission(self):
        """TC202 NFSv4 ACL: deny writing to a file to its owner

        This test verifies that the user cannot write to a file without the write permission

        Steps:
            1. Create a new file
            2. Change permissions of the file: deny writing to the file to the current user
            3. Try to write to the file

        Expected results:
            Attempt to write to the file rises the exception "PermissionError"
        """
        logging.debug("Starting test: " + str(self.test_deny_write_permission.__doc__.split('\n', 1)[0]))

        # generate the string
        string = str(uuid.uuid4())
        logging.debug("Expected string: " + string)

        # generate the filename
        filename = "not_write_file-" + str(uuid.uuid4())
        logging.debug("New file name: " + os.path.join(self.dirname, filename))

        # prepare the file for the test
        open(os.path.join(self.dirname, filename), mode='x').close()

        logging.debug("ACL for a file before changing permissions:\n"
                      + str(os.popen("nfs4_getfacl " + os.path.join(self.dirname, filename)).read().strip()))

        # change NFSv4 ACL permission to deny writing to the file owner
        os.system("nfs4_setfacl -a D::OWNER@:W " + os.path.join(self.dirname, filename))

        logging.debug("ACL for a file after changing permissions:\n"
                      + str(os.popen("nfs4_getfacl " + os.path.join(self.dirname, filename)).read().strip()))

        # try to write to the file
        with self.assertRaises(PermissionError):
            with open(os.path.join(self.dirname, filename), mode='w') as file:
                file.write(string)


if __name__ == '__main__':
    unittest.main()
