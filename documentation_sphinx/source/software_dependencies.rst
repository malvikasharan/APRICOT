|Latest Version| |License| |DOI| |image3|

|image4|

Resources requirements of APRICOT
---------------------------------

-  Basic Linux programs
   (`pip <https://pip.pypa.io/en/stable/installing/>`__ or
   `apt-get <https://wiki.ubuntuusers.de/apt/apt-get/>`__,
   `git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`__,
   `Python 3 <https://www.python.org/downloads/>`__)
-  Python dependencies:
   `numpy <http://docs.scipy.org/doc/numpy/user/install.html>`__,
   `scipy <https://www.scipy.org/install.html>`__,
   `matplotlib <http://matplotlib.org/users/installing.html>`__,
   `openpyxl <https://pypi.python.org/pypi/openpyxl>`__,
   `requests <http://docs.python-requests.org/en/master/user/install/>`__,
   `biopython <http://biopython.org/DIST/docs/install/Installation.html>`__
-  APRICOT software from PyPI:
   `bio-apricot <https://pypi.python.org/pypi/bio-apricot>`__
-  Latest CDD database:
   ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little\_endian/
-  Latest InterPro databases and InterProScan:
   ftp://ftp.ebi.ac.uk/pub/databases/interpro
-  InterProScan requires `pfsearch
   wrapper <http://web.expasy.org/pftools/#Downloads>`__ and `Java
   8 <https://wiki.ubuntuusers.de/Java/Installation/Oracle_Java/Java_8/>`__
   or above
-  BLAST executables (from:
   ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
   (psiblast, rpsblast, blastp, makeblastdb)
-  `Gene Ontology
   (go.obo) <http://geneontology.org/page/download-ontology>`__
-  PDB files: `proteins sequence and
   secondary-structure <http://www.rcsb.org/pdb/files/ss.txt>`__ and
   `PDB to InterPro mapping <http://www.uniprot.org/docs/pdbtosp.txt>`__
-  `Taxonomy data <http://www.uniprot.org/docs/speclist.txt>`__
-  `needle <http://emboss.sourceforge.net/download/>`__ from EMBOSS
   software
-  `Psortb <https://github.com/brinkmanlab/psortb-docker>`__ for
   localization prediction (only for the subcomand addanno)
-  `RaptorX <https://github.com/Indicator/RaptorX-SS8.git>`__ for
   secondary structure presiction (only for the subcomand addanno)

Click `here <.././database_dependencies/index.html>`__, to see the explanation of the database requirement and their structure.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please see the instructions for working with the `Docker
image <.././docker/index.html>`__.

In case, users do not wish to run Docker image, the complete file system
with the tool and dataset can be installed using the shell script
`APRICOT/shell\_scripts/apricot\_minimum\_required\_files.sh <https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/apricot_minimum_required_files.sh>`__.
Please see the instructions for `local
installation <.././local_installation/index.html>`__.

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
