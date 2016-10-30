[![Latest Version](https://img.shields.io/pypi/v/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![License](https://img.shields.io/pypi/l/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![DOI](https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg)](https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT)

![alt tag](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_logo.png)

##Resources requirements of APRICOT 
  - Basic Linux programs ([pip](https://pip.pypa.io/en/stable/installing/) or [apt-get](https://wiki.ubuntuusers.de/apt/apt-get/), [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Python 3](https://www.python.org/downloads/))
  - Python dependencies: [numpy](http://docs.scipy.org/doc/numpy/user/install.html), [scipy](https://www.scipy.org/install.html), [matplotlib](http://matplotlib.org/users/installing.html), [openpyxl](https://pypi.python.org/pypi/openpyxl), [requests](http://docs.python-requests.org/en/master/user/install/), [biopython](http://biopython.org/DIST/docs/install/Installation.html)
  - APRICOT software from PyPI: [bio-apricot](https://pypi.python.org/pypi/bio-apricot)
  - Latest CDD database: ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/
  - Latest InterPro databases and InterProScan: ftp://ftp.ebi.ac.uk/pub/databases/interpro
  - InterProScan requires [pfsearch wrapper](http://web.expasy.org/pftools/#Downloads) and [Java 8](https://wiki.ubuntuusers.de/Java/Installation/Oracle_Java/Java_8/) or above
  - BLAST executables (from: ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) (psiblast, rpsblast, blastp, makeblastdb)
  - [Gene Ontology (go.obo)](http://geneontology.org/page/download-ontology)
  - PDB files: [proteins sequence and secondary-structure](http://www.rcsb.org/pdb/files/ss.txt) and [PDB to InterPro mapping ](http://www.uniprot.org/docs/pdbtosp.txt)
  - [Taxonomy data](http://www.uniprot.org/docs/speclist.txt)
  - [needle](http://emboss.sourceforge.net/download/) from EMBOSS software
  - [Psortb](https://github.com/brinkmanlab/psortb-docker) for localization prediction (only for the subcomand addanno)
  - [RaptorX](https://github.com/Indicator/RaptorX-SS8.git) for secondary structure presiction (only for the subcomand addanno)

####The database requirement and and how they need to be structured are explained [here](https://github.com/malvikasharan/APRICOT/blob/master/documentation/database_dependencies.md) in details.

Please see the instructions for working with the [Docker image](https://github.com/malvikasharan/APRICOT/blob/master/documentation/docker.md).

In case, users do not wish to run Docker image, the complete file system with the tool and dataset can be installed using the shell script 
[APRICOT/shell_scripts/apricot_minimum_required_files.sh](https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/apricot_minimum_required_files.sh). Please see the instructions for [local installation](https://github.com/malvikasharan/APRICOT/blob/master/documentation/local_installation.md).

