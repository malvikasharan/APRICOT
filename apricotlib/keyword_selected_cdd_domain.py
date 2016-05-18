#!/usr/bin/env python 

'''selects rna related domains from cdd database.'''

import sys
import argparse
import re

__description__ = ""
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"
__version__ = ""


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("keywords_file")
    parser.add_argument("cdd_whole_data_file")
    parser.add_argument("interpro_mapped_cdd")
    parser.add_argument("domain_data_path")
    args = parser.parse_args()

    keyword_selected_cdd_selection = RnaRelatedCDDSelection(
        args.keywords_file, args.cdd_whole_data_file,
        args.interpro_mapped_cdd, args.domain_data_path)
    keyword_selected_cdd_selection.read_keyword_file()
    keyword_selected_cdd_selection.read_interpro_mapped_cdd_file()
    keyword_selected_cdd_selection.read_cdd_whole_data_file()
    keyword_selected_cdd_selection.create_keyword_selected_domain_file()


class RnaRelatedCDDSelection(object):
    def __init__(self, keywords_file,
                 cdd_whole_data_file,
                 interpro_mapped_cdd,
                 domain_data_path):
        self._keywords_file = keywords_file
        self._cdd_whole_data_file = cdd_whole_data_file
        self._interpro_mapped_cdd = interpro_mapped_cdd
        self._domain_data_path = domain_data_path
        
        self.cdd_whole_data_list = []
        self._cdd_dict = {}
        self._mapped_cdd_members = {}
    
    def select_cdd_domains(self):
        '''To call from apriot'''
        self.read_keyword_file()
        self.read_interpro_mapped_cdd_file()
        self.read_cdd_whole_data_file()
        self.create_keyword_selected_domain_file()
        
    def read_keyword_file(self):
        '''reads user provided keywords for domain selection'''
        self._keyword_list = [rna_keyword.strip()
                              for rna_keyword in open(
                                self._keywords_file, 'r')]
        return self._keyword_list
    
    def read_interpro_mapped_cdd_file(self):
        '''Parses cdd interpro mapped file for
        the extraction of common information'''
        with open(self._interpro_mapped_cdd, 'r') as in_fh:
            for entry in in_fh:
                ipr_id = entry.strip().split('\t')[0]
                ipr_members = entry.strip().split('\t')[1]
                cdd_id = entry.strip().split('\t')[2]
                cdd_member = entry.strip().split('\t')[3]
                domain_length = entry.strip().split('\t')[4]
                self._mapped_cdd_members[cdd_member] = ipr_members
        self._mapped_cdd_members
    
    def read_cdd_whole_data_file(self):
        '''Parses CDD annotation data from table'''
        with open(self._cdd_whole_data_file, 'r') as cdd_data_fh:
            for cdd_entry in cdd_data_fh:
                if 'smart' in cdd_entry.split('\t')[1]:
                    cdd_entry = cdd_entry.replace(
                        cdd_entry.split('\t')[1], 'SM'+cdd_entry.split(
                            '\t')[1].split('smart')[-1])
                elif 'pfam' in cdd_entry.split('\t')[1]:
                    cdd_entry = cdd_entry.replace(
                        cdd_entry.split('\t')[1], 'PF'+cdd_entry.split(
                            '\t')[1].split('pfam')[-1])
                cdd_domain = cdd_entry.split('\t')[1]
                if cdd_domain in self._mapped_cdd_members.keys():
                    members = self._mapped_cdd_members[cdd_domain]
                else:
                    members = 'NA'
                self.cdd_whole_data_list.append(
                    cdd_entry.strip())
                self._cdd_dict[cdd_entry.strip()] = " ".join(cdd_entry.strip(
                    ).split('\t')[2:4])
        return self.cdd_whole_data_list, self._cdd_dict
    
    def create_keyword_selected_domain_file(self):
        '''Creates a file with CDD derived domain of interest'''
        self._keyword_annotation_dict = {}
        self._keyword_selected_domain = {}
        for cdd_entry in self.cdd_whole_data_list:
            domain_full_name = list(self._cdd_dict[
                cdd_entry].lower().replace('-', ' ').replace('_', ' ').split(' '))
            for keyword in self._keyword_list:
                check_keyword = keyword.lower()
                #if 'rna' in check_keyword:
                if '-' in check_keyword:
                    ref_kw_list = check_keyword.split('-')
                    new_kw_list = []
                    for domain_name in domain_full_name:
                        for string in ref_kw_list:
                            if string == 'rna':
                                if re.findall(
                                        r"(?:\s|^)%s(?=\s|$)" % '*rna', domain_name):
                                    if not string in set(new_kw_list):
                                        new_kw_list.append(string)
                            else:
                                if re.findall(
                                        r"(?:\s|^)%s(?=\s|$)" % string, domain_name):
                                    if not string in set(new_kw_list):
                                        new_kw_list.append(string)
                    if str(ref_kw_list) == str(new_kw_list):
                        self._keyword_annotation_dict.setdefault(
                            keyword, []).append(cdd_entry)
                else:
                    for domain_name in domain_full_name:
                        if re.findall(
                                r"(?:\s|^)%s(?=\s|$)" % check_keyword, domain_name):
                            self._keyword_annotation_dict.setdefault(
                                keyword, []).append(cdd_entry)
        for fkeyword in self._keyword_list:
            fkeyword = fkeyword.replace(' ', '_')
            with open(self._domain_data_path + '/' + fkeyword +
                      '_related_cdd_ids.tab',
                      'w') as keyword_specific_domain:
                if self._keyword_annotation_dict.get(fkeyword):
                    for each_entry in self._keyword_annotation_dict[fkeyword]:
                        each_entry = each_entry.replace(
                            each_entry.split('\t')[3], " ".join(
                                each_entry.split(
                                    '\t')[3].split())).replace(';', ',')
                        cdd_domain = each_entry.split('\t')[1]
                        if cdd_domain in set(self._mapped_cdd_members.keys()):
                            members = self._mapped_cdd_members[cdd_domain]
                        else:
                            members = 'NA'
                        self._keyword_selected_domain.setdefault(
                            '%s\t%s\t%s' % (
                                '\t'.join(each_entry.split('\t')[0:-1]),
                                members,
                                each_entry.split(
                                    '\t')[-1]), set()).add(fkeyword)
                        keyword_specific_domain.write('%s\t%s\t%s\t%s\n' % (
                            '\t'.join(each_entry.split('\t')[0:-1]), members,
                            each_entry.split('\t')[-1], fkeyword))
        with open(self._domain_data_path+'/all_keyword_selected_cdd_data.tab',
                  'w') as keyword_selected_domain_file:
            for domain_entry in self._keyword_selected_domain.keys():
                keywords = ', '.join(list(
                    self._keyword_selected_domain[domain_entry]))
                keyword_selected_domain_file.write(
                    '%s\t%s\n' % (domain_entry, keywords))

if __name__ == "__main__":
    sys.exit(main())

