#!/bin/bash
#AUTHOR: Malvika Sharan {malvikasharan@gmail.com}
#Date: 2015-08-07

PYTHON_PATH=python

apricot_path=$1
##full path where you have cloned/save APRICOT from git
apricot_lib=$apricot_path/apricotlib

##path where you want to store the data
apricot_flatfiles=bin/reference_db_files/

main(){
        create_main_path
        
        ###CDD-MODULES###
        create_cdd_inpath
        check_and_download_cdd
        
        ###InterProScan-MODULES###
        create_interpro_inpath
        check_and_download_interpro
        uniprot_species_to_taxid
        
        ######PDB-MODULES####
        create_pdb_inpath
        download_uniprot_map
        download_pdb_sec_str
        sort_and_format_pdb_data
        
        ###Other-requirements###
        get_pfam_domain_file
        get_blast_executables
        ontology_mapping_to_domains
        get_biojs_dependencies
        get_clustalw
} 

create_main_path(){
    if ! [ -d $apricot_flatfiles ]
        then
            mkdir -p $apricot_flatfiles
    fi
    for FOLDER in cdd interpro blast go_mapping biojs pdb pfam all_taxids clustal
    do
        if ! [ -d $apricot_flatfiles/$FOLDER ]
        then
            mkdir -p $apricot_flatfiles/$FOLDER
        fi
    done
}

create_cdd_inpath(){
    for FOLDER in version_info cdd_annotation_data
    do
        if ! [ -d $apricot_flatfiles/cdd/$FOLDER ]
        then
            mkdir -p $apricot_flatfiles/cdd/$FOLDER
        fi
    done
}

