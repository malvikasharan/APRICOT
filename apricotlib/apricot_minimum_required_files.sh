#!/bin/bash
#AUTHOR: Malvika Sharan {malvikasharan@gmail.com}

PYTHON_PATH=python3

apricot_path=$1

##full path where you have cloned/save APRICOT from git
apricot_lib=$apricot_path/apricotlib

##path where you want to store the flatfiles
apricot_files=bin/reference_db_files

main(){
        #create_main_path
        
        ###CDD-MODULES###
        #create_cdd_inpath
        #check_and_download_cdd
        
        ####InterProScan-MODULES###
        #create_interpro_inpath
        #check_and_download_interpro
        #uniprot_species_to_taxid
        
        #######PDB-MODULES####
        #create_pdb_inpath
        #download_uniprot_map
        #download_pdb_sec_str
        #sort_and_format_pdb_data
        
        ####Other-requirements###
        #get_blast_executables
        ontology_mapping_to_domains
} 

create_main_path(){
    if ! [ -d $apricot_files ]
        then
            mkdir -p $apricot_files
    fi
    for FOLDER in cdd interpro blast go_mapping biojs pdb all_taxids clustal
    do
        if ! [ -d $apricot_files/$FOLDER ]
        then
            mkdir -p $apricot_files/$FOLDER
        fi
    done
}

create_cdd_inpath(){
    for FOLDER in version_info cdd_annotation_data
    do
        if ! [ -d $apricot_files/cdd/$FOLDER ]
        then
            mkdir -p $apricot_files/cdd/$FOLDER
        fi
    done
}

check_and_download_cdd(){
    rm -rf $apricot_files/cdd/cdd_flat_files/*
    wget -c -P $apricot_files/cdd ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.info
    if diff $apricot_files/cdd/cdd.info $apricot_files/cdd/cdd_current.info >/dev/null ; then
        echo '\n**'updated vesion of cdd is present in path $apricot_files/cdd.'**\n'
    else
        wget -c -P $apricot_files/cdd/Cdd ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/*
        
        for binary_files in $(ls $apricot_files/cdd/Cdd)
        do
            tar xvf $apricot_files/cdd/Cdd/$binary_files -C $apricot_files/cdd/Cdd
        done
        rm $apricot_files/cdd/Cdd/*.gz
        cat $apricot_files/cdd/cdd.info > $apricot_files/cdd/cdd_current.info
    fi
    rm $apricot_files/cdd/cdd_annotation_data/*
    wget -c -P $apricot_files/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
    gunzip $apricot_files/cdd/cdd_annotation_data/*
}

create_interpro_inpath(){
    for FOLDER in version_info ipr_annotation_data interproscan
    do
        if ! [ -d $apricot_files/interpro/$FOLDER ]
        then
            mkdir -p $apricot_files/interpro/$FOLDER
        fi
    done
}

check_and_download_interpro(){
    ftp_server=ftp://ftp.ebi.ac.uk/pub/databases/interpro
    wget -O - ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/ > $apricot_files/interpro/ipr_info.html
    #$PYTHON_PATH $apricot_lib/current_interpro_version.py $apricot_files/interpro/InterProScanData/ipr_info.html $apricot_files/interpro/InterProScanData/current_version
    if diff $apricot_files/interpro/ipr_info.html $apricot_files/interpro/ipr_current.html >/dev/null ; then
        echo '\n**'updated vesion of InterPro is present in path $apricot_files/interpro $(cat $apricot_files/current_version)'**\n'
    else
        wget -c -P $apricot_files/interpro $(cat $apricot_files/interpro/current_version)/*-64-bit.tar*
        for files in $(ls $apricot_files/interpro/InterProScanData/*.tar.gz)
        do
            tar xvf $files -C $apricot_files/interpro
        done
        mv $apricot_files/interpro/interproscan-*/* $apricot_files/interpro/interproscan
        cat $apricot_files/interpro/ipr_info.html > $apricot_files/interpro/ipr_current.html
    fi
  
    rm -rf $apricot_files/interpro/interpro_flat_files/*
    wget -O - $ftp_server/ > $apricot_files/interpro/version_info/ipr_flatfile.html
    $PYTHON_PATH $apricot_lib/current_interpro_version.py $apricot_files/interpro/version_info/ipr_flatfile.html $apricot_files/interpro/ipr_flatfile
    ipr_flatfile_server=$(cat $apricot_files/interpro/ipr_flatfile)
    echo $ipr_flatfile
    wget -c -P $apricot_files/interpro/ipr_annotation_data $ipr_flatfile_server/interpro2go
    wget -c -P $apricot_files/interpro/ipr_annotation_data $ipr_flatfile_server/interpro.xml.gz
    gunzip $apricot_files/interpro/ipr_annotation_data/interpro.xml.gz
    $PYTHON_PATH $apricot_lib/interpro_xml_to_table.py $apricot_files/interpro/ipr_annotation_data $apricot_files/interpro/ipr_annotation_data/interpro.xml
}

uniprot_species_to_taxid(){
    wget -c -P $apricot_files/all_taxids http://www.uniprot.org/docs/speclist.txt
}

create_pdb_inpath(){
    for FOLDER in pdb_sequence pdb_secstr pdb2uniprot
    do
        if ! [ -d $apricot_files/pdb/$FOLDER ]
        then
            mkdir -p $apricot_files/pdb/$FOLDER
        fi
    done
}

download_uniprot_map(){
    wget -P $apricot_files/pdb/pdb2uniprot http://www.uniprot.org/docs/pdbtosp.txt
}

download_pdb_sec_str(){
    wget -c -P $apricot_files/pdb/pdb_secstr http://www.rcsb.org/pdb/files/ss.txt
}

sort_and_format_pdb_data(){
    $PYTHON_PATH $apricot_lib/sort_sec_struc_pdb_data.py \
    -i $apricot_files/pdb/pdb_secstr/ss.txt -seq $apricot_files/pdb/pdb_sequence -str $apricot_files/pdb/pdb_secstr
    $apricot_files/blast/makeblastdb -in $apricot_files/pdb/pdb_sequence/pdb_sequence.txt -dbtype prot
}

get_blast_executables(){
    wget -c -P $apricot_files/blast ftp://ftp.ncbi.nih.gov/blast/executables/blast+/2.2.28/*x64-linux*
    tar -xvzf $apricot_files/blast/*x64-linux* -C $apricot_files/blast
    rm -rf $apricot_files/blast/*x64-linux*.gz
    for exepath in $(ls $apricot_files/blast)
    do
        if [ ! -p $apricot_files/blast/makeblastdb ]
        then
            if [ 'ncbi' = $(echo $exepath | cut -d \- -f 1) ]
            then
                cp -r $apricot_files/blast/$exepath/* $apricot_files/blast
            fi
        fi
        install $apricot_files/blast/bin/psiblast $apricot_files/blast
        install $apricot_files/blast/bin/blastp $apricot_files/blast
        install $apricot_files/blast/bin/makeblastdb $apricot_files/blast
    done
}

ontology_mapping_to_domains(){
    GO_PATH=$apricot_files/go_mapping
    rm $GO_PATH/go.obo*
    wget -P $GO_PATH http://www.geneontology.org/ontology/go.obo
    interpro_to_go=$apricot_files/interpro/ipr_annotation_data/interpro2go
    interpro_data=$apricot_files/interpro/ipr_annotation_data/interproid.tbl
    cdd_data=$apricot_files/cdd/cdd_annotation_data/cddid.tbl
    $PYTHON_PATH $apricot_lib/map_domain_to_go.py $GO_PATH $interpro_to_go $interpro_data $cdd_data
}

main