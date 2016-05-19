#!/usr/bin/env python

import os
import sys
import argparse
import math
from collections import defaultdict
import difflib
from difflib import *
try:
    from Bio.Emboss.Applications import NeedleCommandline
except ImportError:
    print('Python package Biopython is missing. Please install/update.\n')
    sys.sxit(0)
from itertools import combinations
try:
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    print('Python package matplotlib is missing. Please install/update.\n')
try:
    import numpy as np
except ImportError:
    print('Python package numpy is missing. Please install/update.\n')
    sys.sxit(0)
import random
try:
    from scipy.spatial import distance
    from scipy.cluster.hierarchy import *
    from scipy import stats
except ImportError:
    print('Python package scipy is missing. Please install/update.\n')
    sys.sxit(0)

__description__ = "Calculates scores for feature based annotation of domains selected by APRICOT"
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("filtered_data") ##selected data with annotation
    parser.add_argument("cdd_pred_files") ##cdd based domain prediction
    parser.add_argument("outpath") ##outpath with distance calculation
    args = parser.parse_args()
    compute_composition_distance = ComputeCompositionDistance(
        args.filtered_data, args.cdd_pred_files, args.outpath)
    compute_composition_distance.parse_filtered_data()
    compute_composition_distance.summarize_rps_analysis_result_files()
    
