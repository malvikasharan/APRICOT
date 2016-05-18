#!/usr/bin/env python 

import argparse
import os

__description__ = "Maps each domains to their corresponding domains from InterPro"
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("go_path")
    parser.add_argument("interpro_to_go")
    parser.add_argument("interpro_data")
    parser.add_argument("cdd_data")
    args = parser.parse_args()
    
    map_domain_to_go = MapDomainToGo(
        args.go_path, args.interpro_to_go,
        args.interpro_data, args.cdd_data)
    map_domain_to_go.read_obo_file()
    map_domain_to_go.map_interpro_to_domains()
    map_domain_to_go.read_mapped_go_data()
    map_domain_to_go.map_cdd_to_go()


class MapDomainToGo(object):

    def __init__(self, go_path,
                 interpro_to_go,
                 interpro_data,
                 cdd_data):
        self._go_path = go_path
        self._interpro_to_go = interpro_to_go
        self._interpro_data = interpro_data
        self._cdd_data = cdd_data
        
        self._go_info_dict = {}
        self._interpro_domain_dict = {}
        self._domain_interpro_dict = {}
        self._interpro_go_dict = {}
        
    def read_obo_file(self):
        '''parses and reads the GO obo file'''
        out_fh = open(self._go_path+'/go_obo_table.csv', 'w')
        for go_file in os.listdir(self._go_path):
            go_fh = open(self._go_path+'/'+go_file, 'r')
            if '.obo' in go_file:
                for entry in go_fh.read().split('[Term]'):
                    if 'id: GO:' in entry:
                        info_dict = {}
                        for info in entry.split('\n'):
                            if info.startswith('id: GO:'):
                                info_dict["go_id"] = info.split(
                                    ': ')[1].strip()
                            if "name:" in info:
                                info_dict["name"] = info.split(
                                    ': ')[1].strip()
                            if "namespace:" in info:
                                if "biological_process" in info:
                                    info_dict["namesp"] = 'bp'
                                elif "cellular_component" in info:
                                    info_dict["namesp"] = 'cc'
                                elif "molecular_function" in info:
                                    info_dict["namesp"] = 'mf'
                        out_fh.write("%s:%s\t%s\n" % (
                                info_dict["namesp"], info_dict["go_id"],
                                info_dict["name"]))
                        self._go_info_dict[info_dict["go_id"]] = (
                            "%s:%s [%s]" % (info_dict["namesp"],
                            info_dict["go_id"], info_dict["name"]))
            go_fh.close()
        out_fh.close()
        return self._go_info_dict
    
    def map_interpro_to_domains(self):
        '''maps ipr ids to domain ids'''
        with open(self._interpro_data, 'r') as in_fh:
            for entry in in_fh:
                ipr_id = entry.split('\t')[0]
                domain_ids = entry.strip().split('\t')[-1]
                self._interpro_domain_dict[ipr_id] = domain_ids
                if '|' in domain_ids:
                    for domains in domain_ids.split('|'):
                        self._domain_interpro_dict[domains] = ipr_id
                else:
                    self._domain_interpro_dict[domain_ids] = ipr_id
        return self._interpro_domain_dict, self._domain_interpro_dict

    def read_mapped_go_data(self):
        '''maps domains to go id'''
        with open(self._interpro_to_go, 'r') as interpro_to_go_fh:
            for mapped_entry in interpro_to_go_fh:
                if "InterPro:" in mapped_entry:
                    ipr_id = mapped_entry.split('InterPro:'
                                                )[1].split(' ')[0]
                    go_id = mapped_entry.split(';')[-1].split(
                        'GO:')[1].strip()
                    self._interpro_go_dict.setdefault(
                        ipr_id, []).append("GO:%s" % go_id)
        with open(self._go_path+'/mapped_interpro_to_go.csv',
                  'w') as map_out_fh:
            with open(self._go_path+'/unmapped_interpro_to_go.csv',
                      'w') as unmap_out_fh:
                for ipr in set(self._interpro_domain_dict.keys()):
                    if ipr in set(self._interpro_go_dict.keys()):
                        if len(self._interpro_go_dict[ipr]) > 1:
                            go_list = []
                            for go in self._interpro_go_dict[ipr]:
                                try:
                                    go_list.append(self._go_info_dict[go])
                                except KeyError:
                                    go_list.append('%s: No description' % go)
                            map_out_fh.write("%s\t%s\t%s\n" % (
                                ipr, self._interpro_domain_dict[ipr],
                                ','.join(go_list)))
                        else:
                            map_out_fh.write("%s\t%s\t%s\n" % (
                                ipr, self._interpro_domain_dict[ipr],
                                self._go_info_dict[
                                    self._interpro_go_dict[ipr][0]]))
                    else:
                        unmap_out_fh.write("%s\t%s\n" % (
                            ipr, self._interpro_domain_dict[ipr]))
        return self._interpro_go_dict
    
    def map_cdd_to_go(self):
        '''maps cdd to go and interpro'''
        map_go_fh = open(
            self._go_path+'/mapped_cdd_to_go.csv', 'w')
        unmap_go_fh = open(
            self._go_path+'/unmapped_cdd_to_go.csv', 'w')
        map_ipr_fh = open(
            self._go_path+'/mapped_cdd_to_interpro.csv', 'w')
        unmap_ipr_fh = open(
            self._go_path+'/unmapped_cdd_to_interpro.csv', 'w')
        interpro_path = '/'.join(self._interpro_to_go.split('/')[0:-1])
        ipr_map_cdd_length = open(
            interpro_path+'/mapped_interpro_to_cdd_length.csv', 'w')
        with open(self._cdd_data, 'r') as cdd_data_fh:
            for cdd_entry in cdd_data_fh:
                cdd_id = cdd_entry.split('\t')[0]
                cdd_db_id = cdd_entry.split('\t')[1]
                cdd_length = cdd_entry.strip().split('\t')[-1]
                if 'pfam' in cdd_db_id:
                    cdd_db_id = cdd_db_id.replace('pfam', 'PF')
                if 'smart' in cdd_db_id:
                    cdd_db_id = cdd_db_id.replace('smart', 'SM')
                if cdd_db_id in set(self._domain_interpro_dict.keys()):
                    ipr = self._domain_interpro_dict[cdd_db_id]
                    ipr_map_cdd_length.write("%s\t%s\t%s\t%s\t%s\n" % (
                        ipr, self._interpro_domain_dict[ipr],
                        cdd_id, cdd_db_id, cdd_length))
                    map_ipr_fh.write("%s\t%s\t%s\t%s\n" % (
                        cdd_id, cdd_db_id,
                        ipr, self._interpro_domain_dict[ipr]))
                    try:
                        if self._interpro_go_dict[ipr]:
                            if len(self._interpro_go_dict[ipr]) > 1:
                                go_list = []
                                for go in self._interpro_go_dict[ipr]:
                                    go_list.append(self._go_info_dict[go])
                                map_go_fh.write("%s\t%s\t%s\n" % (
                                    cdd_id, cdd_db_id, ','.join(go_list)))
                            else:
                                map_go_fh.write("%s\t%s\t%s\n" % (
                                    cdd_id, cdd_db_id, self._go_info_dict[
                                        self._interpro_go_dict[ipr][0]]))
                    except KeyError:
                        unmap_go_fh.write("%s\t%s\n" % (
                            cdd_id, cdd_db_id))
                else:
                    unmap_ipr_fh.write("%s\t%s\n" % (cdd_id, cdd_db_id))
        ipr_map_cdd_length.close()
        map_go_fh.close()
        unmap_go_fh.close()
        map_ipr_fh.close()
        unmap_ipr_fh.close()

if __name__ == '__main__':
    
    main()

