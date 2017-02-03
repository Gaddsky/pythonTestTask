## File operations tests


#### TC001 Create a file

The test verifies possibility to create a new file

###### Steps:
1. Generate a random filename
2. Create a file
3. Check if a file with the filename created in Step 1 exists

###### Expected results:
The file was created


#### TC002 Delete an existing file

The test verifies possibility to delete an existing file

###### Steps:
1. Create a new file
2. Check that the file has been created
3. Delete the file
4. Check that the file has been deleted

###### Expected results:
The created file is absent in the folder's file list (has been deleted)


#### TC003 Delete not existing file

The test verifies that an attempt to delete not existing file rises an exception

###### Steps:
1. Generate a name of not existing file
2. Try to delete file with the name from Step 1

###### Expected results:
Rising exception "FileNotFoundError"


#### TC004 Write to a file

The test verifies correctness of writing to a file

###### Steps:
1. Prepare a randomly generated string
2. Create a file containing the string from Step 1
3. Read the file content
4. Compare the file content and the string from Step 1

###### Expected results:
The file content and the string from Step 1 are equal

#### TC005 Rename a file

The test verifies correctness of a file renaming

###### Steps:
1. Prepare a randomly generated string
2. Prepare an initial filename and a new filename
3. Create a file with the initial filename from Step 2 and containing the string from Step 1
4. Rename file from the initial name to the new name from Step 2
5. Read the content of the file with the new name
6. Compare the read file content and the string from Step 1

###### Expected results:
Content of the file from Step 5 and the string from Step 1 are equal


## File attributes operations tests

#### TC101 Run a file with the executable bit not set

The test verifies, that it's not possible to run a file with the executable bit not set

###### Steps:
1. Create a file containing a shell-script
2. Change permissions of the file: the current user is the file owner, the executable bit is not set
3. Check possibility to run the script with os.access()
4. Try to run the script

###### Expected results:
1. os.access() from Step 3 return False
2. The attempt to run the script rises the "PermissionError" exception


#### TC102 Run a file with executable bit set

The test verifies possibility to run a file with the executable bit set

###### Steps:
1. Prepare a randomly generated string
2. Create a file containing a shell-script, which writes the string from Step 1 to the console
3. Change the file permissions: the current user is the file owner, the executable bit is set
4. Run the script
5. Read the output of the script

###### Expected results:
The output of the shell-script from Step 2 and the string from Step 1 are equal


#### TC103 Write to a file without write permissions

The test verifies that it's not possible to write to a file without write permission

###### Steps:
1. Create a new file
2. Change permissions of the file: the current user has the permission to read, not to write
3. Write to the file

###### Expected results:
The attempt to write to the file rises the exception "PermissionError"


#### TC104 Read from a file without read permissions

The test verifies that it's not possible to read from a file without the read permission

###### Steps:
1. Create a new file with a some content
2. Change permissions of the file: the current user has the permission to write, not to read
3. Read the file

###### Expected results:
Attempt to read from the file rises the exception "PermissionError"

## NFSv4 ACL operations tests

#### TC201 NFSv4 ACL: deny reading a file to its owner

This test verifies that a user cannot read a file without the read permission

###### Steps:
1. Create a new file with some content
2. Change permissions of the file: deny reading the file to the current user
3. Try to read the file

###### Expected results:
Attempt to read the file rises the exception "PermissionError"

#### TC202 NFSv4 ACL: deny writing to a file to its owner

This test verifies that the user cannot write to a file without the write permission

###### Steps:
1. Create a new file
2. Change permissions of the file: deny writing to the file to the current user
3. Try to write to the file

###### Expected results:
Attempt to write to the file rises the exception "PermissionError"
