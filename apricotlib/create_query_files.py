#!/usr/bin/env python 

import sys

__description__ = '''The script creates files to compile user provided keywords
 for domain selection and classification'''
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def create_uid_query_file(uids, query_path):
    ''''''
    with open(query_path, 'a') as out_fh:
        if ',' in uids or ' ' not in uids:
            for uid in uids.split(','):
                out_fh.write("%s:%s\n" % (uid, uid))
        else:
            print(
                "Query Error Message:\nPlease check that the query UniProt "
                "ids are separated by comma\n")


def create_gene_query_file(geneids, query_path, proteome_path):
    entry_dict = create_gene_dict(proteome_path)
    with open(query_path, 'a') as out_fh:
        if ',' in geneids or ' ' not in geneids:
            mapped_data = map_gene_to_uid(geneids, entry_dict)
            for each_map in sorted(mapped_data.keys()):
                entry = "%s:%s" % (
                    each_map, ','.join(list(mapped_data[each_map])))
                print(entry)
                out_fh.write(entry+'\n')
        else:
            print(
                "Query Error Message:\nPlease check that the query "
                "UniProt ids are separated by comma\n")


def create_gene_dict(proteome_path):
    entry_dict = {}
    with open(proteome_path, 'r') as in_fh:
        for entry in in_fh:
            uid = entry.split('\t')[0]
            entry_dict[entry] = uid
    return entry_dict


def map_gene_to_uid(geneids, entry_dict):
    mapped_data = {}
    if ',' in geneids or ' ' not in geneids:
        for each_gene in geneids.split(','):
            if ' ' in each_gene:
                each_gene = each_gene.replace(' ', '')
            gene = each_gene.lower()
            for entry in entry_dict.keys():
                if gene in entry.split('\t')[0].lower():
                    mapped_data.setdefault(
                        each_gene, set()).add(entry_dict[entry])
                elif gene in entry.split('\t')[1].split('_')[0].lower():
                    mapped_data.setdefault(
                        each_gene, set()).add(entry_dict[entry])
                elif gene+' ' in entry.split('\t')[3].lower(
                ) or ' '+gene in entry.split('\t')[3].lower():
                    mapped_data.setdefault(
                        each_gene, set()).add(entry_dict[entry])
                elif gene+' ' in entry.split('\t')[4].lower(
                ) or ' '+gene in entry.split('\t')[4].lower():
                    mapped_data.setdefault(
                        each_gene, set()).add(entry_dict[entry])
            if gene not in mapped_data.keys():
                mapped_data.setdefault(each_gene, set()).add('unmapped')
    return mapped_data


def create_proteome_query_file(query, query_path, proteome_path):
    ''''''
    with open(query_path, 'a') as out_fh:
        with open(proteome_path, 'r') as in_fh:
            for entry in in_fh:
                if 'Entry' not in entry:
                    out_fh.write("%s\n" % (entry.split('\t')[0]))

if __name__ == '__main__':
    qids = sys.argv[1]
    query_path = sys.argv[2]
    try:
        proteome_path = sys.argv[3]
        if qids == 'proteome':
            create_proteome_query_file(qids, query_path, proteome_path)
        else:
            create_gene_query_file(qids, query_path, proteome_path)
    except:
        create_uid_query_file(qids, query_path, proteome_path)
