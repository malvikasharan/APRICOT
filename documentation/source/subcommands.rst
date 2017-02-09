|Latest Version| |License| |DOI| |image3|

|image4|

Subcommands
^^^^^^^^^^^

APRICOT comprises of distinct model designed to carry out specific task.

Each subcommand requires the path to the analysis folder
('APRICOT\_analysis' by deafult). Different subcommands can be quickly
viewed by running ``-h`` for help option (e.g. ``apricot -h`` or
``python3 APRICOT/bin/apricot -h``).

::

    usage: apricot [-h] [--version]
                   {create,taxid,query,keywords,select,predict,filter,classify,annoscore,summary,addanno,vis,format}
                   ...

    positional arguments:
      {create,taxid,query,keywords,select,predict,filter,classify,annoscore,summary,addanno,vis,format}
                            APRICOT commands - Refer documentation for detail
        default             Analysis using all the required subcommands at their
                            default parameters                    
        create              Create analysis folders
        taxid               Download taxonomy ids from UniProt for the user
                            provided query species
        query               Map user provided comma separated queries to UniProt
                            ids
        keywords            Save user provided keywords for domain selection
                            (required) and analysis classification (-cl)
        select              Select functional domains of interest (specified by
                            keywords) from CDD (-C) and InterPro (-I) by default
        predict             Predict functional domains in the queries based on CDD
                            (-C) and InterPro (-I) databases by default
        filter              Filter queries predicted with domains of interest (and
                            optional parameter thresholds) and extend their
                            annotations
        classify            Optional classification of selected prediction in
                            smaller groups by class keywords
        annoscore           Score and rank predicted data by 'annotation scoring'
        summary             Summary analysis output
        addanno             Optional annotation of the selected protein by -PDB,
                            -PSORTB, -RAPTORX or -REFSS (see addanno -h)
        vis                 Visualize analysis results (see vis -h) for detail
        format              Optional output file format as html or excel

    optional arguments:
      -h, --help            show this help message and exit
      --version, -v         show version

subcommand ``default``
----------------------

Quick help: ``$ apricot default -h``

This subcommand calls the analysis pipeline of the software using the
default parameters. This subcommand by-default includes the subcommands
``create``, ``select``, ``predict``, ``filter``, ``classify``,
``annoscore``, ``summary`` and ``format``, which have been discussed
below in details. The two subcommands ``query (-i)`` and
``keywords (-kw)``, should be used by the users to provide the query
proteins (for example, UniProt ids) and functions of interest (for
example, a list of RNA-binding domains 'RRM,KH,RNP') respectively.

The basic syntax to call this subcommand is:

::

    $ apricot default -i {query proteins} -kw {functions of interest}

Several optional arguments associated with other subcommands have been included in ``default``.
Please check the usage for details:

::

    usage: apricot default [-h]
	
Here are a few useful flags, which can be used with this subcommand:

::

	--uids, -i		Comma separated UniProt IDs
	--kw_domain, -kw	Comma separated keywords for domain selection
	--classify, -cl		Optional comma separated keyword for result classification
	--cdd, -C		Uses only CDD
	--ipr, -I		Uses only InterPro
	--skip_select		Skips running the subcommand 'select'
	--needle_dir, -nd	path for the locally configured EMBOSS suite
	
	--taxid, -tx		Select taxonomy id for query species
	--geneids, -gi		Comma separated query genes
	--proteome, -P		Analyze entire proteome
	--fasta, -fa		Analyze fasta sequences
	--force, -F		force flag, removes existing files generated in the previous analysis
	
	--db_root, -dr		Uses to get absolute path of domain annoation files
	--similarity, -sim	Percent similarity of prediction with reference
	--coverage, -cov	Percent coverage of reference domain in prediction
	--identity, -iden	Percent identity of prediction with reference
	--evalue, -eval		Evalue of the domain prediction
	--gap, -gap		Percent gap in predicted domain
	--bit, -bit		Bit score in predicted domain
	
	--xlsx, -XL		create output files in excel file-format

subcommand ``create``
---------------------

Quick help: ``$ apricot create -h``

