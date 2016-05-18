#!/usr/bin/env python 

import argparse
import os

__description__ = "Annotates selected queries with proteins and domain information"
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("filtered_data_path")
    parser.add_argument("selected_data_table")
    args = parser.parse_args()

    selected_protein_table_without_uniprot = SelectedProteinTableWithoutUniprot(
        args.filtered_data_path, args.selected_data_table)
    selected_protein_table_without_uniprot.parse_filtered_data()
    selected_protein_table_without_uniprot.create_selected_data_table()


class SelectedProteinTableWithoutUniprot(object):
    def __init__(self, filtered_data_path,
                 selected_data_table):
        self._filtered_data_path = filtered_data_path
        self._selected_data_table = selected_data_table
        self._filter_data_header = ''
        self._reference_data_header = ''
        self._feature_data_header = ''
        self._filter_data_dict = {}
        self._up_ref_dict = {}
        self._protein_feature_dict = {}
        
    def streamline_selected_protein_table_without_uniprot(self):
        '''To call from apricot exe'''
        self.parse_filtered_data()
        self.create_selected_data_table()
        
    def parse_filtered_data(self):
        '''Parse filtered information'''
        for files in os.listdir(self._filtered_data_path):
            if 'id' not in files:
                with open(self._filtered_data_path+'/'+files,
                          'r') as in_fh:
                    for entry in in_fh:
                        if entry.startswith('Resource'):
                            self._filter_data_header = entry.strip()
                        else:
                            uid = entry.split('\t')[1]
                            self._filter_data_dict.setdefault(
                                uid, set()).add(entry.strip())
        return self._filter_data_header, self._filter_data_dict
    
    def create_selected_data_table(self):
        '''Creates selected data table'''
        with open(self._selected_data_table, 'w') as out_fh:
            filter_header = FilteredData(
                self._filter_data_header.split('\t'))
            self._entries_into_the_file(out_fh, filter_header)
            for uid in self._filter_data_dict.keys():
                if len(self._filter_data_dict[uid]) > 1:
                    for entry in self._filter_data_dict[uid]:
                        filter_data = FilteredData(entry.split('\t'))
                        if filter_data.parameter == 'ParameterSelected':
                            self._entries_into_the_file(out_fh, filter_data)
                else:
                    filter_data = FilteredData(
                        list(self._filter_data_dict[uid])[0].split('\t'))
                    if filter_data.parameter == 'ParameterSelected':
                        self._entries_into_the_file(out_fh, filter_data)
                    
    def _entries_into_the_file(self, out_fh, filter_data):
        '''Creates an output with the protein features'''
        out_fh.write("\t".join([
            filter_data.uid,
            filter_data.resource_id, filter_data.domain_id,
            filter_data.short_name, filter_data.full_name,
            filter_data.keyword, filter_data.domain_go, filter_data.members,
            filter_data.domain_length, filter_data.start,
            filter_data.stop, '\t'.join(filter_data.stats)])+'\n')


class FilteredData(object):
    def __init__(self, row):
        self.resource = row[0]
        self.uid = row[1]
        self.resource_id = row[2]
        self.domain_id = row[3]
        self.short_name = row[4]
        self.full_name = row[5]
        self.keyword = row[6]
        self.domain_go = row[7]
        self.members = row[8]
        self.domain_length = row[9]
        self.start = row[10]
        self.stop = row[11]
        self.stats = row[12:]
        self.parameter = row[-1]

if __name__ == "__main__":
    main()
