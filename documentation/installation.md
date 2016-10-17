[![Latest Version](https://img.shields.io/pypi/v/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![License](https://img.shields.io/pypi/l/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![DOI](https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg)](https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT)
[![](https://images.microbadger.com/badges/image/malvikasharan/apricot.svg)](https://microbadger.com/images/malvikasharan/apricot "Get your own image badge on microbadger.com")

![alt tag](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_logo.png)

####Installing APRICOT software

APRICOT is implemented in Python as a standalone and is executable on Ubuntu (and other debian-based) systems.

Please make sure that your system has pip and git installed 

````
$ apt-get install python3-pip git 
````

#####Get APRICOT via pip

Then install APRICOT via pip (NOTE: this doesn't install the required tools and datasets):
````
$ pip3 install bio-apricot 
````

This will globally install APRICOT, which can be called via the command `apricot`, and the libraries from apricotlib will be saved.


#####Get APRICOT manually

APRICOT is implemented in Python3 and can be executed in Linux/Unix system. APRICOT requires few third party packages, namely [Biopython](http://biopython.org/wiki/Main_Page), [BLAST executables](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download), [interproscan](https://www.ebi.ac.uk/interpro/interproscan.html), python libraries like [Matplotlib](http://matplotlib.org/), [requests](https://pypi.python.org/pypi/requests), openpyxl and few other optional tools that are mentioned below.

````
$ apt-get install python3-matplotlib python3-numpy python3-scipy python3-biopython python3-requests --yes --fix-missing
$ pip3 install openpyxl
````

The git-repository for APRICOT can be [downloaded manually](https://github.com/malvikasharan/APRICOT/archive/master.zip) or locally cloned:

`````
$ git clone https://github.com/malvikasharan/APRICOT.git
`````

Please see the detailed documentation for the alternative installation instructions of the software using [Docker](https://github.com/malvikasharan/APRICOT/blob/master/Dockerfile) or [shell scripts](https://github.com/malvikasharan/APRICOT/blob/master/tests/system_test.sh).

#####Quick test for each subcommands of APRICOT 

Here is a quick way to check how different modules work (without really installing the complete filesystem).

The repository contains a shell script [shell_scripts/run_example.sh](https://github.com/malvikasharan/APRICOT/blob/master/shell_scripts/run_example.sh) with shell commands that can be used for the demonstration of APRICOT installation including analysis with an example. 

It uses [test datasets](https://github.com/malvikasharan/APRICOT/tree/master/tests/demo_files_small) for basic testing, which does not require installation of third party tools.

````
$ wget -N https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/run_example.sh
$ sh run_example.sh
````

By default, this script generates a main analysis folder `APRICOT_analysis` and several sub-directories. To understand each components of the software and generated results, We recomend you to check out the [tutorial](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_tutorial.md). 

When using `--user` flag for a local installation `$ pip3 install --user bio-apricot`, please check the paths for the executable and the libraries.

Hint:

Executable location will be: /home/username/.local/bin/
and the library location will be: /home/username/.local/lib/python3.5/site-packages/apricotlib/

In that case, when calling the software (also edit the path when using the shell script run_example.sh and system_test.sh), please use the complete path name rather than using `apricot`, which will look for a globally installed software.

####APRICOT Docker image

We recommend users to get the complete filesystem for APRICOT using [docker image](https://docs.docker.com/v1.8/userguide/dockerimages/):
````
$ docker pull malvikasharan/apricot
````

#####Run the container:
````
$ docker run -it malvikasharan/apricot bash
````
APRICOT is installed and can be called using command `apricot` and the libraries will be saved at `usr/local/lib/python3.5/site-packages/apricotlib/`

#####Go to the `home` folder to test the software:
````
$ cd home
````

####For the developers

A test folder, [tests](https://github.com/malvikasharan/APRICOT/tree/master/tests), exists in the repository to allow the system testing and demonstration of basic modules without installation. The instructions and commands are provided in the shell scipt [system_test.sh](https://github.com/malvikasharan/APRICOT/blob/master/tests/system_test.sh). 

````
$ cd APRICOT/test
$ sh system_test.sh
````
By default, this script generates a main analysis folder `APRICOT_analysis` and several sub-directories. To understand each components of the software and generated results, We recomend you to check out the [tutorial](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_tutorial.md). 

####Contact

For question, troubleshooting and requests, please feel free to contact Malvika Sharan at <malvika.sharan@uni-wuerzburg.de>.

#####Trivia
The initial focus of this project was to identify functional domains in bacterial proteins that have the potential to interact with RNA (RNA-binding proteins or RBPs) and understand their regulatory roles and mechanisms. Hence, the tool is named **APRICOT** that stands for **A**nalysing **P**rotein **R**NA **I**nteractions by **C**ombined **O**utput **T**echnique. However, due to the adaptability of the pipeline to different sets of reference domains, APRICOT is not limited to RBP identification. The *combined output* referes to the combined scoring method of the software that uses a series of sequence based features to score the proteins predicted with the domains of interest. The pipeline has been tested successfully on the several functional classes. We are carrying out the experimental validations of few RBPs identified by APRICOT in collaboration with the biologists in our lab, which can provide a high confidence dataset and contribute significantly to the improvement of this computational approach.

###Summary of the pipeline

The functionality of APRICOT can be explained in 3 parts: program input, analysis modules and program output. 

#####Program inputs
1) Query proteins that are subjected to characterization by domains and associated functional properties

2) Set of terms indicating protein domains of functional relevance. 

Based on these inputs, APRICOT can be executed for the analysis of the proteins of interest using the analysis modules as explained later.

#####Analysis modules of APRICOT
The functionalities involved in the primary analysis are retrieval of sequences and known annotations of query proteins, collection of domains of interest from domain databases, and identification of all the functional domains in a given query.

The data obtained from the primary analysis is used as a resource for the secondary analysis, which mainly involves the selection of proteins based on the predicted domains, the calculation of the statistical and biological significance of the selected proteins to possess the function of interest by means of sequence-based features, and biological characterization of these proteins by additional annotations like subcellular localization and secondary structures. 

#####Program output
For each analysis step, APRICOT generates results in tablular manner, in addition with an overview of the analysis and graphics associated with the resulting information.


###Detailed documentation

 ####Instructions for the installation of complete filesystem 

#####1. Docker image

######What is docker?

According to the [Docker home page](https://www.docker.com/what-docker):
"Docker containers wrap up a piece of software in a complete filesystem that contains everything it needs to run: code, runtime, system tools, system libraries – anything you can install on a server. This guarantees that it will always run the same, regardless of the environment it is running in."

As stated above, the [Docker image for APRICOT](https://hub.docker.com/r/malvikasharan/apricot/) can be pulled using Docker Pull Command:
````
$ docker pull malvikasharan/apricot
````

Optionally you can create APRICOT image using Dockerfile provided in the repository

````
$ wget -N https://raw.githubusercontent.com/malvikasharan/APRICOT/master/Dockerfile
$ docker build -t imagename .
````
Type `docker images` and press RETURN to see the docker image that you've just created.

######Run the docker-apricot

Please replace malvikasharan/apricot with your locally built Docker image's name.

````
$ docker run -t -i malvikasharan/apricot bash
$ cd home
````

#####2. Installation by shell-scipts

Python modules required for APRIOCT can be installed using pip.

`````
$ pip install bio-apricot
`````
Or update the package list manually: `sudo apt-get update` and install the required packages (`sudo apt-get install python3-matplotlib python3-numpy python3-scipy python3-biopython python3-requests python3-openpyxl`).

The git-repository for APRICOT can be [downloaded manually](https://github.com/malvikasharan/APRICOT/archive/master.zip) or locally cloned:

`````
$ git clone https://github.com/malvikasharan/APRICOT.git
`````

APRICOT repository comprises of a directory tree of the following structure.

`````
APRICOT
│   CHANGELOG.md
│   Dockerfile
│   LICENCE.md
│   README.md
|   ...
|
└───├apricotlib
└───├bin
└───├shell_scripts
└───├...
`````

The run script for the installation can be found in `APRICOT/shell_scripts` folder of this github repository. Users need to provide the path of the APRICOT repository in the system (default name: APRICOT) and the path where the users wish to install APRICOT related tools and files (default path: source_files). 

APRICOT requires to install  BLAST executables (ftp://ftp.ncbi.nih.gov/blast/executables/blast+) and InterProScan (ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/) along with establishing CDD and InterPro databases locally. 

All the required resources can be established using the script `APRICOT/shell_scriptsapricot_minimum_required_files.sh`. 

`````
$ sh apricot_minimum_required_files.sh
`````

To carry out additional annotation by RaptorX and Psortb, users can install these tools individually. RaptorX can be installed using `APRICOT/shell_scripts/install_raptorx.py`. The instructions for the installation of Psortb in given in its homepage: ttp://www.psort.org/downloads/INSTALL.html.


Alternatively, the BLAST executables (rpsblast, blastp, psiblast, makeblastdb) can be installed locally as directed [here](http://bioinformatics.ai.sri.com/ptools/installation-guide/released/blast.html) and CDD can be established locally (in the path apricot_db_and_tools/conserved_domain_database/Cdd) as shown below:

    $ wget ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/*
    $ tar xvf file_name

InterProSan can be downloaded and installed locally (in the path apricot_db_and_tools/interpro/InterProScanData) with the required database as shown below:

    $ wget ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.17-56.0/interproscan-5.17-56.0-64-bit.tar.gz
    $ tar xvf interproscan-5.17-56.0-64-bit.tar.gz

APRICOT requires various flatfiles, namely [CDD tables](ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.info), [InterPro tables](ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5), [PDB secondary structures](http://www.rcsb.org/pdb/files/ss.txt), [taxonomy information] (http://www.uniprot.org/docs/speclist.txt), [Gene Ontology data](http://www.geneontology.org/ontology/go.obo) and [pfam table](ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam29.0/database_files/), which are downloaded and saved locally in the pre-defined location (for e.g. 'reference_db_files' in 'APRICOT' folder).
```
source_files
│   ...
└───├reference_db_files
    └───├all_taxids
    └───├blast  
    └───├cdd  
    └───├go_mapping
    └───├interpro
    └───├pdb
    └───├pfam
```
APRICOT allows additional annotations of the proteins by using third party tools. For the secondary structure predictions APRICOT requires [RaptorX](https://github.com/Indicator/RaptorX-SS8.git)  which requires [RefSeq/nr database](ftp://ftp.ncbi.nih.gov/blast/db/FASTA) and for the subcellular localization APRICOT uses [PSORTb v2](https://github.com/lairdm/psortb-docker.git). These tools should be installed locally (please refer the run script) in order to allow APRICOT to carry out the optional annotations of proteins of interest.

###Versions/Change log
Please check the current version [here](https://github.com/malvikasharan/APRICOT/blob/master/CHANGELOGS.txt).
