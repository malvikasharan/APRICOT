
[![Latest Version](https://img.shields.io/pypi/v/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![License](https://img.shields.io/pypi/l/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![DOI](https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg)](https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT)

![alt tag](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_logo.png)

##Frequently asked questions

1) I installed APRICOT using pip and I am trying to test the software using the script run_example.sh. Why does it shows me error messages about the missing files?

- APRICOT software contains the library and scripts to run the analysis, however it requires databases and tools to run the analysis. Although you do not need to install these resources to run an example (for testing purpose), but you still need a set of data to mimic these data sources. You can get these example datasets in the [gitHub repository](https://github.com/malvikasharan/APRICOT/tree/master/tests/demo_files_small) or download it from [Zenodo](https://zenodo.org/record/51705/files/APRICOT-1.0-demo_files-MS.zip). 

- The path for these files can be defined in the script run_example.sh using the variable `$DEMO_FILES`.

2) I installed APRICOT using pip and I am trying to test the software using the script run_example.sh. Why can't I run the subcommand `annoscore` and `addanno`?

- The subcommand `annoscore` requires the tool `needle` from the EMBOSS pakage and `addanno` used Psortb and RaptorX. Hence, to run these subcommands of APRICOT a complete file-system (tool and database dependencies of the software) is required that is available in APRICOT's Docker image. Alternatively see the script [apricot_minimum_required_files.sh](https://github.com/malvikasharan/APRICOT/blob/master/shell_scripts/apricot_minimum_required_files.sh) for manual installation.

- Please check the documentation or this [video tutorial](https://www.youtube.com/watch?v=V7uT1kgEYjI&index=9&list=PLVJHJxaTACqPD0Y1Ty6Qvi5SfaeWDfrMo) for the usage of these subcommand.

3) What are the options to give query proteins for the analysis?

- The query proteins can be provided as UniProt ids (-ui), gene ids/name (-gi), fasta files (-fa), taxonomy id to restrict the search of query to a specific species (-tx) and flag -P for a  complete proteome analysis of the given taxonomy.

4) What are the rules for the input for domain selection terms?

- There is no specific rule for the selection of these terms in order to provide to the software for the collection of domain of interes. The choices of the term varies from biological or MeSH terms (for example, term "RNA-bind" to select all the domains that mentions this term in its annotation) or specific domain class name or Pfam domain id/name (for example, "RRM" or "RNA-recognition-motif"). Terms containing multiple keywords can be provided using a hyphen (-) and "#" can be used before or after the term as a wild-card.  Please see the documentation for other specific detail.

Do you have a specific question? Please submit it here, we will address it as soon as possible.
