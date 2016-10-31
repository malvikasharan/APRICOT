FROM ubuntu
MAINTAINER Malvika Sharan <malvika.sharan@uni-wuerzburg.de>
ENV DEBIAN_FRONTEND noninteractive

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Get basic required packages and create root folders
RUN apt-get update --yes && apt-get install wget git nano python3-pip build-essential libx11-dev oracle-java7-installer --yes --fix-missing && apt-get clean \
    python3.5 -m pip install bio-apricot && cd /home && git clone https://github.com/malvikasharan/APRICOT.git && \
    mkdir -p \
    /home/emboss/needle \
    /home/emboss/temp_needle \
    /home/source_files/reference_db_files/blast \
    /home/source_files/reference_db_files/cdd/Cdd \
    /home/source_files/reference_db_files/cdd/cdd_annotation_data \
    /home/source_files/reference_db_files/interpro/interproscan \
    /home/source_files/reference_db_files/interpro/interpro_annotation_data \
    /home/source_files/reference_db_files/go_mapping \
    /home/source_files/reference_db_files/pdb/pdb_sequence \
    /home/source_files/reference_db_files/pdb/pdb_secstr \
    /home/source_files/reference_db_files/pdb/pdb2uniprot \
    /home/source_files/reference_db_files/all_taxids \
    /home/source_files/reference_db_files/pfam \
    && wget -c -P /home/source_files/reference_db_files/blast ftp://ftp.ncbi.nih.gov/blast/executables/LATEST/ncbi-blast-*+-x64-linux.tar.gz && \
    tar -xvzf /home/source_files/reference_db_files/blast/ncbi-blast-*+-x64-linux.tar.gz -C /home/source_files/reference_db_files/blast && \
    mv /home/source_files/reference_db_files/blast/ncbi-blast-*+/* /home/source_files/reference_db_files/blast && \
    install /home/source_files/reference_db_files/blast/bin/psiblast /home/source_files/reference_db_files/blast && \
    install /home/source_files/reference_db_files/blast/bin/rpsblast /home/source_files/reference_db_files/blast && \
    install /home/source_files/reference_db_files/blast/bin/blastp /home/source_files/reference_db_files/blast && \
    install /home/source_files/reference_db_files/blast/bin/makeblastdb /home/source_files/reference_db_files/blast && \
    cp /home/source_files/reference_db_files/blast/bin/rpsblast /usr/local/bin && \
    cp /home/source_files/reference_db_files/blast/bin/makeblastdb /usr/local/bin && \
    cp /home/source_files/reference_db_files/blast/bin/psiblast /usr/local/bin && \
    cp /home/source_files/reference_db_files/blast/bin/blastp /usr/local/bin && \
    wget -P /home/emboss/needle ftp://emboss.open-bio.org/pub/EMBOSS/emboss-latest.tar.gz && \
    tar -xvzf /home/emboss/needle/emboss-latest.tar.gz -C /home/emboss/needle && \
    mv /home/emboss/needle/EMBOSS*/* /home/emboss/needle && \
    cd /home/emboss/needle && ./configure && make && cd - && \
    cp /home/emboss/needle/emboss/needle /usr/local/bin && \
    mv /home/emboss/needle/* /home/emboss/temp_needle && \
    mv /home/emboss/temp_needle/ajax /home/emboss/needle && \
    mv /home/emboss/temp_needle/emboss /home/emboss/needle && \
    mv /home/emboss/temp_needle/nucleus /home/emboss/needle && \
    mv /home/emboss/temp_needle/plplot /home/emboss/needle && \
    mv /home/emboss/temp_needle/scripts /home/emboss/needle && \
    rm -rf /home/emboss/temp_needle \
    /home/source_files/reference_db_files/blast/ncbi-blast-*+-x64-linux.tar.gz \
    /home/source_files/reference_db_files/blast/ncbi-blast-*+ \
    /home/source_files/reference_db_files/blast/bin/* \
    /usr/local/python3.4 \
    /usr/local/python2.7 \
    /usr/local/lib/python3.4 \
    /usr/local/lib/python2.7 \
    /usr/lib/python2.7 \
    /usr/lib/python3.4 \
    usr/bin/*python3.4* \
    usr/bin/*python2.7* \
    etc/python3.4 \
    etc/python2.7

# Removed the installation of DB and supporting files from the main Dockerfile to reduce the docker image size tremendously.

## The following actions will now be executed inside the docker image using the command: `cd /home && sh APRICOT/shell_scripts/docker_support.sh` 
## Databases (CDD, InterPro), InterProScan and annotation files
## Supporting files: Gene Ontology, PDB files, pdb2uniprot files,Taxonomy files, pfam annotation data

## RUN cd /home && sh APRICOT/shell_scripts/docker_support.sh

