#APRICOT

###A tool for sequence-based identification and characterization of protein classes

**APRICOT** is a computational pipeline for the identification of specific functional classes of interest in large protein sets. The pipeline uses efficient sequence-based algorithms and predictive models like signature motifs of protein families for the characterization of user-provided query proteins with specific functional features. The dynamic framework of APRICOT allows the identification of unexplored functional classes of interest in the large protein sets or the entire proteome.

###Summary of the pipeline

The functionality of APRICOT can be explained in 3 parts: program input, analysis modules and program output. 

#####Program inputs
1) Query proteins that are subjected to characterization by domains and associated functional properties

2) Set of terms indicating protein domains of functional relevance. Based on these inputs

#####Analysis modules of APRICOT
The functionalities involved in the primary analysis are retrieval of sequences and known annotations of query proteins, collection of domains of interest from domain databases, and identification of all the functional domains in a given query.

The data obtained from the primary analysis is used as a resource for the secondary analysis, which mainly involves the selection of proteins based on the predicted domains, the calculation of the statistical and biological significance of the selected proteins to possess the function of interest by means of sequence-based features, and biological characterization of these proteins by additional annotations like subcellular localization and secondary structures. 

#####Program output
For each analysis step, APRICOT generates results in tablular manner, in addition with an overview of the analysis and graphics associated with the resulting information.

#####Trivia
The initial focus of this project was to identify functional domains in bacterial proteins that have the potential to interact with RNA and understand their regulatory roles and mechanisms. Hence, the tool is named **APRICOT** that stands for **A**nalysing **P**rotein **R**NA **I**nteractions by **Co**mbined-scoring **T**echnique. However, due to the adaptability of the pipeline to different sets of reference domains, APRICOT is not limited to RBP identification and has been tested successfully on the other classes of functional domains as well. We are carrying out the experimental validations of few RBPs identified by APRICOT in collaboration with the biologists in our lab, which can provide a high confidence dataset and contribute significantly to the improvement of this computational approach.

###Authors and Contributors

The tool is designed and developed by Malvika Sharan @malvikasharan in the lab of Prof. Dr. Jörg Vogel in the Institute for Molecular Infection Biology at the University of Würzburg. Dr. Konrad Förstner @konrad contributed to the project by providing important technical supervision and discussions. The authors are grateful to Prof. Thomas dandekar, Dr. Ana Eulalio, Dr. Charlotte Michaux and Caroline Taouk for critical discussions and feedback.

###Source code

The source codes of APRICOT are available at https://github.com/malvikasharan/APRICOT.

##License

APRICOT is open source software and available under the ISC license.

Copyright (c) 2011-2015, Malvika Sharan, <malvika.sharan@uni-wuerzburg.de>

