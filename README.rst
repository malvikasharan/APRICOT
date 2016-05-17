APRICOT
-------

`APRICOT`_ is a computational pipeline for the identification of
specific functional classes of interest in large protein sets. The
pipeline uses efficient sequence-based algorithms and predictive models
like signature motifs of protein families for the characterization of
user-provided query proteins with specific functional features. The
dynamic framework of APRICOT allows the identification of unexplored
functional classes of interest in the large protein sets or the entire
proteome.

Summary of the pipeline
~~~~~~~~~~~~~~~~~~~~~~~

The functionality of APRICOT can be explained in 3 parts: program input,
analysis modules and program output.

Program inputs
''''''''''''''

1) Query proteins that are subjected to characterization by domains and
   associated functional properties

2) Set of terms indicating protein domains of functional relevance.

Based on these inputs, APRICOT can be executed for the analysis of the
proteins of interest using the analysis modules as explained later.

Analysis modules of APRICOT
'''''''''''''''''''''''''''

The functionalities involved in the primary analysis are retrieval of
sequences and known annotations of query proteins, collection of domains
of interest from domain databases, and identification of all the
functional domains in a given query.

The data obtained from the primary analysis is used as a resource for
the secondary analysis, which mainly involves the selection of proteins
based on the predicted domains, the calculation of the statistical and
biological significance of the selected proteins to possess the function
of interest by means of sequence-based features, and biological
characterization of these proteins by additional annotations like
subcellular localization and secondary structures.

Program output
''''''''''''''

For each analysis step, APRICOT generates results in tablular manner, in
addition with an overview of the analysis and graphics associated with
the resulting information.

Trivia
''''''

The initial focus of this project was to identify functional domains in
bacterial proteins that have the potential to interact with RNA
(RNA-binding proteins or RBPs) and understand their regulatory roles and
mechanisms. Hence, the tool is named **APRICOT** that stands for
**A**\ nalysing **P**\ rotein **R**\ NA **I**\ nteractions by
**Co**\ mbined-scoring **T**\ echnique. However, due to the adaptability
of the pipeline to different sets of reference domains, APRICOT is not
limited to RBP identification and has been tested successfully on the
other classes of functional domains as well. We are carrying out the
experimental validations of few RBPs identified by APRICOT in
collaboration with the biologists in our lab, which can provide a high
confidence dataset and contribute significantly to the improvement of
this computational approach.

Documentation and source code
-----------------------------

The documentation and source codes of APRICOT are available at
https://github.com/malvikasharan/APRICOT.

License
-------

APRICOT is open source software and available under the ISC license.

Copyright (c) 2011-2015, Malvika Sharan, malvika.sharan@uni-wuerzburg.de

Please read the license content `here`_.

.. _APRICOT: http://malvikasharan.github.io/APRICOT/
.. _here: https://github.com/malvikasharan/APRICOT/blob/master/LICENSE.md