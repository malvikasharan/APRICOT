#!/usr/bin/env python 

import argparse
import re

__description__ = "Identifies keyword selected domains from InterPro database."
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("keywords_file")
    parser.add_argument("ipr_whole_data_file")
    parser.add_argument("interpro_mapped_cdd")
    parser.add_argument("domain_data_path")
    args = parser.parse_args()

    keyword_selected_ipr_selection = RnaRelatedIPRSelection(
        args.keywords_file, args.ipr_whole_data_file,
        args.interpro_mapped_cdd, args.domain_data_path)
    keyword_selected_ipr_selection.read_keyword_file()
    keyword_selected_ipr_selection.read_interpro_mapped_cdd_file()
    keyword_selected_ipr_selection.read_ipr_whole_data_file()
    keyword_selected_ipr_selection.create_keyword_selected_domain_file()


class RnaRelatedIPRSelection(object):
    def __init__(self, keywords_file,
                 ipr_whole_data_file,
                 interpro_mapped_cdd,
                 domain_data_path):
        self._keywords_file = keywords_file
        self._ipr_whole_data_file = ipr_whole_data_file
        self._interpro_mapped_cdd = interpro_mapped_cdd
        self._domain_data_path = domain_data_path
        
        self.ipr_whole_data_list = []
        self._ipr_dict = {}
        self._mapped_interpro_length = {}
    
    def select_ipr_domains(self):
        '''To call from apricot'''
        self.read_keyword_file()
        self.read_interpro_mapped_cdd_file()
        self.read_ipr_whole_data_file()
        self.create_keyword_selected_domain_file()
        
    def read_keyword_file(self):
        '''reads user provided keywords for domain selection'''
        self._keyword_list = [
            rna_keyword.strip() for rna_keyword in open(
                self._keywords_file)]
        return self._keyword_list
    
    def read_interpro_mapped_cdd_file(self):
        '''Parses cdd interpro mapped file for
        the extraction of common information'''
        with open(self._interpro_mapped_cdd, 'r') as in_fh:
            for entry in in_fh:
                ipr_id = entry.split('\t')[0]
                ipr_members = entry.split('\t')[1]
                cdd_id = entry.split('\t')[2]
                cdd_member = entry.split('\t')[3]
                domain_length = entry.split('\t')[4].strip()
                self._mapped_interpro_length[cdd_member] = domain_length
        self._mapped_interpro_length
        
    def read_ipr_whole_data_file(self):
        '''Parses InterPro annotation data from table'''
        with open(self._ipr_whole_data_file, 'r') as in_fh:
            for ipr_id_entry in in_fh:
                self.ipr_whole_data_list.append(ipr_id_entry.strip())
                self._ipr_dict[ipr_id_entry.strip()] = ipr_id_entry.strip(
                    ).split('\t')[2]
        return self.ipr_whole_data_list, self._ipr_dict
        
    def create_keyword_selected_domain_file(self):
        '''Creates a file with InterPro derived domain of interest'''
        self._keyword_annotation_dict = {}
        self._keyword_selected_domain = {}
        for ipr_entry in self.ipr_whole_data_list:
            domain_full_name = list(self._ipr_dict[
                ipr_entry].lower().replace('-', ' ').replace(
                    '_', ' ').split(' '))
            for keyword in self._keyword_list:
                check_keyword = keyword.lower()
                if '-' in check_keyword:
                    ref_kw_list = check_keyword.split('-')
                    new_kw_list = []
                    for domain_name in domain_full_name:
                        for string in ref_kw_list:
                            if string == 'rna':
                                if re.findall(
                                        r"(?:\s|^)%s(?=\s|$)" % '*rna',
                                        domain_name):
                                    if not string in set(new_kw_list):
                                        new_kw_list.append(string)
                            else:
                                if re.findall(
                                        r"(?:\s|^)%s(?=\s|$)" % string,
                                        domain_name):
                                    if not string in set(new_kw_list):
                                        new_kw_list.append(string)
                    if str(ref_kw_list) == str(new_kw_list):
                        self._keyword_annotation_dict.setdefault(
                            keyword, []).append(ipr_entry)
                else:
                    for domain_name in domain_full_name:
                        if re.findall(
                                r"(?:\s|^)%s(?=\s|$)" % check_keyword,
                                domain_name):
                            self._keyword_annotation_dict.setdefault(
                                keyword, []).append(ipr_entry)
        for fkeyword in self._keyword_list:
            fkeyword = fkeyword.replace(' ', '_')
            with open(self._domain_data_path+'/'+fkeyword+'_related_ipr_ids.tab',
                      'w') as key_fh:
                if self._keyword_annotation_dict.get(fkeyword):
                    for each_entry in self._keyword_annotation_dict[fkeyword]:
                        each_entry = each_entry.replace(each_entry.split(
                            '\t')[3], " ".join(each_entry.split('\t')[3].split(
                            ))).replace(';', ',')
                        cdd_id = each_entry.split('\t')[1]
                        if cdd_id in set(self._mapped_interpro_length.keys()):
                            length = self._mapped_interpro_length[cdd_id]
                        else:
                            length = 'NA'
                        self._keyword_selected_domain.setdefault("%s\t%s" % (
                            each_entry, length), set()).add(fkeyword)
                        key_fh.write("%s\t%s\t%s\n" % (
                            each_entry, length, fkeyword))
        with open(self._domain_data_path+'/all_keyword_selected_ipr_data.tab',
                  'w') as keyword_selected_domain_file:
            for domain_entry in self._keyword_selected_domain.keys():
                keywords = ', '.join(list(
                    self._keyword_selected_domain[domain_entry]))
                keyword_selected_domain_file.write('%s\t%s\n' % (
                    domain_entry, keywords))

if __name__ == "__main__":

    main()
