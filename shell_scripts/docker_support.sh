#!/bin/bash
#AUTHOR: Malvika Sharan <malvika.sharan@uni-wuerzburg.de>

## Python scripts to support docker image

## full path of APRICOT libraries
PATH=/home
apricot_lib=$PATH/source_files/scripts

## path for apricot source files
apricot_files=$PATH/source_files/reference_db_files

main(){
        create_datapath
        get_python_scripts
        get_cdd_and_interpro
        get_go_pdb_tax
        format_interpro_table
        ontology_mapping_to_domains
        sort_and_format_pdb_data
}

create_datapath(){
    for paths in $apricot_lib \
    $PATH/source_files \
    $PATH/source_files/reference_db_files \
    $PATH/source_files/reference_db_files/cdd \
    $PATH/source_files/reference_db_files/cdd/Cdd \
    $PATH/source_files/reference_db_files/cdd/cdd_annotation_data \
    $PATH/source_files/reference_db_files/interpro \
    $PATH/source_files/reference_db_files/interpro/interproscan \
    $PATH/source_files/reference_db_files/interpro/interpro_annotation_data \
    $PATH/source_files/reference_db_files/go_mapping \
    $PATH/source_files/reference_db_files/pdb \
    $PATH/source_files/reference_db_files/pdb/pdb_sequence \
    $PATH/source_files/reference_db_files/pdb/pdb_secstr \
    $PATH/source_files/reference_db_files/pdb/pdb2uniprot \
    $PATH/source_files/reference_db_files/all_taxids \
    $PATH/source_files/reference_db_files/pfam \
    $PATH/source_files/reference_db_files/needle \
    $PATH/source_files/reference_db_files/temp_needle \
    $PATH/source_files/reference_db_files/blast
    do
        if [ ! -d $paths ]
        then
            mkdir -p $paths
        fi
    done
}

get_python_scripts(){
    for files in interpro_xml_to_table.py sort_sec_struc_pdb_data.py map_domain_to_go.py
    do
        if ! [ -f $apricot_lib/$files ]
        then
            wget -N -c -P $apricotlib https://raw.githubusercontent.com/malvikasharan/APRICOT/master/apricotlib/$files
        fi
    done
}

get_cdd_and_interpro(){
    wget -c -P $PATH/source_files/reference_db_files/cdd/Cdd ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/*.gz
    for folders in $PATH/source_files/reference_db_files/cdd/Cdd/*.gz; do tar xvf $folders -C $PATH/source_files/reference_db_files/cdd/Cdd; done
    wget -c -P $PATH/source_files/reference_db_files/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
    gunzip $PATH/source_files/reference_db_files/cdd/cdd_annotation_data/*
    wget -c -P $PATH/source_files/reference_db_files/interpro ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.20-59.0/interproscan-5.20-59.0-64-bit.tar.gz
    tar xvf $PATH/source_files/reference_db_files/interpro/interproscan-5.20-59.0-64-bit.tar.gz -C $PATH/source_files/reference_db_files/interpro
    mv $PATH/source_files/reference_db_files/interpro/interproscan-*/* $PATH/source_files/reference_db_files/interpro/interproscan
    wget -O - ftp://ftp.ebi.ac.uk/pub/databases/interpro/ > $PATH/source_files/reference_db_files/interpro/ipr_flatfile.html
    wget -c -P $PATH/source_files/reference_db_files/interpro/interpro_annotation_data ftp://ftp.ebi.ac.uk/pub/databases/interpro/59.0/interpro2go
    wget -c -P $PATH/source_files/reference_db_files/interpro/interpro_annotation_data ftp://ftp.ebi.ac.uk/pub/databases/interpro/59.0/interpro.xml.gz
    gunzip $PATH/source_files/reference_db_files/interpro/interpro_annotation_data/interpro.xml.gz
    rm $PATH/source_files/reference_db_files/interpro/interproscan/bin/prosite/pfsearch_wrapper.py
    wget -c -P $PATH/source_files/reference_db_files/interpro/interproscan/bin/prosite/ \
    https://raw.githubusercontent.com/malvikasharan/interproscan/master/core/jms-implementation/support-mini-x86-32/bin/prosite/pfsearch_wrapper.py
    rm -rf $PATH/source_files/reference_db_files/interpro/interproscan-5.20-59.0-64-bit.tar.gz \
    $PATH/source_files/reference_db_files/cdd/Cdd/*.gz
}

# Get Gene Ontology, PDB files, pdb2uniprot files,Taxonomy files, pfam annotation data
get_go_pdb_tax(){
    wget -P $PATH/source_files/reference_db_files/go_mapping http://www.geneontology.org/ontology/go.obo
    wget -c -P $PATH/source_files/reference_db_files/pdb/pdb_secstr http://www.rcsb.org/pdb/files/ss.txt
    wget -P $PATH/source_files/reference_db_files/pdb/pdb2uniprot http://www.uniprot.org/docs/pdbtosp.txt
    wget -c -P $PATH/source_files/reference_db_files/all_taxids http://www.uniprot.org/docs/speclist.txt
    wget -c -P $PATH/source_files/reference_db_files/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam30.0/database_files/pfamA.txt.gz
    gunzip $PATH/source_files/reference_db_files/pfam/pfamA.txt.gz
}

format_interpro_table(){
    python $apricot_lib/interpro_xml_to_table.py \
    $apricot_files/interpro/interpro_annotation_data \
    $apricot_files/interpro/interpro_annotation_data/interpro.xml
}

sort_and_format_pdb_data(){
    python $apricot_lib/sort_sec_struc_pdb_data.py \
    -i $apricot_files/pdb/pdb_secstr/ss.txt -seq $apricot_files/pdb/pdb_sequence -str $apricot_files/pdb/pdb_secstr
    $apricot_files/blast/makeblastdb -in $apricot_files/pdb/pdb_sequence/pdb_sequence.txt -dbtype prot
}

ontology_mapping_to_domains(){
    GO_PATH=$apricot_files/go_mapping
    interpro_to_go=$apricot_files/interpro/interpro_annotation_data/interpro2go
    interpro_data=$apricot_files/interpro/interpro_annotation_data/interproid.tbl
    cdd_data=$apricot_files/cdd/cdd_annotation_data/cddid.tbl
    python $apricot_lib/map_domain_to_go.py $GO_PATH $interpro_to_go $interpro_data $cdd_data
}

main
