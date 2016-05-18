
#!/usr/bin/env python 

import os
import argparse

__description__ = "Sets up all the required folders for APRICOT analysis"
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"
__version__ = ""


def setup_analysis_folders(analysis_path):
    '''sets up folder for APRICOT analysis,
    default folder name is APRICOT_analysis'''
    create_main_folders(analysis_path)
    create_domain_analysis_path(analysis_path)
    create_subanalysis_path(analysis_path)


def create_main_folders(analysis_path):
    '''creates main folders in the APRICOT analysis folder'''
    if not os.path.exists(analysis_path):
        os.mkdir(analysis_path)
    if not os.path.exists('source_files'):
        os.mkdir('source_files')
    if not os.path.exists(analysis_path+'/input'):
        os.mkdir(analysis_path+'/input')
    if not os.path.exists(analysis_path+'/output'):
        os.mkdir(analysis_path+'/output')


def create_domain_analysis_path(analysis_path):
    '''sets up domain analysis and output folders'''
    if not os.path.exists('source_files/domain_data'):
        os.mkdir('source_files/domain_data')
    if not os.path.exists('source_files/reference_db_files'):
        os.mkdir('source_files/reference_db_files')
    if not os.path.exists(
            'source_files/domain_data/cdd'):
        os.mkdir(
                'source_files/domain_data/cdd')
    if not os.path.exists(
            'source_files/domain_data/interpro'):
        os.mkdir(
                'source_files/domain_data/interpro')


def create_subanalysis_path(analysis_path):
    '''create sub paths in the analysis folders'''
    for paths in ('input/query_proteins',
                  'input/mapped_query_annotation',
                  'input/uniprot_reference_table',
                  'output/0_predicted_domains',
                  'output/1_compiled_domain_information',
                  'output/2_selected_domain_information',
                  'output/3_annotation_scoring',
                  'output/4_additional_annotations',
                  'output/5_analysis_summary',
                  'output/format_output_data',
                  'output/visualization_files'):
        if not os.path.exists(analysis_path+'/'+paths):
            os.mkdir(analysis_path+'/'+paths)
    for sub_analysis_path in (
        'input/mapped_query_annotation/xml_path_mapped_query',
        'input/mapped_query_annotation/fasta_path_mapped_query',
        'input/mapped_query_annotation/mapped_protein_xml_info_tables',
        'output/0_predicted_domains/cdd_analysis',
        'output/0_predicted_domains/ipr_analysis',
        'output/1_compiled_domain_information/selected_data',
        'output/1_compiled_domain_information/unfiltered_data',
        'output/2_selected_domain_information/classified_data',
        'output/2_selected_domain_information/combined_data',
        'output/4_additional_annotations/protein_localization',
        'output/4_additional_annotations/protein_secondary_structure',
        'output/4_additional_annotations/pdb_sequence_prediction',
        'output/format_output_data/excel_files',
        'output/format_output_data/html_files',
        'output/visualization_files/overview_and_statistics',
        'output/visualization_files/secondary_structure',
        'output/visualization_files/subcellular_localization',
        'output/visualization_files/homologous_pdb_msa',
            'output/visualization_files/domain_highlighting'):
        if not os.path.exists(analysis_path+'/'+sub_analysis_path):
            os.mkdir(analysis_path+'/'+sub_analysis_path)
            
if __name__ == '__main__':
    analysis_path = sys.argv[1]
    setup_analysis_folders(analysis_path)
