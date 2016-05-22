#!/bin/bash
# AUTHOR: Malvika Sharan <malvikasharan@gmail.com>

## Addition shell script to install only PDB related source files

PYTHON_PATH=python

APRICOT_PATH=$1
## full path where you have cloned/save APRICOT from git
apricot_lib=$APRICOT_PATH/apricotlib

## path where you want to store the data
APRICOT_DB_PATH=$2

main(){
        create_main_path
        
        ### PDB-MODULES ####
        create_pdb_inpath
        download_uniprot_map
        download_pdb_sec_str
        sort_and_format_pdb_data
}

create_main_path(){
    if ! [ -d $APRICOT_DB_PATH ]
        then
            mkdir -p $APRICOT_DB_PATH
    fi
    if ! [ -d $APRICOT_DB_PATH/pdb ]
    then
        mkdir -p $APRICOT_DB_PATH/pdb
    fi
}

create_pdb_inpath(){
    for FOLDER in pdb_sequence pdb_secstr pdb2uniprot
    do
        if ! [ -d $APRICOT_DB_PATH/pdb/$FOLDER ]
        then
            mkdir -p $APRICOT_DB_PATH/pdb/$FOLDER
        fi
    done
}

download_uniprot_map(){
    wget -P $APRICOT_DB_PATH/pdb/pdb2uniprot http://www.uniprot.org/docs/pdbtosp.txt
}

download_pdb_sec_str(){
    wget -c -P $APRICOT_DB_PATH/pdb/pdb_secstr http://www.rcsb.org/pdb/files/ss.txt
}

sort_and_format_pdb_data(){
    $PYTHON_PATH $apricot_lib/sort_sec_struc_pdb_data.py \
    -i $APRICOT_DB_PATH/pdb/pdb_secstr/ss.txt -seq $APRICOT_DB_PATH/pdb/pdb_sequence -str $APRICOT_DB_PATH/pdb/pdb_secstr
    $APRICOT_DB_PATH/blast/makeblastdb -in $APRICOT_DB_PATH/pdb/pdb_sequence/pdb_sequence.txt -dbtype prot
}

main
