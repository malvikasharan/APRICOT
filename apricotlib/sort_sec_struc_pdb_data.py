#!/usr/bin/env python 

import os       
import sys
import argparse

__description__ = "Sorts secondary structre and sequence from PDB"
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


parser = argparse.ArgumentParser()
parser.add_argument("-i","--pdb_ss_file",help="input secondary structure")
parser.add_argument("-seq","--pdb_seq_path",help="output pdb sequence")
parser.add_argument("-str","--pdb_str_path", help="output pdb structure")
args = parser.parse_args()

def main():
    "Sorts secondary structre and sequence from PDB"
    sequence_id_dict = {}
    out_seq_file = args.pdb_seq_path+'/pdb_sequence.txt'
    out_ss_file = args.pdb_str_path+'/pdb_secstr.txt'
    
    with open(args.pdb_ss_file) as in_fh:
        with open(out_seq_file, 'w') as out_seq_fh:
            with open(out_ss_file, 'w') as out_ss_fh:
                for data in in_fh.read().split('>'):
                    if "sequence" in data:
                        seq_id = data.split(':')[0]
                        sequence_id_dict[seq_id] = data
                        out_seq_fh.write('>%s'%data)
                    elif "secstr" in data:
                        str_id = data.split(':')[0]
                        data = data.replace(' ', '0')
                        seq_len = (len(sequence_id_dict[str_id]) - len(data))
                        for short in range(int(seq_len)):
                            data = data.strip()+'0'
                        out_ss_fh.write('>%s'%data)
                            
if __name__ == '__main__':
    
    main()   
