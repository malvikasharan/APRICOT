#!/usr/bin/env python 

import argparse
import re

__description__ = "Classify all the filtered predicted data."
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    '''all commandline arguement dclaration'''
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("selected_protein_table")
    parser.add_argument("keyword_file")
    parser.add_argument("classified_result_path")
    args = parser.parse_args()

    protein_classifier = ProteinClassifier(
        args.selected_protein_table,
        args.keyword_file,
        args.classified_result_path)
    protein_classifier.parse_protein_table()
    protein_classifier.parse_keyword_file()
    protein_classifier.classify_data_by_keywords()
    protein_classifier.create_classified_files()
    protein_classifier.create_unclassified_files()


class ProteinClassifier(object):
    '''classification of data'''
    def __init__(self, selected_protein_table,
                 keyword_file,
                 classified_result_path):
        self._selected_protein_table = selected_protein_table
        self._keyword_file = keyword_file
        self._classified_result_path = classified_result_path
        self._protein_data_set = set()
        self._keyword_set = set()
        self._keyword_candidate_data = {}
        self._file_header = ''
        self._classified_data = set()
        self._unclassified_data = set()
        
    def streamline_protein_classification(self):
        self.parse_protein_table()
        self.parse_keyword_file()
        self.classify_data_by_keywords()
        self.create_classified_files()
        self.create_unclassified_files()
            
    def parse_protein_table(self):
        '''Parses Uniprot reference table'''
        with open(self._selected_protein_table, 'r') as in_fh:
            for entry in in_fh:
                if entry.startswith('Entry') or entry.startswith('UniprotID'):
                    self._file_header = entry
                else:
                    self._protein_data_set.add(entry)
        return self._protein_data_set, self._file_header
    
    def parse_keyword_file(self):
        '''Parse user derived keyoerds for clssififction'''
        with open(self._keyword_file, 'r') as in_fh:
            for entry in in_fh:
                self._keyword_set.add(entry.strip())
        return self._keyword_set
    
    def classify_data_by_keywords(self):
        '''create classified data'''
        for entry in self._protein_data_set:
            if len(entry.split('\t')) > 23:
                protein_name = entry.split('\t')[2]
                protein_go = entry.split('\t')[8]
                short_name = entry.split('\t')[18]
                full_name = entry.split('\t')[19]
                keyword_col = entry.split('\t')[20]
                domain_go = entry.split('\t')[21]
                for keyword in self._keyword_set:
                    self._keyword_selection(keyword, entry, protein_name)
                    self._keyword_selection(keyword, entry, protein_go)
                    self._keyword_selection(keyword, entry, short_name)
                    self._keyword_selection(keyword, entry, full_name)
                    self._keyword_selection(keyword, entry, keyword_col)
                    self._keyword_selection(keyword, entry, domain_go)
            else:
                # ShortName       FullName        DomainKeyword   DomainGo
                short_name = entry.split('\t')[3]
                full_name = entry.split('\t')[4]
                keyword_col = entry.split('\t')[5]
                domain_go = entry.split('\t')[6]
                for keyword in self._keyword_set:
                    self._keyword_selection(keyword, entry, short_name)
                    self._keyword_selection(keyword, entry, full_name)
                    self._keyword_selection(keyword, entry, keyword_col)
                    self._keyword_selection(keyword, entry, domain_go)
                
        return self._keyword_candidate_data
    
    def create_classified_files(self):
        '''Creates individual doamin file foreach keyword selection'''
        for keyword in self._keyword_candidate_data.keys():
            with open(self._classified_result_path+'/%s_selected_data.csv' %
                      keyword, 'w') as out_fh:
                out_fh.write(self._file_header)
                if len(self._keyword_candidate_data[keyword]) > 1:
                    for entry in self._keyword_candidate_data[keyword]:
                        out_fh.write(entry)
                        self._classified_data.add(entry)
                else:
                    out_fh.write(list(
                        self._keyword_candidate_data[keyword])[0])
                    self._classified_data.add(
                        list(self._keyword_candidate_data[keyword])[0])
        return self._classified_data
    
    def create_unclassified_files(self):
        '''Combines all the files in common'''
        for entry in self._protein_data_set:
            if entry not in self._classified_data:
                self._unclassified_data.add(entry.strip())
        if len(list(self._unclassified_data)) > 1:
            with open(
                self._classified_result_path+'/unclassified_selected_data.csv',
                    'w') as out_fh:
                out_fh.write(self._file_header)
                out_fh.write('\n'.join(list(self._unclassified_data)))
    
    def _keyword_selection(self, keyword, entry, info):
        domain_full_name = list(entry.lower().split(' '))
        check_keyword = keyword.lower()
        if '-' in check_keyword:
            ref_kw_list = check_keyword.split('-')
            new_kw_list = []
            for domain_name in domain_full_name:
                for string in ref_kw_list:
                    if string == 'rna':
                        if re.findall(r"(?:\s|^)%s(?=\s|$)" %
                                      '*rna', domain_name):
                            if string not in set(new_kw_list):
                                new_kw_list.append(string)
                    else:
                        if re.findall(r"(?:\s|^)%s(?=\s|$)" %
                                      string, domain_name):
                            if string not in set(new_kw_list):
                                new_kw_list.append(string)
            if str(ref_kw_list) == str(new_kw_list):
                self._keyword_candidate_data.setdefault(
                    keyword, set()).add(entry)
        else:
            for domain_name in domain_full_name:
                if re.findall(r"(?:\s|^)%s(?=\s|$)" %
                              check_keyword, domain_name):
                    self._keyword_candidate_data.setdefault(
                        keyword, set()).add(entry)
        
if __name__ == "__main__":
    main()
