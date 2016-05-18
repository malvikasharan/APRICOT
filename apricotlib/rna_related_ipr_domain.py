#!/usr/bin/env python 

import sys
import os
import argparse
import re

__description__ = "Selects RNA related domains from InterPro database."
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    '''all commandline arguement dclaration'''
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("keywords_file")
    parser.add_argument("ipr_whole_data_file")
    parser.add_argument("interpro_mapped_cdd")
    parser.add_argument("domain_data_path")
    args = parser.parse_args()

    rna_related_ipr_selection = RnaRelatedIPRSelection(
        args.keywords_file, args.ipr_whole_data_file,
        args.interpro_mapped_cdd, args.domain_data_path)
    rna_related_ipr_selection.read_keyword_file()
    rna_related_ipr_selection.read_interpro_mapped_cdd_file()
    rna_related_ipr_selection.read_ipr_whole_data_file()
    rna_related_ipr_selection.create_rna_related_domain_file()
    
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
        self.create_rna_related_domain_file()
        
    def read_keyword_file(self):
        '''reads keywords for domain selection'''
        self.keyword_list = [rna_keyword.strip()
                             for rna_keyword in open(
                                self._keywords_file)]
        return self.keyword_list
    
    def read_interpro_mapped_cdd_file(self):
        '''Parses interpro cdd mapped file to extract common information'''
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
        
    def create_rna_related_domain_file(self):
        '''Creates RNA related domain list'''
        self._keyword_annotation_dict = {}
        self._rna_related_domain = []
        for ipr_entry in self.ipr_whole_data_list:
            #print('--%s-------'%ipr_entry)
            for keyword in self.keyword_list:
                if ' ' in keyword:
                    key_list = []
                    for each_key in keyword.split(' '):
                        key_list.append(each_key)
                    match = re.search(r'\b%s*|\W%s\b'%(key_list[0].lower(),
                                                       key_list[1].lower()),
                                      self._ipr_dict[ipr_entry])
                    if match:
                        self._keyword_annotation_dict.setdefault(
                            keyword, []).append(ipr_entry)
                else:
                    match = re.search(r'\b%s\b'%keyword, self._ipr_dict[ipr_entry])
                    if match:
                        self._keyword_annotation_dict.setdefault(
                            keyword, []).append(ipr_entry)
        for fkeyword in self.keyword_list:
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
                        self._rna_related_domain.append("%s\t%s" % (each_entry, length))
                        key_fh.write("%s\t%s\n" % (each_entry, length))
        uniq_rna_related_domains = list(set(self._rna_related_domain))
        with open(self._domain_data_path+'/all_rna_related_ipr_data.tab',
                  'w') as rna_related_domain_file:
            for domain_entry in uniq_rna_related_domains:
                rna_related_domain_file.write('%s\n'%str(domain_entry))

if __name__ == "__main__":

    main()
