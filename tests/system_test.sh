#!/bin/bash
# AUTHOR: Malvika Sharan <malvikasharan@gmail.com>

## Assumes that users have Java installed, it is required to run InterproScan

#########################################################################
ANALYSIS_PATH=APRICOT_analysis
APRICOT_PATH=APRICOT
ROOT_DB_PATH=source_files
SHELL_SCRIPTS=../shell_scripts
NEEDLE_EMBOSS_PATH=source_files/reference_db_files/needle/emboss/needle
#########################################################################

#########################################################################
# Either use the dev version in the git repo with the default Python version
# or install via pip (pip3 install bio-apricot)
APRICOT_CALL="apricot"

# ... or set a Python version for that call ...
# PYTHON_PATH=python3
# APRICOT_CALL="$APRICOT_PATH/bin/apricot"    #"python3 ../bin/apricot"

# ... or use the installed version of apricot
# APRICOT_CALL="apricot"

#########################################################################


#########################################################################
# FIXED PATHS for flatfiles downloaded by APRICOT
DB_PATH=$ROOT_DB_PATH/reference_db_files

# Path for domain databases
CDD_PATH=$DB_PATH/cdd/Cdd
INTERPRO_PATH=$DB_PATH/interpro/interproscan
#########################################################################


#########################################################################
# External tool's path for additional annotation: PLEASE ADAPT THIS
# PATH
raptorx_tool_path=$DB_PATH/raptorx
# run_raptorx-ss3.pl 
# ss8 script is for 8 state and ss3 script is for 3 state structure prediction
raptorx_perl_script=raptorx-ss3-ss8/bin/run_raptorx-ss8.pl
raptorx_path=$raptorx_tool_path/$raptorx_perl_script

export LD_LIBRARY_PATH=/usr/local/lib64
export PSORT_ROOT=/opt/biotools/psortb/psort/bin
export PSORT_PFTOOLS=/opt/biotools/pftools
#########################################################################


#########################################################################
# *OPTIONAL*. Provide species name to retrieve taxonomy IDS for given
# species
species='coli'
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
# Not used in the demonstration file

# Input-1, option 2: provide comma separated list of gene ids or gene
# name
query_geneids=''

# Input-1, option 3: users can pick a taxonomy id from option 1a
# (source_files/selected_taxonomy_ids.txt), or directly provide it
# when the taxonomy id is known
tax_id=''

# Input-1, option 4: provide absolute path of for query fasta sequence
# default fasta path
# $ANALYSIS_PATH/input/mapped_query_annotation/fasta_path_mapped_query
FASTA_PATH=$ANALYSIS_PATH/input/mapped_query_annotation/fasta_path_mapped_query
    
# Input-2: Keywords, *REQUIRED* for domain selection and *OPTIONAL*
# for classification This can be altered by the users in the
# demonstration file as well
domain_kw='RRM,KH,DEAD'

# *REQUIRED* Input-2, comma separated list of keywords for domain
# *selection
class_kw='ribosom,helicase,synthetase,polymerase,transferase,nuclease,RRM,RNP'
######################################################################
    
main(){
    
    set_up_analysis_folder			            ### Set up analysis folders for APRICOT analysis

    ### Install databases and third-party tools required by APRICOT
    ### Docker image can be pulled: docker pull malvikasharan/apricot
    
    ### Optionally install all the third-party tools using following functions:
    ## Instructions to install psortb: http://www.psort.org/downloads/INSTALL.html
    
    ## install_minimum_required_files           ## doesn't install Psortb and Raptorx
    ## install_raptorx                          ## installs RaptorX and required nr database
                                                
    
    ### Test APRICOT without installing databases and the third-party tools
    ## this test is only for query uids: P0A6X3,P00957
    ## additional annotation is not allowed with this option
    work_with_test_files			            ### Copies small demo files from GitHub
    
    ### This step could be skipped if using uniprot ids as queries
    # retrieve_taxonomy_id_list                 ## select a taxonomy id from the list genetrated by using $species
                                                ## for full list look at $FIXED_DB_FILES/all_taxids/speclist.txt
    provide_input_queries			            ### Subcommand: query
    provide_domain_and_class_keywords		    ### Subcommand: keywords
    select_domains_by_keywords			        ### Subcommand: select
    run_domain_prediction			            ### Subcommand: predict
    filter_domain_analysis			            ### Subcommand: filter
    classify_filtered_result			        ### Subcommand: classify
    create_analysis_summary			            ### Subcommand: summary
    output_file_formats                         ### Subcommand: format (output file conversion fro csv to HTML or xlsx)
    
    # calculate_annotation_score			    ### Subcommand: annoscore (requires EMBOSS suit to run needle cline, and python numpy, scipy)
    ###ADDITIONAL ANNOTATION###                 ### requires third party tools, which can be installed by 'install_complete_db_and_tools'###
    #calculate_additional_annotation            ## Subcommand: addanno (PsortB and -RaptorX must be installed for their respective annotation)
    #create_visualization_files                 ## Subcommand: vis
}

