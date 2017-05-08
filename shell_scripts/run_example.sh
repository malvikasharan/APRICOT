#!/bin/bash
# AUTHOR: Malvika Sharan <malvika.sharan@uni-wuerzburg.de>

#########################################################################
APRICOT_CALL='python3.5 APRICOT/bin/apricot'
			# 'apricot' 	# It will work for the globally installed software.
			# If locally installed change the path, 
			# for e.g. /home/username/local/bin/
			# Or, use 'python APRICOT/bin/apricot' 
ANALYSIS_PATH=APRICOT_analysis
APRICOT_PATH=APRICOT
APRICOT_LIB_PATH=APRICOT/apricotlib
ROOT_DB_PATH=source_files
NEEDLE_EMBOSS_PATH=needle
PFAM_RELEASE=Pfam30.0
#########################################################################


#########################################################################
# Download mimic datasets for demonstation 
# Option-1
DEMO_FILES=APRICOT/tests/demo_files_small
# Option-2
ZENODO_LINK_FOR_DEMO_DATA=https://zenodo.org/record/51705/files/APRICOT-1.0-demo_files-MS.zip
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
QUERY_UIDS='P0A6X3,P00957' #examples
#######################################################################


######################################################################
# Not used in this demonstration:
# Input-1, option 2: provide comma separated list of gene ids or gene
# name 
query_geneids=''

# Input-1, option 3: users can pick a taxonomy id from option 1a
# (source_files/selected_taxonomy_ids.txt), or directly provide it
# when the taxonomy id is known
tax_id='83333' # E.coli K-12

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
##
DOMAIN_KEYWORDS='RRM,RNP'

# All the keywords as originally used in the manuscript:
#DOMAIN_KEYWORDS='RRM,RGG,DEAD,zf-CCCH,KH,GTP_EFTU,GTP_EFTU_D2,GTP_EFTU_D3,dsrm,zf-CCHC,LSM,OB_NTP_bind,HA2,G-patch,IBN_N,SAP,TUDOR,RnaseA,zf-C2H2_jaz,MMR_HSR1,KOW,RNase_T,MIF4G,zf-RanBP,NTF2,PAZ,RBM1CTR,PAM2,Xpo1,S1,HGTP_anticodon,tRNA-synt_2b,Piwi,CSD,Ribosomal_L7Ae,RNase_Zc3h12a,Anticodon_1,R3H,La,PUF,PUA,ZnFC2HC,SWAP,RAP,pumilio,Ribosomal,MMR_HSR1,Brix,WD40,Nop,YTH,zf-CCHC,LSM,PurA,RNase_PH,RNase_PH_C,S4,GTP_EFTU_D2,GTP_EFTU,Nol1_Nop2_Fmu,R3H,RNase_T,MIF4G,Btz,Helicase_RecD,RNase_P_p30,SURF6,UPF1_Zn_bind,SAP,eRF1_3,Fibrillarin,Gar1,HABP4_PAI-RBP1,S10_plectin,TruD,XRN_N,THUMP,RNB,RrnaAD,Tap-RNA_bind,tRNA-synt_1b,APOBEC_N,Surp,PAP_assoc,PAZ,Piwi,zf-C2H2,zf-C3HC4,Alba,FtsJ,Pept_tRNA_hydro,PseudoU_synth_1,PseudoU_synth_2,RNA_bind,RNase_P_pop3,RTC,RTC_insert,SAM,SpoU_sub_bind,SpoU_sub_bind,SRP14,SRP72,TRM,tRNA_anti,tRNA_m1G_MT,tRNA_U5-meth_tr,tRNA-synt_2,TROVE,TrpBP,TruB_N,zf-RNPHF,Helicase_C'
######################################################################


#######################################################################
# Input-2, comma separated list of keywords for domain selection
# *REQUIRED* 
CLASS_KEYWORDS=$DOMAIN_KEYWORDS   #'ribosom,helicase,nuclease,RRM,RNP'
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
    
	#calculate_annotation_score	  # subcommand annoscore
}

set_up_analysis_folder(){
    mkdir -p $ROOT_DB_PATH $APRICOT_PATH $ANALYSIS_PATH $APRICOT_LIBRARY
    for DB_SUBPATH1 in cdd go_mapping interpro pfam
    do
	mkdir -p $DB_PATH/$DB_SUBPATH1
    done
    for DB_SUBPATH2 in cdd/cdd_annotation_data interpro/interpro_annotation_data
    do
	mkdir -p $DB_PATH/$DB_SUBPATH2
    done
    
    $APRICOT_CALL create $ANALYSIS_PATH
}

