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
species='coli' #retrieve $tax_id in bin/selected_taxonomy_ids.txt
tax_id='83333'
query_uids='P26599'
query_geneids=''
#domain_kw='RRM,KH,DEAD,cold-shock,La-domain,PIWI,zf-CCCH,Pumilio,PUF,S1-domain,DSRM,PUA-domain,ribosomal,#RNA-bind#'
domain_kw='zf-CCCH,S1-domain,RRM,RNA-bind#,Ribosomal_S9,Ribosomal_S8e,Ribosomal_S8,Ribosomal_S7e,Ribosomal_S7,Ribosomal_S6e,Ribosomal_S6,Ribosomal_S5_C,Ribosomal_S5,Ribosomal_S4Pg,Ribosomal_S4e,Ribosomal_S4,Ribosomal_S3Ae,Ribosomal_S30AE,Ribosomal_S30,Ribosomal_S3_N,Ribosomal_S3_C,Ribosomal_S28e,Ribosomal_S27e,Ribosomal_S27,Ribosomal_S26e,Ribosomal_S25,Ribosomal_S24e,Ribosomal_S23p,Ribosomal_S22,Ribosomal_S21e,Ribosomal_S21,Ribosomal_S20p,Ribosomal_S2,Ribosomal_S19e,Ribosomal_S19,Ribosomal_S18,Ribosomal_S17e,Ribosomal_S17,Ribosomal_S16,Ribosomal_S15,Ribosomal_S14,Ribosomal_S13_N,Ribosomal_S13,Ribosomal_S11,Ribosomal_S10,Ribosomal_L9_N,Ribosomal_L9_C,Ribosomal_L7Ae,Ribosomal_L6e_N,Ribosomal_L6e,Ribosomal_L6,Ribosomal_L50,Ribosomal_L5_C,Ribosomal_L5,Ribosomal_L44,Ribosomal_L41,Ribosomal_L40e,Ribosomal_L4,Ribosomal_L39,Ribosomal_L38e,Ribosomal_L37e,Ribosomal_L37ae,Ribosomal_L37,Ribosomal_L36e,Ribosomal_L36,Ribosomal_L35p,Ribosomal_L35Ae,Ribosomal_L34e,Ribosomal_L34,Ribosomal_L33,Ribosomal_L32p,Ribosomal_L32e,Ribosomal_L31e,Ribosomal_L31,Ribosomal_L30_N,Ribosomal_L30,Ribosomal_L3,Ribosomal_L29e,Ribosomal_L29,Ribosomal_L28e,Ribosomal_L28,Ribosomal_L27e,Ribosomal_L27,Ribosomal_L25p,Ribosomal_L23eN,Ribosomal_L22e,Ribosomal_L22,Ribosomal_L21p,Ribosomal_L21e,Ribosomal_L20,Ribosomal_L2_C,Ribosomal_L2,Ribosomal_L19e,Ribosomal_L19,Ribosomal_L18p,Ribosomal_L18e,Ribosomal_L18ae,Ribosomal_L17,Ribosomal_L16,Ribosomal_L15e,Ribosomal_L14e,Ribosomal_L14,Ribosomal_L13e,Ribosomal_L13,Ribosomal_L12,Ribosomal_L11_N,Ribosomal_L11,Ribosomal_L10,Ribosomal_L1,Ribosomal_60s,Ribosom_S12_S23,Pumilio,PUF-domain,PUA-domain,PIWI,La-domain,KOW,KH,DSRM,DEAD,cold-shock,Ribosomal_L24e,Ribosomal_L23'
class_kw='ribosom,helicase,synthetase,polymerase,transferase,nuclease,RRM,RNP'

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
    run_domain_prediction
    filter_domain_analysis
    classify_filtered_result
    calculate_annotation_score                 ####-Derive pvalues--TODO--
    create_analysis_summary
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
    $PYTHON_PATH $APRICOT_PATH/bin/apricot query \
    --analysis_path $ANALYSIS_PATH \
    --uids $query_uids
    
    ##Option-2
    #$PYTHON_PATH $APRICOT_PATH/bin/apricot query \
    #--analysis_path $ANALYSIS_PATH \
    #--tx $tax_id \
    #--uids $query_uids \
    #--geneids $query_geneids
    
    ##Option-3
    #$PYTHON_PATH $APRICOT_PATH/bin/apricot query \
    #--analysis_path $ANALYSIS_PATH \
    #-tx $tax_id -P
    
    ##Option-4
    #$PYTHON_PATH $APRICOT_PATH/bin/apricot query \
    #--analysis_path $ANALYSIS_PATH \
    #-fa $fasta_file
}

provide_domain_and_class_keywords(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot keywords \
    $domain_kw \
    -cl $class_kw
}

select_domains_by_keywords(){
    ##Selection of domains from both CDD and InterPro by default
    ##use from flags -C for CDD or -I for InterPro
    $PYTHON_PATH $APRICOT_PATH/bin/apricot select -I
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
    --similarity 25 --coverage 40
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

calculate_additional_annotation(){
    #$PYTHON_PATH $APRICOT_PATH/bin/apricot addanno -PDB \
    #--analysis_path $ANALYSIS_PATH \
    #--fasta $FASTA_PATH -F
    #
    #$PYTHON_PATH $APRICOT_PATH/bin/apricot addanno -PSORTB \
    #--psortb_path $PSORT_ROOT/psort \
    #--analysis_path $ANALYSIS_PATH \
    #--fasta $FASTA_PATH -F
    #
    #$PYTHON_PATH $APRICOT_PATH/bin/apricot addanno -REFSS \
    #--analysis_path $ANALYSIS_PATH \
    #--fasta $FASTA_PATH -F
    
    $PYTHON_PATH $APRICOT_PATH/bin/apricot addanno -RAPTORX \
    --raptorx_path $raptorx_path \
    --analysis_path $ANALYSIS_PATH \
    --fasta $FASTA_PATH -F
}

create_visualization_files(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot vis \
    --analysis_path $ANALYSIS_PATH \
    -S #-M -A -C -D -L 
}

output_file_formats(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot format \
    --analysis_path $ANALYSIS_PATH \
    -XL -HT 
}

main
