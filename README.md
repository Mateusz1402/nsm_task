# NMS DevOps Intern Programming Task
<pre>
Author: Mateusz Sabat      
        mateusz.sabat38@gmail.com
</pre>

## The purpose

The project purpose is to design and implement a program based on Python for generating 'manifest' files in specified directory.

The program has to work inside the AlmaLinux container. 
In addition, data integral veryfication should be done by SHA256.



## The technology used in the project

- Python 3.13,
- Docker
- AlmaLinux 9



## Workflow

* **1**<br>
        Design the project structure and requirements.

* **2**<br>
        Implement the 'get_hash()' for generating unique SHA256 hash, based on the input directory file. 
        Testing the functionality of created function.


* **3**<br>
        Implement the main() program: inserting the argument; searching all files (starting from input directory); type of input parameter control logic and type of searched file control logic; appending the desired list with file directory and the SHA256 hash.<br>

        Testing Procedures

        To ensure the reliability and security of the manifest program, the following testing scenarios were performed: 
        - Hash verification: manual verification using the system tool 'sha256sum',

        - Empty directory: verified that the tool handles directories with no files without crashing,

        - Large file: create a 100MB dummy file to ensure  the 4096 bytes buffering prevent memory overflow,

        - File with spaces: the program correctly add the direcotry into " ",

        - Special characters: used polish characters to ensure encoding stability,

        - Deep nesting: creates the sub, sub-folder to find out the program reaction. It correctly go inside. 

        - Symlink links outside: program correctly handle an error of poining a file that is outside valid directory area.


* **4**<br>
        Implement the verify_manifest() function: function compare all hash codes from existed manifest file with a new ones. In case of mismatch of any pair, the result is Failed.
        Old main logic goes into generate_manifest(), to clear the code layout. The verification feature was tested and passed the tests.<br>

        Testing Procedures

        Generating new manifest file, change a single char or add additional space inside test's file. After running the verification, the program returns the fail. In other case (not performing any changes) the result is OK.


* **5**<br>
        Uses almalinux/9-base to meet the OS requirements and install Python inside repository. The previous logic has been copied inside. 
        Implement bash scrip, to meet the functionality of running the logic. Configured a check of docker/podman, relative paths convertion and read-only flag.
        The output volume enables mounting the host's current working directory inside the container.
        The script uses a bash array OTHER_ARGS to capture additional flags (--check). 


