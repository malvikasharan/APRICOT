#!/usr/bin/env python 

import os
import sys

__description__ = "Merges domains files selected from CDD and InterPro"
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def merge_domain_data(cdd_domains, ipr_domains, merged_file):
    with open(merged_file, 'w') as out_fh:
        header = '\t'.join(['ReferenceId', 'DomainId',
                            'ShortName', 'FullName',
                            'Members', 'Length', 'SelectionTerm'])+'\n'
        out_fh.write(header)
        if os.path.exists(cdd_domains):
            with open(cdd_domains, 'r') as cdd_fh:
                out_fh.write(cdd_fh.read()+'\n')
        if os.path.exists(ipr_domains):
            with open(ipr_domains, 'r') as ipr_fh:
                out_fh.write(ipr_fh.read()+'\n')

if __name__ == '__main__':
    cdd_domains = sys.argv[1]
    ipr_domains = sys.argv[2]
    merged_file = sys.argv[3]
    merge_domain_data(cdd_domains, ipr_domains, merged_file)
