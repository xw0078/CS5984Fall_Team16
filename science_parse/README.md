## Single script to completely set-up science-parse on remote server (with dependencies)

### Benefits:
One single unified shell script to completely setup science-parse on a remote server without needing sudo access.

### Hardware Requirements:
1. Needs internet access on the remote server.
2. For parsing PDFs, science-parse needs 6 gb of memory (RAM), which is usually easily available on VT's ARC cluster.
3. Needs less than 5 gb of disk space for models.

### Steps to setup science-parse:
1. ``scp setup_science_parse.sh vt_pid@cascades1.arc.vt.edu:~``
2. ``ssh vt_pid@cascades1.arc.vt.edu`` 
2. ``sudo chmod +x setup_science_parse.sh``
3. ``./setup_science_parse.sh``. This will need internet access so run it on a login node of ARC. Should take less than 30 minutes.

### Steps to run science-parse for a single pdf:
1. ``module load jdk/1.8.0u172``
2. ``java -Xmx6g -jar ~/science-parse/cli/target/scala-2.11/science-parse-cli-assembly-2.0.2-SNAPSHOT.jar <path_to_your_pdf>``

### Steps to run for multiple pdfs:
1. ``module load jdk/1.8.0u172``
2. ``java -Xmx6g -jar ~/science-parse/cli/target/scala-2.11/science-parse-cli-assembly-2.0.2-SNAPSHOT.jar -p <path_to_the_folder_with_PDFs> -o <output_directory_path>`` 

### Help:
1. ``module load jdk/1.8.0u172``
2. ``java -Xmx6g -jar ~/science-parse/cli/target/scala-2.11/science-parse-cli-assembly-2.0.2-SNAPSHOT.jar --help``
