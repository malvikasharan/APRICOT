#!/bin/bash
#AUTHOR: Malvika Sharan <malvika.sharan@uni-wuerzburg.de>

## Python scripts to support docker image

## full path of APRICOT libraries
apricot_lib=APRICOT/apricotlib

## path for apricot source files
apricot_files=source_files/reference_db_files

main(){
        format_interpro_table
        ontology_mapping_to_domains
        sort_and_format_pdb_data
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
