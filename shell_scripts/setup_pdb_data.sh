#!/bin/bash
# AUTHOR: Malvika Sharan <malvika.sharan@uni-wuerzburg.de>

# Installs PDB related source files

PYTHON_PATH=python

APRICOT_PATH=$1

# Full path where you have cloned/save APRICOT
apricot_lib=../$APRICOT_PATH/apricotlib

# Path where you want to store the data
APRICOT_DB_PATH=$2

main(){
        create_folder
        ### PDB-MODULES ####
        download_uniprot_map
        download_pdb_sec_str
        sort_and_format_pdb_data
}

create_folders(){
    mkdir -p \
	  $APRICOT_DB_PATH \
	  $APRICOT_DB_PATH/pdb \
	  $APRICOT_DB_PATH/pdb/pdb_sequence \
	  $APRICOT_DB_PATH/pdb/pdb_secstr \
	  $APRICOT_DB_PATH/pdb/pdb2uniprot
}

download_uniprot_map(){
    wget -P $APRICOT_DB_PATH/pdb/pdb2uniprot \
	 http://www.uniprot.org/docs/pdbtosp.txt
}

download_pdb_sec_str(){
    wget -c -P $APRICOT_DB_PATH/pdb/pdb_secstr \
	 http://www.rcsb.org/pdb/files/ss.txt
}

sort_and_format_pdb_data(){
    $PYTHON_PATH $apricot_lib/sort_sec_struc_pdb_data.py \
	 -i $APRICOT_DB_PATH/pdb/pdb_secstr/ss.txt\
	 -seq $APRICOT_DB_PATH/pdb/pdb_sequence \
	 -str $APRICOT_DB_PATH/pdb/pdb_secstr
    $APRICOT_DB_PATH/blast/makeblastdb \
	-in $APRICOT_DB_PATH/pdb/pdb_sequence/pdb_sequence.txt \
	-dbtype prot
}

main
