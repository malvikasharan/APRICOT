#!/bin/bash
# AUTHOR: Malvika Sharan <malvika.sharan@uni-wuerzburg.de>

## Assumes that the psiblast and makeblastdb are installed
psiblast_path=psiblast
makeblastdb_path=makeblastdb

## Path for datasets and tools required for APRICOT
apricot_files=source_files/reference_db_files

## Please change the path if nr database is  already installed and skip the function install_nr_for_raptorx
nr_path=$apricot_files/nr

main(){
    create_directories
    install_nr_for_raptorx
    install_raptorx
}

create_directories(){
    if ! [ -d $apricot_files/raptorx ]
    then
        mkdir -p $apricot_files/raptorx
    fi
}

install_raptorx(){
    install_nr_for_raptorx
    git clone https://github.com/Indicator/RaptorX-SS8.git $apricot_files/raptorx/raptorx-ss3-ss8

    echo "Optionally download from raptorX package from its server in the folder $apricot_db/raptorx"
    #wget -c -P $apricot_db/raptorx http://ttic.uchicago.edu/~zywang/RaptorX-SS8/raptorx-ss8-0.1.tgz
    #tar -xvzf $apricot_db/raptorx/raptorx-ss8-0.1.tgz -C $apricot_db/raptorx
    
    ####needs nr database####
    perl $apricot_files/raptorx/raptorx-ss3-ss8/setup.pl \
    -home $apricot_files/raptorx/raptorx-ss3-ss8 \
    -blast $psiblast_path \
    -nr $apricot_files/nr/nr
}

install_nr_for_raptorx(){
    if ! [ -d $apricot_files/nr ]
    then
        mkdir -p $apricot_files/nr
    fi
    if ! [ -f $nr_path/nr ]
    then
        wget -c -P $nr_path ftp://ftp.ncbi.nih.gov/blast/db/FASTA/nr.gz
        gunzip $nr_path/nr.gz
        if ! [ -f $nr_path/nr.15.psq ]
        then
            $makeblastdb_path -in $nr_path/nr -dbtype prot
        fi
    fi
}

main
