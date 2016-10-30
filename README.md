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

####License

APRICOT is open source software and is available under the ISC license.

Copyright (c) 2011-2015, Malvika Sharan, <malvika.sharan@uni-wuerzburg.de>

Please read the license content [here](https://github.com/malvikasharan/APRICOT/blob/master/LICENSE.md).

####APRICOT software 

#####(not the complete filesystem)

APRICOT is implemented in Python as a standalone and is executable on Ubuntu (and other debian-based) systems.

Please make sure that your system has pip and git installed 

````
$ apt-get install python3-pip git 
````

#####Get APRICOT via pip

Then install APRICOT via pip (NOTE: this doesn't install the complete filesystem):
````
$ pip3 install bio-apricot 
````

This will globally install APRICOT, which can be called via the command `apricot`, and the libraries from apricotlib will be saved.

####OR

#####Get APRICOT manually

APRICOT is implemented in Python 3 and can be executed in Linux/Unix system. APRICOT requires few third party packages, namely [Biopython](http://biopython.org/wiki/Main_Page), [BLAST executables](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download), [interproscan](https://www.ebi.ac.uk/interpro/interproscan.html), python libraries like [Matplotlib](http://matplotlib.org/), [requests](https://pypi.python.org/pypi/requests), openpyxl and few other optional tools that are mentioned below.

````
$ apt-get install python3-matplotlib python3-numpy python3-scipy python3-biopython python3-requests --yes --fix-missing
$ pip3 install openpyxl
````

The git-repository for APRICOT can be [downloaded manually](https://github.com/malvikasharan/APRICOT/archive/master.zip) or locally cloned:

`````
$ git clone https://github.com/malvikasharan/APRICOT.git
`````

Hint:

Executable location will be: /home/username/.local/bin/
and the library location will be: /home/username/.local/lib/python3.5/site-packages/apricotlib/

In that case, when calling the software (also edit the path when using the shell script run_example.sh and system_test.sh), please use the complete path name rather than using `apricot`, which will look for a globally installed software.

When using `--user` flag for a local installation `$ pip3 install --user bio-apricot`, please check the paths for the executable and the libraries.

####APRICOT Docker image

We recommend users to get the complete tool requirements for APRICOT using [docker image](https://docs.docker.com/v1.8/userguide/dockerimages/):
````
$ docker pull malvikasharan/apricot
````

#####Run the container:
````
$ docker run -it malvikasharan/apricot bash
````
APRICOT is installed and can be called using command `apricot` and the libraries will be saved at `usr/local/lib/python3.5/site-packages/apricotlib/`

#####Go to the `home` folder to test the software (instructions below):
````
$ cd home
````

####Test if the software is successfully installed

Here is a quick way to test if different modules work in your system (without really installing the complete filesystem).

The repository contains a shell script [APRICOT/shell_scripts/run_example.sh](https://github.com/malvikasharan/APRICOT/blob/master/shell_scripts/run_example.sh) with shell commands that can be used for the demonstration of APRICOT installation including analysis with an example. 

````
$ wget -N https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/run_example.sh
$ sh run_example.sh
````

By default, this script generates a main analysis folder `APRICOT_analysis` and several sub-directories. To understand each components of the software and generated results, We recomend you to check out the [tutorial](https://github.com/malvikasharan/APRICOT/blob/master/documentation/APRICOT_tutorial.md).

####Documentation

1. [Overview of the pipeline](https://github.com/malvikasharan/APRICOT/blob/master/documentation/pipeline_overview.md)
1. [Tutorial](https://github.com/malvikasharan/APRICOT/blob/master/documentation/APRICOT_tutorial.md)
1. [Working with docker](https://github.com/malvikasharan/APRICOT/blob/master/documentation/docker.md)
1. [Instructions for local installation](https://github.com/malvikasharan/APRICOT/blob/master/documentation/installation.md)
1. [Tool and data dependencies](https://github.com/malvikasharan/APRICOT/blob/master/documentation/software_dependencies.md)
1. [Different subcommands](https://github.com/malvikasharan/APRICOT/blob/master/documentation/subcommands.md)
1. [Frequently asked questions](https://github.com/malvikasharan/APRICOT/blob/master/documentation/FAQs.md)
1. [Troubleshoot](https://github.com/malvikasharan/APRICOT/blob/master/documentation/troubleshooting.md)
1. [License](https://github.com/malvikasharan/APRICOT/blob/master/LICENSE.md)
1. [For the developers](https://github.com/malvikasharan/APRICOT/blob/master/documentation/for_the_developers.md)

####Contact

For question, troubleshooting and requests, please feel free to contact Malvika Sharan at <malvika.sharan@uni-wuerzburg.de>.
