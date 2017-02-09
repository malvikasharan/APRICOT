|Latest Version| |License| |DOI| |image3|

|image4|

Frequently asked questions
--------------------------

**1) I installed APRICOT using pip and I am trying to test the software
using the script run\_example.sh. Why does it shows me error messages
about the missing files?**

-  APRICOT contains the library and scripts to run the analysis, however
   it requires additionally databases and tools to run the analysis.
   Although you do not need to install these resources to run an example
   (for testing purpose), you still need a set of data to mimic these
   data sources. You can get these example datasets in the `git
   repository <https://github.com/malvikasharan/APRICOT/tree/master/tests/demo_files_small>`__
   or download it from
   `Zenodo <https://zenodo.org/record/51705/files/APRICOT-1.0-demo_files-MS.zip>`__.

-  The path for these files can be defined in the script run\_example.sh
   using the variable ``$DEMO_FILES``.

**2) I installed APRICOT using pip and I am trying to test the software
using the script run\_example.sh. Why can't I run the subcommand
``annoscore`` and ``addanno``?**

-  The subcommand ``annoscore`` requires the tool ``needle`` from the
   EMBOSS pakage and ``addanno`` uses Psortb and RaptorX. Hence, in
   order to run these subcommands of APRICOT a complete file-system
   (tool and database dependencies of the software) is required, which
   is supplied through APRICOT's Docker image. Alternatively see the
   script
   `apricot\_minimum\_required\_files.sh <https://github.com/malvikasharan/APRICOT/blob/master/shell_scripts/apricot_minimum_required_files.sh>`__
   for manual installation.

-  Please check the documentation or this `video
   tutorial <./video_tutorial.html>`__
   for the usage of these subcommand.

-  The complete list of software requirements can be seen
   `here <./software_dependencies.html>`__,
   alternatively see the Dockerfile.

**3) What are the options to give query proteins for the analysis?**

-  The query proteins can be provided as UniProt ids (-ui), gene
   ids/name (-gi), fasta files (-fa), taxonomy id to restrict the search
   of query to a specific species (-tx) and flag -P for a complete
   proteome analysis of the given taxonomy.

**4) What are the rules for the input for domain selection terms?**

-  There is no specific rule for the selection of these terms in order
   to provide to the software for the collection of domains of interest.
   The choices of the term ranges from biological or MeSH terms (for
   example, term "RNA-bind" to select all the domains that mentions this
   term in its annotation) to specific domain class name or Pfam domain
   id/name (for example, "RRM" or "RNA-recognition-motif").

-  Terms containing multiple keywords can be provided using a hyphen (-)
   and "#" can be used before or after the term as a wild-card. Please
   see the documentation for other specific detail.

Do you have any specific question? Please submit it here, we will address it as soon as possible.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. |Latest Version| image:: https://img.shields.io/pypi/v/bio-apricot.svg
   :target: https://pypi.python.org/pypi/bio-apricot/
.. |License| image:: https://img.shields.io/pypi/l/bio-apricot.svg
   :target: https://pypi.python.org/pypi/bio-apricot/
.. |DOI| image:: https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg
   :target: https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT
.. |image3| image:: https://images.microbadger.com/badges/version/malvikasharan/apricot.svg
   :target: https://microbadger.com/images/malvikasharan/apricot
.. |image4| image:: https://raw.githubusercontent.com/malvikasharan/APRICOT/master/APRICOT_logo.png
   :target: http://malvikasharan.github.io/APRICOT/

