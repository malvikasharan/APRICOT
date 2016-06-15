.. image:: https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg
   :target: https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT
  
APRICOT
-------

A tool for sequence-based identification and characterization of protein classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`APRICOT`_ is a computational pipeline for the identification of
specific functional classes of interest in large protein sets. The
pipeline uses efficient sequence-based algorithms and predictive models
like signature motifs of protein families for the characterization of
user-provided query proteins with specific functional features. The
dynamic framework of APRICOT allows the identification of unexplored
functional classes of interest in the large protein sets or the entire
proteome.

Authors and Contributors
~~~~~~~~~~~~~~~~~~~~~~~~

The tool is designed and developed by Malvika Sharan in
the lab of Prof. Dr. Jörg Vogel and Dr. Ana Eulalio in the Institute for
Molecular Infection Biology at the University of Würzburg. Dr. Konrad
Förstner contributed to the project by providing important
technical supervision and discussions. The authors are grateful to
Prof. Thomas dandekar, Dr. Charlotte Michaux, Caroline Taouk and
Dr. Lars Barquist for critical discussions and feedback.

Source code
~~~~~~~~~~~

The source codes of APRICOT are available via git
https://github.com/malvikasharan/APRICOT and pypi
https://pypi.python.org/pypi/bio-apricot.

License
-------

APRICOT is open source software and is available under the ISC license.

Copyright (c) 2011-2015, Malvika Sharan, malvika.sharan@uni-wuerzburg.de

Please read the license content `here`_.

Installation
------------

Python packages required for APRICOT can be installed with pip

::

    $ pip install bio-apricot
    

Or update the package list manually: sudo apt-get update and install the required packages (sudo apt-get install python3-matplotlib python3-numpy python3-scipy python3-biopython python3-requests python3-openpyxl).

The scripts for the installaton of the different componenents of APRICOT
(databases, tools and flatfiles) are available on the GitHub repository.
You can manually download the APRICOT repository or simply clone it.

::

    $ git clone https://github.com/malvikasharan/APRICOT.git

The `Docker image for APRICOT`_ will be available soon.

The shell script to install and run the analysis in a streamlined manner
is provided with the package (`see here`_).

Working example
---------------

We recomend you to check out the `tutorial`_ that discusses each module
of APRICOT in detail. The repository contains a shell script
`run\_example.sh`_, which can be used for the demonstration of APRICOT
analysis with an example.

Contact
-------

For question, troubleshooting and requests, please feel free to contact
Malvika Sharan at malvika.sharan@uni-wuerzburg.de

.. _APRICOT: http://malvikasharan.github.io/APRICOT/
.. _here: https://github.com/malvikasharan/APRICOT/blob/master/LICENSE.md
.. _Docker image for APRICOT: https://github.com/malvikasharan/APRICOT/blob/master/Dockerfile
.. _see here: https://github.com/malvikasharan/APRICOT/blob/master/system_test.sh
.. _tutorial: https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_tutorial.md
.. _run\_example.sh: https://github.com/malvikasharan/APRICOT/blob/master/shell_scripts/run_example.sh
.. _tests: https://github.com/malvikasharan/APRICOT/tree/master/tests
.. _system\_test.sh: https://github.com/malvikasharan/APRICOT/blob/master/tests/system_test.sh
.. _test datasets: https://github.com/malvikasharan/APRICOT/tree/master/tests/demo_files_small
