#APRICOT TUTORIAL

With this tutorial we will explore different modules of APRICOT and its basic usage.

###Requirements:

1) Shell script `run_example.sh` that can be executed in a linux environment. [DOWNLOAD](https://github.com/malvikasharan/APRICOT/blob/master/run_example.sh)

2) Please clone `git clone https://github.com/malvikasharan/APRICOT.git` download the APRICOT repository.  [DOWNLOAD](http://malvikasharan.github.io/APRICOT/)

3) Please use the pypi link to update/install python packages.
`pip install bio-apricot`

4) Basic files required to run the APRICOT pipeline for tutorial/demonstration purpose. [DOWNLOAD]

####Not required

APRICOT requires local databases of Cdd and InterPro databases, along with the BLAST executables and InterProScan to carry out domain predictions. These requirements have been discussed in detail in the [documentation](https://github.com/malvikasharan/APRICOT/blob/master/README.md). 

We will **NOT** install these for the tutorial. For the demonstration of the APRICOT pipeline, we have provided few required files on [zenodo].

###Tutorial with an example analysis

In this part, we will go through the shell script `run_example.sh` step by step.

####Defining paths

Users can provide information for these paths.

`````

##User defined PATHS 

PYTHON_PATH=python3             #python version, works with python2, python3 and up
ANALYSIS_PATH=APRICOT_analysis  #path where the analysis data by APRICOT will be stored
APRICOT_PATH=APRICOT            #path where APRICOT modules are located, by-default we use APRICOT as the name of git library
ROOT_DB_PATH=source_files       #path where the source files and databases will be stored

`````

APRICOT stores databases and source files in these paths.

`````

##FIXED PATHS 

#Source data downloaded by APRICOT
DB_PATH=$ROOT_DB_PATH/reference_db_files

##PATHS for domain databases
CDD_PATH=$DB_PATH/cdd/Cdd
INTERPRO_PATH=$DB_PATH/interpro/interproscan

`````

####Defining input data

In this analysis we will identify protein that contains RRM/RNP, which is a family of conserved RNA-binding domains.

##Input-1: query proteins

Users can provide query proteins using various options. Here we use the input option as UniProt identifiers and provide 2 query proteins: P0A6X3,P00957.

P0A6X3 is used as an example for positive test, it is Hfq protein that contains sm and RRM/RNP like domain. P00957 is used as an example for negative test, it is alaS protein that contains domain related to tRNA-ligase therefore, it must not be identified with domains reltaed to RRM/RNP.

`````

## *REQUIRED* INPUT-1: provide comma separated list of UniProt ids##

query_uids='P0A6X3,P00957'

`````

##Input-1: keywords/terms

There are two sets of keyword inputs, first-set is required to select domains from domain databases and second set, which is an optional input, should comprise of terms that will classify our results accordingly.

Since, we are interested in identifying RRM containing protein, we will use it as one term. Additionally, we can provide other terms (for example, KH and DEAD) to see if there are domains associtaed with those terms could be identified in our query proteins.

For the second set, we have listed names of enzymes along with RRM and RNP.

`````

### *REQUIRED* Input-2, comma separated list of keywords for domain selection
domain_kw='RRM,KH,DEAD'

## *OPTIONAL* Input-2, comma separated list of keywords for protein classification based on the predicted domains
class_kw='ribosom,helicase,synthetase,polymerase,transferase,nuclease,RRM,RNP'
    
`````

####Creating analysis folders

1) We will create each of the paths that we defined above in the section: *Defining paths*.

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

2) Using `create` subcommand from APRICOT, we will create the analysis folder and its subfolder. 

`````
set_up_analysis_folder(){
    ...
    $PYTHON_PATH $APRICOT_PATH/bin/apricot create \
    $ANALYSIS_PATH
}

`````

####Fetching required source files

We have provided few processed files, which is available in *apricot_demo_files* and was downloaded via zenodo. We can copy these files to the APRICOT defined paths.

Additionally, we will download domain annotation files from CDD and Pfam databases.

`````

basic_requirements_for_demo(){
    ##zenodo_link_for_demo_data=
    wget $zenodo_link_for_demo_data
    unzip apricot_demo_files.zip
    cp apricot_demo_files/go_mapping/* $DB_PATH/go_mapping
    cp apricot_demo_files/interpro_annotation_data/* $DB_PATH/interpro/interpro_annotation_data
    cp apricot_demo_files/cdd_analysis/* $ANALYSIS_PATH/output/0_predicted_domains/cdd_analysis
    cp apricot_demo_files/ipr_analysis/* $ANALYSIS_PATH/output/0_predicted_domains/ipr_analysis
    
    ##CDD annotation table
    wget -c -P $DB_PATH/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
    gunzip $DB_PATH/cdd/cdd_annotation_data/*
    
    ##PfamA annotation table
    pfam_release=Pfam30.0
    wget -c -P $DB_PATH/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/$pfam_release/database_files/pfamA.txt.gz
    gunzip $DB_PATH'/pfam/pfamA.txt.gz'
}

`````