check_and_download_cdd(){
    rm -rf $apricot_flatfiles/cdd/cdd_flat_files/*
    wget -c -P $apricot_flatfiles/cdd/ ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.info
    if diff $apricot_flatfiles/cdd/cdd.info $apricot_flatfiles/cdd/version_info/cdd.info >/dev/null ; then
        echo '\n**'updated vesion of cdd is present in path $apricot_flatfiles/cdd.'**\n'
    fi
    cp $apricot_flatfiles/cdd/cdd.info $apricot_flatfiles/cdd/version_info/cdd.info
    rm $apricot_flatfiles/cdd/cdd_annotation_data/*
    wget -c -P $apricot_flatfiles/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
    gunzip $apricot_flatfiles/cdd/cdd_annotation_data/*
}

create_interpro_inpath(){
    for FOLDER in version_info ipr_annotation_data
    do
        if ! [ -d $apricot_flatfiles/interpro/$FOLDER ]
        then
            mkdir -p $apricot_flatfiles/interpro/$FOLDER
        fi
    done
}

check_and_download_interpro(){
    ftp_server=ftp://ftp.ebi.ac.uk/pub/databases/interpro
    wget -O - ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/ > $apricot_flatfiles/interpro/ipr_info.html
    if diff $apricot_flatfiles/interpro/ipr_info.html $apricot_flatfiles/interpro/version_info/ipr_info.html >/dev/null ; then
  	echo '\n**'updated vesion of InterPro is present in path $apricot_flatfiles/interpro.'**\n'
    fi
    cp $apricot_flatfiles/interpro/ipr_info.html $apricot_flatfiles/interpro/version_info/ipr_info.html
    rm -rf $apricot_flatfiles/interpro/interpro_flat_files/*
    wget -O - $ftp_server/ > $apricot_flatfiles/interpro/version_info/ipr_flatfile.html
    $PYTHON_PATH $apricot_lib/current_interpro_version.py $apricot_flatfiles/interpro/version_info/ipr_flatfile.html $apricot_flatfiles/interpro/ipr_flatfile
    ipr_flatfile=$(cat $apricot_flatfiles/interpro/ipr_flatfile)
    wget -c -P $apricot_flatfiles/interpro/ipr_annotation_data $ftp_server/$ipr_flatfile/interpro2go
    wget -c -P $apricot_flatfiles/interpro/ipr_annotation_data $ftp_server/interpro.xml.gz
    gunzip $apricot_flatfiles/interpro/ipr_annotation_data/interpro.xml.gz
    $PYTHON_PATH $apricot_lib/interpro_xml_to_table.py $apricot_flatfiles/interpro/ipr_annotation_data $apricot_flatfiles/interpro/ipr_annotation_data/interpro.xml
}

uniprot_species_to_taxid(){
    wget -c -P $apricot_flatfiles/all_taxids http://www.uniprot.org/docs/speclist.txt
}

create_pdb_inpath(){
    for FOLDER in pdb_sequence pdb_secstr pdb2uniprot
    do
        if ! [ -d $apricot_flatfiles/pdb/$FOLDER ]
        then
            mkdir -p $apricot_flatfiles/pdb/$FOLDER
        fi
    done
}

download_uniprot_map(){
    wget -P $apricot_flatfiles/pdb/pdb2uniprot http://www.uniprot.org/docs/pdbtosp.txt
}

download_pdb_sec_str(){
    wget -c -P $apricot_flatfiles/pdb/pdb_secstr http://www.rcsb.org/pdb/files/ss.txt
}

sort_and_format_pdb_data(){
    $PYTHON_PATH $apricot_lib/sort_sec_struc_pdb_data.py \
    -i $apricot_flatfiles/pdb/pdb_secstr/ss.txt -seq $apricot_flatfiles/pdb/pdb_sequence -str $apricot_flatfiles/pdb/pdb_secstr
    $apricot_flatfiles/blast/makeblastdb -in $apricot_flatfiles/pdb/pdb_sequence/pdb_sequence.txt -dbtype prot
}

get_pfam_domain_file(){
    wget -O - ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/ > $apricot_flatfiles/pfam/index.html
    current_release=$(cut -d'>' -f2 $apricot_flatfiles/pfam/index.html | cut -d'/' -f1 | cut -d'm' -f2 | sort -g | tail -n1)
    echo $current_release
    wget -c -P $apricot_flatfiles'/pfam' 'ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam'$current_release'/database_files/pfamA.txt.gz'
    gunzip $apricot_flatfiles'/pfam/pfamA.txt.gz'
}

get_blast_executables(){
    wget -c -P $apricot_flatfiles/blast ftp://ftp.ncbi.nih.gov/blast/executables/blast+/2.2.28/*x64-linux*
    tar -xvzf $apricot_flatfiles/blast/*x64-linux* -C $apricot_flatfiles/blast
    rm -rf $apricot_flatfiles/blast/*x64-linux*.gz
    for exepath in $(ls $apricot_flatfiles/blast)
    do
        if [ ! -p $apricot_flatfiles/blast/makeblastdb ]
        then
            if [ 'ncbi' = $(echo $exepath | cut -d \- -f 1) ]
            then
                cp -r $apricot_flatfiles/blast/$exepath/* $apricot_flatfiles/blast
            fi
        fi
        install $apricot_flatfiles/blast/bin/psiblast $apricot_flatfiles/blast
        install $apricot_flatfiles/blast/bin/blastp $apricot_flatfiles/blast
        install $apricot_flatfiles/blast/bin/makeblastdb $apricot_flatfiles/blast
    done
}

ontology_mapping_to_domains(){
    GO_PATH=$apricot_flatfiles/go_mapping
    wget -P $GO_PATH http://www.geneontology.org/ontology/go.obo
    interpro_to_go=$apricot_flatfiles/interpro/ipr_annotation_data/interpro2go
    interpro_data=$apricot_flatfiles/interpro/ipr_annotation_data/interproid.tbl
    cdd_data=$apricot_flatfiles/cdd/cdd_annotation_data/cddid.tbl
    $PYTHON_PATH $apricot_lib/map_domain_to_go.py $GO_PATH $interpro_to_go $interpro_data $cdd_data
}

get_biojs_dependencies(){
    for module in sequence protein msa
    do
        if ! [ -d  $apricot_flatfiles/biojs/$module ]
        then
            mkdir $apricot_flatfiles/biojs/$module
        fi
    done
    npm install -g mkdirp
    npm install -g browserify
    npm install biojs-vis-protein-viewer --prefix $apricot_flatfiles/biojs/protein
    npm install biojs-vis-sequence --prefix $apricot_flatfiles/biojs/sequence
    npm install msa --prefix $apricot_flatfiles/biojs/msa
}

get_clustalw(){
    wget -P $apricot_flatfiles/clustal ftp://ftp.ebi.ac.uk/pub/software/clustalw2/2.0.12/clustalw-2.0.12-linux-i686-libcppstatic.tar.gz
    tar -xvzf $apricot_flatfiles/clustal/clustalw-2.0.12-linux-i686-libcppstatic.tar.gz -C $apricot_flatfiles/clustal
    rm -rf $apricot_flatfiles/clustal/clustalw-2.0.12-linux-i686-libcppstatic.tar.gz
    mv $apricot_flatfiles/clustal/clustalw*/* $apricot_flatfiles/clustal
    rm -rf $apricot_flatfiles/clustal/clustalw-2.0.12-linux-i686-libcppstatic
}
main
