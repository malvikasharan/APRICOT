#!/usr/bin/env python 

import argparse
import re

__description__ = "selects rna related domains from cdd database."
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    '''all commandline arguement dclaration'''
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("keywords_file")
    parser.add_argument("cdd_whole_data_file")
    parser.add_argument("interpro_mapped_cdd")
    parser.add_argument("domain_data_path")
    args = parser.parse_args()

    keyword_selected_domain_selection = RnaRelatedDomainSelection(
        args.keywords_file, args.cdd_whole_data_file,
        args.interpro_mapped_cdd, args.domain_data_path)
    keyword_selected_domain_selection.read_keyword_file()
    keyword_selected_domain_selection.read_interpro_mapped_cdd_file()
    keyword_selected_domain_selection.read_cdd_whole_data_file()
    keyword_selected_domain_selection.create_keyword_selected_domain_file()


class RnaRelatedDomainSelection(object):
    '''classification of data'''
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
        
    def read_keyword_file(self):
        '''read keywords for selection'''
        self._keyword_list = [rna_keyword.strip()
                              for rna_keyword in open(
                                self._keywords_file, 'r')]
        return self._keyword_list
    
    def read_interpro_mapped_cdd_file(self):
        ''''''
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
        '''read and annotation data from table'''
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
                self._cdd_dict[cdd_entry.strip()] = cdd_entry.strip(
                    ).split('\t')[3]
        return self.cdd_whole_data_list, self._cdd_dict
    
    def create_keyword_selected_domain_file(self):
        '''create rne related domain list'''
        self._keyword_annotation_dict = {}
        self._keyword_selected_domain = []
        for cdd_entry in self.cdd_whole_data_list:
            for keyword in self._keyword_list:
                if ' ' in keyword:
                    key_list = []
                    for each_key in keyword.split(' '):
                        key_list.append(each_key)
                    match = re.search(r'\b%s*|\W%s\b'%(key_list[0].lower(),
                                                       key_list[1].lower()),
                                      self._cdd_dict[cdd_entry])
                    if match:
                        self._keyword_annotation_dict.setdefault(
                            keyword, []).append(cdd_entry)
                else:
                    match = re.search(r'\b%s\b'%keyword, self._cdd_dict[cdd_entry])
                    if match:
                        self._keyword_annotation_dict.setdefault(
                            keyword, []).append(cdd_entry)
                        
        for fkeyword in self._keyword_list:
            fkeyword = fkeyword.replace(' ', '_')
            with open(self._domain_data_path+'/'+fkeyword+'_related_cdd_ids.tab',
                      'w') as keyword_specific_domain:
                if self._keyword_annotation_dict.get(fkeyword):
                    for each_entry in self._keyword_annotation_dict[fkeyword]:
                        each_entry = each_entry.replace(
                            each_entry.split('\t')[3], " ".join(
                                each_entry.split('\t')[3].split())).replace(';', ',')
                        cdd_domain = each_entry.split('\t')[1]
                        if cdd_domain in set(self._mapped_cdd_members.keys()):
                            members = self._mapped_cdd_members[cdd_domain]
                        else:
                            members = 'NA'
                        keyword_specific_domain.write('%s\t%s\t%s\n'%(
                            '\t'.join(each_entry.split('\t')[0:-1]), members,
                            each_entry.split('\t')[-1]))
                        self._keyword_selected_domain.append(
                            ('%s\t%s\t%s' % (
                                '\t'.join(each_entry.split('\t')[0:-1]),
                                members, each_entry.split('\t')[-1])))
            
        uniq_keyword_selected_domains = list(
            set(self._keyword_selected_domain))
        with open(self._domain_data_path+'/all_keyword_selected_cdd_data.tab',
                  'w') as keyword_selected_domain_file:
            for domain_entry in uniq_keyword_selected_domains:
                keyword_selected_domain_file.write(
                    '%s\n' % str(domain_entry))

if __name__ == "__main__":

    main()

