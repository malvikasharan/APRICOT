#!/bin/bash
# AUTHOR: Malvika Sharan <malvika.sharan@uni-wuerzburg.de>

PYTHON_PATH=python
apricot_path=$1
apricot_lib= ../$apricot_path/apricotlib        ## provide full path where you have cloned/save APRICOT from git
apricot_db=source_files/reference_db_files      ## apricot_db_path ##provide full path where you want to store the data

main(){
        create_db_path
        
        ### DATABASES ###
        create_cdd_inpath
        check_and_download_cdd
        create_interpro_inpath
        check_and_download_interpro
        ### ANNOTATION TOOLS ###
        install_raptorx
        install_psortb
        
        ### FLAT-FILE DATA ###
        create_flatfile_path
        ### CDD-MODULES ###
        create_cdd_flatfiles_inpath
        check_and_download_cdd_flatfiles
        ### InterProScan-MODULES ###
        create_interpro_flatfiles_inpath
        check_and_download_interpro_flatfiles
        uniprot_species_to_taxid
        ### PDB-MODULES ###
        create_pdb_inpath
        download_uniprot_map
        download_pdb_sec_str
        sort_and_format_pdb_data
        ### Other-requirements ###
        get_pfam_domain_file
        get_blast_executables
        get_emboss
        ontology_mapping_to_domains
        get_biojs_dependencies
        get_clustalw
} 

create_db_path(){
    for FOLDER in $apricot_db/apricot_db_and_tools
        
    do
        if ! [ -d $apricot_db/apricot_db_and_tools ]
        then
            mkdir -p $apricot_db/$FOLDER
        fi
    done
    for FOLDER in conserved_domain_database \
        interpro psortb raptorx nr
    do
        if ! [ -d $apricot_db/$FOLDER ]
        then
            mkdir -p $apricot_db/$FOLDER
        fi
    done
}

create_cdd_inpath(){
    for FOLDER in Cdd version_info
    do
        if ! [ -d $apricot_db/conserved_domain_database/$FOLDER ]
        then
            mkdir -p $apricot_db/conserved_domain_database/$FOLDER
        fi
    done
}

