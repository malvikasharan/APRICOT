import sys
import urllib.request
from urllib.request import urlopen

def format_uniprot_table(proteome_table, uniprot_link):
    '''Downloads protein information
    table from UniProt database for
    the selected taxonomy id'''
    response = urlopen(uniprot_link)
    for entry in str(response.read()).split('\\n'):
        if not entry == "'" and not entry == '"':
            if not entry.startswith("b'Entry") and not entry.startswith('b"Entry'):
                proteome_table.write("%s\n" % '\t'.join(list(entry.split('\\t'))))
    print('"\nDownloaded protein information using UniProt link: %s\n"' % (
        uniprot_link))
    
if __name__ == '__main__':
    proteome_table = sys.argv[1]
    uniprot_query = sys.argv[2]
    if "http://www.uniprot.org/" in uniprot_link:
        format_uniprot_table(proteome_table, uniprot_query)
    else:
        try:
            format_uniprot_table(proteome_table, uniprot_query)
        except KeyError:
            print("Please provide query UniProt ids or a taxonomy id for UniProt table retrieval.")