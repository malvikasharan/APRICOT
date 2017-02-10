#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='bio-APRICOT',
      version='1.2.6',
      description=('Sequence-based identification and characterization '
                   'of protein classes'),
      author='Malvika Sharan',
      author_email='malvikasharan@gmail.com',
      url='https://www.python.org/pypi/bio-apricot',
      packages=['apricotlib', 'bin'],
      install_requires=[
        "biopython >= 1.66",
        "requests >= 2.10.0",
        "openpyxl >= 2.3.1",
        "numpy >= 1.9.0",
        "scipy >= 0.16.0",
        "matplotlib >= 1.5.1"
      ],
      scripts=['bin/apricot'],
      license='ISC License (ISCL)',
      classifiers=[
          'License :: OSI Approved :: ISC License (ISCL)',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
      ])
