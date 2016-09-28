#!/bin/bash
#AUTHOR: Malvika Sharan <malvika.sharan@uni-wuerzburg.de>

## Python scripts to support docker image

## full path of APRICOT libraries
apricot_lib=APRICOT/apricotlib

## path for apricot source files
apricot_files=source_files/reference_db_files

main(){
        get_cdd_and_interpro
        get_go_pdb_tax
        format_interpro_table
        ontology_mapping_to_domains
        sort_and_format_pdb_data
}

get_cdd_and_interpro(){
    wget -c -P /home/source_files/reference_db_files/cdd/Cdd ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/*.gz && \
    for folders in /home/source_files/reference_db_files/cdd/Cdd/*.gz; do tar xvf $folders -C /home/source_files/reference_db_files/cdd/Cdd; done && \
    wget -c -P /home/source_files/reference_db_files/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz && \
    gunzip /home/source_files/reference_db_files/cdd/cdd_annotation_data/* && \
    wget -c -P /home/source_files/reference_db_files/interpro ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.19-58.0/interproscan-5.19-58.0-64-bit.tar.gz && \
    tar xvf /home/source_files/reference_db_files/interpro/interproscan-5.19-58.0-64-bit.tar.gz -C /home/source_files/reference_db_files/interpro && \
    mv /home/source_files/reference_db_files/interpro/interproscan-*/* /home/source_files/reference_db_files/interpro/interproscan && \
    wget -O - ftp://ftp.ebi.ac.uk/pub/databases/interpro/ > /home/source_files/reference_db_files/interpro/ipr_flatfile.html && \
    wget -c -P /home/source_files/reference_db_files/interpro/interpro_annotation_data ftp://ftp.ebi.ac.uk/pub/databases/interpro/58.0/interpro2go && \
    wget -c -P /home/source_files/reference_db_files/interpro/interpro_annotation_data ftp://ftp.ebi.ac.uk/pub/databases/interpro/58.0/interpro.xml.gz && \
    gunzip /home/source_files/reference_db_files/interpro/interpro_annotation_data/interpro.xml.gz && \
    rm /home/source_files/reference_db_files/interpro/interproscan/bin/prosite/pfsearch_wrapper.py && \
    wget -c -P /home/source_files/reference_db_files/interpro/interproscan/bin/prosite/ \
    https://raw.githubusercontent.com/malvikasharan/interproscan/master/core/jms-implementation/support-mini-x86-32/bin/prosite/pfsearch_wrapper.py && \
    rm -rf /home/source_files/reference_db_files/interpro/interproscan-5.19-58.0-64-bit.tar.gz \
    /home/source_files/reference_db_files/cdd/Cdd/*.gz
}

# Get Gene Ontology, PDB files, pdb2uniprot files,Taxonomy files, pfam annotation data
get_go_pdb_tax(){
    wget -P /home/source_files/reference_db_files/go_mapping http://www.geneontology.org/ontology/go.obo && \
    wget -c -P /home/source_files/reference_db_files/pdb/pdb_secstr http://www.rcsb.org/pdb/files/ss.txt && \
    wget -P /home/source_files/reference_db_files/pdb/pdb2uniprot http://www.uniprot.org/docs/pdbtosp.txt && \
    wget -c -P /home/source_files/reference_db_files/all_taxids http://www.uniprot.org/docs/speclist.txt && \
    wget -c -P /home/source_files/reference_db_files/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam30.0/database_files/pfamA.txt.gz && \
    gunzip /home/source_files/reference_db_files/pfam/pfamA.txt.gz
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

# run command `cd /home && sh APRICOT/shell_scripts/docker_support.sh`
