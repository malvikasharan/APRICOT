#!/bin/bash
#AUTHOR: Malvika Sharan {malvikasharan@gmail.com}

PYTHON_PATH=python3
ANALYSIS_PATH=APRICOT_analysis
APRICOT_PATH=APRICOT
DB_PATH=bin/reference_db_files

##FIXED PATHS for flatfiles downloaded by APRICOT
DB_PATH=source_files/reference_db_files

##PATHS for domain databases, can be changed by the users
CDD_PATH=$DB_PATH/cdd/Cdd
INTERPRO_PATH=$DB_PATH/interpro/interproscan

for paths in bin $APRICOT_PATH $ANALYSIS_PATH $DB_PATH $APRICOT_LIBRARY
do
    if ! [ -d $paths ] 
    then
        mkdir $paths
    fi
done
if ! [ -e $APRICOT_PATH/apricotlib ] 
then
    git clone https://github.com/malvikasharan/APRICOT.git $APRICOT_PATH
    ln -s $APRICOT_PATH/apricotlib $APRICOT_PATH/bin
fi

####Required inputs####
###Input-1: query proteins###

##if the query is limited to a single species
##provide species name or taxonomy id
species='coli'
    #optional input: provide species name to retrieve taxonomy ids for given species in bin/selected_taxonomy_ids.txt
query_uids='P0A6X3,P00957'
    #Input-1, option 1: provide comma separated list of UniProt ids
query_geneids=''
    #Input-1, option 2: provide comma separated list of gene ids or gene name
tax_id='83333'
    #Input-1, option 3: users can pick a taxonomy id from option 1a (source_files/selected_taxonomy_ids.txt), or directly provide it when the taxonomy id is known
FASTA_PATH=$ANALYSIS_PATH/input/mapped_query_annotation/fasta_path_mapped_query
    #Input-1, option 4: provide absolute path of for query fasta sequence
    #default fasta path $ANALYSIS_PATH/input/mapped_query_annotation/fasta_path_mapped_query
    
###Input-2: Keywords for domain selection###

##comma separated list of keywords for domain selection
domain_kw='RRM,KH,DEAD'

##Optional input of comma separated list of keywords for protein classification based on the predicted domains
class_kw='ribosom,helicase,synthetase,polymerase,transferase,nuclease,RRM,RNP'

main(){
    #install_complete_db_and_tools              ###-Includes external tools for additional annotation
    #install_minimum_required_files             ###-Use this to install the minimum required files
    
    #set_up_analysis_folder
    #retrieve_taxonomy_id_list                   ###-This step could be skipped if using uniprot ids as queries
                                                ###-select a taxonomy id from the list genetrated by using $species
                                                ###-for full list look at $FIXED_DB_FILES/all_taxids/speclist.txt
    #provide_input_queries
    #provide_domain_and_class_keywords
    select_domains_by_keywords
    #run_domain_prediction
    #ilter_domain_analysis
    #classify_filtered_result
    #calculate_annotation_score                 
    #create_analysis_summary
    
    ###ADDITIONAL ANNOTATION###
    #calculate_additional_annotation            ####-PsortB and -RaptorX must be installed for their respective annotation
    #create_visualization_files                 ####--Create visualization files
    #output_file_formats                        ####--Format output files as HTML or xlsx
}

install_complete_db_and_tools(){
    sh apricotlib/apricot_complete_db_tool.sh $APRICOT_PATH $DB_PATH 
}

install_minimum_required_files(){
    sh $APRICOT_PATH/apricotlib/apricot_minimum_required_files.sh $APRICOT_PATH
}

set_up_analysis_folder(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot create \
    $ANALYSIS_PATH
}

retrieve_taxonomy_id_list(){
    $PYTHON_PATH $APRICOT_PATH/bin/apricot taxid \
    $DB_PATH \
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
    -HT #-XL  
}

main