check_and_download_cdd(){
    wget -c -P $apricot_db/conserved_domain_database/ ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.info
    if diff $apricot_db/conserved_domain_database/cdd.info $apricot_db/conserved_domain_database/version_info/cdd.info >/dev/null ; then
        echo '\n**'updated vesion of cdd is present in path $apricot_db/conserved_domain_database.'**\n'
    else
        rm $apricot_db/rpsblast_analysis/cdd_annotation_data/*
        get_cdd_data
    fi
}

get_cdd_data(){
    wget -c -P $apricot_db/conserved_domain_database/version_info ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.info
    wget -c -P $apricot_db/conserved_domain_database/Cdd ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/*
    
    for binary_files in $(ls $apricot_db/conserved_domain_database/Cdd)
    do
        tar xvf $apricot_db/conserved_domain_database/Cdd/$binary_files -C $apricot_db/conserved_domain_database/Cdd
    done
    rm $apricot_db/conserved_domain_database/Cdd/*.gz
}

create_interpro_inpath(){
    for FOLDER in InterProScanData version_info
    do
        if ! [ -d $apricot_db/interpro/$FOLDER ]
        then
            mkdir -p $apricot_db/interpro/$FOLDER
        fi
    done
}

check_and_download_interpro(){
    wget -O - ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/ > $apricot_db/interpro/ipr_info.html
    if diff $apricot_db/interpro/ipr_info.html $apricot_db/interpro/version_info/ipr_info.html >/dev/null ; then
  	echo '\n**'updated vesion of InterPro is present in path $apricot_db/interpro.'**\n'
    else
        get_interpro_data
    fi
}

get_interpro_data(){
    wget -O - ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/ > $apricot_db/interpro/version_info/ipr_info.html
    $PYTHON_PATH $apricot_lib/current_interpro_version.py $apricot_db/interpro/ipr_info.html $apricot_db/interpro/ipr_version
    ipr_version=$(cat $apricot_db/interpro/ipr_version)
    wget -c -P $apricot_db/interpro/InterProScanData ftp://ftp.ebi.ac.uk:21/pub/software/unix/iprscan/5/$ipr_version/*-64-bit.tar*
    for files in $(ls $apricot_db/interpro/InterProScanData/*.tar.gz)
    do
        tar xvf $files -C $apricot_db/interpro/InterProScanData
    done
}

install_raptorx(){
    install_nr_for_raptorx
    git clone https://github.com/Indicator/RaptorX-SS8.git $apricot_db/raptorx/raptorx-ss3-ss8
    
    echo "Optionally download from raptorX package from its server in the folder $apricot_db/raptorx"
    #wget -c -P $apricot_db/raptorx http://ttic.uchicago.edu/~zywang/RaptorX-SS8/raptorx-ss8-0.1.tgz
    #tar -xvzf $apricot_db/raptorx/raptorx-ss8-0.1.tgz -C $apricot_db/raptorx
    
    ####needs nr database####
    perl $apricot_db/raptorx/raptorx-ss3-ss8/setup.pl \
    -home $apricot_db/raptorx/raptorx-ss3-ss8 \
    -blast $apricot_db/blast/psiblast \
    -nr $apricot_db/nr/nr
}

install_nr_for_raptorx(){
    if ! [ -f $apricot_db/nr/nr ]
    then
        wget -c -P $apricot_db/nr ftp://ftp.ncbi.nih.gov/blast/db/FASTA/nr.gz
        gunzip $apricot_db/nr/nr.gz
        if ! [ -f $apricot_db/nr/nr.15.psq ]
        then
            $apricot_db/blast/makeblastdb -in $apricot_db/nr/nr -dbtype prot
        fi
    fi
}

install_psortb(){
    echo "\n=========================================================================\n"
    echo "Please install Psortb using the Dockerfile available ïn the git repository:"
    echo "-> https://github.com/lairdm/psortb-docker.git"
    echo "Specified location for Psortb:"
    echo "-> "$apricot_db/psortb
    echo "\n=========================================================================\n"
}

create_flatfile_path(){
    for FOLDER in cdd interpro blast go_mapping biojs pdb all_taxids
    do
        if ! [ -d $apricot_db/$FOLDER ]
        then
            mkdir -p $apricot_db/$FOLDER
        fi
    done
}

create_cdd_flatfiles_inpath(){
    for FOLDER in version_info cdd_annotation_data cdd_flat_files
    do
        if ! [ -d $apricot_db/cdd/$FOLDER ]
        then
            mkdir -p $apricot_db/cdd/$FOLDER
        fi
    done
}

check_and_download_cdd_flatfiles(){
    rm -rf $apricot_db/cdd/cdd_flat_files/*
    wget -c -P $apricot_db/cdd/ ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.info
    if diff $apricot_db/cdd/cdd.info $apricot_db/cdd/version_info/cdd.info >/dev/null ; then
        echo '\n**'updated vesion of cdd is present in path $apricot_db/cdd.'**\n'
    fi
    cp $apricot_db/cdd/cdd.info $apricot_db/cdd/version_info/cdd.info
    rm $apricot_db/cdd/cdd_annotation_data/*
    wget -c -P $apricot_db/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
    gunzip $apricot_db/cdd/cdd_annotation_data/*
}

create_interpro_flatfiles_inpath(){
    for FOLDER in version_info ipr_annotation_data interpro_flat_files
    do
        if ! [ -d $apricot_db/interpro/$FOLDER ]
        then
            mkdir -p $apricot_db/interpro/$FOLDER
        fi
    done
}

check_and_download_interpro_flatfiles(){
    ftp_server=ftp://ftp.ebi.ac.uk/pub/databases/interpro
    wget -O - ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/ > $apricot_db/interpro/ipr_info.html
    if diff $apricot_db/interpro/ipr_info.html $apricot_db/interpro/version_info/ipr_info.html >/dev/null ; then
  	echo '\n**'updated vesion of InterPro is present in path $apricot_db/interpro.'**\n'
    fi
    cp $apricot_db/interpro/ipr_info.html $apricot_db/interpro/version_info/ipr_info.html
    rm -rf $apricot_db/interpro/interpro_flat_files/*
    wget -O - $ftp_server/ > $apricot_db/interpro/version_info/ipr_flatfile.html
    $PYTHON_PATH $apricot_lib/current_interpro_version.py $apricot_db/interpro/version_info/ipr_flatfile.html $apricot_db/interpro/ipr_flatfile
    ipr_flatfile=$(cat $apricot_db/interpro/ipr_flatfile)
    wget -c -P $apricot_db/interpro/ipr_annotation_data $ftp_server/$ipr_flatfile/interpro2go
    wget -c -P $apricot_db/interpro/ipr_annotation_data $ftp_server/interpro.xml.gz
    gunzip $apricot_db/interpro/ipr_annotation_data/interpro.xml.gz
    $PYTHON_PATH $apricot_lib/interpro_xml_to_table.py $apricot_db/interpro/ipr_annotation_data $apricot_db/interpro/ipr_annotation_data/interpro.xml
}

uniprot_species_to_taxid(){
    wget -c -P $apricot_db/all_taxids http://www.uniprot.org/docs/speclist.txt
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

get_pfam_domain_file(){
    wget -O - ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/ > $apricot_files/pfam/index.html
    current_release=$(cut -d'>' -f2 $apricot_files/pfam/index.html | cut -d'/' -f1 | cut -d'm' -f2 | sort -g | tail -n1)
    echo $current_release
    wget -c -P $apricot_files/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam$current_release/database_files/pfamA.txt.gz
    gunzip $apricot_files'/pfam/pfamA.txt.gz'
}

get_blast_executables(){
    wget -c -P $apricot_db/blast ftp://ftp.ncbi.nih.gov/blast/executables/blast+/2.2.28/*x64-linux*
    tar -xvzf $apricot_db/blast/*x64-linux* -C $apricot_db/blast
    rm -rf $apricot_db/blast/*x64-linux*.gz
    for exepath in $(ls $apricot_db/blast)
    do
        if [ ! -p $apricot_db/blast/makeblastdb ]
        then
            if [ 'ncbi' = $(echo $exepath | cut -d \- -f 1) ]
            then
                cp -r $apricot_db/blast/$exepath/* $apricot_db/blast
            fi
        fi
        install $apricot_db/blast/bin/psiblast $apricot_db/blast
        install $apricot_db/blast/bin/blastp $apricot_db/blast
        install $apricot_db/blast/bin/makeblastdb $apricot_db/blast
    done
}

get_emboss(){
    wget -P $apricot_files/needle ftp://emboss.open-bio.org/pub/EMBOSS/old/6.5.0/emboss-latest.tar.gz
    tar -xvzf $apricot_files/needle/emboss-latest.tar.gz -C $apricot_files/needle
    mv $apricot_files/needle/EMBOSS*/* $apricot_files/needle
    cd $apricot_files/needle && ./configure && make && cd -
    echo "In order to re-install please delete (rm) config.log file from your present working directory"
}