class ComputeCompositionDistance(object):
    def __init__(self, filtered_data,
                 cdd_pred_files,
                 outpath):
        self._filtered_data = filtered_data
        self._cdd_pred_files = cdd_pred_files
        self._outpath = outpath
        
        self._cdd_main_entry_dict = defaultdict(lambda: defaultdict(lambda: str()))
        self._final_entry_dict = {}
        self._total_score_dict = {}
        self._ref_value_dict = defaultdict(lambda : defaultdict(lambda : (defaultdict(lambda: float))))
        self._ref_t_stat = defaultdict(lambda : defaultdict(lambda : (defaultdict(lambda: float))))
        self._ref_pval = defaultdict(lambda : defaultdict(lambda : (defaultdict(lambda: float))))
        self._t_stat_distribution = defaultdict(lambda : defaultdict(lambda : (defaultdict(lambda: []))))
        self._pval_distribution = defaultdict(lambda : defaultdict(lambda : (defaultdict(lambda: []))))
        self._composition_dict = defaultdict(
            lambda : (defaultdict(lambda : defaultdict(float))))
        self._calc_type_list = ('Secondary_structure', 'Amino_acid_residue',
                                'Amino_acid_property', 'Dipeptide')
        self._all_distance_data = defaultdict(
            lambda : (defaultdict(lambda : defaultdict(float))))
        
        self._amino_acid_str = {
            'H' : ['E', 'A', 'L', 'M', 'Q', 'K', 'R', 'H', 'Z'],
            'E' : ['V', 'I', 'Y', 'C', 'W', 'F', 'T'],
            'C' : ['G', 'N', 'P', 'S', 'D', 'B']
        }
        #1: alpha-helix (H), 2: beta-sheet(E), 3: turns and loops(C)
        #https://en.wikibooks.org/wiki/Structural_Biochemistry/Proteins/Structures
        
        self._amino_acid_list = ('A', 'C', 'D', 'E', 'F',
                                  'G', 'H', 'I', 'K', 'L',
                                  'M', 'N', 'P', 'Q', 'R',
                                  'S', 'T', 'V', 'W', 'Y',
                                  'O', 'U', 'X')
        
        #http://www.seas.upenn.edu/~cis535/Fall2004/HW/GCB535HW6b.pdf
        #C.Chothia, J. Mol. Biol., 105(1975)1-14 
        #A.A. Zamyatin, Prog. Biophys. Mol. Biol., 24(1972)107-123 
        #C. Tanford, Adv. Prot. Chem., 17(1962)69-165 
        #The Merck Index, Merck & Co. Inc., Nahway, N.J., 11(1989); CRC Handbook of Chem.& Phys., 
        #Cleveland, Ohio, 58(1977)
        #name: information from NIST Chemistry WebBook, three letter code: GIF, one letter code: VRML 
        
        #mass in dalton
        self._amino_acid_mass = {'A' : 71.08, 'C' : 103.15, 'D' : 115.08,
                                 'E' : 129.12, 'F' : 147.18, 'G' : 57.05,
                                 'H' : 137.14, 'I' : 113.16, 'K' : 128.17,
                                 'L' : 113.16, 'M' : 131.19, 'N' : 114.103,
                                 'P' : 97.12, 'Q' : 128.14, 'R' : 156.19,
                                 'S' : 87.08, 'T' : 101.11, 'V' : 99.14,
                                 'W' : 186.12, 'Y' : 163.18, 'U' : 150.039,
                                 'O' : 255.31}
        
        #pI at 25degree: Isoelectric point (pI) is a pH in which net charge of protein is 0
        self._amino_acid_isoelpt = {'A' : 6.107, 'C' : 5.02, 'D' : 2.98,
                                 'E' : 3.08, 'F' : 5.91, 'G' : 6.064,
                                 'H' : 7.64, 'I' : 6.038, 'K' : 9.47,
                                 'L' : 6.036, 'M' : 5.74, 'N' : '-',
                                 'P' : 6.3, 'Q' : '-', 'R' : 10.76,
                                 'S' : 5.68, 'T' : '-', 'V' : 6.002,
                                 'W' : 5.88, 'Y' : 163.18}
        #Solubility (g/100g)
        
        self._amino_acid_solubility = {'A' : 16.65, 'C' : 30, 'D' : 0.778,
                                 'E' : 0.864, 'F' : 2.965, 'G' : 24.99,
                                 'H' : 4.19, 'I' : 4.117, 'K' : 30,
                                 'L' : 2.426, 'M' : 3.381, 'N' : 3.53,
                                 'P' : 162.3, 'Q' : 2.5, 'R' : 15,
                                 'S' : 5.023, 'T' : 30, 'V' : 8.85,
                                 'W' : 1.136, 'Y' : 0.0453}
        
        self._van_der_waal_volume = {'A' : 67, 'C' : 86, 'D' : 91,
                                 'E' : 109, 'F' : 135, 'G' : 48,
                                 'H' : 118, 'I' : 124, 'K' : 135,
                                 'L' : 124, 'M' : 124, 'N' : 96,
                                 'P' : 90, 'Q' : 114, 'R' : 148,
                                 'S' : 73, 'T' : 93, 'V' : 105,
                                 'W' : 163, 'Y' : 141}
        
        self._acid_dissociation_pka = {'A' : 0, 'C' : 8.18, 'D' : 3.9,
                                 'E' : 4.07, 'F' : 0, 'G' : 0,
                                 'H' : 6.04, 'I' : 0, 'K' : 10.54,
                                 'L' : 0, 'M' : 0, 'N' : 0,
                                 'P' : 0, 'Q' : 0, 'R' : 12.48,
                                 'S' : 5.68, 'T' : 5.53, 'U':  5.73,
                                 'V' : 0, 'W' : 163, 'Y' : 141}
        
        self._ph_value = {'C' : 'A', 'D' : 'A', 'E' : 'A', 'H' : 'wB', 'K' : 'B',
                    'O' : 'wB', 'Q' : 'wB', 'R' : 'sB', 'S' : 'wA', 'T' : 'wA',
                     'U':  'A', 'W' : 'wB', 'Y' : 'wA'}
        
        self._solvent_accessibility = {'M' : 'm', 'P' : 'm', 'S' : 'm',
                                       'T' : 'm', 'H' : 'm', 'Y' : 'm',
                                       'R' : 'h', 'K' : 'h', 'Q' : 'h',
                                       'E' : 'h', 'N' : 'h', 'D' : 'h'}
        
        self._charge = {'D' : 'N', 'E' : 'N', 'R' : 'P', 'K' : 'P', 'H' : 'P',
                        'N' : 'U', 'Q' : 'U', 'C' : 'U', 'T' : 'U', 'S' : 'U',
                        'Y' : 'U',}
        
        self._amino_acid_ref = {
            'a_polar' : ['Y', 'N', 'Q', 'T', 'S', 'D', 'E', 'R',
                         'K', 'H', 'Y', 'O', 'W', 'C'],
            'b_non_polar' : ['F', 'G', 'A', 'V', 'P', 'L', 'I', 'M'],
            'c_neutral' : ['T', 'E', 'G', 'S', 'Q', 'D', 'H'],
            'd_hydrophobic' : ['C', 'Y', 'A', 'L', 'I', 'F', 'W', 'V', 'M'],
            'e_hydrophilic' : ['R', 'K', 'N', 'H', 'P', 'E', 'D'],
            'f_van_der_waal=0-4' : ['G', 'A', 'S', 'P', 'D', 'N',
                                    'V', 'E', 'Q', 'I', 'L'],
            'g_van_der_waal>4' : ['M', 'H', 'K', 'F', 'R', 'Y', 'W'],
            'h_mid_polarity' : ['P', 'A', 'T', 'G', 'S'],
            'i_high_polarity' : ['H', 'Q', 'R', 'K', 'N', 'E', 'D'],
            'j_negative' : ['D', 'E'],
            'k_positive' : ['R', 'K', 'H'],
            'l_uncharged' : ['N', 'Q', 'C', 'T', 'S', 'Y'],
            'm_aliphatic' : ['A', 'I', 'L', 'V', 'G'],
            'n_aromatic' : ['F', 'H', 'W', 'Y'],
            'o_basic' : ['K', 'R', 'H', 'W', 'Q', 'O'],
            'p_acidic' : ['C', 'D', 'E', 'U', 'Y', 'T', 'S'],
            'q_tiny' : ['A', 'C', 'G', 'S', 'U'],
            'r_small' : ['A', 'C', 'D', 'G', 'N', 'P', 'S', 'T', 'U'],
            's_large' : ['V', 'L', 'I', 'M', 'P', 'F', 'W'],
            't_mid_solvent_accebility' : ['M', 'P', 'S', 'T', 'H', 'Y'],
            'u_high_solvent_access' : ['R', 'K', 'Q', 'E', 'N', 'D'],
            'v_essential' : ['F', 'H', 'I', 'K', 'L', 'M', 'T', 'V', 'W'],
            'w_non_essential' : ['A', 'D', 'N', 'O', 'P', 'Q', 'S', 'U']
        }
        
    def streamline_annotation_scoring(self):
        self.parse_filtered_data()
        self.summarize_rps_analysis_result_files()
        
    def parse_filtered_data(self):
        '''Parse the selected data'''
        with open(self._filtered_data, 'r') as in_fh:
            for entry in in_fh:
                if entry.startswith('Entry'):
                    self._header_filter_data = entry.strip()
                else:
                    filter_data_annotation = FilteredData(
                        entry.strip().split('\t'))
                    if filter_data_annotation.resource == 'CDD':
                        cdd_main = "%s\t%s\t%s\t%s" % (
                        filter_data_annotation.resource_id,
                        filter_data_annotation.domain_id,
                        filter_data_annotation.start,
                        filter_data_annotation.stop)
                        self._cdd_main_entry_dict[
                            filter_data_annotation.uid][cdd_main] = entry.strip()
        return self._cdd_main_entry_dict, self._header_filter_data
    
    def summarize_rps_analysis_result_files(self):
        '''summarize all the RPS-BLAST results in dictionary'''
        summary_file = open(self._outpath+'/annotation_scoring_of_selected_data.csv', 'w')
        filter3_file = open(self._outpath+'/annotation_scoring_of_selected_data_filter3.csv', 'w')
        filter4_file = open(self._outpath+'/annotation_scoring_of_selected_data_filter4.csv', 'w')
        filter3_dist_file = open(self._outpath+'/filter3_pval_distribution.csv', 'w')
        filter4_dist_file = open(self._outpath+'/filter4_pval_distribution.csv', 'w')
        self._result_detail_dict = defaultdict(lambda: defaultdict(
            lambda: defaultdict(lambda: str)))
        summary_header = ('\t'.join([
        '\t'.join(self._header_filter_data.split('\t')[0:5]),
        '\t'.join(self._header_filter_data.split('\t')[15:20]),
        '\t'.join(self._header_filter_data.split('\t')[23:26]),
        'ReferenceSequence', 'QuerySequence',
        'ReferenceSecStr (H:alpha-helix, E:beta-sheet, C:turns&loops)',
        'QuerySecStr (H:alpha-helix, E:beta-sheet, C:turns&loops)',
        'Coverage','Identity', 'Similarity','Gap',
        'CoverageByDomainLength (filter-1)', 'IdentityByCoverage (filter-1)',
        'SimilarityByCoverage (filter-1)', 'UngappedByCoverage (filter-1)',
        'MolecularMass (filter-2)', 'IsoelectricPoint (filter-2)',
        'Solubility (filter-2)', 'VanDerWaalValue (filter-2)',
        'PkaValue (filter-2)', 'AA-RODistance(filter-3)',
        'SecStr-RODistance (filter-3)', 'PhysiChemiComp-EDistance (filter-4)',
        'DipeptideComp-EDistance (filter-4)', 'TripeptideComp-EDistance (filter-4)',
        'Average filter-1 (Predicted properties (PP))',
        'Average filter-2 (Chemical properties)',
        'Average filter-3 (Needleman Wunsch sequence similarity)',
        'Average filter-4 (Euclidean distance for composition)',
        'Bayesian Score (based on all the filters)'])+'\n')
        filter3_file.write('\t'.join(['ProteinId',
        'ReferenceSequence', 'QuerySequence', 'AA-RODistance (filter-3)',
        'AA-RODistance - t_statistics', 'AA-RODistance -P_value',
        'SecStr-RODistance (filter-3)', 'SecStr-RODistance - t_statistics',
        'SecStr-RODistance - P_value', 'Average filter-3 (Ratcliff Obershelp distance of PP)',
        'Average filter-3 - t_statistics', 'Average filter-3 - P_value'])+'\n')
        filter4_file.write('\t'.join(['ProteinId', 'ReferenceSequence', 'QuerySequence',
        'PhysiChemiComp-EDistance (filter-4)', 'PhysiChemiComp-EDistance - t_statistics',
        'PhysiChemiComp-EDistance - P_value', 'DipeptideComp-EDistance (filter-4)',
        'DipeptideComp-EDistance - t_statistics', 'DipeptideComp-EDistance - P_value',
        'TripeptideComp-EDistance (filter-4)', 'TripeptideComp-EDistance - t_statistics',
        'TripeptideComp-EDistance - P_value', 'Average filter-4 (Euclidean distance of PP)',
        'Average filter-4 - t_statistics', 'Average filter-4 -P_value'])+'\n')
        filter3_dist_file.write('\t'.join(['ProteinId',
        'Ref-AA-RODistance - t_statistics', 'Ref-AA-RODistance -P_value',
        'Random-AA-RODistance - t_statistics', 'Random-AA-RODistance -P_value',
        'Ref-SecStr-RODistance - t_statistics', 'Ref-SecStr-RODistance - P_value',
        'Random-SecStr-RODistance - t_statistics', 'Random-SecStr-RODistance - P_value',
        'Ref-Average filter-3 - t_statistics', 'Ref-Average filter-3 - P_value',
        'Random-Average filter-3 - t_statistics', 'Random-Average filter-3 - P_value'])+'\n')
        filter4_dist_file.write('\t'.join(['ProteinId', 
        'Ref-PhysiChemiComp-EDistance - t_statistics', 'Ref-PhysiChemiComp-EDistance - P_value',
        'Random-PhysiChemiComp-EDistance - t_statistics', 'Random-PhysiChemiComp-EDistance - P_value',
        'Ref-DipeptideComp-EDistance - t_statistics', 'Ref-DipeptideComp-EDistance - P_value',
        'Random-DipeptideComp-EDistance - t_statistics', 'Random-DipeptideComp-EDistance - P_value',
        'Ref-TripeptideComp-EDistance - t_statistics', 'Ref-TripeptideComp-EDistance - P_value',
        'Random-TripeptideComp-EDistance - t_statistics', 'Random-TripeptideComp-EDistance - P_value',
        'Ref-Average filter-4 - t_statistics', 'Ref-Average filter-4 -P_value',
        'Random-Average filter-4 - t_statistics', 'Random-Average filter-4 -P_value'])+'\n')
        summary_file.write(summary_header)
        for rps_result_file in os.listdir(self._cdd_pred_files):
            protein_id = rps_result_file.split('.')[0]
            if protein_id in self._cdd_main_entry_dict.keys():
                individual_rps_result_fh = open(
                    self._cdd_pred_files+'/'+rps_result_file)
                for individual_rps_result_section in individual_rps_result_fh.read(
                    ).split('>gnl'):
                    if individual_rps_result_section.startswith('|CDD|'):
                        location = self._get_location(individual_rps_result_section)
                        stat_data = individual_rps_result_section.split("Score = ")
                        for individual_rps_result in stat_data[0].split('\n'):
                            if individual_rps_result.startswith('|CDD|'):
                                for entry in individual_rps_result.split('\n'):
                                    if '|CDD|' in entry:
                                        pssm_id = entry.split('|CDD|')[1].split(' ')[0]
                                        parent_id = entry.split(',')[0].split(' ')[1]
                                        if 'smart' in parent_id:
                                            domain_id = parent_id.replace(
                                                'smart', 'SM')
                                        elif 'pfam' in parent_id:
                                            domain_id = parent_id.replace(
                                                'pfam', 'PF')
                                        else:
                                            domain_id = parent_id
                                        cdd_main = ('%s\t%s\t%s' % (
                                            pssm_id, domain_id, location))
                                        if cdd_main in self._cdd_main_entry_dict[protein_id].keys():
                                            cdd_main_entry = self._cdd_main_entry_dict[protein_id][cdd_main]
                                            cdd_main_entry1 = '\t'.join(
                                                cdd_main_entry.split('\t')[0:5])
                                            cdd_main_entry2 = '\t'.join(
                                                cdd_main_entry.split('\t')[15:20])
                                            cdd_main_entry3 = '\t'.join(
                                                cdd_main_entry.split('\t')[23:26])
                                            
                                            cdd_main_entry_items = FilteredData(cdd_main_entry.split('\t'))
                                            coverage = float(cdd_main_entry_items.cover_length)
                                            coverage_percent = (float(cdd_main_entry_items.cover_length)/
                                                                float(cdd_main_entry_items.length))
                                            if coverage_percent > 1:
                                                coverage_percent = 1
                                            identity = cdd_main_entry_items.identity
                                            identity_percent = (float(cdd_main_entry_items.identity.split(
                                                '/')[0])/float(cdd_main_entry_items.cover_length))
                                            similarity = cdd_main_entry_items.similarity
                                            similarity_percent = (float(cdd_main_entry_items.similarity.split(
                                                '/')[0])/float(cdd_main_entry_items.cover_length))
                                            if not cdd_main_entry_items.gaps == 'None':
                                                gaps = cdd_main_entry_items.gaps
                                                ungap_percent = 1-(float(cdd_main_entry_items.gaps.split(
                                                '/')[0])/float(cdd_main_entry_items.cover_length))
                                            else:
                                                gaps = 0
                                                ungap_percent = 1
                                            for each_stat_group in stat_data[1:]:
                                                common_seq = []
                                                query_seq, subject_seq =  self._compile_cdd_stat(
                                                    each_stat_group)
                                                seq_distance = 0
                                                needle_cline_seq = NeedleCommandline(asequence="asis:"+query_seq,
                                                bsequence="asis:"+subject_seq, gapopen=0, gapextend=0, outfile="stdout")
                                                stdout, stderr = needle_cline_seq()
                                                for entry_seq in stdout.split('\n'):
                                                    if entry_seq.startswith("# Similarity: "):
                                                        seq_distance = float(entry_seq.strip().split(
                                                        '(')[1].split('%)')[0])/100
                                                query_dp_comp = self._compute_dp_comp(query_seq)
                                                subject_dp_comp = self._compute_dp_comp(subject_seq)
                                                dp_comp_distance = 1-distance.euclidean(
                                                    query_dp_comp, subject_dp_comp)/100
                                                
                                                query_tp_comp = self._compute_tp_comp(query_seq)
                                                subject_tp_comp = self._compute_tp_comp(subject_seq)
                                                tp_comp_distance = 1-distance.euclidean(
                                                    query_tp_comp, subject_tp_comp)/100
                                                
                                                query_mass, query_pi, query_solub, \
                                                query_vdw, query_pka = self._compute_properties(
                                                    query_seq)
                                                subject_mass, subject_pi, subject_solub, \
                                                subject_vdw, subject_pka = self._compute_properties(
                                                    subject_seq)
                                                 
                                                mass_score, mass_entry = self._calculate_score(
                                                    subject_mass, query_mass)
                                                pi_score, pi_entry = self._calculate_score(
                                                    subject_pi, query_pi)
                                                solub_score, solub_entry = self._calculate_score(
                                                    subject_solub, query_solub)
                                                vdw_score, vdw_entry = self._calculate_score(
                                                    subject_vdw, query_vdw)
                                                pka_score, pka_entry = self._calculate_score(
                                                    subject_pka, query_pka)
                                                
                                                query_ss = self._compute_sec_str(query_seq)
                                                subject_ss = self._compute_sec_str(subject_seq)
                                                #ss_distance = difflib.SequenceMatcher(
                                                #    None, query_ss, subject_ss).ratio()
                                                ss_distance = 0
                                                needle_cline_ss = NeedleCommandline(asequence="asis:"+query_ss,
                                                bsequence="asis:"+subject_ss, gapopen=0, gapextend=0, outfile="stdout")
                                                stdout, stderr = needle_cline_ss()
                                                for entry_ss in stdout.split('\n'):
                                                    if entry_ss.startswith("# Similarity: "):
                                                        ss_distance = float(entry_ss.strip().split(
                                                        '(')[1].split('%)')[0])/100
                                                query_pcn, query_pcn_comp = self._compute_group_aac(
                                                    query_seq)
                                                subject_pcn, subject_pcn_comp = self._compute_group_aac(
                                                    subject_seq)
                                                pcn_comp_distance = 1-distance.euclidean(
                                                    query_pcn_comp, subject_pcn_comp)/100
                                                filter1 = (coverage_percent+identity_percent+
                                                        similarity_percent+ungap_percent)/4
                                                filter2 = (float(mass_score)+ float(
                                                    pi_score)+ float(solub_score)+ float(vdw_score)+
                                                    float(pka_score))/5
                                                filter3 = (float(seq_distance)+
                                                         float(ss_distance))/2
                                                filter4 = (float(dp_comp_distance)+
                                                           float(tp_comp_distance)+
                                                         float(pcn_comp_distance))/3
                                                bayesian_score = (filter1 + filter2 + filter3 + filter4)/4
                                                self._ref_value_dict[protein_id][domain_id]['seq_distance'] = float(seq_distance)
                                                self._ref_value_dict[protein_id][domain_id]['ss_distance'] = float(ss_distance)
                                                #self._ref_value_dict[protein_id][domain_id]['pcn_distance'] = float(pcn_distance)
                                                self._ref_value_dict[protein_id][domain_id]['dp_comp_distance'] = float(dp_comp_distance)
                                                self._ref_value_dict[protein_id][domain_id]['tp_comp_distance'] = float(tp_comp_distance)
                                                self._ref_value_dict[protein_id][domain_id]['pcn_comp_distance'] = float(pcn_comp_distance)
                                                self._ref_value_dict[protein_id][domain_id]['filter-3'] = "%.4f" % float(filter3)
                                                self._ref_value_dict[protein_id][domain_id]['filter-4'] = "%.4f" % float(filter4)
                                                self._get_t_stats(protein_id, domain_id, query_seq, subject_seq)
                                                final_entry = "\t".join(map(str, [cdd_main_entry1,
                                                    cdd_main_entry2, cdd_main_entry3,
                                                    subject_seq, query_seq, subject_ss,
                                                    query_ss, coverage, identity,
                                                    similarity, gaps, 
                                                    "%.4f" % float(coverage_percent),
                                                    "%.4f" % float(identity_percent),
                                                    "%.4f" % float(similarity_percent),
                                                    "%.4f" % float(ungap_percent),
                                                    mass_entry, pi_entry,
                                                    solub_entry, vdw_entry, pka_entry,
                                                    "%.4f" % float(seq_distance),
                                                    "%.4f" % float(ss_distance),
                                                    "%.4f" % float(pcn_comp_distance),
                                                    "%.4f" % float(dp_comp_distance),
                                                    "%.4f" % float(tp_comp_distance),
                                                    "%.4f" % float(filter1), "%.4f" % float(
                                                        filter2), "%.4f" % float(filter3),
                                                    "%.4f" % float(filter4), bayesian_score]))
                                                summary_file.write(final_entry+'\n')
                                                filter3_file.write('\t'.join(map(str, [protein_id,
                                                    subject_seq, query_seq,
                                                    "%.4f" % float(seq_distance),
                                                    self._ref_t_stat[protein_id][domain_id]['seq_distance'],
                                                    self._ref_pval[protein_id][domain_id]['seq_distance'],
                                                    "%.4f" % float(ss_distance),
                                                    self._ref_t_stat[protein_id][domain_id]['ss_distance'],
                                                    self._ref_pval[protein_id][domain_id]['ss_distance'],
                                                    "%.4f" % float(filter3), self._ref_t_stat[protein_id][domain_id]['filter-3'],
                                                    self._ref_pval[protein_id][domain_id]['filter-3']]))+'\n')
                                                filter4_file.write('\t'.join(map(str, [protein_id,
                                                    subject_seq, query_seq,
                                                    "%.4f" % float(pcn_comp_distance),
                                                    self._ref_t_stat[protein_id][domain_id]['pcn_comp_distance'],
                                                    self._ref_pval[protein_id][domain_id]['pcn_comp_distance'],
                                                    "%.4f" % float(dp_comp_distance),
                                                    self._ref_t_stat[protein_id][domain_id]['dp_comp_distance'],
                                                    self._ref_pval[protein_id][domain_id]['dp_comp_distance'],
                                                    "%.4f" % float(tp_comp_distance),
                                                    self._ref_t_stat[protein_id][domain_id]['tp_comp_distance'],
                                                    self._ref_pval[protein_id][domain_id]['tp_comp_distance'],
                                                    "%.4f" % float(filter4), self._ref_t_stat[protein_id][domain_id]['filter-4'],
                                                    self._ref_pval[protein_id][domain_id]['filter-4']]))+'\n')
                                                filter3_dist_file.write('\t'.join(map(str, [protein_id,
                                                self._ref_t_stat[protein_id][domain_id]['seq_distance'],
                                                self._ref_pval[protein_id][domain_id]['seq_distance'],
                                                ','.join(self._t_stat_distribution[protein_id][domain_id]['seq_distance']),
                                                ','.join(self._pval_distribution[protein_id][domain_id]['seq_distance']),
                                                self._ref_t_stat[protein_id][domain_id]['ss_distance'],
                                                self._ref_pval[protein_id][domain_id]['ss_distance'],
                                                ','.join(self._t_stat_distribution[protein_id][domain_id]['ss_distance']),
                                                ','.join(self._pval_distribution[protein_id][domain_id]['ss_distance']),
                                                self._ref_t_stat[protein_id][domain_id]['filter-3'],
                                                self._ref_pval[protein_id][domain_id]['filter-3'],
                                                ','.join(self._t_stat_distribution[protein_id][domain_id]['filter-3']),
                                                ','.join(self._pval_distribution[protein_id][domain_id]['filter-3'])]))+'\n')
                                                filter4_dist_file.write('\t'.join(map(str, [protein_id,
                                                self._ref_t_stat[protein_id][domain_id]['pcn_comp_distance'],
                                                self._ref_pval[protein_id][domain_id]['pcn_comp_distance'],
                                                ','.join(self._t_stat_distribution[protein_id][domain_id]['pcn_comp_distance']),
                                                ','.join(self._pval_distribution[protein_id][domain_id]['pcn_comp_distance']),
                                                self._ref_t_stat[protein_id][domain_id]['dp_comp_distance'],
                                                self._ref_pval[protein_id][domain_id]['dp_comp_distance'],
                                                ','.join(self._t_stat_distribution[protein_id][domain_id]['dp_comp_distance']),
                                                ','.join(self._pval_distribution[protein_id][domain_id]['dp_comp_distance']),
                                                self._ref_t_stat[protein_id][domain_id]['tp_comp_distance'],
                                                self._ref_pval[protein_id][domain_id]['tp_comp_distance'],
                                                ','.join(self._t_stat_distribution[protein_id][domain_id]['tp_comp_distance']),
                                                ','.join(self._pval_distribution[protein_id][domain_id]['tp_comp_distance']),
                                                self._ref_t_stat[protein_id][domain_id]['filter-4'],
                                                self._ref_pval[protein_id][domain_id]['filter-4'],
                                                ','.join(self._t_stat_distribution[protein_id][domain_id]['filter-4']),
                                                ','.join(self._pval_distribution[protein_id][domain_id]['filter-4'])]))+'\n')
                individual_rps_result_fh.close()
        filter3_file.close()
        filter4_file.close()
        filter3_dist_file.close()
        filter3_dist_file.close()
        summary_file.close()
        
    def _get_t_stats(self, protein_id, domain_id, query_seq, ref_subject):
        ''''''
        value_dict = {}
        ref_subject_list = []
        ref_subject_list.append(ref_subject)
        query_aac = self._compute_each_aac(query_seq)
        query_ss = self._compute_sec_str(query_seq)
        query_dp_comp = self._compute_dp_comp(query_seq)
        query_tp_comp = self._compute_tp_comp(query_seq)
        query_pcn, query_pcn_comp = self._compute_group_aac(
            query_seq)
        value_dict.setdefault('seq_distance', []).append(
            self._ref_value_dict[protein_id][domain_id]['seq_distance'])
        value_dict.setdefault('ss_distance', []).append(
            self._ref_value_dict[protein_id][domain_id]['ss_distance'])
        #value_dict.setdefault('pcn_distance', []).append(
        #    self._ref_value_dict[protein_id][domain_id]['pcn_distance'])
        value_dict.setdefault('dp_comp_distance', []).append(
            self._ref_value_dict[protein_id][domain_id]['dp_comp_distance'])
        value_dict.setdefault('tp_comp_distance', []).append(
            self._ref_value_dict[protein_id][domain_id]['tp_comp_distance'])
        value_dict.setdefault('pcn_comp_distance', []).append(
            self._ref_value_dict[protein_id][domain_id]['pcn_comp_distance'])
        value_dict.setdefault('filter-3', []).append(
            self._ref_value_dict[protein_id][domain_id]['filter-3'])
        value_dict.setdefault('filter-4', []).append(
            self._ref_value_dict[protein_id][domain_id]['filter-4'])
        for i in range(1, 501):
            subject_list = list(ref_subject)
            random.shuffle(subject_list, random.random)
            subject_seq = ''.join(subject_list)
            ref_subject_list.append(subject_seq)
            seq_distance = 0
            needle_cline_seq = NeedleCommandline(asequence="asis:"+query_seq,
            bsequence="asis:"+subject_seq, gapopen=0, gapextend=0, outfile="stdout")
            stdout, stderr = needle_cline_seq()
            for entry_seq in stdout.split('\n'):
                if entry_seq.startswith("# Similarity: "):
                    seq_distance = float(entry_seq.strip().split(
                        '(')[1].split('%)')[0])/100
            subject_ss = self._compute_sec_str(subject_seq)
            ss_distance = 0
            needle_cline_ss = NeedleCommandline(asequence="asis:"+query_ss,
            bsequence="asis:"+subject_ss, gapopen=0, gapextend=0, outfile="stdout")
            stdout, stderr = needle_cline_ss()
            for entry_ss in stdout.split('\n'):
                if entry_ss.startswith("# Similarity: "):
                    ss_distance = float(entry_ss.strip().split(
                    '(')[1].split('%)')[0])/100
            subject_dp_comp = self._compute_dp_comp(subject_seq)
            dp_comp_distance = 1-distance.euclidean(
                query_dp_comp, subject_dp_comp)/100
            subject_tp_comp = self._compute_tp_comp(subject_seq)
            tp_comp_distance = 1-distance.euclidean(
                query_tp_comp, subject_tp_comp)/100
            subject_pcn, subject_pcn_comp = self._compute_group_aac(
                subject_seq)
            pcn_comp_distance = 1-distance.euclidean(
                query_pcn_comp, subject_pcn_comp)/100
            filter3 = (float(seq_distance)+
                    float(ss_distance))/2
            filter4 = (float(dp_comp_distance)+
                      float(tp_comp_distance)+
                    float(pcn_comp_distance))/3
            value_dict.setdefault('seq_distance', []).append(
                float(seq_distance))
            value_dict.setdefault('ss_distance', []).append(
                float(seq_distance))
            #value_dict.setdefault('pcn_distance', []).append(
            #    float(seq_distance))
            value_dict.setdefault('dp_comp_distance', []).append(
                float(seq_distance))
            value_dict.setdefault('tp_comp_distance', []).append(
                float(seq_distance))
            value_dict.setdefault('pcn_comp_distance', []).append(
                float(seq_distance))
            value_dict.setdefault('filter-3', []).append(filter3)
            value_dict.setdefault('filter-4', []).append(filter4)
        for value_key in sorted(value_dict.keys()):
            value_array = np.asarray(value_dict[value_key], float)
            t_stat, pval =  stats.ttest_1samp(value_array,
                        float(self._ref_value_dict[protein_id][domain_id][value_key]))
            self._ref_t_stat[protein_id][domain_id][value_key] = '%.4f' % float(t_stat)
            self._ref_pval[protein_id][domain_id][value_key] = '%.4f' % float(pval)
            for each_val in sorted(value_array):
                pval, t_stat =  stats.ttest_1samp(value_array,
                                                 each_val)
                self._t_stat_distribution[protein_id][domain_id][value_key].append(
                    '%.4f' % t_stat)
                self._pval_distribution[protein_id][domain_id][value_key].append(
                    '%.4f' % pval)
        return self._ref_t_stat, self._ref_pval, \
        self._t_stat_distribution, self._pval_distribution


    def _get_location(self, each_stat_group):
        '''Get locations of predicted domains'''
        start_list = []
        stop_list = []
        for each_stat_data in each_stat_group.split('\n'):
            if 'Expect' in each_stat_data:
                score = 'Score='+each_stat_data.split(',')[0]
                expect = 'Expect='+each_stat_data.split('Expect = '
                                                        )[1].strip()
            if 'Identities = ' in each_stat_data:
                identities = 'Identities='+each_stat_data.split(
                    'Identities = ')[1].split(',')[0]
                try:
                    gaps = 'Gaps='+each_stat_data.split(
                        'Gaps = ')[1].strip()
                    positives = 'Positives='+each_stat_data.split(
                        'Positives = ')[1].split(',')[0]
                except:
                    gaps = 'Gaps=None'
                    positives = 'Positives='+each_stat_data.split(
                        'Positives = ')[1].strip()
            if 'Query:' in each_stat_data:
                start_list.append(each_stat_data.split(' ')[1])
                stop_list.append(each_stat_data.split(' ')[-1].strip())
        start = start_list[0]
        stop = stop_list[-1]
        location = "%s\t%s" % (start, stop)
        return location

    def _compile_cdd_stat(self, each_stat_group):
        query_seq = []
        subject_seq = []
        for each_stat_data in each_stat_group.split('\n'):
            if 'Query:' in each_stat_data:
                query_seq.append(' '.join(
                    each_stat_data.strip().split()).split(' ')[2])
            if 'Sbjct:' in each_stat_data:
                subject_seq.append(' '.join(
                    each_stat_data.strip().split()).split(' ')[2])
        return ''.join(query_seq), ''.join(subject_seq)
    
    def _compute_properties(self, aa_list):
        ''''''
        prot_mass = 0
        prot_pi = 0
        prot_solub = 0
        prot_vdw = 0
        prot_pka = 0
        for aa in aa_list:
            try:
                prot_mass += self._amino_acid_mass[aa]
                prot_pi += self._amino_acid_isoelpt[aa]
                prot_solub += self._amino_acid_solubility[aa]
                prot_vdw += self._van_der_waal_volume[aa]
                prot_pka += self._acid_dissociation_pka[aa]
            except:
                pass
        return prot_mass, prot_pi, prot_solub, prot_vdw, prot_pka
    
    def _calculate_score(self, subject_val, query_val):
        '''calculatd scores of similarity between query and subject'''
        score = ''
        min_query_val = query_val-(query_val*15//100)
        max_query_val = query_val+(query_val*15//100)
        if subject_val >= min_query_val and subject_val <= max_query_val:
            score = 1
        else:
            score = 0
        score_entry = '%s (%.4f, %.4f)' % (score,
                    float(query_val), float(subject_val))
        return score, score_entry
        
    def _compute_sec_str(self, seq_line):
        '''Computes 3-state secondary structure'''
        str_list = []
        seq_dict = defaultdict(
            lambda: defaultdict(lambda: defaultdict()))
        for aa in seq_line:
            str_val = ''
            if aa == 'J':
                str_val = 'x'
            elif aa == 'X':
                str_val = 'x'
            else:
                for sec_str in self._amino_acid_str.keys():
                    if aa in self._amino_acid_str[sec_str]:
                        str_val = sec_str
            str_list.append(str_val)
        return ''.join(str_list)
        
    def _compute_each_aac(self, aa_list):
        ''''''
        aa_comp = []
        amino_acid_count = {
            'A' : 0, 'C' : 0, 'D' : 0, 'E' : 0, 'F' : 0,
            'G' : 0, 'H' : 0, 'I' : 0, 'K' : 0, 'L' : 0,
            'M' : 0, 'N' : 0, 'P' : 0, 'Q' : 0, 'R' : 0, '-' : 0,
            'S' : 0, 'T' : 0, 'V' : 0, 'W' : 0, 'Y' : 0, 'b' : 0,
            'O' : 0, 'U' : 0, 'X' : 0, 'B' : 0, 'Z' : 0, 'J' : 0
        }
        length = len(aa_list)
        
        for aa in aa_list:
            amino_acid_count[aa] = int(amino_acid_count[aa]) + 1
        if amino_acid_count['B'] > 0 or amino_acid_count['b'] > 0:
            amino_acid_count['D'] = int(amino_acid_count['D']
                                        ) + amino_acid_count['B']/2
            amino_acid_count['N'] = int(amino_acid_count['N']
                                        ) + amino_acid_count['B']/2
        if amino_acid_count['Z'] > 0:
            amino_acid_count['E'] = int(amino_acid_count['E']
                                        ) + amino_acid_count['Z']/2
            amino_acid_count['Q'] = int(amino_acid_count['Q']
                                        ) + amino_acid_count['Z']/2
        if amino_acid_count['J'] > 0:
            amino_acid_count['I'] = int(amino_acid_count['I']
                                        ) + amino_acid_count['J']/2
            amino_acid_count['L'] = int(amino_acid_count['L']
                                        ) + amino_acid_count['J']/2
        for aa_count in sorted(self._amino_acid_list):
            if not float(amino_acid_count[aa_count]) == 0:
                aa_comp.append(float(amino_acid_count[aa_count]
                                     )*100/int(length))
            else:
                aa_comp.append(0)
        return aa_comp
            
    def _compute_group_aac(self, aa_seq):
        ''''''
        amino_acid_count = {
        'a_polar' : 0, 'b_non_polar' : 0, 'c_neutral' : 0,
        'd_hydrophobic' : 0, 'e_hydrophilic' : 0,
        'f_van_der_waal=0-4' : 0, 'g_van_der_waal>4' : 0,
        'h_mid_polarity' : 0, 'i_high_polarity' : 0,
        'j_negative' : 0, 'k_positive' : 0, 'l_uncharged' : 0,
        'm_aliphatic' : 0, 'n_aromatic' : 0,
        'o_basic' : 0, 'p_acidic' : 0,
        'q_tiny' : 0, 'r_small' : 0, 's_large' : 0,
        't_mid_solvent_accebility' : 0, 'u_high_solvent_access' : 0,
        'v_essential' : 0, 'w_non_essential' : 0
        }
        aac_list = []
        aac_values = []
        length = len(aa_seq)
        for aa in aa_seq:
            if aa == 'B':
                for aa_type in amino_acid_count.keys():
                    if 'D' in self._amino_acid_ref[aa_type]:
                        aac_list.append(aa_type.split('_')[0])
                        amino_acid_count[aa_type] = int(
                            amino_acid_count[aa_type]) + 0.5
                for aa_type in amino_acid_count.keys():
                    if 'N' in self._amino_acid_ref[aa_type]:
                        aac_list.append(aa_type.split('_')[0])
                        amino_acid_count[aa_type] = int(
                            amino_acid_count[aa_type]) + 0.5
            elif aa == 'Z':
                for aa_type in amino_acid_count.keys():
                    if 'E' in self._amino_acid_ref[aa_type]:
                        aac_list.append(aa_type.split('_')[0])
                        amino_acid_count[aa_type] = int(
                            amino_acid_count[aa_type]) + 0.5
                for aa_type in amino_acid_count.keys():
                    if 'Q' in self._amino_acid_ref[aa_type]:
                        aac_list.append(aa_type.split('_')[0])
                        amino_acid_count[aa_type] = int(
                            amino_acid_count[aa_type]) + 0.5
            elif aa == 'J':
                for aa_type in amino_acid_count.keys():
                    if 'I' in self._amino_acid_ref[aa_type]:
                        aac_list.append(aa_type.split('_')[0])
                        amino_acid_count[aa_type] = int(
                            amino_acid_count[aa_type]) + 0.5
                for aa_type in amino_acid_count.keys():
                    if 'L' in self._amino_acid_ref[aa_type]:
                        aac_list.append(aa_type.split('_')[0])
                        amino_acid_count[aa_type] = int(
                            amino_acid_count[aa_type]) + 0.5
            elif aa == 'X':
                aac_list.append('X')
            else:
                for aa_type in amino_acid_count.keys():
                    if aa in self._amino_acid_ref[aa_type]:
                        aac_list.append(aa_type.split('_')[0])
                        amino_acid_count[aa_type] = int(
                            amino_acid_count[aa_type]) + 1
        for aa_count in sorted(amino_acid_count.keys()):
            if not float(amino_acid_count[aa_count]) == 0:
                aac_values.append(float(amino_acid_count[aa_count])
                *100/int(length))
            else:
                aac_values.append(0)
        return ''.join(aac_list), aac_values
    
    def _split_by_n( self, line, n ):
        """A generator to divide a sequence into chunks of n units."""
        seq = [line[i:i+n] for i in range(0, len(line), n)]
        return seq 
        
    def _compute_dp_comp(self, aa_list):
        '''Computes dipeptide composition'''
        aa_count = {}
        aa_comb_set = set()
        aa_final_list = []
        amino_acid_list = list(self._split_by_n(aa_list, 2))
        for comb in combinations(self._amino_acid_list, 2):
            aa_comb_set.add(''.join([comb[0], comb[1]]))
            aa_comb_set.add(''.join([comb[1], comb[0]]))
        for each_aa in amino_acid_list:
            aa_count.setdefault(each_aa, []).append(each_aa)
        for aa in sorted(list(aa_comb_set)):
            try:
                if aa_count[aa]:
                    aa_final_list.append(float(len(aa_count[aa])
                    *100/(len(aa_count.keys()))))
            except KeyError:
                aa_final_list.append(0)
        return aa_final_list

    def _compute_tp_comp(self, aa_list):
        ''''''     
        aa_count = {}
        aa_comb_set = set()
        aa_final_list = []
        amino_acid_list = list(self._split_by_n(aa_list, 3))
        for comb in combinations(self._amino_acid_list, 3):
            aa_comb_set.add(''.join([comb[0], comb[2], comb[1]]))
            aa_comb_set.add(''.join([comb[0], comb[1], comb[2]]))
            aa_comb_set.add(''.join([comb[1], comb[2], comb[0]]))
            aa_comb_set.add(''.join([comb[1], comb[0], comb[2]]))
            aa_comb_set.add(''.join([comb[2], comb[0], comb[1]]))
            aa_comb_set.add(''.join([comb[2], comb[1], comb[0]]))
        for each_aa in amino_acid_list:
            aa_count.setdefault(each_aa, []).append(each_aa)
        for aa in sorted(list(aa_comb_set)):
            try:
                if aa_count[aa]:
                    aa_final_list.append(float(len(aa_count[aa])
                    *100/(len(aa_count.keys()))))
            except KeyError:
                aa_final_list.append(0)
        return aa_final_list
    
class FilteredData(object):
    '''all the xml data detail'''
    def __init__(self, row):
        self.uid = row[0]
        self.entry_name = row[1]
        self.protein_name = row[2]
        self.species = row[3]
        self.length = row[4]
        self.gene_names = row[5]
        self.locus_tag = row[6]
        self.Type = row[7]
        self.go = row[8]
        self.embl = row[9]
        self.pdb = row[10]
        self.kegg = row[11]
        self.interpro = row[12]
        self.pfam = row[13]
        self.pubmed = row[14]
        self.resource = row[15]
        self.resource_id = row[16]
        self.domain_id = row[17]
        self.short_name = row[18]
        self.full_name = row[19]
        self.domain_kw = row[20]
        self.domain_go = row[21]
        self.members = row[22]
        self.dom_length = row[23]
        self.start = row[24]
        self.stop = row[25]
        self.evalue = row[26]
        self.bit_score = row[27]
        self.bits = row[28]
        self.cover_length = row[29]
        self.coverage_percent = row[30]
        self.identity = row[31]
        self.identity_percent = row[32]
        self.similarity = row[33]
        self.similarity_percent = row[34]
        self.gaps = row[35]
        self.gap_percent = row[36]
        self.parameter_tag = row[-1]
    
if __name__ == '__main__':
    
    main()

