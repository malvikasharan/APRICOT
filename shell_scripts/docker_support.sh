#!/bin/sh

#AUTHOR: Malvika Sharan <malvika.sharan@uni-wuerzburg.de>
## Python scripts to support docker image

## NOTE: provide full path where the database required to run APRICOT will be installed
ROOT=/home  ## When installing inside the docker contaniner, please use the path `/home`

apricot_lib=$ROOT/source_files/scripts
interproversion=59.0
interproscanversion=5.20-$interproversion

## path for apricot source files
apricot_files=$ROOT/source_files/reference_db_files

main(){
        create_datapath
        get_python_scripts
        get_cdd_and_interpro
        get_go_pdb_tax
        get_blast
        format_interpro_table
        ontology_mapping_to_domains
        sort_and_format_pdb_data
}

create_datapath(){
    for paths in \
    $apricot_lib \
    $ROOT/source_files/reference_db_files \
    $ROOT/source_files/reference_db_files/cdd \
    $ROOT/source_files/reference_db_files/cdd/Cdd \
    $ROOT/source_files/reference_db_files/cdd/cdd_annotation_data \
    $ROOT/source_files/reference_db_files/interpro \
    $ROOT/source_files/reference_db_files/interpro/interproscan \
    $ROOT/source_files/reference_db_files/interpro/interpro_annotation_data \
    $ROOT/source_files/reference_db_files/go_mapping \
    $ROOT/source_files/reference_db_files/pdb \
    $ROOT/source_files/reference_db_files/pdb/pdb_sequence \
    $ROOT/source_files/reference_db_files/pdb/pdb_secstr \
    $ROOT/source_files/reference_db_files/pdb/pdb2uniprot \
    $ROOT/source_files/reference_db_files/all_taxids \
    $ROOT/source_files/reference_db_files/pfam \
    $ROOT/source_files/reference_db_files/blast
    do
        mkdir -p $paths
    done
}

get_python_scripts(){
    for files in interpro_xml_to_table.py sort_sec_struc_pdb_data.py map_domain_to_go.py
    do
        if ! [ -f $apricot_lib/$files ]
        then
           wget -N -c -P $apricot_lib 'https://raw.githubusercontent.com/malvikasharan/APRICOT/master/apricotlib'/$files
        fi
    done
}

get_cdd_and_interpro(){
    wget -c -P $ROOT/source_files/reference_db_files/cdd/Cdd ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/*.gz
    for folders in $ROOT/source_files/reference_db_files/cdd/Cdd/*.gz; do tar xvf $folders -C $ROOT/source_files/reference_db_files/cdd/Cdd; done
    wget -c -P $ROOT/source_files/reference_db_files/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
    gunzip $ROOT/source_files/reference_db_files/cdd/cdd_annotation_data/*
    wget -c -P $ROOT/source_files/reference_db_files/interpro ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/$interproscanversion/interproscan-$interproscanversion-64-bit.tar.gz
    tar xvf $ROOT/source_files/reference_db_files/interpro/interproscan-$interproscanversion-64-bit.tar.gz -C $ROOT/source_files/reference_db_files/interpro
    mv $ROOT/source_files/reference_db_files/interpro/interproscan-*/* $ROOT/source_files/reference_db_files/interpro/interproscan
    wget -O - ftp://ftp.ebi.ac.uk/pub/databases/interpro/ > $ROOT/source_files/reference_db_files/interpro/ipr_flatfile.html
    wget -c -P $ROOT/source_files/reference_db_files/interpro/interpro_annotation_data ftp://ftp.ebi.ac.uk/pub/databases/interpro/$interproversion/interpro2go
    wget -c -P $ROOT/source_files/reference_db_files/interpro/interpro_annotation_data ftp://ftp.ebi.ac.uk/pub/databases/interpro/$interproversion/interpro.xml.gz
    gunzip $ROOT/source_files/reference_db_files/interpro/interpro_annotation_data/interpro.xml.gz
    rm $ROOT/source_files/reference_db_files/interpro/interproscan/bin/prosite/pfsearch_wrapper.py
    wget -c -P $ROOT/source_files/reference_db_files/interpro/interproscan/bin/prosite/ \
    https://raw.githubusercontent.com/malvikasharan/interproscan/master/core/jms-implementation/support-mini-x86-32/bin/prosite/pfsearch_wrapper.py
    rm -rf $ROOT/source_files/reference_db_files/interpro/interproscan-$interproscanversion-64-bit.tar.gz \
    $PATH/source_files/reference_db_files/cdd/Cdd/*.gz
}

# Get Gene Ontology, PDB files, pdb2uniprot files,Taxonomy files, pfam annotation data
get_go_pdb_tax(){
    wget -P $ROOT/source_files/reference_db_files/go_mapping http://www.geneontology.org/ontology/go.obo
    wget -c -P $ROOT/source_files/reference_db_files/pdb/pdb_secstr http://www.rcsb.org/pdb/files/ss.txt
    wget -P $ROOT/source_files/reference_db_files/pdb/pdb2uniprot http://www.uniprot.org/docs/pdbtosp.txt
    wget -c -P $ROOT/source_files/reference_db_files/all_taxids http://www.uniprot.org/docs/speclist.txt
    wget -c -P $ROOT/source_files/reference_db_files/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam30.0/database_files/pfamA.txt.gz
    gunzip $ROOT/source_files/reference_db_files/pfam/pfamA.txt.gz
}

get_blast(){
    wget -c -P $ROOT/source_files/reference_db_files/blast ftp://ftp.ncbi.nih.gov/blast/executables/LATEST/ncbi-blast-*+-x64-linux.tar.gz && \
    tar -xvzf $ROOT/source_files/reference_db_files/blast/ncbi-blast-*+-x64-linux.tar.gz -C $ROOT/source_files/reference_db_files/blast && \
    mv $ROOT/source_files/reference_db_files/blast/ncbi-blast-*+/* $ROOT/source_files/reference_db_files/blast && \
    install $ROOT/source_files/reference_db_files/blast/bin/makeblastdb $ROOT/source_files/reference_db_files/blast && \
    rm -rf $ROOT/source_files/reference_db_files/blast/ncbi-blast-*+-x64-linux.tar.gz \
    $ROOT/source_files/reference_db_files/blast/ncbi-blast-*+ \
    $ROOT/source_files/reference_db_files/blast/bin/*
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
