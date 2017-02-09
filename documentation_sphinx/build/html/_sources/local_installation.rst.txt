|Latest Version| |License| |DOI| |image3|

|image4|

Installing APRICOT via ``pip`` from PyPI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

APRICOT is implemented in Python as a standalone and is executable on
Ubuntu (and other debian-based) systems.

Please make sure that your system has pip and git installed

::

    $ apt-get install python3-pip git 

Then install APRICOT via pip (NOTE: this doesn't install the required
tools and datasets):

::

    $ pip3 install bio-apricot 

This will globally install APRICOT, which can be called via the command
``apricot``, and the libraries from apricotlib will be saved.

Install APRICOT via GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^^

APRICOT is implemented in Python3 and can be executed in Linux/Unix
systems. APRICOT requires few third party packages, namely
`Biopython <http://biopython.org/wiki/Main_Page>`__, `BLAST
executables <https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download>`__,
`interproscan <https://www.ebi.ac.uk/interpro/interproscan.html>`__,
python libraries like `Matplotlib <http://matplotlib.org/>`__,
`requests <https://pypi.python.org/pypi/requests>`__, openpyxl and few
other optional tools that are mentioned below.

::

    $ apt-get install python3-matplotlib python3-numpy python3-scipy python3-biopython python3-requests --yes --fix-missing
    $ pip3 install openpyxl

The git-repository for APRICOT can be `downloaded
manually <https://github.com/malvikasharan/APRICOT/archive/master.zip>`__
or locally cloned:

::

    $ git clone https://github.com/malvikasharan/APRICOT.git

Please see the detailed documentation for the alternative installation
instructions of the software using
`Docker <https://github.com/malvikasharan/APRICOT/blob/master/Dockerfile>`__
or `shell
script <https://github.com/malvikasharan/APRICOT/blob/master/tests/system_test.sh>`__
provided in the repository.

Third party requirements for the software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An additional step for the installation of the third party tools and the
databases, which are required to carry out analysis by the software.

The shell script:
`APRICOT/shell\_scripts/apricot\_minimum\_required\_files.sh <https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/apricot_minimum_required_files.sh>`__,
can be installed locally that could be used for multiple analysis.

::

    $ wget -N https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/apricot_minimum_required_files.sh
    $ sh apricot_minimum_required_files.sh

This script will install all the required tools and will create a
directory ``source_files`` with all the required datasets as dicussed
`here <.././software_dependencies/index.html>`__.

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
