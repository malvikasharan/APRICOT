#!/usr/bin/env python 

import os
import argparse

__description__ = ""
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"
__version__ = ""


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("prediction_method")
    parser.add_argument("analysis_result_path")
    parser.add_argument("domain_description_file")
    parser.add_argument("go_path")
    parser.add_argument("filtered_result_path")
    parser.add_argument("all_prediction_output")
    parser.add_argument("filter_parameters")
    args = parser.parse_args()
    
    filter_predicted_domains = FilterPredictedDomains(
        args.prediction_method,
        args.analysis_result_path,
        args.domain_description_file,
        args.go_path,
        args.filtered_result_path,
        args.all_prediction_output,
        args.filter_parameters)
    filter_predicted_domains.read_id_description_file()
    filter_predicted_domains.summarize_analysis_result_files()
    filter_predicted_domains.create_filtered_result_file()


class FilterPredictedDomains(object):
    '''Filter the predicted domain by
    parameters and domain of interest'''
    def __init__(self, prediction_method,
                 analysis_result_path,
                 domain_description_file,
                 go_path,
                 filtered_result_path,
                 all_prediction_output,
                 filter_parameters):
        self._prediction_method = prediction_method
        self._analysis_result_path = analysis_result_path
        self._domain_description_file = domain_description_file
        self._go_path = go_path
        self._filtered_result_path = filtered_result_path
        self._all_prediction_output = all_prediction_output
        self._filter_parameters = filter_parameters
        
        self._id_description_dict = {}
        self._domain_length = {}
        self._cdd_go_dict = {}
        self._interpro_go_dict = {}
        self._filter_parameters_dict = {}
        self._result_detail_dict = {}
        
    def streamline_filter_predicted_domains(self):
        '''To call from apricot'''
        self.read_id_description_file()
        self.read_filter_parameters()
        self.summarize_analysis_result_files()
        self.create_filtered_result_file()
        
    def read_id_description_file(self):
        '''read id file.'''
        with open(self._domain_description_file,
                  'r') as id_description_fh:
            for entry in id_description_fh:
                if 'ReferenceId' not in entry:
                    try:
                        length = entry.split('\t')[-2]
                        parent_id = entry.split('\t')[1]
                        if 'smart' in parent_id:
                            parent_id = parent_id.replace('smart', 'SM')
                        elif 'pfam' in parent_id:
                            parent_id = parent_id.replace('pfam', 'PF')
                        if parent_id not in set(self._domain_length.keys()):
                            self._domain_length[parent_id] = length
                        self._id_description_dict[entry.split(
                            '\t')[0]] = entry.strip().replace(
                            entry.split('\t')[1], parent_id)
                        self._id_description_dict[entry.split(
                            '\t')[1]] = entry.strip().replace(
                            entry.split('\t')[1], parent_id)
                    except IndexError:
                        pass
        return self._id_description_dict, self._domain_length
    
    def read_filter_parameters(self):
        '''Records the filtering parameter for cut-off'''
        for param in self._filter_parameters:
            param_key = param.split(':')[0]
            param_val = param.split(':')[1]    
            if not param_val == 'NA':
                self._filter_parameters_dict[param_key] = float(param_val)
        return self._filter_parameters_dict
    
    def summarize_analysis_result_files(self):
        '''summarize all the the results in dictionary'''
        if self._prediction_method == 'cdd':
            self.read_cdd_go_file()
            self.summarize_rps_analysis_result_files()
        elif self._prediction_method == 'ipr':
            self.read_interpro_go_file()
            self.summarize_ipr_analysis_result_files()
            
    def read_cdd_go_file(self):
        '''read mapped file for cdd id to go.'''
        with open(self._go_path+'/mapped_cdd_to_go.csv',
                  'r') as cdd_go_fh:
            for cdd_entry in cdd_go_fh:
                self._cdd_go_dict[cdd_entry.split(
                    '\t')[0]] = cdd_entry.split('\t')[-1].strip()
        return self._cdd_go_dict
        
    def read_interpro_go_file(self):
        '''read mapped file for interpro id to go.'''
        with open(self._go_path+'/mapped_interpro_to_go.csv',
                  'r') as interpro_go_fh:
            for interpro_entry in interpro_go_fh:
                self._interpro_go_dict[interpro_entry.split(
                    '\t')[0]] = interpro_entry.split('\t')[-1].strip()
        return self._interpro_go_dict
        
    def summarize_rps_analysis_result_files(self):
        '''summarize all the RPS-BLAST results in dictionary'''
        for individual_rps_result_file in os.listdir(
                self._analysis_result_path):
            protein_id = individual_rps_result_file.split('.')[0]
            with open(
                    self._analysis_result_path+'/'+individual_rps_result_file
            ) as individual_rps_result_fh:
                for individual_rps_result_section in \
                individual_rps_result_fh.read().split('>gnl'):
                    if individual_rps_result_section.startswith('|CDD|'):
                        stat_data = individual_rps_result_section.split(
                            "Score = ")
                        for individual_rps_result in stat_data[0].split('\n'):
                            if individual_rps_result.startswith('|CDD|'):
                                cdd_main = self._compile_cdd_main(
                                    individual_rps_result)
                            if 'Length = ' in individual_rps_result:
                                try:
                                    length = individual_rps_result.split(
                                        'Length = ')[1].strip()
                                except:
                                    length = self._domain_length[
                                        cdd_main.split('\t')[1]]
                        for each_stat_group in stat_data[1:]:
                            check_list = set()
                            parameter_dict = self._compile_cdd_stat(
                                each_stat_group)
                            coverage_percent = "%.4f" % ((int(
                                parameter_dict[
                                    "cover_length"])/int(length)) * 100)
                            if float(coverage_percent) > 100:
                                coverage_percent = 100
                            similarity_percent = "%.4f" % ((int(
                                parameter_dict["similarity_value"].split(
                                    '/')[0])/int(length))*100)
                            identity_percent = "%.4f" % ((int(
                                parameter_dict["identity_value"].split(
                                    '/')[0])/int(length))*100)
                            if parameter_dict["gaps_value"] == 'None':
                                gap_percent = 0
                            else:
                                gap_percent = "%.4f" % ((int(
                                    parameter_dict["gaps_value"].split(
                                        '/')[0])/int(length)) * 100)
                            evalue = parameter_dict["evalue"]
                            bits = parameter_dict["bit"].split(' ')[0]
                            start = parameter_dict["start"]
                            stop = parameter_dict["stop"]
                            compiled_data = '\t'.join([
                                'CDD', protein_id, cdd_main,
                                str(length), str(start), str(stop),
                                str(evalue),
                                str(parameter_dict["bit"]),
                                str(bits),
                                str(parameter_dict["cover_length"]),
                                str(coverage_percent),
                                str(parameter_dict["identity_value"]),
                                str(identity_percent),
                                str(parameter_dict["similarity_value"]),
                                str(similarity_percent),
                                str(parameter_dict["gaps_value"]),
                                str(gap_percent)])
                            parameter_dict["coverage"] = coverage_percent
                            parameter_dict["identity"] = identity_percent
                            parameter_dict["similarity"] = similarity_percent
                            parameter_dict["gaps"] = gap_percent
                            if self._filter_parameters_dict:
                                for param in self._filter_parameters_dict.keys():
                                    if not param == 'evalue':
                                        if not self._filter_parameters_dict[param] == 'NA':
                                            if not float(parameter_dict[param]) >= float(
                                                self._filter_parameters_dict[param]):
                                                check_list.add('no')
                                    else:
                                        if not self._filter_parameters_dict[param] == 'NA':
                                            if not float(parameter_dict[param]) <= float(
                                                self._filter_parameters_dict[param]):
                                                check_list.add('no')
                                if 'no' not in check_list:
                                    self._result_detail_dict.setdefault(
                                        cdd_main.split('\t')[0], []).append(
                                            compiled_data+'\tParameterSelected')
                                    self._result_detail_dict.setdefault(
                                        cdd_main.split('\t')[1], []).append(
                                            compiled_data+'\tParameterSelected')
                                else:
                                    self._result_detail_dict.setdefault(
                                        cdd_main.split('\t')[0], []).append(
                                            compiled_data+'\tParameterDiscarded')
                                    self._result_detail_dict.setdefault(
                                        cdd_main.split('\t')[1], []).append(
                                        compiled_data+'\tParameterDiscarded')
        return self._result_detail_dict
    
    def _compile_cdd_main(self, individual_rps_result):
        '''Collects non statistical information
        from CDD derived predictions'''
        cdd_main = ''
        for entry in individual_rps_result.split('\n'):
            if '|CDD|' in entry:
                pssm_id = entry\
                          .split('|CDD|')[1].split(' ')[0]
                parent_id = entry\
                               .split(',')[0].split(' ')[1]
                if 'smart' in parent_id:
                    parent_id = parent_id.replace('smart', 'SM')
                elif 'pfam' in parent_id:
                    parent_id = parent_id.replace('pfam', 'PF')
                try:
                    go_id = self._cdd_go_dict[pssm_id]
                except:
                    go_id = "Not-known"
                if pssm_id in self._id_description_dict.keys():
                    short_name = self._id_description_dict[
                        pssm_id].split('\t')[2]
                    pssm_detail = self._id_description_dict[
                        pssm_id].split('\t')[3]
                    members = self._id_description_dict[
                        pssm_id].split('\t')[-3]
                    keyword = self._id_description_dict[
                        pssm_id].strip().split('\t')[-1]
                elif parent_id in self._id_description_dict.keys():
                    short_name = self._id_description_dict[
                        parent_id].split('\t')[2]
                    pssm_detail = self._id_description_dict[
                        parent_id].split('\t')[3]
                    members = self._id_description_dict[
                        parent_id].split('\t')[-3]
                    keyword = self._id_description_dict[
                        parent_id].strip().split('\t')[-1]
                else:
                    try:
                        short_name = entry.split(',')[2]
                    except IndexError:
                        short_name = entry[2]
                    if ";" in short_name:
                        short_name = short_name.split(';')[0]
                    elif "." in short_name:
                        short_name = short_name.split('.')[0]
                    pssm_detail = short_name
                    members = 'NotSelected'
                    keyword = 'NA'
                cdd_main = (
                '%s\t%s\t%s\t%s\t%s\t%s\t%s' %
                (pssm_id, parent_id, short_name, pssm_detail, 
                 keyword, go_id, members))
            return cdd_main

    def _compile_cdd_stat(self, each_stat_group):
        '''Collects statistical information
        from CDD derived predictions'''
        parameter_dict = {}
        start_list = []
        stop_list = []
        for each_stat_data in each_stat_group.split('\n'):
            if 'Expect' in each_stat_data:
                score = each_stat_data.split(',')[0]
                expect = each_stat_data.split(
                    'Expect = ')[1].strip()
                if expect.startswith('e'):
                    expect = float(expect.replace('e', '1e'))
                parameter_dict["evalue"] = float(expect)
                parameter_dict["bit"] = score
            if 'Identities = ' in each_stat_data:
                identities = each_stat_data.split(
                    'Identities = ')[1].split(',')[0]
                parameter_dict["identity_value"] = identities
                try:
                    gaps = each_stat_data.split(
                        'Gaps = ')[1].strip()
                    parameter_dict["gaps_value"] = gaps
                    positives = each_stat_data.split(
                        'Positives = ')[1].split(',')[0]
                    parameter_dict["similarity_value"] = positives
                except:
                    gaps = 'None'
                    parameter_dict["gaps_value"] = gaps
                    positives = each_stat_data.split(
                        'Positives = ')[1].strip()
                    parameter_dict["similarity_value"] = positives
            if 'Query:' in each_stat_data:
                start_list.append(each_stat_data.split(' ')[1])
                stop_list.append(each_stat_data.split(' ')[-1].strip())
        start = start_list[0]
        stop = stop_list[-1]
        parameter_dict["start"] = start
        parameter_dict["stop"] = stop
        parameter_dict["cover_length"] = int(stop)-int(start)
        return parameter_dict
    
    def summarize_ipr_analysis_result_files(self):
        '''summarize all the InterProScan results in dictionary'''
        for individual_ipr_result_file in os.listdir(
            self._analysis_result_path):
            if '.tsv' in individual_ipr_result_file:
                protein_id = individual_ipr_result_file.split('.')[0]
                if '_' in protein_id:
                    protein_id = protein_id.split('_')[0]
                with open(
                self._analysis_result_path+'/'+individual_ipr_result_file,
                    'r') as individual_ipr_result_fh:
                    for ipr_entry in individual_ipr_result_fh:
                        try:
                            parameter_tag = 'ParameterNotApplicable'
                            parent_db = ipr_entry.split('\t')[3]
                            parent_db_id = ipr_entry.split('\t')[4]
                            name = ipr_entry.split('\t')[5]
                            start = ipr_entry.split('\t')[6]
                            stop = ipr_entry.split('\t')[7]
                            expect = ipr_entry.split('\t')[8]
                            if expect == '-':
                                expect = 0
                            if self._filter_parameters_dict:
                                if 'evalue' in self._filter_parameters_dict.keys() and not self._filter_parameters_dict['evalue'] == 'NA':
                                    if float(expect) <= float(
                                        self._filter_parameters_dict['evalue']):
                                        parameter_tag = 'ParameterSelected'
                                    else:
                                        parameter_tag = 'ParameterDiscarded'
                            try:
                                ipr_id = ipr_entry.split('\t')[11]
                            except:
                                ipr_id = ipr_entry.split('\t')[4]
                            try:
                                go_id = '%s' % (
                                    self._interpro_go_dict[ipr_id])
                            except:
                                go_id = 'NA'
                            if self._id_description_dict.get(
                                parent_db_id):
                                long_name = self._id_description_dict[
                                    parent_db_id].split('\t')[3]
                                members = ('%s' %
                                           self._id_description_dict[
                                    parent_db_id].split('\t')[-3])
                                keyword = ('%s' %
                                           self._id_description_dict[
                                    parent_db_id].strip().split('\t')[-1])
                            else:
                                long_name = name
                                members = 'NotSelected'
                                keyword = 'NA'
                            try:
                                length = self._domain_length[parent_db_id]
                            except KeyError:
                                length = '-'
                            cover_length = int(stop)-int(start)
                            if not length == '-' and not length == 'NA':
                                cover_percent = "%.4f" % ((int(cover_length)/int(length))*100)
                            else:
                                cover_percent = '-'
                            ipr_data = ('\t'.join(['INTERPRO',
                            protein_id, ipr_id, parent_db_id, name,
                            long_name, keyword, go_id, members, str(length),
                            str(start), str(stop), str(expect), '\t'.join('-'*2),
                            str(cover_length), str(cover_percent),
                            '\t'.join('-'*6), parameter_tag]))  
                            self._result_detail_dict.setdefault(
                                ipr_id, set()).add(ipr_data)
                        except IndexError:
                            pass
        return self._result_detail_dict
    
    def create_filtered_result_file(self):
        '''select the result data with domain of interest'''
        self._candidate_set = set()
        self._discard_set = set()
        self._id_set = set()
        header = "\t".join([
            'Resource', 'UniProtID', 'ResourceID',
            'DomainID', 'ShortName', 'FullName', 'DomainKeyword',
            'DomainGo', 'Members', 'DomainLength', 'Start', 'Stop',
            'Evalue', 'BitScore', 'Bits', 'CoverLength',
            'CoveragePercent', 'Identity', 'IdentityPercent',
            'Similarity', 'SimilarityPercent', 'Gaps', 'GapPercent',
            'ParameterFilterTag'])
        summary_file = open(
            self._all_prediction_output + '/%s_unfiltered_all_prediction.csv' %
            self._prediction_method, 'w')
        filtered_file = open(
            self._filtered_result_path + '/' +
            self._prediction_method+'_filtered.csv', 'w')
        summary_file.write(header+'\tDomainFilterTag\n')
        filtered_file.write(header+'\n')
        id_file = open(
            self._filtered_result_path + '/' +
            self._prediction_method+'_filtered_id.csv', 'w')
        for selected_id in set(self._id_description_dict.keys()):
            if selected_id in set(self._result_detail_dict.keys()):
                for each_data in self._result_detail_dict[selected_id]:
                    self._candidate_set.add(each_data)
        filtered_file.write('\n'.join(list(self._candidate_set)))
        summary_file.write('\tSelected\n'.join(list(self._candidate_set))+'\n')
        print("Filtered uniprot IDs by %s:" % self._prediction_method)
        for candidate_entry in self._candidate_set:
            uid = candidate_entry.split('\t')[1]
            db_id = candidate_entry.split('\t')[2]
            self._id_set.add('%s\t%s' % (uid, db_id))
        id_list = sorted(self._id_set)
        print('UID\tDomainID\n'+'\n'.join(id_list))
        id_file.write('\n'.join(id_list))
        for remaining_id in set(self._result_detail_dict.keys()):
            for each_entry in self._result_detail_dict[remaining_id]:
                if each_entry not in self._candidate_set:
                    self._discard_set.add(each_entry)
        summary_file.write(
            '\tNotSelected\n'.join(list(self._discard_set))+'\n')
        summary_file.close()
        filtered_file.close()
        id_file.close()

if __name__ == '__main__':
    
    main()
    
