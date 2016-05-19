#!/usr/bin/env python 

import argparse
import os
try:
    import subprocess
except ImportError:
    print('Python package subprocess is missing. Please install/update.\n')
    sys.exit(0)
try:
    from Bio.Blast import NCBIXML
except ImportError:
    print('Python package Biopython is missing. Please install/update.\n')
    sys.exit(0)

__description__ = "Lists homologous PDB structures for the selected proteins"
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    '''all commandline arguement dclaration'''
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("selected_poteins")
    parser.add_argument("pdb_path")
    parser.add_argument("fasta_path")
    parser.add_argument("outpath")
    args = parser.parse_args()

    pdb_homology_analysis = PdbHomologyAnalysis(
        args.selected_proteins, args.pdb_path,
        args.fasta_path, args.outpath)
    pdb_homology_analysis.parse_selected_data()
    pdb_homology_analysis.run_pdb_analysis()
    pdb_homology_analysis.parse_blast_xml()
    pdb_homology_analysis.create_job_completion_file()


class PdbHomologyAnalysis(object):
    def __init__(self, selected_proteins, pdb_path,
                 fasta_path, outpath):
        self._selected_proteins = selected_proteins
        self._pdb_path = pdb_path
        self._fasta_path = fasta_path
        self._outpath = outpath
        
        self._selected_protein_set = set()
        
    def streamline_pdb_homology_analysis(self):
        self.parse_selected_data()
        self.run_pdb_analysis()
        self.parse_blast_xml()
        self.create_job_completion_file()
        
    def parse_selected_data(self):
        with open(self._selected_proteins, 'r') as in_fh:
            for entry in in_fh:
                if not entry.startswith('Entry'):
                    self._selected_protein_set.add(entry.split('\t')[0])
        return self._selected_protein_set
    
    def run_pdb_analysis(self):
        for files in os.listdir(self._fasta_path):
            if files.split('.')[0] in self._selected_protein_set:
                print("PDB homology analysis for %s" % files)
                subprocess.Popen(
                    ["bin/reference_db_files/blast/blastp -query %s/%s -db "
                     "%s -task blastp -outfmt 0 -out %s/%s.txt" % (
                        self._fasta_path, files, self._pdb_path,
                        self._outpath, files.split('.')[0])],
                    shell=True).wait()
                subprocess.Popen(
                    ["bin/reference_db_files/blast/blastp -query %s/%s "
                     "-db %s -task blastp -outfmt 5 -out %s/%s.xml" % (
                         self._fasta_path, files, self._pdb_path,
                         self._outpath, files.split('.')[0])],
                    shell=True).wait()
                
    def parse_blast_xml(self):
        '''parese blast xml to get seq'''
        for files in os.listdir(self._outpath):
            if '.xml' in files:
                data_list = []
                hit_set = set('None')
                identity_align_dict = {}
                with open(self._outpath+'/'+files) as blast_fh:
                    blast_records = NCBIXML.parse(blast_fh)
                    for blast_record in blast_records:
                        for alignment in blast_record.alignments:
                            pdb_id = alignment.title.split(
                                " ")[1].split(':')[0]
                            sub_id = alignment.title.split(
                                " ")[1].split(':')[1]
                            pdb_header = "%s_%s" % (pdb_id, sub_id)
                            for hsp in alignment.hsps:
                                align_seq = hsp.sbjct
                                hsp_identity = hsp.identities
                                identity_align_dict[float(hsp_identity)
                                ] = ">%s (hsp_identity: %s)\n%s\n" % (
                                    pdb_header, hsp_identity, align_seq)
                with open(self._outpath+'/' + files.split('.')[0] +
                          '_top5.fasta', 'w') as out_fh:
                    with open(self._fasta_path+'/'+files.split('.')[0]
                              + '.fasta', 'r') as fa_fh:
                        fasta_line = []
                        for entry in fa_fh:
                            if '>' in entry:
                                out_fh.write(">%s\n" % entry.split('|')[1])
                            else:
                                fasta_line.append(entry.strip())
                        out_fh.write(''.join(fasta_line)+'\n')
                    for entry in reversed(sorted(identity_align_dict.keys())):
                        hit_id = identity_align_dict[
                            entry].split('>')[1].split(' ')[0]
                        if hit_id not in hit_set and not len(list(
                                hit_set)) > 6:
                            hit_set.add(hit_id)
                            out_fh.write(identity_align_dict[entry])

    def create_job_completion_file(self):
        with open(self._outpath+'/pdb_analysis.txt', 'w') as out_fh:
            out_fh.write("Structural homologs for the selected "
                         "proteins are calculated from PDB database.\n")
            out_fh.write("The files generated by the analysis:.\n")
            out_fh.write('\n'.join(os.listdir(self._outpath)))
    
if __name__ == '__main__':
    main
