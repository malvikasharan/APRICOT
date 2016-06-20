#!/bin/bash
# AUTHOR: Malvika Sharan <malvika.sharan@uni-wuerzburg.de>

#########################################################################
APRICOT_CALL='apricot' 	# It will work for the globally installed software.
			# If locally installed change the path, 
			# for e.g. /home/username/local/bin/
			# Or, use 'python APRICOT/bin/apricot' 
ANALYSIS_PATH=APRICOT_analysis
APRICOT_PATH=APRICOT
APRICOT_LIB_PATH=APRICOT/apricotlib
ROOT_DB_PATH=source_files
NEEDLE_EMBOSS_PATH=source_files/reference_db_files/needle/emboss/needle
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
    get_small_demo_files		  # or download original domain annotation data using "downloads_files"
    provide_input_queries		  # subcommand query
    provide_domain_and_class_keywords	  # subcommand keywords
    select_domains_by_keywords	          # subcommand select
    run_domain_prediction		  # subcommand predict
    filter_domain_analysis		  # subcommand filter
    classify_filtered_result		  # subcommand classify
    create_analysis_summary		  # subcommand summary
    format_output			  # subcommand format
    
    ## The subcommand 'annoscore' requires locally configured needle from EMBOSS suite
    ## It is installed using the Dockerfile or provided shell scripts for installation
    ## or, if already installed, please change the path name $NEEDLE_EMBOSS_PATH
    calculate_annotation_score	  # subcommand annoscore
}

set_up_analysis_folder(){
    mkdir -p $ROOT_DB_PATH $APRICOT_PATH $ANALYSIS_PATH $APRICOT_LIBRARY
    for DB_SUBPATH1 in cdd go_mapping interpro pfam
    do
	mkdir -p $DB_PATH/$DB_SUBPATH1
    done
    for DB_SUBPATH2 in cdd/cdd_annotation_data interpro/interpro_annotation_data source_files/domain_data
    do
	mkdir -p $DB_PATH/$DB_SUBPATH2
    done
    
    $APRICOT_CALL create $ANALYSIS_PATH
}

get_small_demo_files(){
    if ! [ -f $DB_PATH/cdd/cdd_annotation_data/cddid.tbl ]
    then
    	cp APRICOT/tests/demo_files_small/cdd $DB_PATH
    fi
    if ! [ -f $DB_PATH/interpro/interpro_annotation_data/interproid.tbl ]
    then
        cp -r APRICOT/tests/demo_files_small/interpro $DB_PATH
    fi
    if ! [ -f $DB_PATH/go_mapping/mapped_cdd_to_go.csv ]
    then
        cp -r APRICOT/tests/demo_files_small/go_mapping $DB_PATH
    fi
    if ! [ -f $DB_PATH/pfam/pfamA.txt ]
    then
        cp -r APRICOT/tests/demo_files_small/pfam $DB_PATH
    fi
    cp -r APRICOT/tests/demo_files_small/cdd_analysis $ANALYSIS_PATH/output/0_predicted_domains/
    cp -r APRICOT/tests/demo_files_small/ipr_analysis $ANALYSIS_PATH/output/0_predicted_domains/
}

downloads_files(){
    # Demo files stored at Zenodo
    
    DEMO_ZIP=$(basename $ZENODO_LINK_FOR_DEMO_DATA)
    DEMO_FOLDER=$(basename $DEMO_ZIP .zip)/apricot_demo_files/
    wget $ZENODO_LINK_FOR_DEMO_DATA
    unzip ${DEMO_ZIP}
    if [ -f APRICOT/tests/demo_files_small/go_mapping/mapped_cdd_to_go.csv ]
    then
    	cp -r ${DEMO_FOLDER}/go_mapping $DB_PATH
    fi
    if [ -f APRICOT/tests/demo_files_small/interpro/interpro_annotation_data/interproid.tbl ]
    then
        cp -r ${DEMO_FOLDER}/interpro_annotation_data $DB_PATH/interpro
    fi
    # CDD annotation table
     if [ -f APRICOT/tests/demo_files_small/cdd/cdd_annotation_data/cddid.tbl ]
    then
	wget -c \
	    -P $DB_PATH/cdd/cdd_annotation_data \
	    ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
	gunzip $DB_PATH/cdd/cdd_annotation_data/*
    fi
    
    # PfamA annotation table
    if [ -f APRICOT/tests/demo_files_small/pfam/pfamA.txt ]
    then
        wget -c \
            -P $DB_PATH/pfam \
            ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/$PFAM_RELEASE/database_files/pfamA.txt.gz
        gunzip $DB_PATH/pfam/pfamA.txt.gz
    fi
    cp -r ${DEMO_FOLDER}/cdd_analysis $ANALYSIS_PATH/output/0_predicted_domains
    cp -r ${DEMO_FOLDER}/ipr_analysis $ANALYSIS_PATH/output/0_predicted_domains
    rm -rf $DEMO_ZIP $DEMO_FOLDER $(basename $DEMO_ZIP .zip)
}

provide_input_queries(){
    # Option-1: UniProt identifiers
    $APRICOT_CALL query \
	    --analysis_path $ANALYSIS_PATH \
	    --uids $QUERY_UIDS
}

provide_domain_and_class_keywords(){
    $APRICOT_CALL keywords \
	    --db_root $ROOT_DB_PATH \
	    -cl $CLASS_KEYWORDS \
	    $DOMAIN_KEYWORDS 
}

select_domains_by_keywords(){
    $APRICOT_CALL select --db_root $ROOT_DB_PATH
}

run_domain_prediction(){
    $APRICOT_CALL predict \
	    --analysis_path $ANALYSIS_PATH
}

filter_domain_analysis(){
    $APRICOT_CALL filter \
	    --analysis_path $ANALYSIS_PATH \
	    --similarity 24 \
	    --coverage 39
}

classify_filtered_result(){
    $APRICOT_CALL classify \
	    --analysis_path $ANALYSIS_PATH
}

calculate_annotation_score(){
    $APRICOT_CALL annoscore \
	    --analysis_path $ANALYSIS_PATH \
	    --needle_dir $NEEDLE_EMBOSS_PATH
}

create_analysis_summary(){
    $APRICOT_CALL summary \
	    --analysis_path $ANALYSIS_PATH
}

format_output(){
    $APRICOT_CALL format \
	    --analysis_path $ANALYSIS_PATH \
	    -HT
}
main
