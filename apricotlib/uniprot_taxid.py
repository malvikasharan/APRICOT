#!/usr/bin/env python 

import os
import sys

__description__ = "Parses the taxonomy id file from UniProt for all the species."
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"

def select_taxids(species, reference_taxonomy_file, selected_taxonomy_file):
    '''Selects taxonomy ids for the query species'''
    if not str(species) == 'None':
        parse_uniprot_tax_file(species, reference_taxonomy_file, selected_taxonomy_file)
    else:
        parse_uniprot_tax_file('N=', reference_taxonomy_file, selected_taxonomy_file)
    
def parse_uniprot_tax_file(species, reference_taxonomy_file, selected_taxonomy_file):
    '''Parses the taxonomy id file from UniProt for all the species'''
    with open(selected_taxonomy_file, 'w') as out_fh:
        out_fh.write("Official (scientific) name\tTaxonomy ID\n")
        with open(reference_taxonomy_file, 'r') as in_fh:
            for entry in in_fh:
                if 'N=' in entry:
                    if ',' in species:
                        for each_species in species.split(','):
                            if each_species.lower() in entry.lower():
                                tax_id = entry.split(':')[0].split(' ')[-1]
                                species_name = entry.strip().split('=')[1]
                                out_fh.write("%s\t%s\n" % (species_name, tax_id))
                    else:
                        if species.lower() in entry.lower():
                            tax_id = entry.split(':')[0].split(' ')[-1]
                            species_name = entry.strip().split('=')[1]
                            out_fh.write("%s\t%s\n" % (species_name, tax_id))
  
if __name__ == '__main__':
    species = sys.argv[1]
    reference_taxonomy_file = sys.argv[2]
    selected_taxonomy_file = sys.argv[3]
    setup_analysis_folders(species, reference_taxonomy_file, selected_taxonomy_file)
