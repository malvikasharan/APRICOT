import os
import sys

def select_taxids(db_path, species):
    '''Selects taxonomy ids for the query species'''
    if not str(species) == 'None':
        parse_uniprot_tax_file(species, db_path)
    else:
        parse_uniprot_tax_file('N=', db_path)
    
def parse_uniprot_tax_file(species, db_path):
    '''Parses the taxonomy id file from UniProt for all the species'''
    with open('bin/selected_taxonomy_ids.txt', 'w') as out_fh:
        out_fh.write("Official (scientific) name\tTaxonomy ID\n")
        with open(db_path+'/all_taxids/speclist.txt', 'r') as in_fh:
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
    db_path = sys.argv[1]
    species = sys.argv[2]
    setup_analysis_folders(db_path, species)
