#!/bin/bash
#AUTHOR: Malvika Sharan <malvikasharan@gmail.com>

PYTHON_PATH=python3
ANALYSIS_PATH=APRICOT_analysis
APRICOT_PATH=APRICOT
ROOT_DB_PATH=source_files

## FIXED PATHS for flatfiles downloaded by APRICOT
DB_PATH=$ROOT_DB_PATH/reference_db_files

## PATHS for domain databases
CDD_PATH=$DB_PATH/cdd/Cdd
INTERPRO_PATH=$DB_PATH/interpro/interproscan

if ! [ -e $APRICOT_PATH/apricotlib ]
then
    git clone https://github.com/malvikasharan/APRICOT.git $APRICOT_PATH
    ln -s $APRICOT_PATH/apricotlib $APRICOT_PATH/bin
fi
    
### Inputs: *REQUIRED* or *OPTIONAL* ###

## *OPTIONAL* provide species name to retrieve taxonomy ids for given species in bin/selected_taxonomy_ids.txt##
species=''

## *REQUIRED* INPUT-1: query proteins##

### This must not be altered by the users in the demonstration file
query_uids='P0A6X3,P00957'
    # Input-1, option 1: provide comma separated list of UniProt ids
    # P0A6X3 (positive test) is Hfq protein that contains sm and RRM/RNP like domain
    # P00957 (negative test) is alaS protein is a tRNA-ligase, hence will not be selected by RRM, KH or DEAD domains
    
## Not used in the demonstration file  
query_geneids=''
    # Input-1, option 2: provide comma separated list of gene ids or gene name
tax_id=''
    # Input-1, option 3: users can pick a taxonomy id from option 1a (source_files/selected_taxonomy_ids.txt), or directly provide it when the taxonomy id is known
FASTA_PATH=$ANALYSIS_PATH/input/mapped_query_annotation/fasta_path_mapped_query
    # Input-1, option 4: provide absolute path of for query fasta sequence
    # default fasta path $ANALYSIS_PATH/input/mapped_query_annotation/fasta_path_mapped_query
    
### Input-2:  Keywords, *REQUIRED* for domain selection and *OPTIONAL* for classification###
### This can be altered by the users in the demonstration file as well
domain_kw='RRM,KH,DEAD'
    # *REQUIRED* Input-2, comma separated list of keywords for domain selection
class_kw='ribosom,helicase,synthetase,polymerase,transferase,nuclease,RRM,RNP'
    ## *OPTIONAL* Input-2, comma separated list of keywords for protein classification based on the predicted domains

main(){
    set_up_analysis_folder			# set_up_analysis_folder
    basic_requirements_for_demo			# downloads all the files required for this demo, provide zenodo link
    provide_input_queries			# subcommand: query
    provide_domain_and_class_keywords		# subcommand: keywords
    select_domains_by_keywords			# subcommand: select
    run_domain_prediction			# subcommand: predict
    filter_domain_analysis			# subcommand: filter
    classify_filtered_result			# subcommand: classify
    calculate_annotation_score			# subcommand: annoscore
    create_analysis_summary			# subcommand: summary
    output_file_formats				# subcommand: format
}

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
    
    $PYTHON_PATH $APRICOT_PATH/bin/apricot create \
    $ANALYSIS_PATH
}

basic_requirements_for_demo(){
    zenodo_link_for_demo_data=https://zenodo.org/record/51705/files/APRICOT-1.0-demo_files-MS.zip
    wget $zenodo_link_for_demo_data
    unzip APRICOT-1.0-demo_files-MS
    cp APRICOT-1.0-demo_files-MS/go_mapping/* $DB_PATH/go_mapping
    cp -r APRICOT-1.0-demo_files-MS/interpro_annotation_data $DB_PATH/interpro
    cp APRICOT-1.0-demo_files-MS/cdd_analysis/* $ANALYSIS_PATH/output/0_predicted_domains/cdd_analysis
    cp APRICOT-1.0-demo_files-MS/ipr_analysis/* $ANALYSIS_PATH/output/0_predicted_domains/ipr_analysis
    ## CDD annotation table
    wget -c -P $DB_PATH/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
    gunzip $DB_PATH/cdd/cdd_annotation_data/*
    ## PfamA annotation table
    pfam_release=Pfam30.0
    wget -c -P $DB_PATH/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/$pfam_release/database_files/pfamA.txt.gz
    gunzip $DB_PATH'/pfam/pfamA.txt.gz'
}

provide_input_queries(){
    ## Option-1: UniProt identifiers
    $PYTHON_PATH $APRICOT_PATH/bin/apricot query \
    --analysis_path $ANALYSIS_PATH \
    --uids $query_uids
}

provide_domain_and_class_keywords(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot keywords \
    $domain_kw \
    -cl $class_kw
}

select_domains_by_keywords(){
    ## Selection of domains from both CDD and InterPro by default
    ## use from flags -C for CDD or -I for InterPro
    $PYTHON_PATH $APRICOT_PATH/bin/apricot select
}

run_domain_prediction(){
    ## prediction by both CDD and InterPro by default
    ## use from flags -C for CDD or -I for InterPro
    ## use --force or -F option to overwrite the existing analysis
    $PYTHON_PATH $APRICOT_PATH/bin/apricot predict \
    --analysis_path $ANALYSIS_PATH \
    --fasta $FASTA_PATH \
    --cdd_db $CDD_PATH \
    --ipr_db $INTERPRO_PATH
    #-F -C -I
}

filter_domain_analysis(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot filter \
    --analysis_path $ANALYSIS_PATH \
    --similarity 24 --coverage 39
}

classify_filtered_result(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot classify \
    --analysis_path $ANALYSIS_PATH
}

calculate_annotation_score(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot annoscore \
    --analysis_path $ANALYSIS_PATH
}

create_analysis_summary(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot summary \
    --analysis_path $ANALYSIS_PATH
}

output_file_formats(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot format \
    --analysis_path $ANALYSIS_PATH \
    -HT
}

main
