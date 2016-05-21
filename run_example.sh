#!/bin/bash
# AUTHOR: Malvika Sharan <malvikasharan@gmail.com>

#########################################################################
ANALYSIS_PATH=APRICOT_analysis
APRICOT_PATH=APRICOT
ROOT_DB_PATH=source_files
#########################################################################


#########################################################################
# Download parameters
ZENODO_LINK_FOR_DEMO_DATA=https://zenodo.org/record/51705/files/APRICOT-1.0-demo_files-MS.zip
PFAM_RELEASE=Pfam30.0
#########################################################################


#########################################################################
# FIXED PATHS for flatfiles downloaded by APRICOT
DB_PATH=$ROOT_DB_PATH/reference_db_files

# Path for domain databases
CDD_PATH=$DB_PATH/cdd/Cdd
INTERPRO_PATH=$DB_PATH/interpro/interproscan
#########################################################################


#########################################################################
# *OPTIONAL*. Provide species name to retrieve taxonomy IDS for given
# species
SPECIES=''
#########################################################################


#######################################################################
# Input-1, option 1: provide comma separated list of UniProt ids
#
# * P0A6X3 (positive test) is Hfq protein that contains sm and RRM/RNP
#   like domain
# * P00957 (negative test) is alaS protein is a tRNA-ligase, hence
#   will not be selected by RRM, KH or DEAD domains
QUERY_UIDS='P0A6X3,P00957'
#######################################################################


######################################################################
# Not used in this demonstration:
# Input-1, option 2: provide comma separated list of gene ids or gene
# name 
query_geneids=''

# Input-1, option 3: users can pick a taxonomy id from option 1a
# (source_files/selected_taxonomy_ids.txt), or directly provide it
# when the taxonomy id is known
tax_id=''

# Input-1, option 4: provide absolute path of for query fasta sequence
# default fasta path is $ANALYSIS_PATH/input/mapped_query_annotation/fasta_path_mapped_query
FASTA_PATH=''
######################################################################


######################################################################
# Input-2: Keywords
#
# *REQUIRED* for domain selection
# *OPTIONAL* for classification
# This can be altered by the users in the demonstration file as well
DOMAIN_KEYWORDS='RRM,KH,DEAD'
######################################################################


#######################################################################
# Input-2, comma separated list of keywords for domain selection
# *REQUIRED* 
CLASS_KEYWORDS='ribosom,helicase,synthetase,polymerase,transferase,nuclease,RRM,RNP'
#######################################################################


#######################################################################
# Input-2, comma separated list of keywords for protein
# *classification based on the predicted domains
# *OPTIONAL* 
#######################################################################

main(){
    set_up_analysis_folder			
    downloads_files		                
    provide_input_queries		  # subcommand query
    provide_domain_and_class_keywords	  # subcommand keywords
    select_domains_by_keywords	          # subcommand select
    run_domain_prediction		  # subcommand predict
    filter_domain_analysis		  # subcommand filter
    classify_filtered_result		  # subcommand classify
    calculate_annotation_score	          # subcommand annoscore
    create_analysis_summary		  # subcommand summary
    format_output			  # subcommand format
}

set_up_analysis_folder(){
    mkdir -p $ROOT_DB_PATH $APRICOT_PATH $ANALYSIS_PATH $APRICOT_LIBRARY
    for DB_SUBPATH in cdd go_mapping interpro pfam
    do
	mkdir -p $DB_PATH/$DB_SUBPATH
    done
    apricot create $ANALYSIS_PATH
}

downloads_files(){
    # Demo files stored at Zenodo
    
    DEMO_ZIP=$(basename $ZENODO_LINK_FOR_DEMO_DATA)
    DEMO_FOLDER=$(basename $DEMO_ZIP .zip)/apricot_demo_files/
    wget $ZENODO_LINK_FOR_DEMO_DATA
    unzip ${DEMO_ZIP}
    cp -r ${DEMO_FOLDER}/go_mapping/* $DB_PATH
    cp -r ${DEMO_FOLDER}/interpro_annotation_data $DB_PATH/interpro
    cp ${DEMO_FOLDER}/cdd_analysis/* $ANALYSIS_PATH/output/0_predicted_domains/cdd_analysis
    cp ${DEMO_FOLDER}/ipr_analysis/* $ANALYSIS_PATH/output/0_predicted_domains/ipr_analysis
    rm -rf $DEMO_ZIP $DEMO_FOLDER $(basename $DEMO_ZIP .zip)

    # CDD annotation table
    wget -c \
	 -P $DB_PATH/cdd/cdd_annotation_data \
	 ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
    gunzip $DB_PATH/cdd/cdd_annotation_data/*
    
    # PfamA annotation table
    wget -c \
	 -P $DB_PATH/pfam \
	 ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/$PFAM_RELEASE/database_files/pfamA.txt.gz
    gunzip $DB_PATH/pfam/pfamA.txt.gz
}

provide_input_queries(){
    # Option-1: UniProt identifiers
    apricot query \
	    --analysis_path $ANALYSIS_PATH \
	    --uids $QUERY_UIDS
}

provide_domain_and_class_keywords(){
    apricot keywords \
	    --db_root $ROOT_DB_PATH \
	    -cl $CLASS_KEYWORDS \
	    $DOMAIN_KEYWORDS 
}

select_domains_by_keywords(){
    apricot select --db_root $ROOT_DB_PATH
}

run_domain_prediction(){
    apricot predict \
	    --analysis_path $ANALYSIS_PATH
}

filter_domain_analysis(){
    apricot filter \
	    --analysis_path $ANALYSIS_PATH \
	    --similarity 24 \
	    --coverage 39
}

classify_filtered_result(){
    apricot classify \
	    --analysis_path $ANALYSIS_PATH
}

calculate_annotation_score(){
    apricot annoscore \
	    --analysis_path $ANALYSIS_PATH
}

create_analysis_summary(){
    apricot summary \
	    --analysis_path $ANALYSIS_PATH
}

format_output(){
    apricot format \
	    --analysis_path $ANALYSIS_PATH \
	    -HT
}

main
