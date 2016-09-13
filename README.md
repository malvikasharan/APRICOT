[![Latest Version](https://img.shields.io/pypi/v/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![License](https://img.shields.io/pypi/l/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![DOI](https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg)](https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT)
[![](https://images.microbadger.com/badges/image/malvikasharan/apricot.svg)](https://microbadger.com/images/malvikasharan/apricot "Get your own image badge on microbadger.com")

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

####APRICOT software (not the complete filesystem)

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

APRICOT is implemented in Python 3 and can be executed in Linux/Unix system. APRICOT requires few third party packages, namely [Biopython](http://biopython.org/wiki/Main_Page), [BLAST executables](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download), [interproscan](https://www.ebi.ac.uk/interpro/interproscan.html), python libraries like [Matplotlib](http://matplotlib.org/), [requests](https://pypi.python.org/pypi/requests), openpyxl and few other optional tools that are mentioned below.

````
$ apt-get install python3-matplotlib python3-numpy python3-scipy python3-biopython python3-requests --yes --fix-missing
$ pip3 install openpyxl
````

The git-repository for APRICOT can be [downloaded manually](https://github.com/malvikasharan/APRICOT/archive/master.zip) or locally cloned:

`````
$ git clone https://github.com/malvikasharan/APRICOT.git
`````

Please see the detailed documentation below for the alternative installation instructions of the software using [Docker](https://github.com/malvikasharan/APRICOT/blob/master/Dockerfile) or [shell scripts](https://github.com/malvikasharan/APRICOT/blob/master/tests/system_test.sh).

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
$ docker run -t -i malvikasharan/apricot bash
````
APRICOT is installed and can be called using command `apricot` and the libraries will be saved at `usr/local/lib/python3.5/site-packages/apricotlib/`

#####Go to the `home` folder to test the software:
````
$ cd home
````

####For the developers

We have provided a test folder named [tests](https://github.com/malvikasharan/APRICOT/tree/master/tests), to allow the system testing and demonstration of basic modules without installation. The instructions and commands are provided in the shell scipt [system_test.sh](https://github.com/malvikasharan/APRICOT/blob/master/tests/system_test.sh). 

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

####APRICOT’s subcommands

Each subcommand requires the path to the analysis folder ('APRICOT_analysis' by deafult). Different subcommands can be quickly viewed by running `python3 APRICOT/bin/apricot -h`.

``````
usage: apricot [-h] [--version]
               {create,taxid,query,keywords,select,predict,filter,classify,annoscore,summary,addanno,vis,format}
               ...

positional arguments:
  {create,taxid,query,keywords,select,predict,filter,classify,annoscore,summary,addanno,vis,format}
                        APRICOT commands - Refer documentation for detail
    create              Create analysis folders
    taxid               Download taxonomy ids from UniProt for the user
                        provided query species
    query               Map user provided comma separated queries to UniProt
                        ids
    keywords            Save user provided keywords for domain selection
                        (required) and analysis classification (-cl)
    select              Select functional domains of interest (specified by
                        keywords) from CDD (-C) and InterPro (-I) by default
    predict             Predict functional domains in the queries based on CDD
                        (-C) and InterPro (-I) databases by default
    filter              Filter queries predicted with domains of interest (and
                        optional parameter thresholds) and extend their
                        annotations
    classify            Optional classification of selected prediction in
                        smaller groups by class keywords
    annoscore           Score and rank predicted data by 'annotation scoring'
    summary             Summary analysis output
    addanno             Optional annotation of the selected protein by -PDB,
                        -PSORTB, -RAPTORX or -REFSS (see addanno -h)
    vis                 Visualize analysis results (see vis -h) for detail
    format              Optional output file format as html or excel

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show version
``````
 
####subcommand `create`
Quick help: `$ python3 APRICOT/bin/apricot create -h`

This subcommand creates all the required directories to store input and output data acquired from APRICOT analysis. The main analysis folder can be provided by the users (default name: APRICOT_analysis).
````
usage: apricot create [-h] analysis_path

positional arguments:
  analysis_path  Creates APRICOT_analysis folder for anlysis unless other
                 name/path is provided
````

The structure and annotation of directories and the enclosing files in the 'input' folder in the analysis directory:
```
APRICOT_analysis
    └───├input
            └───├query_proteins
            └───├uniprot_reference_table
            └───├mapped_query_annotation  
```

The structure of directories and the enclosing files in the 'output' folder in the analysis directory:
```
APRICOT_analysis
    └───├output
            └───├0_predicted_domains            # Location for the output data obtained from the subcommand 'predict'
            └───├1_compiled_domain_information  # Location for the output data obtained from the subcommand 'filter'          
            └───├2_selected_domain_information  # Location for the classified data obtained from the subcommand 'classify' 
            └───├3_annotation_scoring           # Location for the output data obtained from the subcommand 'annoscore'
            └───├4_additional_annotations       # Location for additional annotations for the selected 
            |                                   # queries using subcommand 'addanno'
            └───├5_analysis_summary             # Location for the output data obtained from the subcommand 'summary'
            └───├format_output_data             # Location for the output data obtained from the subcommand 'format'
            └───├visualization_files            # Location for the output data obtained from the subcommand 'vis'
```

####subcommand `taxid`
Quick help: `$ python3 APRICOT/bin/apricot taxid -h`
    
The users can provide gene ids or protein names as queries to APRICOT, which is mapped against UniProt Knowledgebase in order to extract relevant information. Since, same gene/protein ids exist across various genomes/proteomes, one can limit the search of the query to a certain organism (rather than all the organisms in the database) by providing one or multiple taxonomy ids. 

When the taxonomy id is not known by the users, this subcommand --taxid  can be used to extract the id by providing species name.

````
usage: apricot taxid [-h] [--species SPECIES] db_path

positional arguments:
  db_path

optional arguments:
  -h, --help            show this help message and exit
  --species SPECIES, -s SPECIES
                        Species name (comma separated if more than one) for
                        taxonomy id retreival
````
The taxonomy ids are saved in the text file taxonomy_ids.txt in the directory reference_db_files.
````
source_files
    └───├reference_db_files
            |    taxonomy_ids.txt
````

####subcommand `query`
Quick help: `$ python3 APRICOT/bin/apricot query -h`

As mentioned already, APRICOT gives multiple options to the users to supply queries. For example, the queries can be provided as UniProt ids (--uids), gene ids or protein names (--geneids), fasta sequences (--fasta) or only the taxonomy id (--taxid) for a complete proteome analysis (using flag -P). 

Paths for the saving the query data and their corresponding fasta files, xml files, annotation tables etc. can be optinally provided by the users.

`````
usage: apricot query [-h] [--analysis_path ANALYSIS_PATH] [--uids UIDS]
                     [--taxid TAXID] [--geneids GENEIDS] [--proteome]
                     [--fasta] [--query_path QUERY_PATH]
                     [--proteome_path PROTEOME_PATH] [--xml_path XML_PATH]
                     [--fasta_path FASTA_PATH] [--feature_table FEATURE_TABLE]

optional arguments:
  -h, --help            show this help message and exit
  --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                        Main analysis path
  --uids UIDS, -ui UIDS
                        Comma separated UniProt IDs
  --taxid TAXID, -tx TAXID
                        Select taxonomy id for query species
  --geneids GENEIDS, -gi GENEIDS
                        Comma separated query genes
  --proteome, -P        Analyze entire proteome
  --fasta, -fa          Analyze fasta sequences
  --query_path QUERY_PATH, -qp QUERY_PATH
                        Get proteome table from UniProt
  --proteome_path PROTEOME_PATH, -pp PROTEOME_PATH
                        Get proteome table from UniProt
  --xml_path XML_PATH, -o XML_PATH
                        Get proteome table from UniProt
  --fasta_path FASTA_PATH, -fp FASTA_PATH
                        Get proteome table from UniProt
  --feature_table FEATURE_TABLE, -ft FEATURE_TABLE
                        Get proteome table from UniProt
``````

APRICOT saves the user provided queries and related information extracted from UniProt knowledgebase (fasta files, xml files, reference files etc.) in the directories as described below.
````
APRICOT_analysis
    └───├input
            └───├query_proteins
            |   query_to_uids.txt           # User provided queries (gene ids/protein names/whole proteome set) 
            |                               # mapped to the UniProt Ids (flag --uids, --geneids)
            └───├uniprot_reference_table
            |   query_uids_reference.tab    # Basic annotations of the query protein IDs (flag --uids, --geneids)  set
            |                               # or the whole proteome (flag -P) from a certain taxonomy (flag --taxid)
            └───├mapped_query_annotation  
                    └───├fasta_path_mapped_query  # Location for protein FASTA sequences of each query
                    |   |                         # qery fasta sequences are also saved here (flag --fasta)
                    |   | query_id-1.fasta 
                    |   | query_id-2.fasta
                    |   | ...
                    |   | query_id-n.fasta
                    |
                    └───├xml_path_mapped_query    # Location for protein FASTA sequences of each query
                    |   | query_id-1.xml
                    |   | query_id-2.xml
                    |   | ...
                    |   | query_id-n.xml
                    |
                    └───├mapped_protein_xml_info_tables  
                        | query_feature_table.csv  # File containing all the features of the queries 
                                                   # obtained by parsing xml files
````

    
####subcommand `keywords`
Quick help: `$ python3 APRICOT/bin/apricot keywords -h`

Since APRICOT allows identification of certain protein classes like RNA-binding proteins by means of domains, one of the most essential input data, beside the query protein itself, is a comma-separated list of terms or keywords that potentially indicates to a protein functional classes (*domain selection terms*). Such terminologies could be any pfam id, Gene Ontology term, mesh term, simple biological terms like 'RRM' and 'ribosome', or a combination of all these types. 

Multi-word terms can be provided by using ‘-’ as a connector, for example, 'RNA-binding' and 'La-domain'. 

In order to maintain stringent selection of truly functional domains, APRICOT by-default does not allow the selection of a domain entry if the *domain selection term* occurs in its annotation with any trailing words like prefixes or suffixes. This indicates the possibilities of omitting few relevant entries from the domain selection keywords, but it also ensures exclusion of several non-relevant domains that might get included by chance. However, users can allow prefix by using the hash symbol (#) in the beginning of a term and suffix when # is used at the end of the term. For example, by using '#RNA-binding' one can allow the inclusion of 'tRNA-binding', 'mtRNA-binding'etc, and by allowing 'RNA-bind#' one can allow varying verb forms for bind like binder, binding etc. Of course, one can allow both prefixes and suffixes (#RNA-bind#).

Optionally a second set of keywords for the classification of predicted domains can be provided by using flag -cl (*result classification terms*). This list can comprise of terms associated to biological functions, enzymatic activities or specific features. For example, the predicted RNA related domain data could be divided into the classification tags of RRM, ribosome, synthetase, helicases etc. Such classification can help users tremendously in navigating the large datasets or for the selection of representative protein for certain function conferred by the domains. When users do not provide *result classification terms*, APRICOT uses the *domain selection terms* for this purpose as well.
        
````
usage: apricot keywords [-h] [--classify CLASSIFY] [--kw_path KW_PATH]
                        kw_domain

positional arguments:
  kw_domain             Comma separated keywords for domain selection

optional arguments:
  -h, --help            show this help message and exit
  --classify CLASSIFY, -cl CLASSIFY
                        Optional comma separated keyword for result
                        classification
  --kw_path KW_PATH, -kp KW_PATH
                        Path for keyword files
````

The keywords are saved in the directory `source_files` in the subfolder `domain_data` shown below.
````
source_files
    └───├domain_data
            keywords_for_domain_selection.txt         # All the terms for domain selection
            keywords_for_result_classification.txt    # All the terms for result classification
````

####subcommand `select`
Quick help: `python3 APRICOT/bin/apricot select -h`

This subcommand allows the selection of reference domains based on the *domain selection terms* (in subcommand keywords). For this purpose, by-default APRICOT scans each entries of the domains in both CDD and InterPro domain consortiums for the occurance of any *domain selection term*. 

In case of multi word terms (which are provided by using '-' as a connector), the co-occurance of the terms are considered when the words in the same sentence or same context. To ensure a more complete selection of the domains, the gene-ontology associated to the domains are also checked and selected accordingly.

It is possible to limit the selection process in only one of the consortiums by providing flags -C for CDD or -I for InterPro. For cross mapping the domains in both the consortiums, APRICOT uses domain ids from the databases (Pfam, SMART and TIGRFAM) that are shared by both the consortiums.

````
usage: apricot select [-h] [--cdd_dom] [--ipr_dom] [--dom_kw DOM_KW]
                      [--cdd_table CDD_TABLE] [--ipr_table IPR_TABLE]
                      [--interpro_mapped_cdd INTERPRO_MAPPED_CDD]
                      [--domain_path DOMAIN_PATH]
                      [--pfam_domain_file PFAM_DOMAIN_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --cdd_dom, -C         Selects functional domains of interest from CDD
  --ipr_dom, -I         Selects functional domains of interest from CDD
  --dom_kw DOM_KW, -dk DOM_KW
                        Absolute path of keyword files
  --cdd_table CDD_TABLE, -cdd CDD_TABLE
                        Absolute path of CDD domain table
  --ipr_table IPR_TABLE, -ipr IPR_TABLE
                        Absolute path of InterPro domain table
  --interpro_mapped_cdd INTERPRO_MAPPED_CDD, -map INTERPRO_MAPPED_CDD
                        InterPro domains mapped to CDD domains.
  --domain_path DOMAIN_PATH, -dp DOMAIN_PATH
                        Absolute path for keyword selected domains
  --pfam_domain_file PFAM_DOMAIN_FILE, -pf PFAM_DOMAIN_FILE
                        The domain summary from PfamA
````

The domains that are selected from CDD and InterPro are stored in the directory domains_data in the bin folder. The selected domains are compiled and saved into the file all_keyword_selected_domain_data.tab in the domain_data.

````
bin
│   ...
└───├domain_data
    └───├cdd
    └───├interpro
    | all_keyword_selected_domain_data.tab
````
    
####subcommand `predict`
Quick help: `$ python3 APRICOT/bin/apricot predict -h`

This subcommand is used to begin the process of domain predictions in the query proteins by all the possible functional domains using RPSBLAST against CDD and InterProScan against InetrPro. APRICOT carries out the domain prediction from both CDD and InterPro consortiums by default but users can choose to predict domains from only one of the databases by using the flag -C for CDD and -I for InterPro. To overwrite old predictions, the flag -F (for force) can be used.

The run time of RPSBLAST is considerably less, therefore -C flag can be used to obtain a quick information of the functional domains. However, we recommend the default setting because the different databases involved in both the consortiums provide a larger scope for completeness of domain predictions.

The execution of this subcommand is the basic requirement for the APRICOT analysis. The main input of this step is fasta sequences of query proteins. This subcommand can be executed simultabeously or even before running the subcommand 'select'.

````
usage: apricot predict [-h] [--analysis_path ANALYSIS_PATH] [--cdd] [--ipr]
                       [--force] [--cdd_db CDD_DB] [--ipr_db IPR_DB]
                       [--outpath OUTPATH] [--fasta FASTA]

optional arguments:
  -h, --help            show this help message and exit
  --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                        Provide output path for the analysis result of the
                        chosen method
  --cdd, -C             domain prediction based on CDD only
  --ipr, -I             domain prediction based on InterProScan only
  --force, -F           force flag for the current analysis, removes already
                        existing predictions
  --cdd_db CDD_DB, -cdb CDD_DB
                        Provide absolute path of CDD databases based on the
                        chosen method
  --ipr_db IPR_DB, -idb IPR_DB
                        Provide absolute path of InterPro databases based on
                        the chosen method
  --outpath OUTPATH, -o OUTPATH
                        Provide output path for domain prediction files
  --fasta FASTA, -f FASTA
                        Provide absolute path of fasta files for query
                        proteins
````

The resulting files of this analysis is stored in the first analysis directory '0_predicted_domains' in the output folder of the main analysis directory. As shown below, the information of the domain predictions are stored as text files in the sub-folders corresponding to the domain consortiums. Since this subcommand is independent of the reference domains, these files containing information on domain predictions can be recycled or re-visited for the selection of different functional classes.

````
APRICOT_analysis
    └───├output
            └───├0_predicted_domains # Location for the output data obtained from the subcommand 'predict'
                    └───├cdd_analysis  # Details of domain predicted from CDD for each query
                    |   | query_id-1.txt
                    |   | query_id-2.txt
                    |   | ...
                    |   | query_id-n.txt
                    |
                    └───├ipr_analysis  # Details of domain predicted from InterPro for each query
                        | query_id-1.tsv
                        | query_id-2.tsv
                        | ...
                        | query_id-n.tsv
````
    
####subcommand `filter`
Quick help: `$ python3 APRICOT/bin/apricot filter -h`

The filtering of the predicted domains by this subcommand take place by using the *domain selection terms*, hence this subcommand should be executed after 'select' and 'predict' subcommands. 

Query proteins that consist of at least one of the selected domains are retained whereas the rest of the proteins are discarded from the downstream analysis. To limit the analysis to one of the consortiums only, flag -C for CDD based information and -I for InterPro based information can be used. 

The users can choose their cut-offs for the parameters by using the flags --similarity, --coverage, --identity, --evalue, --bit (bit score) and --gap. However, the default parameters for the selection of predicted domains are defined as 'coverage > 39' and 'similarity > 24', which have been derived from a large RNA-binding positive and negative training sets collected from SwissProt database. 
        
````
usage: apricot filter [-h] [--analysis_path ANALYSIS_PATH] [--cdd] [--ipr]
                      [--domain_description_file DOMAIN_DESCRIPTION_FILE]
                      [--similarity SIMILARITY] [--coverage COVERAGE]
                      [--identity IDENTITY] [--evalue EVALUE] [--gap GAP]
                      [--bit BIT] [--go_path GO_PATH] [--pred_path PRED_PATH]
                      [--up_table UP_TABLE] [--xml_info XML_INFO]
                      [--compile_out COMPILE_OUT] [--selected SELECTED]

optional arguments:
  -h, --help            show this help message and exit
  --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                        Provide analysis path
  --cdd, -C             Filter of domain prediction based on CDD only
  --ipr, -I             Filter of domain prediction based on InterProScan only
  --domain_description_file DOMAIN_DESCRIPTION_FILE, -d DOMAIN_DESCRIPTION_FILE
                        Description table of the selected domains
  --similarity SIMILARITY, -sim SIMILARITY
                        Percent similarity of prediction with reference
  --coverage COVERAGE, -cov COVERAGE
                        Percent coverage of reference domain in prediction
  --identity IDENTITY, -iden IDENTITY
                        Percent identity of prediction with reference
  --evalue EVALUE, -eval EVALUE
                        Evalue of the domain prediction
  --gap GAP, -gap GAP   Percent gap in predicted domain
  --bit BIT, -bit BIT   Bit score in predicted domain
  --go_path GO_PATH, -gp GO_PATH
                        Go mapping data from fixed database reference files
  --pred_path PRED_PATH, -pp PRED_PATH
                        Raw files of domain prediction
  --up_table UP_TABLE, -ref UP_TABLE
                        Uniprot proteome table from UniProt
  --xml_info XML_INFO, -feat XML_INFO
                        Uniprot proteome table from UniProt
  --compile_out COMPILE_OUT, -co COMPILE_OUT
                        Data with annotation after filtering
  --selected SELECTED, -sel SELECTED
                        output path for the selected data with annotations
````

APRICOT saves all the domain data in the directory '1_compiled_domain_information' of the output folder. All the predicted domains (independent of reference domains and parameter cut-offs) are saved in the sub-folder 'unfiltered_data' and the selected data is saved in the sub-folder 'selected_data' in separate files for different domain resources as shown below. 

Files in the sub-folder 'selected_data' contain predicted domain entry based on the reference domain sets and are marked with the tags *ParameterSelected* when the domain predictions satisfy the defined parameter cut-offs (or default cut-offs) or *Parameter Discarded* when it does not pass the parameter filters. In those cases, when certain parameter is not available for the predicted domain, a tag *ParameterNotApplicable* is used.

````
APRICOT_analysis
    └───├output
        └───├1_compiled_domain_information  # Location for the output data obtained from the subcommand 'filter'          
                    └───├unfiltered_data  # Information of all the domains in the query proteins predicted.
                    |   | cdd_unfiltered_all_prediction.csv  # CDD 
                    |   | ipr_unfiltered_all_prediction.csv  # InterPro
                    |
                    └───├selected_data      # Information of the selected reference domains in the query proteins
                        | cdd_filtered.csv                   # CDD 
                        | ipr_filtered.csv                   # InterPro 
````
Queries, that are selected on the basis of reference domains and parameter cut-offs, are compiled and stored in the directory '2_selected_domain_information' in the sub-folder 'combined_data'. These files contain the information of selected domains along with the additional annotations of the query proteins extracted from various resources like UniProt and Gene Ontology
.
````
APRICOT_analysis
    └───├output    
            └───├2_selected_domain_information            
                    └───├combined_data         # All the selected domain data extended 
                        |                       # with the UniProt annotation
                        | annotation_extended_for_selected.csv
````

###Sub-commands for downstream analysis

####subcommand `classify`
Quick help: `$ python3 APRICOT/bin/apricot classify -h`

This subcommand classifies the resulting domain information of the selected queries by using the *result classification terms* (provided in the subcommand 'keywords').

````
usage: apricot classify [-h] [--analysis_path ANALYSIS_PATH]
                        [--selected SELECTED] [--class_kw CLASS_KW]
                        [--outpath OUTPATH]

optional arguments:
  -h, --help            show this help message and exit
  --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                        Provide analysis path
  --selected SELECTED, -sel SELECTED
                        Selected data file (from select) with annotations
  --class_kw CLASS_KW, -ck CLASS_KW
                        Path for keyword files
  --outpath OUTPATH, -o OUTPATH
                        Classification of selected data based on provided
                        keywords
````

The classified data are stored in the folder as shown below:
````
APRICOT_analysis
    └───├output    
            └───├2_selected_domain_information            
                    └───├classified_data                            # Location for the output data obtained 
                        |                                           # from the subcommand 'classify'
                        | classification_key-1_selected_data.csv    # Files containing subsets of predicted data...
                        | classification_key-2_selected_data.csv    # ... based on user provided classification keys.
````
            
####subcommand `annoscore`

This subcommand is executed for the annotation based scoring of the selcted domains in the query proteins. 

In order to differentiate domain predictions of low confidence from that of high confidence, the predicted domain sites are compared with their corresponding references and scored by means of methods that measure their similarities by means of various sequence-based features. The comparisons of the features between the predicted domain sites and reference are scored based on the principle of Bayesian probability, where a score closer to 1 represents a favourable scenario.

There are four groups of features that are involved in the annotation based scoring.
1. Chemical properties
2. Needleman-Wunsch global alignment scores
3. Euclidean distances of protein compositions
4. Prediction parameters of the predicted sites

Quick help: `$ python3 APRICOT/bin/apricot annoscore -h`


````
usage: apricot annoscore [-h] [--analysis_path ANALYSIS_PATH]
                         [--selected SELECTED] [--cdd_pred CDD_PRED]
                         [--outpath OUTPATH]

optional arguments:
  -h, --help            show this help message and exit
  --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                        Provide analysis path
  --selected SELECTED, -sel SELECTED
                        Provided selected protein table
  --cdd_pred CDD_PRED, -cp CDD_PRED
                        Raw files obtained from CDD based domain prediction
  --outpath OUTPATH, -o OUTPATH
                        Output path for annotation scoring files
````
The data with annotation scores are stored in the folder as shown below:

````
APRICOT_analysis
    └───├output
            └───├3_annotation_scoring          # Location for the output data obtained 
                |                              # from the subcommand 'annoscore'
                | annotation_extended_for_selected.csv
````

####subcommand `addanno`
Quick help: `$ python3 APRICOT/bin/apricot addanno -h`

This subcommand allows users to further annotate the query sequences that are selected based on the defined functional domains. 

Following modules can be used with their respective flags for additional annotations of the selected proteins:

1. Identification sub-cellular localization of the proteins (flag -psortb)
2. Secondary structure calculation by RaptorX (flag -raptorx)
3. Tertiary structure homologs from Protein Data Bank (flag -pdb)
4. Gene Ontology (flag -go) 

````
usage: apricot addanno [-h] [--force] [--pdb] [--psortb] [--raptorx] [--refss]
                       [--analysis_path ANALYSIS_PATH] [--fasta FASTA]
                       [--selected SELECTED] [--outpath OUTPATH]
                       [--pdb_path PDB_PATH] [--psortb_path PSORTB_PATH]
                       [--raptorx_path RAPTORX_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --force, -F           force flag for the current analysis, removes already
                        existing predictions
  --pdb, -PDB           Optional annotation of the selected protein by PDB
                        structure homolog
  --psortb, -PSORTB     Optional annotation of the selected protein by
                        localization using PsortB
  --raptorx, -RAPTORX   Optional annotation of the selected protein by
                        secondary structure using RaptorX
  --refss, -REFSS       Optional annotation of the selected protein by
                        secondary structure using literature reference
  --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                        Provide analysis path
  --fasta FASTA, -fa FASTA
                        Provide absolute path of fasta files for query
                        proteins
  --selected SELECTED, -sel SELECTED
                        Provided selected protein table
  --outpath OUTPATH, -o OUTPATH
                        Output path for additional annotation data
  --pdb_path PDB_PATH, -pdb_path PDB_PATH
                        Provide absolute path of APRICOT formatted pdb
                        database ~pdb/pdb_sequence/pdb_sequence.txt
  --psortb_path PSORTB_PATH, -psortb_path PSORTB_PATH
                        Provide absolute path of APRICOT installed psortb
  --raptorx_path RAPTORX_PATH, -raptorx_path RAPTORX_PATH
                        Provide absolute path of APRICOT installed raptorx
                        till the perl script run_raptorx-ss8.pl
````

The resulting files are stored in the directory 4_additional_annotations in the corresponding sub-folders, as shown below:
````
APRICOT_analysis
    └───├output
            └───├4_additional_annotations               # Location for additional annotations for the 
                    |                                   # selected queries using subcommand 'addanno'
                    └───├pdb_sequence_prediction        # PDB structure homologs of the selected 
                    |                                   # queries (flag --pdb, -PDB)
                    └───├protein_localization           # PSORTb based localization of the selected 
                    |                                   # queries (flag --psortb, -PSORTB)
                    └───├protein_secondary_structure    # RaptorX based structure of the selected 
                                                        # queries (flag --raptorx, -RAPTORX)
````

####subcommand `summary`
Quick help: `$ python3 APRICOT/bin/apricot summary -h`

To get an overview of the analysis carried out on a set of query proteins, this sub command can be used. It generate information like, how many queries could be mapped to the UniProt IDs, how many contain the reference domains etc., to provide analysis overview.

````
usage: apricot summary [-h] [--analysis_path ANALYSIS_PATH]
                       [--query_map QUERY_MAP] [--domains DOMAINS]
                       [--unfilter_path UNFILTER_PATH] [--outpath OUTPATH]

optional arguments:
  -h, --help            show this help message and exit
  --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                        Provide analysis path
  --query_map QUERY_MAP, -q QUERY_MAP
                        query_to_uids.txt file created by APRICOT to save
                        query mapping information
  --domains DOMAINS, -d DOMAINS
                        File containing all the keyword selected_domains of
                        interest
  --unfilter_path UNFILTER_PATH, -uf UNFILTER_PATH
                        Directory with the unfiltered domain data from
                        output-1 (unfiltered_data)
  --outpath OUTPATH, -o OUTPATH
                        Provide output path
````
The resulting files are stored in the directory 5_analysis_summary in the corresponding sub-folders, as shown below:
````
APRICOT_analysis
    └───├output
            └───├5_analysis_summary # Location for the output data obtained from the subcommand 'summary'
                | APRICOT_analysis_summary.csv
````

####subcommand `format`
Quick help: `$ python3 APRICOT/bin/apricot format -h`

Formats and stores various tables in the HTML tabels (--html), excel files (--xlsx) or both.

````
usage: apricot format [-h] [--analysis_path ANALYSIS_PATH] [--inpath INPATH]
                      [--html] [--xlsx] [--outpath OUTPATH]

optional arguments:
  -h, --help            show this help message and exit
  --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                        Provide analysis path
  --inpath INPATH, -i INPATH
                        Choose folder from analysis to be converted
  --html, -HT
  --xlsx, -XL
  --outpath OUTPATH, -o OUTPATH
                        Output path for files with different file formats
````
The resulting files are stored in the directory format_output_data in the corresponding sub-folders, as shown below:
````
APRICOT_analysis
    └───├output
            └───├format_output_data # Location for the output data obtained from the subcommand 'format'
                    └───├excel_files               # excel files (flag -XL)
                    └───├html_files                # HTML files (flag -HT)
````

####subcommand `vis`
Quick help: `$ python3 APRICOT/bin/apricot vis -h`

Visualize different resulting data like predicted domains sites, tertiary structure of selected proteins etc.

````
usage: apricot vis [-h] [--analysis_path ANALYSIS_PATH]
                   [--ann_score ANN_SCORE] [--add_anno ADD_ANNO] [--domain]
                   [--annoscore] [--secstr] [--localiz] [--msa] [--complete]
                   [--outpath OUTPATH]

optional arguments:
  -h, --help            show this help message and exit
  --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                        Provide analysis path
  --ann_score ANN_SCORE, -an ANN_SCORE
                        Provide annotation score file
  --add_anno ADD_ANNO, -ad ADD_ANNO
                        Provide path to additional annotation
  --domain, -D          Visualizes predicted domains on the query by
                        highlighting
  --annoscore, -A       Visualizes overview of prediction statistics
  --secstr, -S          Visualizes secondary structures predicted by RaptorX
  --localiz, -L         Visualizes subcellular localization predcited by
                        PsortB
  --msa, -M             Visualizes Multiple Sequence Alignments of homologous
                        sequences from PDB
  --complete, -C        Visualizes all the possible features
  --outpath OUTPATH, -o OUTPATH
                        Output path for visualization files
````
The resulting files are stored in the directory visualization_files in the corresponding sub-folders, as shown below:

````
APRICOT_analysis
    └───├output
            └───├visualization_files # Location for the output data obtained from the subcommand 'vis'
                    └───├domain_highlighting      # Visualizing the domain sites on the protein sequences
                    └───├homologous_pdb_msa       # Multiple sequence alignment of the structure homologs
                    └───├overview_and_statistics  # Visualizing the overview of the selected query proteins
                    └───├secondary_structure      # Visualizing 3-state secondary struvture of the query sequence
                    └───├subcellular_localization # Heatmap showing the probability of different localization sites 
````

###Versions/Change log
Please check the current version [here](https://github.com/malvikasharan/APRICOT/blob/master/CHANGELOGS.txt).
