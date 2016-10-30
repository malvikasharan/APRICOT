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

###OR

####Get APRICOT manually

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

####Third party requirements for the software

An additional step for the installation of the third party tools and the databases, which are required to carry out analysis by the software.

The shell script: [APRICOT/shell_scripts/apricot_minimum_required_files.sh](https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/apricot_minimum_required_files.sh), can be installed locally that could be used for multiple analysis.

````
$ wget -N https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/apricot_minimum_required_files.sh
$ sh apricot_minimum_required_files.sh
````

This script will install all the required tools and will create a directory `source_files` with all the required datasets as dicussed [here](https://github.com/malvikasharan/APRICOT/blob/master/documentation/data_requirements.md).
