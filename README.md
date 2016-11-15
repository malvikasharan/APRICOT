[![Latest Version](https://img.shields.io/pypi/v/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![License](https://img.shields.io/pypi/l/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![DOI](https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg)](https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT)
[![](https://images.microbadger.com/badges/version/malvikasharan/apricot.svg)](https://microbadger.com/images/malvikasharan/apricot "Get your own version badge on microbadger.com")

![alt tag](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_logo.png)

###A tool for sequence-based identification and characterization of protein classes

[APRICOT](http://malvikasharan.github.io/APRICOT/) is a computational pipeline for the identification of specific functional classes of interest in large protein sets. The pipeline uses efficient sequence-based algorithms and predictive models like signature motifs of protein families for the characterization of user-provided query proteins with specific functional features. The dynamic framework of APRICOT allows the identification of unexplored functional classes of interest in the large protein sets or the entire proteome.

####Authors and Contributors

The tool is designed and developed by Malvika Sharan in the lab of Prof. Dr. Jörg Vogel and Dr. Ana Eulalio in the Institute for Molecular Infection Biology at the University of Würzburg. Dr. Konrad Förstner contributed to the project by providing important technical supervision and discussions. The authors are grateful to Prof. Thomas dandekar, Dr. Charlotte Michaux, Caroline Taouk and Dr. Lars Barquist for critical discussions and feedback.

####Source code

The source codes of APRICOT are available via git https://github.com/malvikasharan/APRICOT and pypi https://pypi.python.org/pypi/bio-apricot.

APRICOT is open source software and is available under the ISC license.

Copyright (c) 2011-2016, Malvika Sharan, <malvika.sharan@uni-wuerzburg.de>

###Detailed documentations

1. [Overview of the pipeline](https://github.com/malvikasharan/APRICOT/blob/master/documentation/pipeline_overview.md)
1. [Tutorial](https://github.com/malvikasharan/APRICOT/blob/master/documentation/APRICOT_tutorial.md)
1. [Working with Docker](https://github.com/malvikasharan/APRICOT/blob/master/documentation/docker.md)
1. [Instructions for local installation](https://github.com/malvikasharan/APRICOT/blob/master/documentation/local_installation.md)
1. [Tools and data dependencies](https://github.com/malvikasharan/APRICOT/blob/master/documentation/software_dependencies.md)
1. [Different subcommands](https://github.com/malvikasharan/APRICOT/blob/master/documentation/subcommands.md)
1. [For the developers](https://github.com/malvikasharan/APRICOT/blob/master/documentation/for_the_developers.md)
1. [Troubleshoot](https://github.com/malvikasharan/APRICOT/blob/master/documentation/troubleshooting.md)
1. [Frequently asked questions](https://github.com/malvikasharan/APRICOT/blob/master/documentation/FAQs.md)
1. [License](https://github.com/malvikasharan/APRICOT/blob/master/LICENSE.md)
1. [Changelogs](https://github.com/malvikasharan/APRICOT/blob/master/CHANGELOGS.txt)
1. [Contact](https://github.com/malvikasharan/APRICOT/blob/master/documentation/contact.md)


###Get APRICOT software 

APRICOT is implemented in Python as a standalone and is executable on Ubuntu (and other debian-based) systems.

####APRICOT Docker image

We recommend users to install Docker software in their system to use the [docker images](https://hub.docker.com/r/malvikasharan/). 

In order to work with the Docker image for APRICOT, please follow these directions:

**1. Get Docker image**

  The image can be acquired by simply using this command:

  ```
  $ docker pull malvikasharan/apricot
  ```

**2. Create the Docker container for testing the software**
  
  ```
  $ docker run -it malvikasharan/apricot bash
  ```
  
  Here is a quick way to test if different modules work in your system (without really installing the complete filesystem).
  
  **Run the analysis in the `home` folder**
  
  ```
  $ cd home
  $ apricot -h
  ```
  
   **Run test/example analysis**
  
   The git repository contains a shell script [APRICOT/shell_scripts/run_example.sh](https://github.com/malvikasharan/APRICOT/blob/master/shell_scripts/run_example.sh) with shell commands that can be used for the demonstration of APRICOT installation including analysis with an example. 

  ```
  $ wget https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/run_example.sh
  $ sh run_example.sh
  ```
  
  By default, this script generates a main analysis folder `APRICOT_analysis` and several sub-directories. To understand each components of the software and generated results, We recomend you to check out the [tutorial](https://github.com/malvikasharan/APRICOT/blob/master/documentation/APRICOT_tutorial.md).

**3. Get the supporting data required for running your queries**

  Users are required to establish a directory `source_files` containing all the [required files](https://github.com/malvikasharan/APRICOT/blob/master/documentation/database_dependencies.md), which can be set-up as shown below inside the docker container (in the `home` folder) or in the local system (in that case exit the Docker container by `exit`):

  ```
  $ wget http://data.imib-zinf.net/APRICOT-supporting_dataset.zip
  $ unzip APRICOT-supporting_dataset.zip
  ```

  Alternatively, these files can be installed/downloaded using the script docker_support.sh provided in the git repository of APRICOT.

  ```
  $ wget https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/docker_support.sh
  $ sh docker_support.sh
  ```

**4. Using the supporting data from the local system (Recommended)**
    
  When the directory `source_files` is set-up in the local system, use the following command to mount the directory `source_file` into the Docker container (provide full path for $FULL_PATH_SOURCE_FILES):

  ```
  $ docker run -it -v /{$FULL_PATH_SOURCE_FILES}/source_files/:/home/source_files malvikasharan/apricot bash
  $ cd home
  ```
  
**5. Carry out analysis by APRICOT**
  ```
  $ wget -N https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/run_example.sh
  $ sh run_example.sh
  ```
  For further details, please check the [Tutorial](https://github.com/malvikasharan/APRICOT/blob/master/documentation/APRICOT_tutorial.md) and [Tools and data dependencies](https://github.com/malvikasharan/APRICOT/blob/master/documentation/software_dependencies.md)

###Alternative ways to install APRICOT

####Locally install the software using pip

In order to work with locally installed software, follow these instructions.

1. Make sure that your system has pip and git installed 

  ````
  $ apt-get install python3-pip git 
  ````

2. Then install APRICOT via pip (NOTE: this doesn't install the complete filesystem):

  ````
  $ pip3 install bio-apricot 
  ````

  This will globally install APRICOT, which can be called via the command `apricot`, and the libraries from apricotlib will be saved.
  Follow the above listed points 3 & 5 to execute the software as shown above.
###OR

####Get APRICOT manually

APRICOT is implemented in Python3 and can be executed in Linux/Unix system. APRICOT requires few third party packages, namely [Biopython](http://biopython.org/wiki/Main_Page), [BLAST executables](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download), [interproscan](https://www.ebi.ac.uk/interpro/interproscan.html), python libraries like [Matplotlib](http://matplotlib.org/), [requests](https://pypi.python.org/pypi/requests), openpyxl and other required tools.

Follow these instructions to manually establish the software locally.

1. Get the python dependencies

  ````
  $ apt-get install python3-matplotlib python3-numpy python3-scipy python3-biopython python3-requests --yes --fix-missing
  $ pip3 install openpyxl
  ````

2. Get the repository for APRICOT from git either by clicking [here](https://github.com/malvikasharan/APRICOT/archive/master.zip) or locally cloned by using the following command:

  ```
  $ git clone https://github.com/malvikasharan/APRICOT.git
  ```  
  Follow the above listed points 3 & 5 to execute the software as shown above.

###Hint:

When installed locally, the location of the executable will be: /home/username/.local/bin/
and the library location will be: /home/username/.local/lib/python3.5/site-packages/apricotlib/

In that case, when calling the software (also edit the path when using the shell script run_example.sh and system_test.sh), please use the complete path name rather than using `apricot`, which will look for a globally installed software.

When using `--user` flag for a local installation `$ pip3 install --user bio-apricot`, please check the paths for the executable and the libraries.