set_up_analysis_folder(){
    ## paths for source files/databases
    mkdir -p $DB_PATH # $APRICOT_PATH $APRICOT_LIBRARY
    
    ## Paths for APRICOT analysis
    $APRICOT_CALL create $ANALYSIS_PATH
}

install_complete_db_and_tools(){
    sh $shell_path/apricot_complete_db_tool.sh
    # sh $APRICOT_PATH/shell_scripts/apricot_complete_db_tool.sh $APRICOT_PATH
}

install_minimum_required_files(){
    sh $SHELL_SCRIPTS/apricot_minimum_required_files.sh
}

install_raptorx(){
    sh $SHELL_SCRIPTS/install_raptorx.sh
}

work_with_test_files (){
    cp -r demo_files_small/cdd $DB_PATH
    cp -r demo_files_small/interpro $DB_PATH
    cp -r demo_files_small/go_mapping $DB_PATH
    cp -r demo_files_small/pfam $DB_PATH
    cp -r demo_files_small/cdd_analysis $ANALYSIS_PATH/output/0_predicted_domains/
    cp -r demo_files_small/ipr_analysis $ANALYSIS_PATH/output/0_predicted_domains/
}


retrieve_taxonomy_id_list(){
    $APRICOT_CALL taxid \
    $DB_PATH \
    --species $species
}

provide_input_queries(){
    ## Option-1
    $APRICOT_CALL query \
    --analysis_path $ANALYSIS_PATH \
    --uids $QUERY_UIDS
    
    ## Option-2
    #$APRICOT_CALL query \
    #--analysis_path $ANALYSIS_PATH \
    #--tx $tax_id \
    #--uids $query_uids \
    #--geneids $query_geneids
    
    ## Option-3
    #$APRICOT_CALL query \
    #--analysis_path $ANALYSIS_PATH \
    #-tx $tax_id -P
    
    ## Option-4
    #$APRICOT_CALL query \
    #--analysis_path $ANALYSIS_PATH \
    #-fa $fasta_file
}

provide_domain_and_class_keywords(){
    $APRICOT_CALL keywords $domain_kw  \
    --class $class_kw \
    --db_root $ROOT_DB_PATH
}

select_domains_by_keywords(){
    ## Selection of domains from both CDD and InterPro by default
    ## use from flags -C for CDD or -I for InterPro
    $APRICOT_CALL select --db_root $ROOT_DB_PATH
}

run_domain_prediction(){
    ## prediction by both CDD and InterPro by default
    ## use from flags -C for CDD or -I for InterPro
    ## use --force or -F option to overwrite the existing analysis
    $APRICOT_CALL predict \
    --analysis_path $ANALYSIS_PATH \
    --fasta $FASTA_PATH \
    --cdd_db $CDD_PATH \
    --ipr_db $INTERPRO_PATH
    #-F -C -I
}

filter_domain_analysis(){
    $APRICOT_CALL filter \
    --analysis_path $ANALYSIS_PATH \
    --similarity 24 --coverage 39
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

calculate_additional_annotation(){
    #$APRICOT_CALL addanno -PDB \
    #--analysis_path $ANALYSIS_PATH \
    #--fasta $FASTA_PATH -F
    #
    #$APRICOT_CALL addanno -PSORTB \
    #--psortb_path $PSORT_ROOT/psort \
    #--analysis_path $ANALYSIS_PATH \
    #--fasta $FASTA_PATH -F
    #
    #$APRICOT_CALL addanno -REFSS \
    #--analysis_path $ANALYSIS_PATH \
    #--fasta $FASTA_PATH -F
    
    $APRICOT_CALL addanno -RAPTORX \
    --raptorx_path $raptorx_path \
    --analysis_path $ANALYSIS_PATH \
    --fasta $FASTA_PATH -F
}

create_visualization_files(){
    $APRICOT_CALL vis \
    --analysis_path $ANALYSIS_PATH \
    -S #-M -A -C -D -L 
}

output_file_formats(){
    $APRICOT_CALL format \
    --analysis_path $ANALYSIS_PATH \
    -HT #-XL  
}

main
