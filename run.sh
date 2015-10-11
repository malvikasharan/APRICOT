#!/bin/bash
#AUTHOR: Malvika Sharan {malvikasharan@gmail.com}
#Date: 2015-08-07

####can be changed by the users####
PYTHON_PATH=python3
ANALYSIS_PATH=APRICOT_analysis #test
APRICOT_PATH=APRICOT
DB_PATH=/maui/malvika/rbp_prediction/seq_analysis/RnaBindEff_pipeline/APRICOT_manuscript/apricot_check/apricot_db_and_tools


####Tool path for additional annotation####
raptorx_tool_path=$DB_PATH/raptorx
raptorx_perl_script=raptorx-ss3-ss8/bin/run_raptorx-ss8.pl #run_raptorx-ss3.pl ##8-state secondary structure analysis takes longer
raptorx_path=$raptorx_tool_path/$raptorx_perl_script

export LD_LIBRARY_PATH=/usr/local/lib64
export PSORT_ROOT=/opt/biotools/psortb/psort/bin
export PSORT_PFTOOLS=/opt/biotools/pftools

###Python3 modules must be installed##
#urllib.request, scipy, numpy, matplotlib

####Input by users###
species='Salmonella' #retrieve $tax_id in bin/selected_taxonomy_ids.txt
tax_id='216597'
query_uids=D0ZIB5,O34105
query_geneids='ssph1,ssph2'
domain_kw='secretion,flagellar,eurkary'
class_kw=''

##absolute path of Fasta files
FASTA_PATH=$ANALYSIS_PATH/input/mapped_query_annotation/fasta_path_mapped_query #default fasta path

##FIXED PATHS
CDD_PATH=$DB_PATH/conserved_domain_database/Cdd
INTERPRO_PATH=$DB_PATH/interpro/InterProScanData/interproscan-5.14-53.0
DOMAIN_PRED_PATH=output/interm_analysis_data ##excluding the $ANALYSIS_PATH

####Installed by APRICOT####
FIXED_DB_FILES=bin/reference_db_files
if ! [ -e $APRICOT_PATH/bin/apricotlib ] 
then
    ln -s $APRICOT_PATH/apricotlib $APRICOT_PATH/bin
fi

main(){
    #install_apricot_db_and_tool                ####-All the DB and tools set-up for APRICOT (optionally only install flatfiles by retrieve_db_flatfiles)
    #retrieve_db_flatfiles                      ####-This step can be skipped by copying the $FIXED_DB_FILES from previous analysis to current $FIXED_DB_FILES

    #set_up_analysis_folder
    #retrieve_taxonomy_id_list                  ####-This step could be skipped if using uniprot ids as queries
                                                ####-select a taxonomy id from the list genetrated by using $species
                                                ####-for full list look at $FIXED_DB_FILES/all_taxids/speclist.txt
    #provide_input_queries
    #provide_domain_and_class_keywords
    #select_domains_by_keywords
    #run_domain_prediction
    #filter_domain_analysis
    #classify_filtered_result
    calculate_annotation_score                 ####-Derive pvalues--TODO--
    #calculate_additional_annotation            ####-PsortB and -RaptorX must be installed for their respective annotation
    #create_visualization_files                 ####--TODO--
    #output_file_formats
}

apricot_install_tools_and_db(){
    sh $APRICOT_PATH/apricotlib/apricot_db_tool.sh $APRICOT_PATH $DB_PATH ##-TODO-Docker--
}

retrieve_db_flatfiles(){
    if ! [ -d $DB_FILES/cdd ]
    then
        sh $APRICOT_PATH/apricotlib/setup_flatfiles.sh $APRICOT_PATH
        #sh $APRICOT_PATH/apricotlib/setup_pdb_flatfiles.sh $APRICOT_PATH ##only pdb data for annotation
    fi
}

set_up_analysis_folder(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot create \
    $ANALYSIS_PATH
}

retrieve_taxonomy_id_list(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot taxid \
    $FIXED_DB_FILES \
    --species $species
}

provide_input_queries(){
    ##Option-1
    #$PYTHON_PATH $APRICOT_PATH/bin/apricot query \
    #--analysis_path $ANALYSIS_PATH \
    #--uids $query_uids
    
    ##Option-2
    $PYTHON_PATH $APRICOT_PATH/bin/apricot query \
    --analysis_path $ANALYSIS_PATH \
    --tx $tax_id \
    --uids $query_uids \
    --geneids $query_geneids
    
    ##Option-3
    #$PYTHON_PATH $APRICOT_PATH/bin/apricot query \
    #--analysis_path $ANALYSIS_PATH \
    #--tx $tax_id -P
}

provide_domain_and_class_keywords(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot keywords \
    $domain_kw
    #--classify $class_kw
}

select_domains_by_keywords(){
    ##Selection of domains from both CDD and InterPro by default
    ##use from flags -C for CDD or -I for InterPro
    $PYTHON_PATH $APRICOT_PATH/bin/apricot select
}

run_domain_prediction(){
    ##prediction by both CDD and InterPro by default
    ##use from flags -C for CDD or -I for InterPro
    ##use --force or -F option to overwrite the existing analysis
    $PYTHON_PATH $APRICOT_PATH/bin/apricot predict \
    --analysis_path $ANALYSIS_PATH \
    --fasta $FASTA_PATH \
    --cdd_db $CDD_PATH \
    --ipr_db $INTERPRO_PATH
}

filter_domain_analysis(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot filter \
    --analysis_path $ANALYSIS_PATH \
    --similarity 20 --coverage 30 --evalue 1
}

classify_filtered_result(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot classify \
    --analysis_path $ANALYSIS_PATH
}

calculate_annotation_score(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot annoscore \
    --analysis_path $ANALYSIS_PATH
}

calculate_additional_annotation(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot addanno -PDB \
    --analysis_path $ANALYSIS_PATH \
    --fasta $FASTA_PATH
    
    $PYTHON_PATH $APRICOT_PATH/bin/apricot addanno -PSORTB \
    --psortb_path $PSORT_ROOT/psort \
    --analysis_path $ANALYSIS_PATH \
    --fasta $FASTA_PATH
    
    $PYTHON_PATH $APRICOT_PATH/bin/apricot addanno -REFSS \
    --analysis_path $ANALYSIS_PATH \
    --fasta $FASTA_PATH
    
    $PYTHON_PATH $APRICOT_PATH/bin/apricot addanno -RAPTORX \
    --raptorx_path $raptorx_path \
    --analysis_path $ANALYSIS_PATH \
    --fasta $FASTA_PATH
}

create_visualization_files(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot vis \
    --analysis_path $ANALYSIS_PATH \
    -D -S -L -M #-D -L -S -M -A -C 
}

output_file_formats(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot format \
    --analysis_path $ANALYSIS_PATH \
    -HT -XL 
}

main
