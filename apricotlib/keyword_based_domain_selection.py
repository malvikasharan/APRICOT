#!/usr/bin/env python

import sys
import argparse
import re

__description__ = "selects rna related domains from cdd and interpro database."
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("keywords_file")
    parser.add_argument("pfam_domain_file")
    parser.add_argument("cdd_whole_data_file", )
    parser.add_argument("interpro_whole_data_file")
    parser.add_argument("interpro_mapped_cdd")
    parser.add_argument("cdd_domain_path")
    parser.add_argument("ipr_domain_path")
    args = parser.parse_args()

    keyword_based_domain_selection = KeywordBasedDomainSelection(
        args.keywords_file, args.pfam_domain_file,
        args.cdd_whole_data_file, args.interpro_whole_data_file,
        args.interpro_mapped_cdd, args.cdd_domain_path, args.ipr_domain_path)
    keyword_based_domain_selection.read_keyword_file()
    keyword_based_domain_selection.read_pfam_domain_file()
    keyword_based_domain_selection.read_interpro_mapped_cdd_file()
    keyword_based_domain_selection.map_cdd_data_to_keywords()
    keyword_based_domain_selection.map_ipr_data_to_keywords()


class KeywordBasedDomainSelection(object):
    def __init__(self, keywords_file,
                 pfam_domain_file,
                 cdd_whole_data_file,
                 interpro_whole_data_file,
                 interpro_mapped_cdd,
                 cdd_domain_path,
                 ipr_domain_path):
        self._keywords_file = keywords_file
        self._pfam_domain_file = pfam_domain_file
        self._cdd_whole_data_file = cdd_whole_data_file
        self._interpro_whole_data_file = interpro_whole_data_file
        self._interpro_mapped_cdd = interpro_mapped_cdd
        self._cdd_domain_path = cdd_domain_path
        self._ipr_domain_path = ipr_domain_path
        
        self._keyword_list = []
        self._pfam_domain_dict = {}
        self._mapped_cdd_members = {}
        self._mapped_ipr_legnth = {}
        self._selected_cdd_entry_dict = {}
        self._selected_ipr_entry_dict = {}
    
    def select_cdd_and_ipr_domains(self):
        self.read_keyword_file()
        self.read_pfam_domain_file()
        self.read_interpro_mapped_cdd_file()
        self.map_cdd_data_to_keywords()
        self.map_ipr_data_to_keywords()
        
    def select_cdd_domains(self):
        self.read_keyword_file()
        self.read_pfam_domain_file()
        self.read_interpro_mapped_cdd_file()
        self.map_cdd_data_to_keywords()
        
    def select_ipr_domains(self):
        self.read_keyword_file()
        self.read_pfam_domain_file()
        self.read_interpro_mapped_cdd_file()
        self.map_ipr_data_to_keywords()
    
    def _string_search(self, keyword, annotation):
        if ' ' not in keyword:
            if '. ' not in annotation:
                if ',' in str(annotation):
                    annotation = ' '.join(str(annotation).split(','))
                keyword_match = self._match_keys_in_annotation(keyword, annotation)
                if keyword_match:
                    return True
            else:
                for each_annotation in annotation.split('. '):
                    keyword_match = self._match_keys_in_annotation(keyword, each_annotation)
                    if keyword_match:
                        return True
        else:
            ref_kw_list = keyword.lower().split(' ')
            if not '. ' in annotation:
                if ',' in str(annotation):
                    annotation = ' '.join(str(annotation).split(','))
                new_kw_list = []
                for each_word in ref_kw_list:
                    current_search = self._match_keys_in_annotation(each_word, annotation)
                    if current_search:
                        new_kw_list.append(each_word)
                keyword_match = ref_kw_list == new_kw_list
                if keyword_match:
                    return True
            else:
                for each_annotation in annotation.split('. '):
                    
                    new_kw_list = []
                    for each_word in ref_kw_list:
                        current_search = self._match_keys_in_annotation(each_word, each_annotation)
                        if current_search:
                            new_kw_list.append(each_word)
                    keyword_match = ref_kw_list == new_kw_list
                    if keyword_match:
                        return True
        return False
    
    def _match_keys_in_annotation(self, keyw, annotation):
        if not '#' in keyw:
            annotation = annotation.lower().replace(
                    '_', ' ').replace('-', ' ')
            if ' ' in annotation:
                for each_annotation in list(annotation.split(' ')):
                    if re.findall(r"(?:\s|^)%s(?=\s|$)" %
                        keyw.lower(), each_annotation):
                        return True
            else:
                if re.findall(r"(?:\s|^)%s(?=\s|$)" %
                              keyw.lower(), annotation):
                    return True
        else:
            keyw = keyw.replace('#', str('\w*'))
            annotation = annotation.lower().replace(
                    '_', ' ').replace('-', ' ')
            for each_annotation in list(annotation.split(' ')):
                    if re.findall(r'%s' % keyw.lower(), each_annotation):
                        return True
            else:
                if re.findall(r'%s' % keyw.lower(), annotation):
                    return True
        return False
    
    def read_keyword_file(self):
        '''reads user provided keywords for domain selection'''
        self._keyword_list = [rna_keyword.strip()
                              for rna_keyword in open(
                                self._keywords_file, 'r')]
        return self._keyword_list
    
    def read_pfam_domain_file(self):
        ''''''
        with open(self._pfam_domain_file, 'r') as in_fh:
            try:
                for entry in in_fh:
                    pfam_id = entry.split('\t')[0]
                    family_id = entry.split('\t')[1]
                    short_name = entry.split('\t')[3]
                    full_name = entry.split('\t')[8]
                    for check_keyword in self._keyword_list:
                        new_keyword = check_keyword.replace('-', ' ').replace('_', ' ')
                        if ' like' in new_keyword:
                            new_keyword = new_keyword.replace(' like', ' ').strip().replace('  ', ' ')
                        for search_annotation in list([family_id, short_name, full_name]):
                            if self._string_search(new_keyword, search_annotation):
                                self._pfam_domain_dict.setdefault(check_keyword, set()).add(pfam_id)
            except UnicodeDecodeError:
                pass
        return self._pfam_domain_dict
   
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
                if '|' in ipr_members:
                    for each_ipr_member in ipr_members.split('|'):
                        self._mapped_ipr_legnth[each_ipr_member] = domain_length
        self._mapped_cdd_members, self._mapped_ipr_legnth
    
    def map_cdd_data_to_keywords(self):
        '''Parses CDD annotation data from table'''
        with open(self._cdd_whole_data_file, 'r') as cdd_data_fh:
            for each_entry in cdd_data_fh:
                cdd_id = each_entry.split('\t')[0]
                domain_id = each_entry.split('\t')[1]
                each_entry = each_entry.replace(each_entry.split('\t')[3], " ".join(
                        each_entry.split('\t')[3].split())).replace(';', ',')
                if 'smart' in domain_id:
                    each_entry = each_entry.replace(domain_id, 'SM'+domain_id.split('smart')[-1])
                    domain_id = 'SM'+domain_id.split('smart')[-1]
                if 'pfam' in domain_id:
                    each_entry = each_entry.replace(domain_id, 'PF'+domain_id.split('pfam')[-1])
                    domain_id = 'PF'+domain_id.split('pfam')[-1]
                if domain_id in self._mapped_cdd_members.keys():
                    cdd_entry = "%s\t%s\t%s" % ('\t'.join(each_entry.split('\t')[0:-1]),
                            self._mapped_cdd_members[domain_id], each_entry.split('\t')[-1])
                else:
                    cdd_entry = "%s\tNA\t%s" % ('\t'.join(each_entry.split('\t')[0:-1]),
                                                each_entry.split('\t')[-1])
                for check_keyword in self._keyword_list:
                    try:
                        if domain_id in self._pfam_domain_dict[check_keyword]:
                            self._selected_cdd_entry_dict.setdefault(check_keyword, set()).add(cdd_entry.strip())
                    except KeyError:
                        pass
                    else:
                        new_keyword = check_keyword.replace('-', ' ').replace('_', ' ')
                        if ' like' in new_keyword:
                            new_keyword = new_keyword.replace(' like', ' ').replace('  ', ' ')
                        for search_annotation in cdd_entry.strip().split('\t')[0:4]:
                            if self._string_search(new_keyword, search_annotation):
                                self._selected_cdd_entry_dict.setdefault(check_keyword, set()).add(cdd_entry.strip())
        self.create_keyword_selected_domain_file('cdd', self._selected_cdd_entry_dict, self._cdd_domain_path)
    
    def map_ipr_data_to_keywords(self):
        '''Parses InterPro annotation data from table'''
        with open(self._interpro_whole_data_file, 'r') as in_fh:
            for ipr_entry in in_fh:
                domain_id = ipr_entry.split('\t')[1]
                try:
                    if domain_id in self._mapped_ipr_legnth.keys():
                        mapped_length = self._mapped_ipr_legnth[domain_id]
                    else:
                        mapped_length = 'NA'
                except:
                    mapped_length = 'NA'
                for check_keyword in self._keyword_list:
                    try:
                        if domain_id in self._pfam_domain_dict[check_keyword]:
                            self._selected_ipr_entry_dict.setdefault(check_keyword, set()).add(
                                '%s\t%s' % (ipr_entry.strip(), mapped_length))
                    except KeyError:
                        pass
                    else:
                        new_keyword = check_keyword.replace('-', ' ').replace('_', ' ')
                        if ' like' in new_keyword:
                            new_keyword = new_keyword.replace(' like', ' ').replace('  ', ' ')
                        for search_annotation in ipr_entry.strip().split('\t')[0:4]:
                            if self._string_search(new_keyword, search_annotation):
                                self._selected_ipr_entry_dict.setdefault(check_keyword, set()).add(
                                    '%s\t%s' % (ipr_entry.strip(), mapped_length))
        self.create_keyword_selected_domain_file('interpro', self._selected_ipr_entry_dict, self._ipr_domain_path)
    
    def create_keyword_selected_domain_file(self, domain_db, selected_domain_entry_dict, domain_data_path):
        '''Creates a file with CDD or interpro derived domain of interest'''
        keyword_selected_domain_dict = {}
        for keyword in self._keyword_list:
            with open(domain_data_path+'/'+keyword+'_related_'+domain_db+'_domains.tab',
                      'w') as selected_domain_file:
                if keyword in selected_domain_entry_dict.keys():
                    for each_entry in selected_domain_entry_dict[keyword]:
                        keyword_selected_domain_dict.setdefault(each_entry, set()).add(keyword)
                        if '#'in keyword:
                            keyword = keyword.replace('#', '')
                        selected_domain_file.write("%s\t%s\n" % (each_entry.strip(), keyword))
        with open(domain_data_path+'/all_keyword_selected_'+domain_db+'_data.tab',
                  'w') as keyword_selected_domain_file:
            for domain_entry in keyword_selected_domain_dict.keys():
                all_keywords = ', '.join(list(keyword_selected_domain_dict[domain_entry]))
                keyword_selected_domain_file.write('%s\t%s\n' % (domain_entry.strip(), all_keywords))

if __name__ == "__main__":

    sys.exit(main())
