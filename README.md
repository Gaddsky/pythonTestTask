# pythonTestTask

This test suite consists of some tests of NFSv4 file system. This tests are divided into three groups:  
1. Testing some file operations  
2. Testing some file attributes operations  
3. Testing some operations with NFSv4 ACL  

This test suite has been checked in Ubuntu 16.04 using Python 3.5.2.
It must be runnable in other Linux distributive and with other versions of Python 3.

### Prerequisites
To run the test suite at a local computer several packages must be installed (for Ubuntu 16.04):  
1. `nfs-kernel-server`  
2. `nfs-common`  
3. `nfs4-acl-tools` (utilities `nfs4_setfacl` and `nfs4_getfacl` are used)  

This test suite has been run with the following content of `/etc/exports`:  
`/opt/testnfs 127.0.0.1(rw)` 
 
Current user must have read/write permissions in `/opt/testnfs` 

NFS server must be started. Also you must mount NFS-filesystem using the following command:  
`sudo mount 127.0.0.1:/opt/testnfs {path-to-your-mount-point}`

You can use a NFS folder from remote computer, it requires other actions.

### Run the test suite
To run the test suite from the project folder run:  
`python3 pythonTestTask.py [path-to-nfs-mount-point] [--debug]`


`--debug` option will cause more verbose output in the log-file.
Without this option only the results of the tests will be in the log-file.  
If `path-to-nfs-mount-point` is not used, the tests will be run in the test suite's folder (in local file system
it will cause failure of the NFS ACL tests).

### Test documentation
The test documentation where the test-cases are described is located in `test_documentation.md` file.




