#!/usr/bin/env python
# Description = Download UniProt based proteome data for a taxonomy id

import sys
try:
    from urllib.request import urlopen
except ImportError:
    print('Python package urllib is missing. Please install/update.\n')
    sys.exit(0)


def format_uniprot_table(proteome_table, uniprot_link):
    '''Downloads protein information
    table from UniProt database for
    the selected taxonomy id'''
    try:
        response = urlopen(uniprot_link)
        for entry in str(response.read()).split('\\n'):
            if not entry == "'" and not entry == '"':
                if not entry.startswith(
                        "b'Entry") and not entry.startswith('b"Entry'):
                    proteome_table.write("%s\n" % '\t'.join(
                        list(entry.split('\\t'))))
        print('"\nDownloaded protein information using UniProt link: %s\n"' % (
            uniprot_link))
    except:
        print(
            "UniProt entry is apparently deleted, please check: %s"
            % uniprot_link)
