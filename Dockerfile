FROM ubuntu
MAINTAINER Malvika Sharan <malvika.sharan@uni-wuerzburg.de>
ENV DEBIAN_FRONTEND noninteractive

FROM python:3.5

RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install git nano python3-pip python3-matplotlib python3-numpy python3-scipy python3-biopython python3-requests --yes --fix-missing

RUN python3.5 -m pip install openpyxl=="2.3.1" 
RUN python3.5 -m pip bio-apricot 

# RUN git clone https://github.com/malvikasharan/APRICOT.git

RUN mkdir -p source_files
RUN mkdir -p source_files/reference_db_files

RUN mkdir source_files/reference_db_files/cdd
RUN mkdir source_files/reference_db_files/cdd/Cdd
RUN mkdir source_files/reference_db_files/cdd/cdd_annotation_data

RUN wget -c -P source_files/reference_db_files/cdd/Cdd ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/*.gz
RUN for folders in source_files/reference_db_files/cdd/Cdd/*.gz; do tar xvf $folders -C source_files/reference_db_files/cdd/Cdd; done
RUN rm source_files/reference_db_files/cdd/Cdd/*.gz
RUN wget -c -P source_files/reference_db_files/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
RUN gunzip source_files/reference_db_files/cdd/cdd_annotation_data/*

RUN mkdir source_files/reference_db_files/interpro
RUN mkdir source_files/reference_db_files/interpro/interproscan
RUN mkdir source_files/reference_db_files/interpro/interpro_annotation_data
RUN wget -c -P source_files/reference_db_files/interpro ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.19-58.0/interproscan-5.19-58.0-64-bit.tar.gz
RUN tar xvf source_files/reference_db_files/interpro/interproscan-5.19-58.0-64-bit.tar.gz -C source_files/reference_db_files/interpro
RUN mv source_files/reference_db_files/interpro/interproscan-*/* source_files/reference_db_files/interpro/interproscan
RUN wget -O - ftp://ftp.ebi.ac.uk/pub/databases/interpro/ > source_files/reference_db_files/interpro/ipr_flatfile.html
RUN wget -c -P source_files/reference_db_files/interpro/interpro_annotation_data ftp://ftp.ebi.ac.uk/pub/databases/interpro/58.0/interpro2go
RUN wget -c -P source_files/reference_db_files/interpro/interpro_annotation_data ftp://ftp.ebi.ac.uk/pub/databases/interpro/58.0/interpro.xml.gz
RUN gunzip source_files/reference_db_files/interpro/interpro_annotation_data/interpro.xml.gz

RUN mkdir source_files/reference_db_files/blast
RUN wget -c -P source_files/reference_db_files/blast ftp://ftp.ncbi.nih.gov/blast/executables/blast+/2.2.28/ncbi-blast-2.2.28+-x64-linux.tar.gz
RUN tar -xvzf source_files/reference_db_files/blast/ncbi-blast-2.2.28+-x64-linux.tar.gz -C source_files/reference_db_files/blast
RUN cp -r source_files/reference_db_files/blast/ncbi-blast-2.2.28+/* source_files/reference_db_files/blast
RUN rm -rf source_files/reference_db_files/blast/ncbi-blast-2.2.28+-x64-linux.gz
RUN install source_files/reference_db_files/blast/bin/psiblast source_files/reference_db_files/blast
RUN install source_files/reference_db_files/blast/bin/blastp source_files/reference_db_files/blast
RUN install source_files/reference_db_files/blast/bin/makeblastdb source_files/reference_db_files/blast
    
RUN mkdir source_files/reference_db_files/go_mapping
RUN wget -P source_files/reference_db_files/go_mapping http://www.geneontology.org/ontology/go.obo

RUN mkdir source_files/reference_db_files/pdb
RUN mkdir source_files/reference_db_files/pdb/pdb_sequence

RUN mkdir source_files/reference_db_files/pdb/pdb_secstr
RUN wget -c -P source_files/reference_db_files/pdb/pdb_secstr http://www.rcsb.org/pdb/files/ss.txt
#
RUN mkdir source_files/reference_db_files/pdb/pdb2uniprot
RUN wget -P source_files/reference_db_files/pdb/pdb2uniprot http://www.uniprot.org/docs/pdbtosp.txt

RUN mkdir source_files/reference_db_files/all_taxids
RUN wget -c -P source_files/reference_db_files/all_taxids http://www.uniprot.org/docs/speclist.txt

RUN mkdir source_files/reference_db_files/pfam
RUN wget -c -P source_files/reference_db_files/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam30.0/database_files/pfamA.txt.gz
RUN gunzip source_files/reference_db_files/pfam/pfamA.txt.gz
    
RUN mkdir source_files/reference_db_files/needle
RUN wget -P source_files/reference_db_files/needle ftp://emboss.open-bio.org/pub/EMBOSS/old/6.5.0/emboss-latest.tar.gz
RUN tar -xvzf source_files/reference_db_files/needle/emboss-latest.tar.gz -C source_files/reference_db_files/needle
RUN mv source_files/reference_db_files/needle/EMBOSS*/* source_files/reference_db_files/needle
RUN cd source_files/reference_db_files/needle && ./configure && make && cd -