ontology_mapping_to_domains(){
    GO_PATH=$apricot_db/go_mapping
    wget -P $GO_PATH http://www.geneontology.org/ontology/go.obo
    interpro_to_go=$apricot_db/interpro/ipr_annotation_data/interpro2go
    interpro_data=$apricot_db/interpro/ipr_annotation_data/interproid.tbl
    cdd_data=$apricot_db/cdd/cdd_annotation_data/cddid.tbl
    $PYTHON_PATH $apricot_lib/map_domain_to_go.py $GO_PATH $interpro_to_go $interpro_data $cdd_data
}

get_biojs_dependencies(){
    for module in sequence protein msa
    do
        if ! [ -d  $apricot_db/biojs/$module ]
        then
            mkdir $apricot_db/biojs/$module
        fi
    done
    npm install -g mkdirp
    npm install -g browserify
    npm install biojs-vis-protein-viewer --prefix $apricot_db/biojs/protein
    npm install biojs-vis-sequence --prefix $apricot_db/biojs/sequence
    npm install msa --prefix $apricot_db/biojs/msa
}

get_clustalw(){
    wget -P $apricot_db/clustal ftp://ftp.ebi.ac.uk/pub/software/clustalw2/2.0.12/clustalw-2.0.12-linux-i686-libcppstatic.tar.gz
    tar -xvzf $apricot_db/clustal/clustalw-2.0.12-linux-i686-libcppstatic.tar.gz -C $apricot_db/clustal
    rm -rf $apricot_db/clustal/clustalw-2.0.12-linux-i686-libcppstatic.tar.gz
    mv $apricot_db/clustal/clustalw*/* $apricot_db/clustal
    rm -rf $apricot_db/clustal/clustalw-2.0.12-linux-i686-libcppstatic
}

main

