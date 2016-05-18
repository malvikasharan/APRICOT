#!/usr/bin/env python 

import argparse
import os

__description__ = "Annotates selected queries with proteins and domain information"
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("filtered_data_path")
    parser.add_argument("uniprot_reference_table")
    parser.add_argument("xml_feature_table")
    parser.add_argument("selected_data_table")
    args = parser.parse_args()

    selected_protein_table = SelectedProteinTable(
        args.filtered_data_path, args.uniprot_reference_table,
        args.xml_feature_table, args.selected_data_table)
    selected_protein_table.parse_filtered_data()
    selected_protein_table.parse_uniprot_reference()
    selected_protein_table.read_xml_protein_table()
    selected_protein_table.create_selected_data_table()


class SelectedProteinTable(object):
    def __init__(self, filtered_data_path,
                 uniprot_reference_table,
                 xml_feature_table,
                 selected_data_table):
        self._filtered_data_path = filtered_data_path
        self._uniprot_reference_table = uniprot_reference_table
        self._xml_feature_table = xml_feature_table
        self._selected_data_table = selected_data_table
        self._filter_data_header = ''
        self._reference_data_header = ''
        self._feature_data_header = ''
        self._filter_data_dict = {}
        self._up_ref_dict = {}
        self._protein_feature_dict = {}
        
    def streamline_selected_protein_table(self):
        '''To call from apricot exe'''
        self.parse_filtered_data()
        self.parse_uniprot_reference()
        self.read_xml_protein_table()
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
        
    def parse_uniprot_reference(self):
        '''Parse UniProt reference table'''
        for files in os.listdir(self._uniprot_reference_table):
            if '_reference' in files:
                with open(self._uniprot_reference_table+'/'+files,
                          'r') as in_fh:
                    for entry in in_fh:
                        if entry.startswith('Entry'):
                            self._reference_data_header = entry.strip()
                        else:
                            uid = entry.split('\t')[0]
                            if uid in set(
                                    self._filter_data_dict.keys()):
                                self._up_ref_dict[uid] = entry.strip()
        return self._reference_data_header, self._up_ref_dict
    
    def read_xml_protein_table(self):
        '''Read and record data from xml'''
        with open(self._xml_feature_table
                  ) as protein_xml_table_fh:
            for entry in protein_xml_table_fh:
                if entry.startswith('Entry'):
                    self._feature_data_header = entry.strip()
                else:
                    uid = entry.split('\t')[0]
                    if uid in set(
                            self._filter_data_dict.keys()):
                        self._protein_feature_dict[uid] = entry.strip()
        return self._feature_data_header, self._protein_feature_dict

    def create_selected_data_table(self):
        '''Creates selected data table'''
        with open(self._selected_data_table, 'w') as out_fh:
            filter_header = FilteredData(
                self._filter_data_header.split('\t'))
            reference_header = UniProtReference(
                self._reference_data_header.split('\t'))
            feature_header = ProteinFeature(
                self._feature_data_header.split('\t'))
            self._entries_into_the_file(
                out_fh, reference_header, feature_header, filter_header)
            for uid in self._filter_data_dict.keys():
                reference_data = UniProtReference(
                    self._up_ref_dict[uid].split('\t'))
                feature_data = ProteinFeature(
                    self._protein_feature_dict[uid].split('\t'))
                if len(self._filter_data_dict[uid]) > 1:
                    for entry in self._filter_data_dict[uid]:
                        filter_data = FilteredData(entry.split('\t'))
                        if filter_data.parameter == 'ParameterSelected':
                            self._entries_into_the_file(
                                out_fh, reference_data, feature_data,
                                filter_data)
                else:
                    filter_data = FilteredData(
                        list(self._filter_data_dict[uid])[0].split('\t'))
                    if filter_data.parameter == 'ParameterSelected':
                        self._entries_into_the_file(
                            out_fh, reference_data, feature_data, filter_data)
                    
    def _entries_into_the_file(self, out_fh,
                               reference_data, feature_data, filter_data):
        '''Creates an output with the protein features'''
        out_fh.write("\t".join([
            reference_data.uid,
            reference_data.entry_name, reference_data.protein_name,
            reference_data.species, reference_data.length,
            reference_data.gene_name, feature_data.gene_locus,
            feature_data.type, feature_data.go,
            feature_data.embl, feature_data.pdb, feature_data.kegg,
            feature_data.interpro, feature_data.pfam,
            feature_data.pubmed, filter_data.resource,
            filter_data.resource_id, filter_data.domain_id,
            filter_data.short_name, filter_data.full_name,
            filter_data.keyword, filter_data.domain_go, filter_data.members,
            filter_data.domain_length, filter_data.start,
            filter_data.stop, '\t'.join(filter_data.stats)])+'\n')


class ProteinFeature(object):
    def __init__(self, row):
        self.uid = row[0]
        self.protein_name = row[1]
        self.gene = row[2]
        self.gene_locus = row[3]
        self.species = row[4]
        self.pubmed = row[5]
        self.embl = row[6]
        self.refseq = row[7]
        self.kegg = row[8]
        self.pdb = row[9]
        self.go = row[10]
        self.interpro = row[11]
        self.pfam = row[12]
        self.type = row[13]


class UniProtReference(object):
    def __init__(self, row):
        self.uid = row[0]
        self.entry_name = row[1]
        self.status = row[2]
        self.protein_name = row[3]
        self.gene_name = row[4]
        self.species = row[5]
        self.length = row[6]
        try:
            self.gene_ontology = row[7]
        except:
            self.gene_ontology = '-'


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
