#APRICOT TUTORIAL

This tutorial provides an easy way to test different modules of APRICOT and understand the basic usage of this pipeline.

###Requirements:

1) Basic files required to run the APRICOT pipeline for tutorial/demonstration purpose including the Shell script [run_example.sh](https://github.com/malvikasharan/APRICOT/blob/master/run_example.sh) that can be executed in a linux environment.

use wget

    $ wget https://zenodo.org/record/51705/files/APRICOT-1.0-demo_files-MS.zip
    $ unzip APRICOT-1.0-demo_files-MS.zip
    $ cp APRICOT-1.0-demo_files-MS/run_example.sh .


or [download manually](https://zenodo.org/record/51705/files/APRICOT-1.0-demo_files-MS.zip)

2) Get APRICOT repository via git

    $ git clone https://github.com/malvikasharan/APRICOT.git

 or, use pip to install/update the package
 
     $ pip install bio-apricot
 
 or [download manually](http://malvikasharan.github.io/APRICOT/)

####Not required

APRICOT requires local databases of Cdd and InterPro databases, along with the BLAST executables and InterProScan to carry out domain predictions. Additonally, in order to use the provide additional annotation of the proteins with biological features, it uses locally installed Psort and RaptorX tools. These requirements have been discussed in detail in the [documentation](https://github.com/malvikasharan/APRICOT/blob/master/README.md). 

We will **NOT** install these for the tutorial, instead we have provided the required files that should allow you test the functionality of the tool [ [Zenodo record](https://zenodo.org/record/51705/files) ].

###Tutorial with an example analysis

APRICOT can be executed by python (python3 is recommended) in a linux environment. In this part, we will go through the shell script `run_example.sh` step by step.

####Defining paths

Users can provide information for these paths.

`````

## User defined PATHS (default paths are given)

ANALYSIS_PATH=APRICOT_analysis  # path where the analysis data by APRICOT will be stored
APRICOT_PATH=APRICOT            # path where APRICOT modules are located, by-default we use APRICOT as the name of git library
ROOT_DB_PATH=source_files       # path where the source files and databases will be stored

`````

APRICOT stores databases and source files in these paths.

`````

## FIXED PATHS 

# Source data downloaded by APRICOT
DB_PATH=$ROOT_DB_PATH/reference_db_files

## PATHS for domain databases
CDD_PATH=$DB_PATH/cdd/Cdd
INTERPRO_PATH=$DB_PATH/interpro/interproscan

`````

####Creating analysis folders

1) We will create each of the paths that we defined above in the section: **Defining paths**.

`````

set_up_analysis_folder(){
    
    for paths in $ROOT_DB_PATH $APRICOT_PATH $ANALYSIS_PATH $APRICOT_LIBRARY
    do
        if ! [ -d $paths ] 
        then
            mkdir $paths
        fi
    done
    if ! [ -d $DB_PATH ] 
        then
            mkdir $DB_PATH
    fi
    for db_subpath in cdd go_mapping interpro pfam
    do
        if ! [ -d $DB_PATH/$db_subpath ] 
        then
            mkdir $DB_PATH/$db_subpath
        fi
    done
    ...
}

`````

This will create a main folder `source_files` with subfolder as shown below.


`````

source_files
    └───├domain_data            #Location for the files containing keywords for domain selection and subsequently selected domains
    |
    └───├reference_db_files
            └───├cdd                            #Cdd related reference files
            |   └───├Cdd                        #Cdd database (Not required for the tutorial)
            |   └───├cdd_annotation_data        #Cdd related annotation file
            └───├pfam
            └───├interpro                       #InterPro related reference files
            |   └───├interproscan               #Interpro database and InterProScan related tools (Not required for the tutorial)
            |   └───├interpro_annotation_data   #interPro related annotation files
            └───├go_mapping                     #GO related data containing GO anotation for the domains obtained from CDD and InterPro 

`````


2) Using `create` subcommand from APRICOT, we will create the analysis folder and its subfolder. 

`````
set_up_analysis_folder(){
    ...
    python $APRICOT_PATH/bin/apricot create $ANALYSIS_PATH
}

`````

This generates a main folder `APRICOT_analysis` (name can be defined by users), which contains subfolders as shown below.

`````

APRICOT_analysis
    └───├input                                 # Location used by subcommand 'query' to store all the related files
    |       └───├query_proteins                 # Location for the list of query proteins
    |       |
    |       └───├uniprot_reference_table        # Location for storing the reference table downloaded from UniProt 
    |       |
    |       └───├mapped_query_annotation        # All the query proteins that are mapped to at least one UniProt annotations 
    |       |   ├fasta_path_mapped_query        # Fasta files obtained for all the query proteins, can be used for query fasta files
    |       |   ├xml_path_mapped_query          # UniProt xml files obtained for all the query proteins
    |
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

`````


####Fetching required source files

We have provided few processed files, which is available in *apricot_demo_files* and was downloaded via zenodo, if it is already available, please comment the first three lines in the script, which copies these files to the APRICOT defined paths.

Additionally, we will download domain annotation files from CDD and Pfam databases.

`````

basic_requirements_for_demo(){
    zenodo_link_for_demo_data=https://zenodo.org/record/51705/files/APRICOT-1.0-demo_files-MS.zip
    wget $zenodo_link_for_demo_data
    unzip apricot_demo_files.zip
    cp apricot_demo_files/go_mapping/* $DB_PATH/go_mapping
    cp apricot_demo_files/interpro_annotation_data/* $DB_PATH/interpro/interpro_annotation_data
    cp apricot_demo_files/cdd_analysis/* $ANALYSIS_PATH/output/0_predicted_domains/cdd_analysis
    cp apricot_demo_files/ipr_analysis/* $ANALYSIS_PATH/output/0_predicted_domains/ipr_analysis
    
    ## CDD annotation table
    wget -c -P $DB_PATH/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
    gunzip $DB_PATH/cdd/cdd_annotation_data/*
    
    ## PfamA annotation table
    pfam_release=Pfam30.0
    wget -c -P $DB_PATH/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/$pfam_release/database_files/pfamA.txt.gz
    gunzip $DB_PATH'/pfam/pfamA.txt.gz'
}

`````

####Providing query proteins using the subcommand: `query`

In this analysis we will identify protein that contains RRM/RNP, which is a family of conserved RNA-binding domains.

Users can provide query proteins using various options. Here we use the input option as UniProt identifiers and provide 2 query proteins: P0A6X3,P00957.

P0A6X3 is used as an example for positive test, it is Hfq protein that contains sm and RRM/RNP like domain. P00957 is used as an example for negative test, it is alaS protein that contains domain related to tRNA-ligase therefore, it must not be identified with domains reltaed to RRM/RNP.

`````

## *REQUIRED* INPUT-1: provide comma separated list of UniProt ids##
query_uids='P0A6X3,P00957'

provide_input_queries(){
    ## Option-1: UniProt identifier
    python $APRICOT_PATH/bin/apricot query --analysis_path $ANALYSIS_PATH --uids $query_uids
}

````

####Providing keyword inputs using the subcommand: `keywords`

There are two sets of keyword inputs, first-set is required to select domains from domain databases and second set, which is an optional input, should comprise of terms that will classify our results accordingly.

In this turtorial we are interested in identifying RRM containing protein, hence, we will use RRM as one of the terms. Additionally, we can provide other terms (for example, KH and DEAD) to see if there are domains associtaed with those terms could be identified in our query proteins. 

For the second set, we have listed few enzymes along with RRM and RNP.

`````

### *REQUIRED* Input-2, comma separated list of keywords for domain selection
domain_kw='RRM,KH,DEAD'

### *OPTIONAL* Input-2, comma separated list of keywords for protein classification based on the predicted domains
class_kw='ribosom,helicase,synthetase,polymerase,transferase,nuclease,RRM,RNP'

provide_domain_and_class_keywords(){
    python $APRICOT_PATH/bin/apricot keywords $domain_kw -cl $class_kw
}

`````

These keywords are listed in the files `keywords_for_domain_selection.txt` and `keywords_for_result_classification.txt` present in the folder `source_files` as shown below.

`````

source_files
    └───├domain_data
            keywords_for_domain_selection.txt  
            keywords_for_result_classification.txt
    
`````


####Selecting domains of interest using the subcommand: `select`

APRICOT uses the keywords provided in previous section and uses them to select functional domains. Users can use `-C` flag to select only CDD related domains or `-I` flag to select only InterPro related domains.

In this tutorial we will use the default option, which selects domains from both CDD and InterPro databases.

`````
    
select_domains_by_keywords(){
    python $APRICOT_PATH/bin/apricot select
}

`````

The selected domains are saved in theor respective location as ashown below.

`````

source_files
    └───├domain_data            
            └───├cdd                                #Containes individual files generated for each keyword related domains      
            |    key1_related_cdd_domains.tab
            |    key2_related_cdd_domains.tab
            |    ..
            └───├interpro                           #Containes individual files generated for each keyword related domains
            |    key1_related_interpro_domains.tab
            |    key2_related_interpro_domains.tab
            |    ..
            |all_keyword_selected_domain_data.tab   #All the keyword selected domains are mapped and combined
    
`````

####Domain predictions using the subcommand: `predict`

This subcommand uses one of the core modules of APRICOT, which predicts all the possible domains in the query domains. 

For this analysis, APRICOT uses both the databases by default, however single database can be defined by using flag `-C` or `-I` for CDD and InterPro respectively. In case users provide the input as fasta files, the `query` subcommand can be skipped and the prediction of domains can be carried out directly, however in that case the path for fasta files (FASTA_PATH) can be provided using the option `--fasta $FASTA_PATH`.

 APRICOT skips re-prediction of the domains when the output files are present for the analysis of each query proteins, however users can use the flag `-F` to *force* the re-analysis. 

`````

run_domain_prediction(){
    python $APRICOT_PATH/bin/apricot predict --analysis_path $ANALYSIS_PATH --cdd_db $CDD_PATH --ipr_db $INTERPRO_PATH
}

`````

For this tutorial, to avoid the use of domain databases and tools (avoid the prediction of domains), we provided the output files generated by domain prediction analysis and copied to the required subfolders as shown below.

`````

APRICOT_analysis
    └───├output                             
            └───├0_predicted_domains    #location for storing files generated by domain prediction
                └───├cdd_analysis       #domains predicted for each protein using CDD datasets
                |       P00957.txt
                |       P0A6X3.txt
                |
                └───├ipr_analysis       #domains predicted for each protein using InterPro datasets
                        P00957.tsv
                        P0A6X3.tsv

`````


####Filtering the predicted domains using the subcommand: `filter`

All the domains (predicted by `predict`) undergoes a filtering step in order to select proteins that are predicted with the domains of interest (selected from databases using `select`).

In this tutorial we have used the parameters defined as default (`--similarity 24` for 24% minimum similarity between the reference and predicted domain and `--coverage 39`` for 39% minimum domain coverage in the query protein), however users can provide cut-offs for different parameters (refer documentation).

`````

filter_domain_analysis(){
    python $APRICOT_PATH/bin/apricot filter --analysis_path $ANALYSIS_PATH \
    --similarity 24 --coverage 39
}

`````

The files obtained from this analysis are stored in the subfolder `1_compiled_domain_information` in the main analysis folder. Additionally, the information of the proteins obtained from uniProt are combined and store in the folder combined_data. These file location are as shown below. 

`````

APRICOT_analysis
    └───├output                             
            └───├1_compiled_domain_information  #Formatted flat files containg domain information
            |   └───├selected_data              #Files containing proteins that contain domains of interest with the predcited domains
            |   |       cdd_filtered.csv        #proteins containing CDD domains of interest
            |   |       cdd_filtered_id.csv     #proteins IDs containing CDD domains IDs of interest
            |   |       ipr_filtered.csv        #proteins containing InterPro domains of interest
            |   |       ipr_filtered_id.csv     #proteins IDs containing InterPro domains IDs of interest
            |   |
            |   └───├unfiltered_data                            #All the domains predicted in the query proteins (unfiltered)
            |            cdd_unfiltered_all_prediction.csv  
            |            ipr_unfiltered_all_prediction.csv
            |
            └───├2_selected_domain_information
                └───├combined_data                              #Annotation extended for the selected proteins
                        annotation_extended_for_selected.csv    
`````


####Classify all the selected domains from previous analysis using the subcommand: `classify`

All the selected proteins with their domains (selected by `filter`) are classified into smaller subsets to help navigating the output files. This classification uses the keywords provided by users, which are either explicitely defined (`-cl` flag in `keywords`) or are used for the domain selection. 

`````

classify_filtered_result(){
    python $APRICOT_PATH/bin/apricot classify --analysis_path $ANALYSIS_PATH
}

`````

The selected proteins that are selected based on the domains of interest are classified when the annotations contain on ethese proteins can stored in the subfolder `2_selected_domain_information` as shown below.

`````

APRICOT_analysis
    └───├output                             
            └───├2_selected_domain_information         #Selected data classified into smaller subsets based on the keyword input
                └───├classified_data
                        RNP_selected_data.csv  
                        RRM_selected_data.csv
                
`````

####Calculating annotation scores for the selected domains using the subcommand: `annoscore`

This subcommand uses another important module of APRICOT to calculate annotation-based scores for each predicted domains in the query proteins. Please refer documentation to understand different sets of features, which have been used in APRICOT for the scoring of the predicted domains with respect to their reference consensus.

`````

calculate_annotation_score(){
    python $APRICOT_PATH/bin/apricot annoscore \
    --analysis_path $ANALYSIS_PATH
}

`````

The files generated from this analysis are stored in the subfolder `3_annotation_scoring in the analysis` folder as shown below.

`````

APRICOT_analysis
    └───├output                             
            └───├2_selected_domain_information
            
`````

####generating analysis summary using the subcommand: `summary`

Users can summarize the analysis result using this module. The summary file contains an overview of the entire analysis that includes, for example, the query proteins mapped to UniPro, total selected domains per keyword, summary of domain predictions and their selection.

`````

create_analysis_summary(){
    python $APRICOT_PATH/bin/apricot summary \
    --analysis_path $ANALYSIS_PATH
}

`````

The summary file is stored in the subfolder `5_analysis_summary` analysis folder as shown below.

`````

APRICOT_analysis
    └───├output                             
            └───├5_analysis_summary
                       APRICOT_analysis_summary.csv         #Summary file
            
`````

#####Format output files using the subcommand: `format`

APRICOT by default produces output files in comma-separated version (.csv). Users can convert these files to HTML format using `-HT` flag or excel format (.xlsx) using `-XL` flag, where the later one uses `openpyxl` python module.

In this tutorial we have used `-HT` option.

`````

output_file_formats(){
    python $APRICOT_PATH/bin/apricot format \
    --analysis_path $ANALYSIS_PATH \
    -HT
}

`````

All the files in the format of selection are stored in the subfolder `format_output_data` in the main analysis folder as shown below.

`````

APRICOT_analysis
    └───├output                             
            └───├format_output_data
                └───├html_files                         #Output files for each folder in HTML format
                |   └───├0_predicted_domains  
                |   └───├1_compiled_domain_information  
                |   └───├2_selected_domain_information  
                |   └───├3_annotation_scoring  
                |   └───├4_additional_annotations 
                |   └───├5_analysis_summary
                |
                └───├excel_files                        #Output files for each folder in Excel format
                    └───├ ...
            
`````

This concludes the tutorial for the analysis conducted by APRICOT. All of these modules can be run in an automated streamlined manner using the provided shell script as shown below.

`````

sh run_example.sh

`````

###Troubleshooting

We have tested the described modules intensively, however if you encounter any bugs and have problems running any of these modules, please contact me via email: malvikasharan@gmail.com or report the issues in this repository.

Your feedback and comments are welcome.



