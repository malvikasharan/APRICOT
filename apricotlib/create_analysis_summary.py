#!/usr/bin/env python 

import argparse
import os
from collections import defaultdict

__description__ = "Summarizes APRICOT analysis results."
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("query_map")
    parser.add_argument("selected_domains")
    parser.add_argument("unfilter_path")
    parser.add_argument("outpath")
    args = parser.parse_args()

    create_analysis_summary = CreateAnalysisSummary(
        args.query_map, args. selected_domains,
        args.unfilter_path, args.outpath)
    create_analysis_summary.count_queries()
    create_analysis_summary.count_domains()
    create_analysis_summary.domain_stat()
    create_analysis_summary.record_selected_stat()


class CreateAnalysisSummary(object):
    '''APRICOT analysis summary'''
    
    def __init__(self, query_map, selected_domains,
                 unfilter_path, outpath):
        self._query_map = query_map
        self._selected_domains = selected_domains
        self._unfilter_path = unfilter_path
        self._outpath = outpath
        
        self._query_info = {}
        self._qury_info_list = []
        self._domain_keyword_info = {}
        self._prot_domain_dict = defaultdict(lambda: defaultdict(
            lambda: defaultdict(lambda: set())))
        self._info_tag_dict = {}
        self._prot_go_dict = {}
        
    def streamline_create_analysis_summary(self):
        '''To call from apricot exe'''
        self.count_queries()
        self.count_domains()
        self.domain_stat()
        self.record_selected_stat()
        
    def count_queries(self):
        '''Records query mapping information'''
        with open(self._query_map, 'r') as in_fh:
            self._query_info.setdefault('mapped', set()).add('')
            self._query_info.setdefault('unmapped', set()).add('')
            for entry in in_fh:
                if not entry.strip() == '':
                    if ':' not in entry.strip():
                        self._query_info.setdefault(
                            'mapped', set()).add(entry.strip())
                    else:
                        if not entry.strip().split(':')[1] == 'unmapped':
                            self._query_info.setdefault(
                                'mapped', set()).add(entry.split(':')[0])
                        else:
                            self._query_info.setdefault(
                                'unmapped', set()).add(entry.split(':')[0])
                        self._qury_info_list.append(
                            entry.strip().replace(':', '\t'))
        return self._query_info, self._qury_info_list
    
    def count_domains(self):
        '''Records selected domain information'''
        with open(self._selected_domains, 'r') as in_fh:
            for entry in in_fh:
                if not entry.strip() == '' and not entry.startswith(
                        'ReferenceId'):
                    keyword = entry.strip().split("\t")[-1]
                    self._domain_keyword_info.setdefault(
                        keyword, []).append(entry.strip())
        return self._domain_keyword_info
        
    def domain_stat(self):
        '''Records statistics of predicted domains'''
        for files in os.listdir(self._unfilter_path):
            if '_unfiltered_all_prediction.csv' in files:
                if 'cdd' in files.lower():
                    data_source = 'CDD'
                else:
                    data_source = 'InterPro'
                with open(self._unfilter_path+'/'+files, 'r') as in_fh:
                    for entry in in_fh:
                        if not entry.startswith('Resource'):
                            if not entry.strip() == '':
                                data_detail = NonFilteredData(
                                    entry.strip().split('\t'))
                                self._prot_domain_dict[
                                    data_source][data_detail.uid][
                                    data_detail.domain_id].add("%s:%s" % (
                                        data_detail.start,
                                        data_detail.stop))
                                self._info_tag_dict["%s:%s:%s:%s:%s" % (
                                    data_source, data_detail.uid,
                                    data_detail.domain_id,
                                    data_detail.start, data_detail.stop)] = "%s:%s" % (
                                    data_detail.parameter, data_detail.domain_tag)
            if not 'cdd_unfiltered_all_prediction.csv' in os.listdir(
                    self._unfilter_path):
                print("The folder %s does not contain cdd_unfiltered_all_prediction.csv." %
                      self._inpath+'/output/1_all_domain_predictions')
            if not 'ipr_unfiltered_all_prediction.csv' in os.listdir(
                    self._unfilter_path):
                print("The folder %s does not contain ipr_unfiltered_all_prediction.csv." %
                      self._inpath+'/output/1_all_domain_predictions')
        return self._prot_domain_dict, self._info_tag_dict
    
    def record_selected_stat(self):
        '''Creates an output file with summary information'''
        with open(self._outpath, 'w') as out_fh:
            out_fh.write("Total query proteins: %s\n" % str(
                len(list(self._query_info[
                    'mapped'])+list(self._query_info['unmapped']))-2))
            out_fh.write(
                "Total query proteins mapped to UniProt IDs: %s\n" % str(
                    len(self._query_info['mapped'])-1))
            out_fh.write(
                "Total query proteins not mapped to UniProt IDs: %s\n\n" % str(
                    len(self._query_info['unmapped'])-1))
            out_fh.write("ID mapping details:\n%s\n\n" % '\n'.join(
                self._qury_info_list))
            out_fh.write(
                "Keywords used for retreiving the domains of interest: %s\n"
                % len(self._domain_keyword_info.keys()))
            for kw in self._domain_keyword_info.keys():
                out_fh.write("%s\t%s\n" % (
                    kw, len(self._domain_keyword_info[kw])))
            for database in self._prot_domain_dict.keys():
                out_fh.write("\n--------------------------------------------------------")
                out_fh.write("--------------------------------------------------------\n\n")
                out_fh.write("Domain prediction summary for %s:\n" % database)
                total_proteins = len(
                    list(set(self._prot_domain_dict[database].keys())))
                out_fh.write(
                    "Total proteins with domains: %s\n" % total_proteins)
                protein_pred_dict = {}
                parameter_selected_data = {}
                domain_selected_data = {}
                proteins_location = {}
                for proteins in self._prot_domain_dict[database].keys():
                    total_locations = 0
                    protein_pred_dict[proteins] = len(list(set(
                        self._prot_domain_dict[
                            database][proteins].keys())))
                    for domain_id in self._prot_domain_dict[
                            database][proteins].keys():
                        total_locations += len(self._prot_domain_dict[
                            database][proteins][domain_id])
                        for location in self._prot_domain_dict[
                                database][proteins][domain_id]:
                            tag_key = "%s:%s:%s:%s" % (
                                database, proteins, domain_id, location)
                            if self._info_tag_dict[tag_key].split(
                                    ':')[0] == 'ParameterSelected':
                                parameter_selected_data.setdefault(
                                    proteins, set()).add(domain_id)
                                if self._info_tag_dict[tag_key].split(
                                        ':')[1] == 'Selected':
                                    domain_selected_data.setdefault(
                                        proteins, set()).add(domain_id)
                    proteins_location[proteins] = total_locations
                out_fh.write(
                    "Query\tTotal predictions (locations identified)\tUnique "
                    "domains (ids)\tUnique domains that pass the parameter "
                    "filter\n")
                preds = 0
                uniq = 0
                param_uniq = 0
                for uid in parameter_selected_data.keys():
                    out_fh.write("%s\t%s\t%s\t%s\n" % (
                        uid, proteins_location[uid],
                        protein_pred_dict[uid],
                        len(parameter_selected_data[uid])))
                    preds += proteins_location[uid]
                    uniq += protein_pred_dict[uid]
                    param_uniq += len(parameter_selected_data[uid])
                out_fh.write(
                    "Total domain predictions (locations in the queries): %s\n"
                    % str(preds))
                out_fh.write(
                    "Unique domains predicted in the queries: %s\n" % str(
                        uniq))
                out_fh.write(
                    "Unique domain that pass the parameter filter: %s\n" %
                    str(param_uniq))
                out_fh.write(
                    "\nTotal proteins with 'domains of interest' that pass "
                    "the parameter filter:\n%s\n" %
                    ', '.join(domain_selected_data.keys()))
                out_fh.write("Proteins\tDomains of interest\tDomain count\n")
                for each_key in domain_selected_data.keys():
                    out_fh.write("%s\t%s\t%s\n" % (
                        each_key, ', '.join(domain_selected_data[each_key]),
                        len(domain_selected_data[each_key])))
 

class NonFilteredData(object):
    '''all the column details of unfiltered table'''
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
        self.stats = row[12:-2]
        self.domain_tag = row[-1]
        self.parameter = row[-2]

if __name__ == '__main__':
    main()