This subcommand creates all the required directories to store input and
output data acquired from APRICOT analysis. The main analysis folder can
be provided by the users (default name: APRICOT\_analysis).

::

    usage: apricot create [-h] analysis_path

    positional arguments:
      analysis_path  Creates APRICOT_analysis folder for anlysis unless other
                     name/path is provided

The structure and annotation of directories and the enclosing files in
the 'input' folder in the analysis directory:

::

    APRICOT_analysis
        └───├input
                └───├query_proteins
                └───├uniprot_reference_table
                └───├mapped_query_annotation  

The structure of directories and the enclosing files in the 'output'
folder in the analysis directory:

::

    APRICOT_analysis
        └───├output
                └───├0_predicted_domains            # Location for the output data obtained from the subcommand 'predict'
                └───├1_compiled_domain_information  # Location for the output data obtained from the subcommand 'filter'          
                └───├2_selected_domain_information  # Location for the classified data obtained from the subcommand 'classify' 
                └───├3_annotation_scoring           # Location for the output data obtained from the subcommand 'annoscore'
                └───├4_additional_annotations       # Location for additional annotations for the selected 
                |                                   # queries using subcommand 'addanno'
                └───├5_analysis_summary             # Location for the output data obtained from the subcommand 'summary'
                └───├format_output_data             # Location for the output data obtained from the subcommand 'format'
                └───├visualization_files            # Location for the output data obtained from the subcommand 'vis'

subcommand ``taxid``
--------------------

Quick help: ``$ apricot taxid -h``

The users can provide gene ids or protein names as queries to APRICOT,
which is mapped against UniProt Knowledgebase in order to extract
relevant information. Since, same gene/protein ids exist across various
genomes/proteomes, one can limit the search of the query to a certain
organism (rather than all the organisms in the database) by providing
one or multiple taxonomy ids.

When the taxonomy id is not known by the users, this subcommand --taxid
can be used to extract the id by providing species name.

::

    usage: apricot taxid [-h] [--species SPECIES] db_path

    positional arguments:
      db_path

    optional arguments:
      -h, --help            show this help message and exit
      --species SPECIES, -s SPECIES
                            Species name (comma separated if more than one) for
                            taxonomy id retreival

The taxonomy ids are saved in the text file taxonomy\_ids.txt in the
directory reference\_db\_files.

::

    source_files
        └───├reference_db_files
                |    taxonomy_ids.txt

subcommand ``query``
--------------------

Quick help: ``$ apricot query -h``

As mentioned already, APRICOT gives multiple options to the users to
supply queries. For example, the queries can be provided as UniProt ids
(--uids), gene ids or protein names (--geneids), fasta sequences
(--fasta) or only the taxonomy id (--taxid) for a complete proteome
analysis (using flag -P).

Paths for the saving the query data and their corresponding fasta files,
xml files, annotation tables etc. can be optinally provided by the
users.

::

    usage: apricot query [-h] [--analysis_path ANALYSIS_PATH] [--uids UIDS]
                         [--taxid TAXID] [--geneids GENEIDS] [--proteome]
                         [--fasta] [--query_path QUERY_PATH]
                         [--proteome_path PROTEOME_PATH] [--xml_path XML_PATH]
                         [--fasta_path FASTA_PATH] [--feature_table FEATURE_TABLE]

    optional arguments:
      -h, --help            show this help message and exit
      --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                            Main analysis path
      --uids UIDS, -ui UIDS
                            Comma separated UniProt IDs
      --taxid TAXID, -tx TAXID
                            Select taxonomy id for query species
      --geneids GENEIDS, -gi GENEIDS
                            Comma separated query genes
      --proteome, -P        Analyze entire proteome
      --fasta, -fa          Analyze fasta sequences
      --query_path QUERY_PATH, -qp QUERY_PATH
                            Get proteome table from UniProt
      --proteome_path PROTEOME_PATH, -pp PROTEOME_PATH
                            Get proteome table from UniProt
      --xml_path XML_PATH, -o XML_PATH
                            Get proteome table from UniProt
      --fasta_path FASTA_PATH, -fp FASTA_PATH
                            Get proteome table from UniProt
      --feature_table FEATURE_TABLE, -ft FEATURE_TABLE
                            Get proteome table from UniProt

