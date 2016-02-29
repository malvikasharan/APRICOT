##APRICOT: A tool for sequence-based identification and characterization of protein classes

###APRICOT in a nutshell

**APRICOT** is a computational pipeline for the identification of specific functional classes of interest in large protein sets. The pipeline uses efficient sequence-based algorithms and predictive models like signature motifs of protein families for the characterization of user-provided query proteins with specific functional features. The dynamic framework of APRICOT allows the identification of unexplored functional classes of interest in the large protein sets or the entire proteome.

###Summary of the pipeline

The initial focus of this project was to identify functional domains in bacterial proteins that have the potential to interact with RNA and understand their regulatory roles and mechanisms, therefore it was named as **APRICOT** (stands for **A**nalysing **P**rotein **R**NA **I**nteractions by **Co**mbined-scoring **T**echniques). 

The functionality of APRICOT can be explained in 3 parts: program input, analysis modules and program output. There are two program inputs, query proteins, which are subjected to characterization by domains and associated functional properties, and terms (like RNA-binding) indicating protein domains of functional relevance, which are RBDs in this case. Based on these inputs, APRICOT carries out an analysis using different components of the pipeline. The analysis modules of APRICOT can be explained as primary analysis and secondary analysis. The functionalities involved in primary analysis are retrieval of sequences and known annotations of query proteins, collection of domain of interest from domain databases, and, prediction of all the functional domains in a given query using tools for domain prediction. The data obtained from the primary analysis is used as a resource for the secondary analysis, which mainly involves the selection of proteins based on the predicted domains, the calculation of the statistical and biological significance of the selected proteins to possess the function of interest and, biological characterization of these proteins by additional annotations like subcellular localization and secondary structures. For each analysis, APRICOT generates consistent overview and several tables and graphics associated with the resulting information.

Due to the flexible choice of reference predictive models, several proteins of known classes are being tested by this computational pipeline. We are also carrying out experimental validations of few RBPs in collaboration with the biologists in our lab, which can contribute significantly to the improved functional characterization of the query proteins by APRICOT.  

###Authors and Contributors

The tool is designed and developed by Malvika Sharan @malvikasharan in the lab of Prof. Dr. Jörg Vogel in the Institute for Molecular Infection Biology at the University of Würzburg. Dr. Konrad Förstner @konrad contributed to the project by providing important technical supervision and discussions. The authors are grateful to Prof. Thomas dandekar, Dr. Ana Eulalio, Dr. Charlotte Michaux and Caroline Taouk for critical discussions and feedback.

###Source code
The source code of READemption can be found at https://github.com/malvikasharan/APRICOT.

###Contact
For question, troubleshooting and pull-requests, please feel free to contact Malvika Sharan <malvika.sharan@uni-wuerzburg.de> or <malvikasharan@gmail.com>

###Installation and updating

##Requirements
APRICOT is implemented in Python 3 and therefore users are advised to have Python 3 installed in their system. APRICOT requires the third party packages [Biopython](http://biopython.org/wiki/Main_Page), [BLAST executables](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download), [interproscan](https://www.ebi.ac.uk/interpro/interproscan.html), python libraries like [Matplotlib](http://matplotlib.org/), [requests](https://pypi.python.org/pypi/requests) and few other optional tools that are mentioned below.

Please update the package list: `sudo apt-get update` and install the required packages:
    `sudo apt-get install python3 python3-setuptools python3-pip python3-matplotlib`
    

##Instructions for the installation

Please clone or download this repository in your system `git clone https://github.com/malvikasharan/APRICOT.git`, which will create a directory tree of the following structure.
```
APRICOT
│   README.md
│   LICENCE
│
└───├apricotlib
    ├bin
    ├run_scripts
```

The run script for the installation of all the required files (apricot_db_tool.sh) can be found in the github folder https://github.com/malvikasharan/APRICOT/run_scripts. Users need to provide the path of the APRICOT repository in the system (APRICOT_PATH) and the path where the users wish to install APRICOT related tools and files (DB_PATH). The APRICOT will mainly install [CDD](ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.info), [InterPro](ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/) and [BLAST executables](ftp://ftp.ncbi.nih.gov/blast/executables/blast+).

    sh $APRICOT_PATH/apricotlib/apricot_db_tool.sh $APRICOT_PATH $DB_PATH
    
Alternatively, CDD can downloaded and installed locally by:

    wget -c -P $apricot_db/conserved_domain_database/version_info ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.info
    wget -c -P $apricot_db/conserved_domain_database/Cdd ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/*
    for binary_files in $(ls $apricot_db/conserved_domain_database/Cdd)
    do
        tar xvf $apricot_db/conserved_domain_database/Cdd/$binary_files -C $apricot_db/conserved_domain_database/Cdd
    done

and InterPro can be downloaded and installed locally by:

    wget -c -P $apricot_db/interpro/InterProScanData ftp://ftp.ebi.ac.uk:21/pub/software/unix/iprscan/55.17-56.0/*-64-bit.tar*
    for files in $(ls $apricot_db/interpro/InterProScanData/*.tar.gz)
    do
        tar xvf $files -C $apricot_db/interpro/InterProScanData
    done

APRICOT also reuires various flatfiles, namely [CDD tables](ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.info), [InterPro tables](ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5), [PDB secondary structures](http://www.rcsb.org/pdb/files/ss.txt), [taxonomy information] (http://www.uniprot.org/docs/speclist.txt), [Gene Ontology data](http://www.geneontology.org/ontology/go.obo) and [pfam table](ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam29.0/database_files/), which are downloaded and saved locally in the pre-defined location (for e.g. reference_db_files in our bin folder).
```
bin
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
APRICOT allows additional annotations of the proteins by using various third party tools. For the secondary structure predictions APRICOT requires [RaptorX](https://github.com/Indicator/RaptorX-SS8.git)  which requires [RefSeq/nr database](ftp://ftp.ncbi.nih.gov/blast/db/FASTA) and for the subcellular localization APRICOT uses [PSORTb v2](https://github.com/lairdm/psortb-docker.git). These tools should be installed locally (please refer the run script) in order to allow APRICOT to carry out the optional annotations of proteins of interest.

###APRICOT’s subcommands

In general the subcommands require the analysis folder, which is 'APRICOT_analysis' by deafult. Different subcommands can be quickly viewed by running `python3 APRICOT/bin/apricot`.

````
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
 ````

###Performing an example analysis

###Troubleshooting

###License

###Versions/Change log

###Docker image
Will be availed shortly.


