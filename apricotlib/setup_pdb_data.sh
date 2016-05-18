#!/bin/bash
#AUTHOR: Malvika Sharan {malvikasharan@gmail.com}

##Addition shell script to install only PDB related source files

PYTHON_PATH=python

apricot_path=$1
##full path where you have cloned/save APRICOT from git
apricot_lib=$apricot_path/apricotlib

##path where you want to store the data
apricot_db=$2

main(){
        create_main_path
        
        ###PDB-MODULES####
        create_pdb_inpath
        download_uniprot_map
        download_pdb_sec_str
        sort_and_format_pdb_data
}

create_main_path(){
    if ! [ -d $apricot_db ]
        then
            mkdir -p $apricot_db
    fi
    if ! [ -d $apricot_db/pdb ]
    then
        mkdir -p $apricot_db/pdb
    fi
}

create_pdb_inpath(){
    for FOLDER in pdb_sequence pdb_secstr pdb2uniprot
    do
        if ! [ -d $apricot_db/pdb/$FOLDER ]
        then
            mkdir -p $apricot_db/pdb/$FOLDER
        fi
    done
}

download_uniprot_map(){
    wget -P $apricot_db/pdb/pdb2uniprot http://www.uniprot.org/docs/pdbtosp.txt
}

download_pdb_sec_str(){
    wget -c -P $apricot_db/pdb/pdb_secstr http://www.rcsb.org/pdb/files/ss.txt
}

sort_and_format_pdb_data(){
    $PYTHON_PATH $apricot_lib/sort_sec_struc_pdb_data.py \
    -i $apricot_db/pdb/pdb_secstr/ss.txt -seq $apricot_db/pdb/pdb_sequence -str $apricot_db/pdb/pdb_secstr
    $apricot_db/blast/makeblastdb -in $apricot_db/pdb/pdb_sequence/pdb_sequence.txt -dbtype prot
}

main
