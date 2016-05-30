# APRICOT TUTORIAL

This tutorial provides an easy way to test different modules of
APRICOT and understand the basic usage of this pipeline.

### Requirements:

1) Get the Shell script
[run_example.sh](https://github.com/malvikasharan/APRICOT/blob/master/shell_scripts/run_example.sh)
from GitHub, which will assist you in following the tutorial.

```
$ wget -N https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/run_example.sh
```

2) Use [pip](https://pip.pypa.io/en/stable/) to install/update the package

```
$ pip install bio-apricot
```

or

```
$ pip install --user bio-apricot
```

or use [APRICOT repository](https://github.com/malvikasharan/APRICOT/archive/master.zip) from GiHub 

```
$ git clone https://github.com/malvikasharan/APRICOT.git
```

#### Not required for this tutorial

APRICOT usually requires local databases of CDD and InterPro, along
with the BLAST executables and InterProScan to carry out domain
predictions. In addition, to provide additional annotation of the proteins
with biological features, it uses locally installed Psort and RaptorX
executable. These requirements have been discussed in detail in the
[documentation](https://github.com/malvikasharan/APRICOT/blob/master/README.md).
We will **NOT** install these for the tutorial, instead we have
provided pre-processed files that should allow you to test the
functionality of the tool. The files are avaialable at: [Zenodo
record](https://zenodo.org/record/51705/files).

### Example analysis

APRICOT can be executed by python (python3 is recommended) on
Unix-flavors (GNU/Linux, BSD, OS X).

We will go through the shell script `run_example.sh` step by
step. This script assumes that users have installed the software using
pip.

**If you are using locally installed git repository**

Please specifiy the the path where APRICOT modules are located (see below: APRICOT_PATH)
and run the tool using `python $APRICOT_PATH/bin/apricot` by editing `APRICOT_CALL="python3 ../bin/apricot"` (which would
have the advantage that you can specify the Python version you would
like to use) or `./$APRICOT_PATH/bin/apricot` command.

```
python $APRICOT_PATH/bin/apricot -h
```

If you get an error message ```system_test.sh: 164: system_test.sh: ../bin/apricot: Permission denied ...`, please open the script `run_example.sh` and and edit the `APRICOT_CALL="../bin/apricot"` to `APRICOT_CALL="python3 ../bin/apricot"` (instead if python3, you can use python or define any version of python, or instead use ./).

#### Defining paths

Users can set the following paths:

```
## User defined PATHS (default paths are given)

# Path where the analysis data by APRICOT will be stored
ANALYSIS_PATH=APRICOT_analysis

# Path where the source files and databases will be stored
ROOT_DB_PATH=source_files

# Path for EMBOSS suite with locally installed needle cline
NEEDLE_EMBOSS_PATH=source_files/reference_db_files/needle/emboss/needle   # Default path

# Path where APRICOT modules are located, by-default we use APRICOT as
# the name of git library
APRICOT_PATH=APRICOT
```

APRICOT stores databases and source files in these paths.

```
## FIXED PATHS 

# Source data downloaded by APRICOT
DB_PATH=$ROOT_DB_PATH/reference_db_files

## PATHS for domain databases
CDD_PATH=$DB_PATH/cdd/Cdd
INTERPRO_PATH=$DB_PATH/interpro/interproscan
```

#### Creating analysis folders

1) We will create each of the paths that we defined above in the section above:

```
donwload_files(){
   mkdir -p $ROOT_DB_PATH $APRICOT_PATH $ANALYSIS_PATH $APRICOT_LIBRARY
   for db_subpath in cdd go_mapping interpro pfam
   do
       mkdir -p $DB_PATH/$db_subpath
   done
   
[...]
}
```

This will create a main folder `source_files` with subfolder as shown
below.


```
source_files
    └───├domain_data            # Location for the files containing keywords for domain selection and subsequently selected domains
    |
    └───├reference_db_files
            └───├cdd                            # Cdd related reference files
            |   └───├Cdd                        # Cdd database (Not required for the tutorial)
            |   └───├cdd_annotation_data        # Cdd related annotation file
            └───├pfam
            └───├interpro                       # InterPro related reference files
            |   └───├interproscan               # Interpro database and InterProScan related tools (Not required for the tutorial)
            |   └───├interpro_annotation_data   # interPro related annotation files
            └───├go_mapping                     # GO related data containing GO anotation for the domains obtained from CDD and InterPro 

```

2) Using the `create` subcommand from APRICOT, we will create the
analysis folder and its subfolder. This generates a main folder
`APRICOT_analysis` (name can be defined by users), which contains
subfolders as shown below.

```
apricot create APRICOT_analysis
```

```
APRICOT_analysis
    └───├input                                  # Location used by subcommand 'query' to store all the related files
    |       └───├query_proteins                 # Location for the list of query proteins
    |       |
    |       └───├uniprot_reference_table        # Location for storing the reference table downloaded from UniProt 
    |       |
    |       └───├mapped_query_annotation        # All the query proteins that are mapped to at least one UniProt annotations 
    |       |   ├fasta_path_mapped_query        # Fasta files obtained for all the query proteins, can be used for query fasta files
    |       |   ├xml_path_mapped_query          # UniProt xml files obtained for all the query proteins
    |
    └───├output
            └───├0_predicted_domains            # Location for the output data obtained from the subcommand 'predict'
            └───├1_compiled_domain_information  # Location for the output data obtained from the subcommand 'filter'          
            └───├2_selected_domain_information            
            └───├3_annotation_scoring           # Location for the output data obtained from the subcommand 'annoscore'
            └───├4_additional_annotations       # Location for additional annotations for the selected 
            |                                   # queries using subcommand 'addanno'
            └───├5_analysis_summary             # Location for the output data obtained from the subcommand 'summary'
            └───├format_output_data             # Location for the output data obtained from the subcommand 'format'
            └───├visualization_files            # Location for the output data obtained from the subcommand 'vis'
```

#### Fetching required source files

We have provided a few pre-processed files, which are available in
*apricot_demo_files* folder (retrieved from zenodo), if it is already
available, please comment the first three lines in the script, which
copies these files to the APRICOT defined paths.

Additionally, we will download domain annotation files from CDD and
Pfam databases.

```
complete_data_for_demo(){

   ## Here DB_PATH=source_files/reference_db_files and $ANALYSIS_PATH=APRICOT_analysis
   
    zenodo_link_for_demo_data=https://zenodo.org/record/51705/files/APRICOT-1.0-demo_files-MS.zip
    wget $zenodo_link_for_demo_data
    unzip APRICOT-1.0-demo_files-MS.zip
    cp -r APRICOT-1.0-demo_files-MS/apricot_demo_files/go_mapping/* $DB_PATH   
    cp -r APRICOT-1.0-demo_files-MS/apricot_demo_files/interpro_annotation_data $DB_PATH/interpro
    cp APRICOT-1.0-demo_files-MS/apricot_demo_files/cdd_analysis/* $ANALYSIS_PATH/output/0_predicted_domains/cdd_analysis
    cp APRICOT-1.0-demo_files-MS/apricot_demo_files/ipr_analysis/* $ANALYSIS_PATH/output/0_predicted_domains/ipr_analysis
    
    ## CDD annotation table
    wget -c -P $DB_PATH/cdd/cdd_annotation_data ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
    gunzip $DB_PATH/cdd/cdd_annotation_data/*
    
    ## PfamA annotation table
    pfam_release=Pfam30.0
    wget -c -P $DB_PATH/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/$pfam_release/database_files/pfamA.txt.gz
    gunzip $DB_PATH'/pfam/pfamA.txt.gz'
}
```

#### Providing query proteins using the subcommand `query`

In this analysis we will identify protein that contains RRM/RNP, which
is a family of conserved RNA-binding domains.

Users can provide query proteins using various options. Here we use
the input option as UniProt identifiers (ID) and provide 2 query proteins:
`P0A6X3`,`P00957`.

The protein ID `P0A6X3` is used as an positive example. It represents the 
Hfq protein that contains sm and RRM/RNP like domain. The protein ID `P00957` 
is used as an negative example which represents the alaS that contains a domain 
related to tRNA-ligase therefore, it must not be identified with domains reltaed to RRM/RNP.

```
## *REQUIRED* INPUT-1: provide comma separated list of UniProt ids##

query_uids='P0A6X3,P00957'          # Option-1: UniProt identifier
apricot query --analysis_path APRICOT_analysis --uids $query_uids
```

#### Providing keyword inputs using the subcommand `keywords`

There are two sets of keyword inputs: the first-set is required to selects
domains from domain databases and the second set, which is an optional
input, should comprise of terms that will classify our results
accordingly.

In this turtorial we are interested in identifying `RRM` containing
protein, hence, we will use `RRM` as one of the terms. Additionally, we
can provide other terms (for example, `KH` and `DEAD`) to see if there are
domains associated with those terms could be identified in our query
proteins.

For the second set, we have listed few enzymes along with RRM and RNP.

```
### *REQUIRED* Input-2, comma separated list of keywords for domain selection
domain_kw='RRM,KH,DEAD'

### *OPTIONAL* Input-2, comma separated list of keywords for protein classification based on the predicted domains

class_kw='ribosom,helicase,synthetase,polymerase,transferase,nuclease,RRM,RNP'
apricot keywords --db_root source_files $domain_kw -cl $class_kw
```

These keywords are listed in the files
`keywords_for_domain_selection.txt` and
`keywords_for_result_classification.txt` present in the folder
`source_files` as shown below.

```
source_files
    └───├domain_data
            keywords_for_domain_selection.txt  
            keywords_for_result_classification.txt
```

#### Selecting domains of interest using the subcommand `select`

APRICOT uses the keywords provided in previous section and uses them
to select functional domains. Users can use `-C` flag to select only
CDD related domains or `-I` flag to select only InterPro related
domains.

In this tutorial we will use the default option, which selects domains
from both CDD and InterPro databases.

```
apricot select --db_root source_files
```

The selected domains are saved in these respective locations as ashown below.

```
source_files
    └───├domain_data            
            └───├cdd                                # Containes individual files generated for each keyword related domains      
            |    key1_related_cdd_domains.tab
            |    key2_related_cdd_domains.tab
            |    ..
            └───├interpro                           # Containes individual files generated for each keyword related domains
            |    key1_related_interpro_domains.tab
            |    key2_related_interpro_domains.tab
            |    ..
            |all_keyword_selected_domain_data.tab   # All the keyword selected domains are mapped and combined
```

#### Domain predictions using the subcommand `predict`

This subcommand uses one of the core modules of APRICOT, which
predicts all the possible domains in the query domains.

For this analysis, APRICOT uses both the databases by default, however
single database can be defined by using flag `-C` or `-I` for CDD and
InterPro respectively. In case users provide the input as fasta files,
the `query` subcommand can be skipped and the prediction of domains
can be carried out directly, however in that case the path for fasta
files (FASTA_PATH) can be provided using the option `--fasta
$FASTA_PATH`.

APRICOT skips re-prediction of the domains when the output files are
present for the analysis of each query proteins, however users can use
the flag `-F` to *force* the re-analysis.

```
apricot predict --analysis_path APRICOT_analysis 
```

Please note that we are using default directory structure for this
tutorial, however, it is possible to define locations of the databases
by using options `--cdd_db $CDD_PATH` and `--ipr_db $INTERPRO_PATH`
for CDD and interpro respectively.

In this tutorial, to avoid the use of domain databases and tools
(avoid the prediction of domains), we provided the output files
generated by domain prediction analysis and copied to the required
subfolders as shown below.

```
APRICOT_analysis
    └───├output                             
            └───├0_predicted_domains    # Location for storing files generated by domain prediction
                └───├cdd_analysis       # Domains predicted for each protein using CDD datasets
                |       P00957.txt
                |       P0A6X3.txt
                |
                └───├ipr_analysis       # Domains predicted for each protein using InterPro datasets
                        P00957.tsv
                        P0A6X3.tsv
```

#### Filtering the predicted domains using the subcommand `filter`

All the domains (predicted by `predict`) undergoes a filtering step in
order to select proteins that are predicted with the domains of
interest (selected from databases using `select`).

In this tutorial we have used the default parameters (refer
documentation) with their optimal cut-offs (`--similarity 24` for 24 %
minimum similarity between the reference and predicted domain and
`--coverage 39` for 39 % minimum domain coverage in the query protein),
however users can provide cut-offs for different parameters (refer
documentation).

```
apricot filter --analysis_path APRICOT_analysis \
--similarity 24 --coverage 39
```

The files obtained from this analysis are stored in the subfolder
`1_compiled_domain_information` in the main analysis
folder. Additionally, the information of the proteins obtained from
uniProt are combined and store in the folder combined_data. These file
location are as shown below.

```
APRICOT_analysis
    └───├output                             
            └───├1_compiled_domain_information  # Formatted flat files containg domain information
            |   └───├selected_data              # Files containing proteins that contain domains of interest with the predcited domains
            |   |       cdd_filtered.csv        # Proteins containing CDD domains of interest
            |   |       cdd_filtered_id.csv     # Proteins IDs containing CDD domains IDs of interest
            |   |       ipr_filtered.csv        # Proteins containing InterPro domains of interest
            |   |       ipr_filtered_id.csv     # Proteins IDs containing InterPro domains IDs of interest
            |   |
            |   └───├unfiltered_data                            # All the domains predicted in the query proteins (unfiltered)
            |            cdd_unfiltered_all_prediction.csv  
            |            ipr_unfiltered_all_prediction.csv
            |
            └───├2_selected_domain_information
                └───├combined_data                              # Annotation extended for the selected proteins
                        annotation_extended_for_selected.csv    
```

#### Classify all the selected domains from previous analysis using the subcommand `classify`

All the selected proteins with their domains (selected by `filter`)
are classified into smaller subsets to help navigating the output
files. This classification uses the keywords provided by users, which
are either explicitely defined (`-cl` flag in `keywords`) or are used
for the domain selection.

```
apricot classify --analysis_path APRICOT_analysis
```

The list of proteins that are selected based on the domains of
interest is classified when the annotations contain one of the
terms. The classified files are stored in the subfolder
`2_selected_domain_information` as shown below.

```
APRICOT_analysis
    └───├output                             
            └───├2_selected_domain_information         # Selected data classified into smaller subsets based on the keyword input
                └───├classified_data
                        RNP_selected_data.csv  
                        RRM_selected_data.csv
```

#### Calculating annotation scores for the selected domains using the subcommand `annoscore`

This subcommand uses another important module of APRICOT to calculate
annotation-based scores for each predicted domains in the query
proteins. Please refer documentation to understand different sets of
features, which have been used in APRICOT for the scoring of the
predicted domains with respect to their reference consensus.

This module require python packages: numpy and scipy, and EMBOSS suit to run 
Needleman Wunsch pairwise-alignment analysis. If not installed, please install it 
using the function `get_emboss`. For basic demonstration, we suggest you to skip 
this module as the configuration and installation of EMBOSS suite takes time. However, 
if installed already, please edit the path name `NEEDLE_EMBOSS_PATH`.

```
NEEDLE_EMBOSS_PATH=source_files/reference_db_files/needle/emboss/needle   # Default path
apricot annoscore --analysis_path APRICOT_analysis --needle_dir $NEEDLE_EMBOSS_PATH
```

The files generated from this analysis are stored in the subfolder
`3_annotation_scoring in the analysis` folder as shown below.


```
APRICOT_analysis
    └───├output                             
            └───├2_selected_domain_information
```

#### Generating analysis summary using the subcommand: `summary`

Users can summarize the analysis result using this module. The summary
file contains an overview of the entire analysis that includes, for
example, the query proteins mapped to UniPro, total selected domains
per keyword, summary of domain predictions and their selection.

```
apricot summary --analysis_path APRICOT_analysis
```
The summary file is stored in the subfolder `5_analysis_summary` analysis folder as shown below.

```
APRICOT_analysis
    └───├output                             
            └───├5_analysis_summary
                       APRICOT_analysis_summary.csv   # Summary file
```

##### Format output files using the subcommand `format`

APRICOT by default produces output files in comma-separated values
(.csv). Users can convert these files to HTML format using `-HT` flag
or excel format (.xlsx) using `-XL` flag, where the later one uses the 
`openpyxl` python module.

In this tutorial we have used `-HT` option.

```
apricot format --analysis_path APRICOT_analysis -HT
```

All the files in the format of selection are stored in the subfolder
`format_output_data` in the main analysis folder as shown below.

```
APRICOT_analysis
    └───├output                             
            └───├format_output_data
                └───├html_files                         # Output files for each folder in HTML format
                |   └───├0_predicted_domains  
                |   └───├1_compiled_domain_information  
                |   └───├2_selected_domain_information  
                |   └───├3_annotation_scoring  
                |   └───├4_additional_annotations 
                |   └───├5_analysis_summary
                |
                └───├excel_files                        # Output files for each folder in Excel format
                    └───├ ...
```

This concludes the tutorial for the analysis conducted by APRICOT. All
of these modules can be run in an automated streamlined manner using
the provided shell script as shown below.

```
$ sh run_example.sh
```

### Troubleshooting

We have tested the described modules intensively, however if you
encounter any bugs and have problems running any of these modules,
please contact me via email: malvikasharan@gmail.com or report the
issues in this repository.

Your feedback and comments are welcome.