get_small_demo_files(){
    # CDD data
    if ! [ -f $DB_PATH/cdd/cdd_annotation_data/cddid.tbl ]
    then
    	cp $DEMO_FILES/cdd/cdd_annotation_data/cddid.tbl \
    	$DB_PATH/cdd/cdd_annotation_data
    fi
    
    # InterPro data
    if ! [ -f $DB_PATH/interpro/interpro_annotation_data/interproid.tbl ]
    then
        cp $DEMO_FILES/interpro/interpro_annotation_data/interproid.tbl \
         $DB_PATH/interpro/interpro_annotation_data/
    fi
    if ! [ -f $DB_PATH/interpro/interpro_annotation_data/mapped_interpro_to_cdd_length.csv ]
    then
        cp $DEMO_FILES/interpro/interpro_annotation_data/mapped_interpro_to_cdd_length.csv \
         $DB_PATH/interpro/interpro_annotation_data/
    fi
    
    # GO data
    if ! [ -f $DB_PATH/go_mapping/mapped_cdd_to_go.csv ]
    then
        cp -r $DEMO_FILES/go_mapping $DB_PATH
    fi
    
    # Pfam data
    if ! [ -f $DB_PATH/pfam/pfamA.txt ]
    then
        cp -r $DEMO_FILES/pfam $DB_PATH
    fi
    
    # Domain prediction, demo files
    cp -r $DEMO_FILES/cdd_analysis $ANALYSIS_PATH/output/0_predicted_domains/
    cp -r $DEMO_FILES/ipr_analysis $ANALYSIS_PATH/output/0_predicted_domains/
}

downloads_files(){
    # Demo files stored at Zenodo
    
    DEMO_ZIP=$(basename $ZENODO_LINK_FOR_DEMO_DATA)
    DEMO_FOLDER=$(basename $DEMO_ZIP .zip)/apricot_demo_files/
    wget $ZENODO_LINK_FOR_DEMO_DATA
    unzip ${DEMO_ZIP}
    
    # InterPro data
    if ! [ -f $DB_PATH/interpro/interpro_annotation_data/interproid.tbl ]
    then
        cp -r ${DEMO_FOLDER}/interpro/interpro_annotation_data/interproid.tbl $DB_PATH/interpro/interpro_annotation_data
    fi
    if ! [ -f $DB_PATH/interpro/interpro_annotation_data/mapped_interpro_to_cdd_length.csv ]
    then
        cp -r ${DEMO_FOLDER}/interpro/interpro_annotation_data/mapped_interpro_to_cdd_length.csv $DB_PATH/interpro/interpro_annotation_data
    fi
    
    # CDD annotation table
     if ! [ -f  $DB_PATH/cdd/cdd_annotation_data/cddid.tbl ]
    then
	wget -c \
	    -P $DB_PATH/cdd/cdd_annotation_data \
	    ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
	gunzip $DB_PATH/cdd/cdd_annotation_data/*
    fi
    
    # GO data
    if ! [ -f $DB_PATH/go_mapping/mapped_cdd_to_go.csv ]
    then
    	cp -r ${DEMO_FOLDER}/go_mapping/mapped_cdd_to_go.csv $DB_PATH/go_mapping
    fi
    
    # PfamA annotation table
    if ! [ -f $DB_PATH/pfam/pfamA.txt ]
    then
        wget -c \
            -P $DB_PATH/pfam \
            ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/$PFAM_RELEASE/database_files/pfamA.txt.gz
        gunzip $DB_PATH/pfam/pfamA.txt.gz
    fi
    
    # Domain prediction, demo files
    cp -r ${DEMO_FOLDER}/cdd_analysis $ANALYSIS_PATH/output/0_predicted_domains
    cp -r ${DEMO_FOLDER}/ipr_analysis $ANALYSIS_PATH/output/0_predicted_domains
    rm -rf $DEMO_ZIP $DEMO_FOLDER $(basename $DEMO_ZIP .zip)
}

provide_input_queries(){
    ## Option-1: UniProt identifiers
    $APRICOT_CALL query \
	    --analysis_path $ANALYSIS_PATH \
	    --uids $QUERY_UIDS
	
	## Option-2: entire proteome
	##replace --uid option by the following:
	# -tx $tax_id -P
}

provide_domain_and_class_keywords(){
    $APRICOT_CALL keywords \
	    --db_root $ROOT_DB_PATH \
	    -cl $DOMAIN_KEYWORDS \
	    --kw_domain $DOMAIN_KEYWORDS
}

select_domains_by_keywords(){
    $APRICOT_CALL select --db_root $ROOT_DB_PATH
}

run_domain_prediction(){
    $APRICOT_CALL predict \
	    -ap $ANALYSIS_PATH
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
