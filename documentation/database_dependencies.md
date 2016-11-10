[![Latest Version](https://img.shields.io/pypi/v/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![License](https://img.shields.io/pypi/l/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![DOI](https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg)](https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT)
[![](https://images.microbadger.com/badges/image/malvikasharan/apricot.svg)](https://microbadger.com/images/malvikasharan/apricot "Get your own image badge on microbadger.com")

![alt tag](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_logo.png)

## Databases for running the software

The docker image can be used to carry out the analysis by APRICOT which comprise of the the main software and the required tools.

Additionally users are required to establish a repository containing all the databases/datasets in a directory `source_files`. 

This can be carried out by using the sheel script [docker_support.sh](https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/docker_support.sh) either locally or inside the docker container, which creates the directory with subfolders as illustrated below.

```
$ wget https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/docker_support.sh
$ sh docker_support.sh
```

```
source_files
    └───├domain_data            # Location for the files containing keywords for domain selection and subsequently selected domains
    |
    └───├emboss                 # EMBOSS package containing needle software
    |
    └───├reference_db_files
            └───├all_taxid                      # Taxonomy ids for the reference of proteome analysis
            └───├blast                          # BLAST package containing required executables
            └───├cdd                            # Cdd related reference files
            |   └───├Cdd                        # Cdd database (Not required for the tutorial)
            |   └───├cdd_annotation_data        # Cdd related annotation file
            └───├pdb                            # All pdb structures as a reference for the tertiary structures
            └───├pfam                           # Pfam annotation data
            └───├interpro                       # InterPro related reference files
            |   └───├interproscan               # Interpro database and InterProScan related tools (Not required for the tutorial)
            |   └───├interpro_annotation_data   # interPro related annotation files
            └───├go_mapping                     # GO related data containing GO anotation for the domains obtained from CDD and InterPro 

```