Please read the license content [here](https://github.com/malvikasharan/APRICOT/blob/master/LICENSE.md).

##Installation
The scripts for the installaton of the different componenents of APRICOT (databases, tools and flatfiles) are available on the GitHub repository.
The [Docker image for APRICOT](https://github.com/malvikasharan/APRICOT/edit/master/Dockerfile) will be available soon.

##Contact

For question, troubleshooting and requests, please feel free to contact Malvika Sharan at <malvika.sharan@uni-wuerzburg.de> / <malvikasharan@gmail.com>

##Tool Requirements

APRICOT is implemented in Python 3 and can be executed in Linux/Unix system. APRICOT requires few third party packages, namely [Biopython](http://biopython.org/wiki/Main_Page), [BLAST executables](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download), [interproscan](https://www.ebi.ac.uk/interpro/interproscan.html), python libraries like [Matplotlib](http://matplotlib.org/), [requests](https://pypi.python.org/pypi/requests) and few other optional tools that are mentioned below.

Please update the package list: `sudo apt-get update` and install the required packages:
    `sudo apt-get install python3 python3-setuptools python3-pip python3-matplotlib`
    

##Instructions for the installation

Please clone `git clone https://github.com/malvikasharan/APRICOT.git` or [download](https://github.com/malvikasharan/APRICOT/archive/master.zip) this repository in your system locally, which comprise of a directory tree of the following structure.
```
APRICOT
│   APRICOT_EXAMPLE.md
│   CHANGELOG.md
│   Dockerfile
│   LICENCE.md
│   README.md
└───├apricotlib
└───├bin
└───├run_scripts
```

The run script for the installation of all the required files (apricot_db_tool.sh) can be found in `run_scripts` folder of this github repository. Users need to provide the path of the APRICOT repository in the system (APRICOT) and the path where the users wish to install APRICOT related tools and files (apricot_db_and_tools). APRICOT will mainly install  BLAST executables (ftp://ftp.ncbi.nih.gov/blast/executables/blast+) and InterProScan (ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/) along with establishing CDD and InterPro databases locally.

    sh apricotlib/apricot_db_tool.sh APRICOT apricot_db_and_tools

Alternatively, the BLAST executables (rpsblast, blastp, psiblast, makeblastdb) can be installed locally as directed [here](http://bioinformatics.ai.sri.com/ptools/installation-guide/released/blast.html) and CDD can be established locally (in the path apricot_db_and_tools/conserved_domain_database/Cdd) as shown below:

    wget ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/*
    tar xvf file_name

InterProSan can be downloaded and installed locally (in the path apricot_db_and_tools/interpro/InterProScanData) with the required database as shown below:

    wget ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.17-56.0/interproscan-5.17-56.0-64-bit.tar.gz
    tar xvf interproscan-5.17-56.0-64-bit.tar.gz

APRICOT also reuires various flatfiles, namely [CDD tables](ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.info), [InterPro tables](ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5), [PDB secondary structures](http://www.rcsb.org/pdb/files/ss.txt), [taxonomy information] (http://www.uniprot.org/docs/speclist.txt), [Gene Ontology data](http://www.geneontology.org/ontology/go.obo) and [pfam table](ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam29.0/database_files/), which are downloaded and saved locally in the pre-defined location (for e.g. 'reference_db_files' in 'APRICOT' folder).
```
APRICOT
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

##APRICOT’s subcommands

Each subcommand requires the path to the analysis folder ('APRICOT_analysis' by deafult). Different subcommands can be quickly viewed by running `python3 APRICOT/bin/apricot -h`.

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
                        (required). An optional list of term can be provided 
                        by using the flag -cl to classify results based on the 
                        functions associated with the identified domains
    select              Select functional domains of interest (specified by
                        keywords) from CDD and InterPro. please use
                        -C for CDD or -I for InterPro to use specific consortium
    predict             Predict functional domains in the queries based on CDD 
                        and InterPro. please use -C for CDD or -I for InterPro 
                        to use specific consortium
    filter              Filter queries predicted with domains of interest and 
                        extend their annotations with UniProt reference. Cut-offs 
                        for the parameters can also be provided (please see -h).
    classify            Optional classification of selected prediction in smaller 
                        groups by class keywords provided by -cl flag of the 
                        subcommand keywords
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
 
##create
Quick help: `python3 APRICOT/bin/apricot create -h`

This subcommand creates all the required directories to store input and output data acquired from APRICOT analysis. The main analysis directory can be named by the users (default name: APRICOT_analysis).
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
            |   query_to_uids.txt  # User provided queries (gene ids/protein names/whole proteome set) 
            |                      # mapped to the UniProt Ids
            |
            └───├uniprot_reference_table
            |   query_uids_reference.tab   # Basic annotations of the queries obtained from 
            |                              # uniProt knowledgebase
            |
            └───├mapped_query_annotation  
                    └───├fasta_path_mapped_query  # Location for protein FASTA sequences of each query
                    |   query_id-1.fasta 
                    |   query_id-2.fasta
                    |   ...
                    |   query_id-n.fasta
                    |        
                    └───├xml_path_mapped_query3  # Location for protein FASTA sequences of each query
                    |    query_id-1.xml
                    |    query_id-2.xml
                    |    ...
                    |    query_id-n.xml
                    |
                    └───├mapped_protein_xml_info_tables  
                         query_feature_table.csv  # File containing all the features of the queries 
                                                  #obtained by parsing xml files
```

The structure of directories and the enclosing files in the 'output' folder in the analysis directory:
```
APRICOT_analysis
    └───├output
            └───├0_predicted_domains            # Location for the output data obtained from the subcommand 'predict'
            |        
            └───├1_compiled_domain_information  # Location for the output data obtained from the subcommand 'filter'          
            |        
            └───├2_selected_domain_information            
            |    
            └───├3_annotation_scoring          # Location for the output data obtained from the subcommand 'annoscore'
            |   
            └───├4_additional_annotations      # Location for additional annotations for the selected queries using subcommand 'addanno'
            |
            └───├5_analysis_summary             # Location for the output data obtained from the subcommand 'summary'
            |
            └───├format_output_data             # Location for the output data obtained from the subcommand 'format'
            |        
            └───├visualization_files            # Location for the output data obtained from the subcommand 'vis'
```

##taxid
Quick help: `python3 APRICOT/bin/apricot taxid -h`
        
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
 
##query
Quick help: `python3 APRICOT/bin/apricot query -h`
        
````
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
````
    
##keywords
Quick help: `python3 APRICOT/bin/apricot keywords -h`
        
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
    
##select
Quick help: `python3 APRICOT/bin/apricot select -h`
        
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
    
##predict
Quick help: `python3 APRICOT/bin/apricot predict -h`
        
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

````
APRICOT_analysis
    └───├output
            └───├0_predicted_domains            # Location for the output data obtained from the subcommand 'predict'
                    └───├cdd_analysis          # Details of domain predicted from CDD for each query
                    |    query_id-1.txt
                    |    query_id-2.txt
                    |    ...
                    |    query_id-n.txt
                    |
                    └───├ipr_analysis          # Details of domain predicted from InterPro for each query
                    |    query_id-1.tsv
                    |    query_id-2.tsv
                    |    ...
                    |    query_id-n.tsv
````


    
##filter
Quick help: `python3 APRICOT/bin/apricot filter -h`
        
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
    
````
APRICOT_analysis
    └───├output
        └───├1_compiled_domain_information  # Location for the output data obtained from the subcommand 'filter'          
                    └───├unfiltered_data                    # Information of all the domains in the query proteins predicted.
                    |    cdd_unfiltered_all_prediction.csv  # CDD 
                    |    ipr_unfiltered_all_prediction.csv  # InterPro
                    |
                    └───├selected_data                      # Information of the selected reference domains in the query proteins
                    |    cdd_filtered.csv                   # CDD 
                    |    ipr_filtered.csv                   # InterPro 
````

##classify
Quick help: `python3 APRICOT/bin/apricot classify -h`
        
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
````
APRICOT_analysis
    └───├output    
            └───├2_selected_domain_information            
                    └───├combined_data         # All the selected domain data extended with the UniProt annotation
                    |    annotation_extended_for_selected.csv
                    |
                    └───├classified_data       # Location for the output data obtained from the subcommand 'classify'
                    |    classification_key-1_selected_data.csv  # Files containing subsets of predicted data...
                    |    classification_key-2_selected_data.csv  # ... based on user provided classification keys.
````
            
##annoscore
Quick help: `python3 APRICOT/bin/apricot annoscore -h`
        
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

````
APRICOT_analysis
    └───├output
            └───├3_annotation_scoring          # Location for the output data obtained from the subcommand 'annoscore'
                |    annotation_extended_for_selected.csv
````

##addanno
Quick help: `python3 APRICOT/bin/apricot addanno -h`
        
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

````
APRICOT_analysis
    └───├output
            └───├4_additional_annotations      # Location for additional annotations for the selected queries using subcommand 'addanno'
            |        └───├pdb_sequence_prediction       # PDB structure homologs of the selected queries (flag --pdb, -PDB)
            |        └───├protein_localization          # PSORTb based localization of the selected queries (flag --psortb, -PSORTB)
            |        └───├protein_secondary_structure   # RaptorX based structure of the selected queries (flag --raptorx, -RAPTORX)
````

##summary
Quick help: `python3 APRICOT/bin/apricot summary -h`
        
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
````
APRICOT_analysis
    └───├output
            └───├5_analysis_summary             # Location for the output data obtained from the subcommand 'summary'
            |    APRICOT_analysis_summary.csv
````

##format
Quick help: `python3 APRICOT/bin/apricot format -h`
        
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

````
APRICOT_analysis
    └───├output
            └───├format_output_data             # Location for the output data obtained from the subcommand 'format'
            |        └───├excel_files               # excel files (flag -XL)
            |        └───├html_files                # HTML files (flag -HT)
````

##vis
Quick help: `python3 APRICOT/bin/apricot vis -h`
        
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

````
APRICOT_analysis
    └───├output
            └───├visualization_files            # Location for the output data obtained from the subcommand 'vis'
            |        └───├domain_highlighting  
            |        └───├homologous_pdb_msa  
            |        └───├overview_and_statistics  
            |        └───├secondary_structure  
            |        └───├subcellular_localization
````

##Versions/Change log
Please check the current version [here](https://github.com/malvikasharan/APRICOT/blob/master/CHNAGELOG.md).



