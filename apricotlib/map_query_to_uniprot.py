#!/usr/bin/env python

import os
import argparse
import csv
import re
from itertools import islice

__description__ = "Collect protein ids from UniProt database for the query genes"
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("query_path")
    parser.add_argument("uniprot_reference_file")
    parser.add_argument("mapped_data_path")
    parser.add_argument("statistics_path")
    args = parser.parse_args()

    collect_uniprot_information = CollectUniprotInformation(
                                            args.query_path,
                                            args.uniprot_reference_file,
                                            args.mapped_data_path,
                                            args.statistics_path)
    collect_uniprot_information.read_protein_file()
    collect_uniprot_information.parse_uniprot_reference_file()
    collect_uniprot_information.map_proteins_to_uniprot()
    collect_uniprot_information.create_mapped_file()


class CollectUniprotInformation(object):
    '''collection of protein ids for the query genes'''
    def __init__(self, query_path,
                 uniprot_reference_file,
                 mapped_data_path,
                 statistics_path):
        self._query_path = query_path
        self._uniprot_reference_file = uniprot_reference_file
        self._mapped_data_path = mapped_data_path
        self._statistics_path = statistics_path
        
        self._query_protein_set = set()
        self._protein_data_dict = {}
        self._gene_to_protein_dict = {}
        self._protein_protein_available = set()
        
    def read_protein_file(self):
        '''read protein files and collect proteins in a list'''
        for query_file in os.listdir(self._query_path):
            with open(self._query_path+'/'+query_file,
                      'r') as query_protein_fh:
                for each_query in query_protein_fh:
                    if not each_query.strip() == '':
                        self._query_protein_set.add(
                            each_query.strip())
        return self._query_protein_set

    def parse_uniprot_reference_file(self):
        '''parse uniprot reference table for posible protein proteins'''
        with open(self._uniprot_reference_file,
                  'r') as uniprot_reference_fh:
            for protein_entry in csv.reader(
                islice(uniprot_reference_fh, 1,
                       None), delimiter='\t'):
                self._protein_data_dict[protein_entry[0]] = (
                    protein_entry[4], protein_entry[3], protein_entry[1])
        return self._protein_data_dict

    def map_proteins_to_uniprot(self):
        '''Maps query gene ids to the UniProt entry'''
        for each_query in list(self._query_protein_set):
            print(each_query)
            print('Retrieving protein for: %s' % each_query)
            self._gene_to_protein_dict.setdefault(
                each_query, []).append(each_query)
            for protein, description in self._protein_data_dict.items():
                exact_protein_match = re.findall('\\b%s\\b' % each_query.lower(
                    ), str(','.join(description).lower()))
                if len(exact_protein_match) > 0:
                    self._protein_protein_available.add(each_query)
                    self._gene_to_protein_dict.setdefault(each_query,
                                                          []).append(protein)
                    print(protein)
        return self._gene_to_protein_dict, self._protein_protein_available
    
    def create_mapped_file(self):
        '''Creates a file with mapping informtion of the
        query genes to UniProt protein ids'''
        with open(self._mapped_data_path,
                  'w') as gene_to_protein:
            with open(self._statistics_path,
                      'w') as statistics_file:
                for mapped_protein_data in self._gene_to_protein_dict:
                    gene_to_protein.write('%s\n' % ';'.join(
                        self._gene_to_protein_dict.get(mapped_protein_data)))
                statistics_file.write(
                    'Total number of proteins: %s\n' % len(
                        list(self._query_protein_set)))
                statistics_file.write(
                    'Total number of available protein proteins: %s\n' % len(
                        list(self._protein_protein_available)))
                uniq_not_available_data = (
                    self._query_protein_set-self._protein_protein_available)
                statistics_file.write(
                    'Total number of unavailable protein proteins: %s\n' %
                    len(uniq_not_available_data))
                statistics_file.write('\nAvailable protein proteins:\n')
                for available in list(self._protein_protein_available):
                    statistics_file.write('%s\n' % available)
                statistics_file.write('\nUnavailable protein proteins: \n')
                for unavailable in uniq_not_available_data:
                    statistics_file.write('%s\n' % unavailable)
                print('Proteins sequences are generated for '
                      'truly mapped genes.')
                statistics_file.close()
                print('Proteins are mapped to the available proteins.')

if __name__ == '__main__':
    main()