APRICOT saves the user provided queries and related information
extracted from UniProt knowledgebase (fasta files, xml files, reference
files etc.) in the directories as described below.

::

    APRICOT_analysis
        └───├input
                └───├query_proteins
                |   query_to_uids.txt           # User provided queries (gene ids/protein names/whole proteome set) 
                |                               # mapped to the UniProt Ids (flag --uids, --geneids)
                └───├uniprot_reference_table
                |   query_uids_reference.tab    # Basic annotations of the query protein IDs (flag --uids, --geneids)  set
                |                               # or the whole proteome (flag -P) from a certain taxonomy (flag --taxid)
                └───├mapped_query_annotation  
                        └───├fasta_path_mapped_query  # Location for protein FASTA sequences of each query
                        |   |                         # qery fasta sequences are also saved here (flag --fasta)
                        |   | query_id-1.fasta 
                        |   | query_id-2.fasta
                        |   | ...
                        |   | query_id-n.fasta
                        |
                        └───├xml_path_mapped_query    # Location for protein FASTA sequences of each query
                        |   | query_id-1.xml
                        |   | query_id-2.xml
                        |   | ...
                        |   | query_id-n.xml
                        |
                        └───├mapped_protein_xml_info_tables  
                            | query_feature_table.csv  # File containing all the features of the queries 
                                                       # obtained by parsing xml files

subcommand ``keywords``
-----------------------

Quick help: ``$ apricot keywords -h``

Since APRICOT allows identification of certain protein classes like
RNA-binding proteins by means of domains, one of the most essential
input data, beside the query protein itself, is a comma-separated list
of terms or keywords that potentially indicates to a protein functional
classes (*domain selection terms*). Such terminologies could be any pfam
id, Gene Ontology term, mesh term, simple biological terms like 'RRM'
and 'ribosome', or a combination of all these types.

Multi-word terms can be provided by using ‘-’ as a connector, for
example, 'RNA-binding' and 'La-domain'.

