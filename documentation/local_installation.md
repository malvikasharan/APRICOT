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

###Test if the software is correctly installed

Here is a quick way to check if the software works in your system (without really installing the complete filesystem).

The repository contains a shell script [shell_scripts/run_example.sh](https://github.com/malvikasharan/APRICOT/blob/master/shell_scripts/run_example.sh) that can be used for the demonstration of APRICOT installation including analysis with an example. 

It uses [test datasets](https://github.com/malvikasharan/APRICOT/tree/master/tests/demo_files_small) for basic testing, which does not require installation of third party tools.

````
$ wget -N https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/run_example.sh
$ sh run_example.sh
````

By default, this script generates a main analysis folder `APRICOT_analysis` and several sub-directories. To understand each components of the software and generated results, We recomend you to check out the [tutorial](https://github.com/malvikasharan/APRICOT/blob/master/documentation/APRICOT_tutorial.md). 

Hint:

The run scripts requires the command to run APRICOT. 

When installed by pip, th executable location will be: /home/username/.local/bin/
and the library location will be: /home/username/.local/lib/python3.5/site-packages/apricotlib/

In that case, when calling the software (also edit the path when using the shell script run_example.sh and system_test.sh), please use the complete path name rather than using `apricot`, which will look for a globally installed software.

When using `--user` flag for a local installation `$ pip3 install --user bio-apricot`, please check the paths for the executable and the libraries and provide them in the script.
