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

We recommend users to [install Docker software](https://docs.docker.com/engine/installation/) in their system to use the [docker images](https://hub.docker.com/r/malvikasharan/). 

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

  Copy the script from the existing repository in the `home` folder.
  ```
  $ cp APRICOT/shell_scripts/run_example.sh .
  ```
  
  Or use `wget` to get the most updated version from the repository.
  ```
  $ wget https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/run_example.sh
  ```
  
  ...and run it.
  ```
  $ sh run_example.sh
  ```
  
  By default, this script generates a main analysis folder `APRICOT_analysis`. To understand the file structure, please see below (point-5). We recomend you to check out the [tutorial](https://github.com/malvikasharan/APRICOT/blob/master/documentation/APRICOT_tutorial.md) to understand each components of the software and the result generated by their analysis. 

**3. Get the supporting data required for running your queries**

  Users are required to set a directory `source_files` containing all the [required supporting data](https://github.com/malvikasharan/APRICOT/blob/master/documentation/database_dependencies.md), which can be setup in the local filesystem (recommended) or inside the docker container (in the home folder). See below for the details. 
  
  *Be aware that the supporting data is a collection of large datasets of size: ~15 G compressed, and ~50 G uncompressed.*
  
  **Options for installation**
  
  **1. In the local filesystem - RECOMMENDED** 
  
  This should be setup once (please exit the container using the command `exit` if already running it) and can be reused in different containers (shown in the point 4).
  
  This will ensure that users would not have to get these files every time a new Docker container for APRICOT is created. Moreover, this will keep the size of the container small by not having to setup the large databases inside the container.
  
  **2. Inside a new Docker conatiner**
  
  The supporting data can be used only inside the Docker container (every Docker container will need such setup individually).
  
  **Commands to acquire the supporting data**
  
  ```
  $ wget http://data.imib-zinf.net/APRICOT-supporting_dataset.zip
  $ unzip APRICOT-supporting_dataset.zip
  ```
  
  Alternatively, these files can be acquired using the script docker_support.sh provided in the git repository of APRICOT.

  ```
  $ cp APRICOT/shell_scripts/docker_support.sh .
  $ sh docker_support.sh
  ```

**4. Using the supporting data**
    
  When the directory `source_files` is located in the local system **(Recommended)**, use the following command to mount this directory into the Docker container (provide full path for $FULL_PATH_SOURCE_FILES):

  ```
  $ docker run -it -v /{$FULL_PATH_SOURCE_FILES}/source_files/:/home/source_files malvikasharan/apricot bash
  $ cd home
  ```
  
  Skip this step when working in the Docker container already.
  
**5. Carry out analysis by APRICOT**
  ```
  $ cp APRICOT/shell_scripts/run_example.sh .
  $ sh run_example.sh
  ```
  
  If the the analysis was successful, a directory `APRICOT_analysis` will be created, which contains following files with the outputs generated by different modules of the software.
  
  ```
  APRICOT_analysis
      └───├input                                  # Location used by subcommand 'query' to store all the related files
      └───├output
              └───├0_predicted_domains            # Location for the output data obtained from the subcommand 'predict'
              └───├1_compiled_domain_information  # Location for the output data obtained from the subcommand 'filter'          
              └───├2_selected_domain_information            
              └───├3_annotation_scoring           # Location for the output data obtained from the subcommand 'annoscore'
              └───├4_additional_annotations       # Location for additional annotations for the selected 
              |                                   # queries using subcommand 'addanno'
              └───├5_analysis_summary             # Location for the output data obtained from the subcommand 'summary'
              └───├format_output_data             # Location for the output data obtained from the subcommand 'format'
              └───├visualization_files            # Location for the output data obtained from the subcommand 'vis'
  ```
  
  You can check `APRICOT_analysis_summary.csv` in the path `APRICOT_analysis/output/5_analysis_summary` file for the quick overview of the analysis.
  
  To run analysis on new query proteins, please edit the "Input-1" part of the `run_example.sh` script, for example, provide Uniprot ids of your query proteins ($QUERY_UIDS, line number 51). To acquire domain information of different classes, please change the keyword values for "Input-2" part in the shell script ($DOMAIN_KEYWORDS, line number 78).
  
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
