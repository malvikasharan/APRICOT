FROM ubuntu
MAINTAINER Malvika Sharan <malvika.sharan@uni-wuerzburg.de>
ENV DEBIAN_FRONTEND noninteractive

RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

FROM python:3.5

RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install git nano python3-pip bioperl --yes --fix-missing

RUN python3.5 -m pip install openpyxl=="2.3.1" 
RUN python3.5 -m pip install bio-apricot 

RUN CD home && git clone https://github.com/malvikasharan/APRICOT.git

RUN mkdir -p home/source_files
RUN mkdir -p home/source_files/reference_db_files


# Create root folders
RUN mkdir home/source_files/reference_db_files/cdd
RUN mkdir home/source_files/reference_db_files/cdd/Cdd
RUN mkdir home/source_files/reference_db_files/cdd/cdd_annotation_data

# Get CDD and annotation files
RUN wget -c -P home/source_files/reference_db_files/cdd/Cdd ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/*.gz
RUN for folders in home/source_files/reference_db_files/cdd/Cdd/*.gz; do tar xvf $folders -C home/source_files/reference_db_files/cdd/Cdd; done
RUN wget -c -P home/source_files/reference_db_files/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
RUN gunzip home/source_files/reference_db_files/cdd/cdd_annotation_data/*

# Get InterPro, InterProScan and annotation files
RUN mkdir home/source_files/reference_db_files/interpro
RUN mkdir home/source_files/reference_db_files/interpro/interproscan
RUN mkdir home/source_files/reference_db_files/interpro/interpro_annotation_data
RUN wget -c -P home/source_files/reference_db_files/interpro ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.19-58.0/interproscan-5.19-58.0-64-bit.tar.gz
RUN tar xvf home/source_files/reference_db_files/interpro/interproscan-5.19-58.0-64-bit.tar.gz -C home/source_files/reference_db_files/interpro
RUN mv home/source_files/reference_db_files/interpro/interproscan-*/* home/source_files/reference_db_files/interpro/interproscan
RUN wget -O - ftp://ftp.ebi.ac.uk/pub/databases/interpro/ > home/source_files/reference_db_files/interpro/ipr_flatfile.html
RUN wget -c -P home/source_files/reference_db_files/interpro/interpro_annotation_data ftp://ftp.ebi.ac.uk/pub/databases/interpro/58.0/interpro2go
RUN wget -c -P home/source_files/reference_db_files/interpro/interpro_annotation_data ftp://ftp.ebi.ac.uk/pub/databases/interpro/58.0/interpro.xml.gz
RUN gunzip home/source_files/reference_db_files/interpro/interpro_annotation_data/interpro.xml.gz

# Get and install BLAST modules
RUN mkdir home/source_files/reference_db_files/blast
RUN wget -c -P home/source_files/reference_db_files/blast ftp://ftp.ncbi.nih.gov/blast/executables/LATEST/ncbi-blast-2.4.0+-x64-linux.tar.gz
RUN tar -xvzf home/source_files/reference_db_files/blast/ncbi-blast-2.4.0+-x64-linux.tar.gz -C home/source_files/reference_db_files/blast
RUN mv home/source_files/reference_db_files/blast/ncbi-blast-2.4.0+/* home/source_files/reference_db_files/blast
RUN install home/source_files/reference_db_files/blast/bin/psiblast home/source_files/reference_db_files/blast
RUN install home/source_files/reference_db_files/blast/bin/blastp home/source_files/reference_db_files/blast
RUN install home/source_files/reference_db_files/blast/bin/makeblastdb home/source_files/reference_db_files/blast

# Get Gene Ontology files
RUN mkdir home/source_files/reference_db_files/go_mapping
RUN wget -P home/source_files/reference_db_files/go_mapping http://www.geneontology.org/ontology/go.obo

# Get PDB sequence and structures
RUN mkdir home/source_files/reference_db_files/pdb
RUN mkdir home/source_files/reference_db_files/pdb/pdb_sequence

RUN mkdir home/source_files/reference_db_files/pdb/pdb_secstr
RUN wget -c -P home/source_files/reference_db_files/pdb/pdb_secstr http://www.rcsb.org/pdb/files/ss.txt

# Get pdb2uniprot files
RUN mkdir home/source_files/reference_db_files/pdb/pdb2uniprot
RUN wget -P home/source_files/reference_db_files/pdb/pdb2uniprot http://www.uniprot.org/docs/pdbtosp.txt

# Get Taxonomy files
RUN mkdir home/source_files/reference_db_files/all_taxids
RUN wget -c -P home/source_files/reference_db_files/all_taxids http://www.uniprot.org/docs/speclist.txt

# Get pfam annotation data
RUN mkdir home/source_files/reference_db_files/pfam
RUN wget -c -P home/source_files/reference_db_files/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam30.0/database_files/pfamA.txt.gz
RUN gunzip home/source_files/reference_db_files/pfam/pfamA.txt.gz
    
# Get EMBOSS needle
RUN mkdir home/source_files/reference_db_files/needle
RUN wget -P home/source_files/reference_db_files/needle ftp://emboss.open-bio.org/pub/EMBOSS/old/6.5.0/emboss-latest.tar.gz
RUN tar -xvzf home/source_files/reference_db_files/needle/emboss-latest.tar.gz -C home/source_files/reference_db_files/needle
RUN mv home/source_files/reference_db_files/needle/EMBOSS*/* home/source_files/reference_db_files/needle
RUN cd home/source_files/reference_db_files/needle && ./configure && make && cd -

# Format flat files
RUN CD home && sh APRICOT/shell_scripts/docker_support.sh

# Remove tar files
RUN rm -rf \
home/source_files/reference_db_files/blast/ncbi-blast-2.4.0+-x64-linux.tar.gz \
home/source_files/reference_db_files/blast/ncbi-blast-2.4.0+ \
home/source_files/reference_db_files/interpro/interproscan-5.19-58.0-64-bit.tar.gz \
home/source_files/reference_db_files/needle/emboss-latest.tar.gz \
home/source_files/reference_db_files/cdd/Cdd/*.gz
