[![Latest Version](https://img.shields.io/pypi/v/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![License](https://img.shields.io/pypi/l/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![DOI](https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg)](https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT)

![alt tag](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_logo.png)

###A tool for sequence-based identification and characterization of protein classes

[APRICOT](http://malvikasharan.github.io/APRICOT/) is a computational pipeline for the identification of specific functional classes of interest in large protein sets. The pipeline uses efficient sequence-based algorithms and predictive models like signature motifs of protein families for the characterization of user-provided query proteins with specific functional features. The dynamic framework of APRICOT allows the identification of unexplored functional classes of interest in the large protein sets or the entire proteome.

####Authors and Contributors

The tool is designed and developed by Malvika Sharan @malvikasharan in the lab of Prof. Dr. Jörg Vogel and Dr. Ana Eulalio in the Institute for Molecular Infection Biology at the University of Würzburg. Dr. Konrad Förstner @konrad contributed to the project by providing important technical supervision and discussions. The authors are grateful to Prof. Thomas dandekar, Dr. Charlotte Michaux, Caroline Taouk and Dr. Lars Barquist for critical discussions and feedback.

####Source code

The source codes of APRICOT are available via git https://github.com/malvikasharan/APRICOT and pypi https://pypi.python.org/pypi/bio-apricot.

####License

APRICOT is open source software and is available under the ISC license.

Copyright (c) 2011-2015, Malvika Sharan, <malvika.sharan@uni-wuerzburg.de>

Please read the license content [here](https://github.com/malvikasharan/APRICOT/blob/master/LICENSE.md).


####Installation
APRICOT can be installed with pip

`````
$ pip install bio-apricot
`````

The scripts for the installaton of the different componenents of APRICOT (databases, tools and flatfiles) are available on the GitHub repository. You can manually download the APRICOT repository or simply clone it.

`````
$ git clone https://github.com/malvikasharan/APRICOT.git
`````
The [Docker image for APRICOT](https://github.com/malvikasharan/APRICOT/blob/master/Dockerfile) will be available soon.

The shell script to install and run the analysis in a streamlined manner is provided with the package, [see here](https://github.com/malvikasharan/APRICOT/blob/master/system_test.sh).

####Working example

We recomend you to check out the [tutorial](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_tutorial.md) that discusses each module of APRICOT in detail. The repository contains a shell script [run_example.sh](https://github.com/malvikasharan/APRICOT/blob/master/shell_scripts/run_example.sh), which can be used for the demonstration of APRICOT analysis with an example. 

In the GitHub repository we have provided a test folder named [tests](https://github.com/malvikasharan/APRICOT/tree/master/tests), to allow the system testing. The instructions and commands are provided in the shell scipt [system_test.sh](https://github.com/malvikasharan/APRICOT/blob/master/tests/system_test.sh). 

Users can choose to install all the tools and databases for a complete test. Optionally, the [test datasets](https://github.com/malvikasharan/APRICOT/tree/master/tests/demo_files_small) can be used for basic testing, which does not require installation of third party tools. 

####Contact

For question, troubleshooting and requests, please feel free to contact Malvika Sharan at <malvika.sharan@uni-wuerzburg.de>