In order to maintain stringent selection of truly functional domains,
APRICOT by-default does not allow the selection of a domain entry if the
*domain selection term* occurs in its annotation with any trailing words
like prefixes or suffixes. This indicates the possibilities of omitting
few relevant entries from the domain selection keywords, but it also
ensures exclusion of several non-relevant domains that might get
included by chance. However, users can allow prefix by using the hash
symbol (#) in the beginning of a term and suffix when # is used at the
end of the term. For example, by using '#RNA-binding' one can allow the
inclusion of 'tRNA-binding', 'mtRNA-binding'etc, and by allowing
'RNA-bind#' one can allow varying verb forms for bind like binder,
binding etc. Of course, one can allow both prefixes and suffixes
(#RNA-bind#).

Optionally a second set of keywords for the classification of predicted
domains can be provided by using flag -cl (*result classification
terms*). This list can comprise of terms associated to biological
functions, enzymatic activities or specific features. For example, the
predicted RNA related domain data could be divided into the
classification tags of RRM, ribosome, synthetase, helicases etc. Such
classification can help users tremendously in navigating the large
datasets or for the selection of representative protein for certain
function conferred by the domains. When users do not provide *result
classification terms*, APRICOT uses the *domain selection terms* for
this purpose as well.

::

    usage: apricot keywords [-h] [--classify CLASSIFY] [--kw_path KW_PATH]
                            kw_domain

    positional arguments:
      kw_domain             Comma separated keywords for domain selection

    optional arguments:
      -h, --help            show this help message and exit
      --classify CLASSIFY, -cl CLASSIFY
                            Optional comma separated keyword for result
                            classification
      --kw_path KW_PATH, -kp KW_PATH
                            Path for keyword files

The keywords are saved in the directory ``source_files`` in the
subfolder ``domain_data`` shown below.

::

    source_files
        └───├domain_data
                keywords_for_domain_selection.txt         # All the terms for domain selection
                keywords_for_result_classification.txt    # All the terms for result classification

subcommand ``select``
---------------------

Quick help: ``apricot select -h``

This subcommand allows the selection of reference domains based on the
*domain selection terms* (in subcommand keywords). For this purpose,
by-default APRICOT scans each entries of the domains in both CDD and
InterPro domain consortiums for the occurance of any *domain selection
term*.

In case of multi word terms (which are provided by using '-' as a
connector), the co-occurance of the terms are considered when the words
in the same sentence or same context. To ensure a more complete
selection of the domains, the gene-ontology associated to the domains
are also checked and selected accordingly.

It is possible to limit the selection process in only one of the
consortiums by providing flags -C for CDD or -I for InterPro. For cross
mapping the domains in both the consortiums, APRICOT uses domain ids
from the databases (Pfam, SMART and TIGRFAM) that are shared by both the
consortiums.

::

    usage: apricot select [-h] [--cdd_dom] [--ipr_dom] [--dom_kw DOM_KW]
                          [--cdd_table CDD_TABLE] [--ipr_table IPR_TABLE]
                          [--interpro_mapped_cdd INTERPRO_MAPPED_CDD]
                          [--domain_path DOMAIN_PATH]
                          [--pfam_domain_file PFAM_DOMAIN_FILE]

    optional arguments:
      -h, --help            show this help message and exit
      --cdd_dom, -C         Selects functional domains of interest from CDD
      --ipr_dom, -I         Selects functional domains of interest from CDD
      --dom_kw DOM_KW, -dk DOM_KW
                            Absolute path of keyword files
      --cdd_table CDD_TABLE, -cdd CDD_TABLE
                            Absolute path of CDD domain table
      --ipr_table IPR_TABLE, -ipr IPR_TABLE
                            Absolute path of InterPro domain table
      --interpro_mapped_cdd INTERPRO_MAPPED_CDD, -map INTERPRO_MAPPED_CDD
                            InterPro domains mapped to CDD domains.
      --domain_path DOMAIN_PATH, -dp DOMAIN_PATH
                            Absolute path for keyword selected domains
      --pfam_domain_file PFAM_DOMAIN_FILE, -pf PFAM_DOMAIN_FILE
                            The domain summary from PfamA

The domains that are selected from CDD and InterPro are stored in the
directory domains\_data in the bin folder. The selected domains are
compiled and saved into the file
all\_keyword\_selected\_domain\_data.tab in the domain\_data.

::

    bin
    │   ...
    └───├domain_data
        └───├cdd
        └───├interpro
        | all_keyword_selected_domain_data.tab

subcommand ``predict``
----------------------

Quick help: ``$ apricot predict -h``

This subcommand is used to begin the process of domain predictions in
the query proteins by all the possible functional domains using RPSBLAST
against CDD and InterProScan against InetrPro. APRICOT carries out the
domain prediction from both CDD and InterPro consortiums by default but
users can choose to predict domains from only one of the databases by
using the flag -C for CDD and -I for InterPro. To overwrite old
predictions, the flag -F (for force) can be used.

The run time of RPSBLAST is considerably less, therefore -C flag can be
used to obtain a quick information of the functional domains. However,
we recommend the default setting because the different databases
involved in both the consortiums provide a larger scope for completeness
of domain predictions.

The execution of this subcommand is the basic requirement for the
APRICOT analysis. The main input of this step is fasta sequences of
query proteins. This subcommand can be executed simultabeously or even
before running the subcommand 'select'.

::

    usage: apricot predict [-h] [--analysis_path ANALYSIS_PATH] [--cdd] [--ipr]
                           [--force] [--cdd_db CDD_DB] [--ipr_db IPR_DB]
                           [--outpath OUTPATH] [--fasta FASTA]

    optional arguments:
      -h, --help            show this help message and exit
      --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                            Provide output path for the analysis result of the
                            chosen method
      --cdd, -C             domain prediction based on CDD only
      --ipr, -I             domain prediction based on InterProScan only
      --force, -F           force flag for the current analysis, removes already
                            existing predictions
      --cdd_db CDD_DB, -cdb CDD_DB
                            Provide absolute path of CDD databases based on the
                            chosen method
      --ipr_db IPR_DB, -idb IPR_DB
                            Provide absolute path of InterPro databases based on
                            the chosen method
      --outpath OUTPATH, -o OUTPATH
                            Provide output path for domain prediction files
      --fasta FASTA, -f FASTA
                            Provide absolute path of fasta files for query
                            proteins

The resulting files of this analysis is stored in the first analysis
directory '0\_predicted\_domains' in the output folder of the main
analysis directory. As shown below, the information of the domain
predictions are stored as text files in the sub-folders corresponding to
the domain consortiums. Since this subcommand is independent of the
reference domains, these files containing information on domain
predictions can be recycled or re-visited for the selection of different
functional classes.

::

    APRICOT_analysis
        └───├output
                └───├0_predicted_domains # Location for the output data obtained from the subcommand 'predict'
                        └───├cdd_analysis  # Details of domain predicted from CDD for each query
                        |   | query_id-1.txt
                        |   | query_id-2.txt
                        |   | ...
                        |   | query_id-n.txt
                        |
                        └───├ipr_analysis  # Details of domain predicted from InterPro for each query
                            | query_id-1.tsv
                            | query_id-2.tsv
                            | ...
                            | query_id-n.tsv

subcommand ``filter``
---------------------

Quick help: ``$ apricot filter -h``

The filtering of the predicted domains by this subcommand take place by
using the *domain selection terms*, hence this subcommand should be
executed after 'select' and 'predict' subcommands.

Query proteins that consist of at least one of the selected domains are
retained whereas the rest of the proteins are discarded from the
downstream analysis. To limit the analysis to one of the consortiums
only, flag -C for CDD based information and -I for InterPro based
information can be used.

The users can choose their cut-offs for the parameters by using the
flags --similarity, --coverage, --identity, --evalue, --bit (bit score)
and --gap. However, the default parameters for the selection of
predicted domains are defined as 'coverage > 39' and 'similarity > 24',
which have been derived from a large RNA-binding positive and negative
training sets collected from SwissProt database.

::

    usage: apricot filter [-h] [--analysis_path ANALYSIS_PATH] [--cdd] [--ipr]
                          [--domain_description_file DOMAIN_DESCRIPTION_FILE]
                          [--similarity SIMILARITY] [--coverage COVERAGE]
                          [--identity IDENTITY] [--evalue EVALUE] [--gap GAP]
                          [--bit BIT] [--go_path GO_PATH] [--pred_path PRED_PATH]
                          [--up_table UP_TABLE] [--xml_info XML_INFO]
                          [--compile_out COMPILE_OUT] [--selected SELECTED]

    optional arguments:
      -h, --help            show this help message and exit
      --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                            Provide analysis path
      --cdd, -C             Filter of domain prediction based on CDD only
      --ipr, -I             Filter of domain prediction based on InterProScan only
      --domain_description_file DOMAIN_DESCRIPTION_FILE, -d DOMAIN_DESCRIPTION_FILE
                            Description table of the selected domains
      --similarity SIMILARITY, -sim SIMILARITY
                            Percent similarity of prediction with reference
      --coverage COVERAGE, -cov COVERAGE
                            Percent coverage of reference domain in prediction
      --identity IDENTITY, -iden IDENTITY
                            Percent identity of prediction with reference
      --evalue EVALUE, -eval EVALUE
                            Evalue of the domain prediction
      --gap GAP, -gap GAP   Percent gap in predicted domain
      --bit BIT, -bit BIT   Bit score in predicted domain
      --go_path GO_PATH, -gp GO_PATH
                            Go mapping data from fixed database reference files
      --pred_path PRED_PATH, -pp PRED_PATH
                            Raw files of domain prediction
      --up_table UP_TABLE, -ref UP_TABLE
                            Uniprot proteome table from UniProt
      --xml_info XML_INFO, -feat XML_INFO
                            Uniprot proteome table from UniProt
      --compile_out COMPILE_OUT, -co COMPILE_OUT
                            Data with annotation after filtering
      --selected SELECTED, -sel SELECTED
                            output path for the selected data with annotations

APRICOT saves all the domain data in the directory
'1\_compiled\_domain\_information' of the output folder. All the
predicted domains (independent of reference domains and parameter
cut-offs) are saved in the sub-folder 'unfiltered\_data' and the
selected data is saved in the sub-folder 'selected\_data' in separate
files for different domain resources as shown below.

Files in the sub-folder 'selected\_data' contain predicted domain entry
based on the reference domain sets and are marked with the tags
*ParameterSelected* when the domain predictions satisfy the defined
parameter cut-offs (or default cut-offs) or *Parameter Discarded* when
it does not pass the parameter filters. In those cases, when certain
parameter is not available for the predicted domain, a tag
*ParameterNotApplicable* is used.

::

    APRICOT_analysis
        └───├output
            └───├1_compiled_domain_information  # Location for the output data obtained from the subcommand 'filter'          
                        └───├unfiltered_data  # Information of all the domains in the query proteins predicted.
                        |   | cdd_unfiltered_all_prediction.csv  # CDD 
                        |   | ipr_unfiltered_all_prediction.csv  # InterPro
                        |
                        └───├selected_data      # Information of the selected reference domains in the query proteins
                            | cdd_filtered.csv                   # CDD 
                            | ipr_filtered.csv                   # InterPro 

Queries, that are selected on the basis of reference domains and
parameter cut-offs, are compiled and stored in the directory
'2\_selected\_domain\_information' in the sub-folder 'combined\_data'.
These files contain the information of selected domains along with the
additional annotations of the query proteins extracted from various
resources like UniProt and Gene Ontology .

::

    APRICOT_analysis
        └───├output    
                └───├2_selected_domain_information            
                        └───├combined_data         # All the selected domain data extended 
                            |                       # with the UniProt annotation
                            | annotation_extended_for_selected.csv

Sub-commands for downstream analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

subcommand ``classify``
-----------------------

Quick help: ``$ apricot classify -h``

This subcommand classifies the resulting domain information of the
selected queries by using the *result classification terms* (provided in
the subcommand 'keywords').

::

    usage: apricot classify [-h] [--analysis_path ANALYSIS_PATH]
                            [--selected SELECTED] [--class_kw CLASS_KW]
                            [--outpath OUTPATH]

    optional arguments:
      -h, --help            show this help message and exit
      --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                            Provide analysis path
      --selected SELECTED, -sel SELECTED
                            Selected data file (from select) with annotations
      --class_kw CLASS_KW, -ck CLASS_KW
                            Path for keyword files
      --outpath OUTPATH, -o OUTPATH
                            Classification of selected data based on provided
                            keywords

The classified data are stored in the folder as shown below:

::

    APRICOT_analysis
        └───├output    
                └───├2_selected_domain_information            
                        └───├classified_data                            # Location for the output data obtained 
                            |                                           # from the subcommand 'classify'
                            | classification_key-1_selected_data.csv    # Files containing subsets of predicted data...
                            | classification_key-2_selected_data.csv    # ... based on user provided classification keys.

subcommand ``annoscore``
------------------------

This subcommand is executed for the annotation based scoring of the
selcted domains in the query proteins.

In order to differentiate domain predictions of low confidence from that
of high confidence, the predicted domain sites are compared with their
corresponding references and scored by means of methods that measure
their similarities by means of various sequence-based features. The
comparisons of the features between the predicted domain sites and
reference are scored based on the principle of Bayesian probability,
where a score closer to 1 represents a favourable scenario.

There are four groups of features that are involved in the annotation
based scoring. 1. Chemical properties 2. Needleman-Wunsch global
alignment scores 3. Euclidean distances of protein compositions 4.
Prediction parameters of the predicted sites

Quick help: ``$ apricot annoscore -h``

::

    usage: apricot annoscore [-h] [--analysis_path ANALYSIS_PATH]
                             [--selected SELECTED] [--cdd_pred CDD_PRED]
                             [--outpath OUTPATH]

    optional arguments:
      -h, --help            show this help message and exit
      --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                            Provide analysis path
      --selected SELECTED, -sel SELECTED
                            Provided selected protein table
      --cdd_pred CDD_PRED, -cp CDD_PRED
                            Raw files obtained from CDD based domain prediction
      --outpath OUTPATH, -o OUTPATH
                            Output path for annotation scoring files

The data with annotation scores are stored in the folder as shown below:

::

    APRICOT_analysis
        └───├output
                └───├3_annotation_scoring          # Location for the output data obtained 
                    |                              # from the subcommand 'annoscore'
                    | annotation_extended_for_selected.csv

subcommand ``addanno``
----------------------

Quick help: ``$ apricot addanno -h``

This subcommand allows users to further annotate the query sequences
that are selected based on the defined functional domains.

Following modules can be used with their respective flags for additional
annotations of the selected proteins:

1. Identification sub-cellular localization of the proteins (flag
   -psortb)
2. Secondary structure calculation by RaptorX (flag -raptorx)
3. Tertiary structure homologs from Protein Data Bank (flag -pdb)
4. Gene Ontology (flag -go)

::

    usage: apricot addanno [-h] [--force] [--pdb] [--psortb] [--raptorx] [--refss]
                           [--analysis_path ANALYSIS_PATH] [--fasta FASTA]
                           [--selected SELECTED] [--outpath OUTPATH]
                           [--pdb_path PDB_PATH] [--psortb_path PSORTB_PATH]
                           [--raptorx_path RAPTORX_PATH]

    optional arguments:
      -h, --help            show this help message and exit
      --force, -F           force flag for the current analysis, removes already
                            existing predictions
      --pdb, -PDB           Optional annotation of the selected protein by PDB
                            structure homolog
      --psortb, -PSORTB     Optional annotation of the selected protein by
                            localization using PsortB
      --raptorx, -RAPTORX   Optional annotation of the selected protein by
                            secondary structure using RaptorX
      --refss, -REFSS       Optional annotation of the selected protein by
                            secondary structure using literature reference
      --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                            Provide analysis path
      --fasta FASTA, -fa FASTA
                            Provide absolute path of fasta files for query
                            proteins
      --selected SELECTED, -sel SELECTED
                            Provided selected protein table
      --outpath OUTPATH, -o OUTPATH
                            Output path for additional annotation data
      --pdb_path PDB_PATH, -pdb_path PDB_PATH
                            Provide absolute path of APRICOT formatted pdb
                            database ~pdb/pdb_sequence/pdb_sequence.txt
      --psortb_path PSORTB_PATH, -psortb_path PSORTB_PATH
                            Provide absolute path of APRICOT installed psortb
      --raptorx_path RAPTORX_PATH, -raptorx_path RAPTORX_PATH
                            Provide absolute path of APRICOT installed raptorx
                            till the perl script run_raptorx-ss8.pl

The resulting files are stored in the directory
4\_additional\_annotations in the corresponding sub-folders, as shown
below:

::

    APRICOT_analysis
        └───├output
                └───├4_additional_annotations               # Location for additional annotations for the 
                        |                                   # selected queries using subcommand 'addanno'
                        └───├pdb_sequence_prediction        # PDB structure homologs of the selected 
                        |                                   # queries (flag --pdb, -PDB)
                        └───├protein_localization           # PSORTb based localization of the selected 
                        |                                   # queries (flag --psortb, -PSORTB)
                        └───├protein_secondary_structure    # RaptorX based structure of the selected 
                                                            # queries (flag --raptorx, -RAPTORX)

subcommand ``summary``
----------------------

Quick help: ``$ apricot summary -h``

To get an overview of the analysis carried out on a set of query
proteins, this sub command can be used. It generate information like,
how many queries could be mapped to the UniProt IDs, how many contain
the reference domains etc., to provide analysis overview.

::

    usage: apricot summary [-h] [--analysis_path ANALYSIS_PATH]
                           [--query_map QUERY_MAP] [--domains DOMAINS]
                           [--unfilter_path UNFILTER_PATH] [--outpath OUTPATH]

    optional arguments:
      -h, --help            show this help message and exit
      --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                            Provide analysis path
      --query_map QUERY_MAP, -q QUERY_MAP
                            query_to_uids.txt file created by APRICOT to save
                            query mapping information
      --domains DOMAINS, -d DOMAINS
                            File containing all the keyword selected_domains of
                            interest
      --unfilter_path UNFILTER_PATH, -uf UNFILTER_PATH
                            Directory with the unfiltered domain data from
                            output-1 (unfiltered_data)
      --outpath OUTPATH, -o OUTPATH
                            Provide output path

The resulting files are stored in the directory 5\_analysis\_summary in
the corresponding sub-folders, as shown below:

::

    APRICOT_analysis
        └───├output
                └───├5_analysis_summary # Location for the output data obtained from the subcommand 'summary'
                    | APRICOT_analysis_summary.csv

subcommand ``format``
---------------------

Quick help: ``$ apricot format -h``

Formats and stores various tables in the HTML tabels (--html), excel
files (--xlsx) or both.

::

    usage: apricot format [-h] [--analysis_path ANALYSIS_PATH] [--inpath INPATH]
                          [--html] [--xlsx] [--outpath OUTPATH]

    optional arguments:
      -h, --help            show this help message and exit
      --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                            Provide analysis path
      --inpath INPATH, -i INPATH
                            Choose folder from analysis to be converted
      --html, -HT
      --xlsx, -XL
      --outpath OUTPATH, -o OUTPATH
                            Output path for files with different file formats

The resulting files are stored in the directory format\_output\_data in
the corresponding sub-folders, as shown below:

::

    APRICOT_analysis
        └───├output
                └───├format_output_data # Location for the output data obtained from the subcommand 'format'
                        └───├excel_files               # excel files (flag -XL)
                        └───├html_files                # HTML files (flag -HT)

subcommand ``vis``
------------------

Quick help: ``$ apricot vis -h``

Visualize different resulting data like predicted domains sites,
tertiary structure of selected proteins etc.

::

    usage: apricot vis [-h] [--analysis_path ANALYSIS_PATH]
                       [--ann_score ANN_SCORE] [--add_anno ADD_ANNO] [--domain]
                       [--annoscore] [--secstr] [--localiz] [--msa] [--complete]
                       [--outpath OUTPATH]

    optional arguments:
      -h, --help            show this help message and exit
      --analysis_path ANALYSIS_PATH, -ap ANALYSIS_PATH
                            Provide analysis path
      --ann_score ANN_SCORE, -an ANN_SCORE
                            Provide annotation score file
      --add_anno ADD_ANNO, -ad ADD_ANNO
                            Provide path to additional annotation
      --domain, -D          Visualizes predicted domains on the query by
                            highlighting
      --annoscore, -A       Visualizes overview of prediction statistics
      --secstr, -S          Visualizes secondary structures predicted by RaptorX
      --localiz, -L         Visualizes subcellular localization predcited by
                            PsortB
      --msa, -M             Visualizes Multiple Sequence Alignments of homologous
                            sequences from PDB
      --complete, -C        Visualizes all the possible features
      --outpath OUTPATH, -o OUTPATH
                            Output path for visualization files

The resulting files are stored in the directory visualization\_files in
the corresponding sub-folders, as shown below:

::

    APRICOT_analysis
        └───├output
                └───├visualization_files # Location for the output data obtained from the subcommand 'vis'
                        └───├domain_highlighting      # Visualizing the domain sites on the protein sequences
                        └───├homologous_pdb_msa       # Multiple sequence alignment of the structure homologs
                        └───├overview_and_statistics  # Visualizing the overview of the selected query proteins
                        └───├secondary_structure      # Visualizing 3-state secondary struvture of the query sequence
                        └───├subcellular_localization # Heatmap showing the probability of different localization sites 

.. |Latest Version| image:: https://img.shields.io/pypi/v/bio-apricot.svg
   :target: https://pypi.python.org/pypi/bio-apricot/
.. |License| image:: https://img.shields.io/pypi/l/bio-apricot.svg
   :target: https://pypi.python.org/pypi/bio-apricot/
.. |DOI| image:: https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg
   :target: https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT
.. |image3| image:: https://images.microbadger.com/badges/image/malvikasharan/apricot.svg
   :target: https://microbadger.com/images/malvikasharan/apricot
.. |image4| image:: https://raw.githubusercontent.com/malvikasharan/APRICOT/master/APRICOT_logo.png
   :target: http://malvikasharan.github.io/APRICOT/
