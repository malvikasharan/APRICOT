#!/usr/bin/env python 

import sys
from datetime import datetime as DT

__description__ = '''Find the current version of InterProData'''
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def read_html_file(input_file, output_file):
    month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
                  'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
                  'Nov': 11, 'Dec': 12}
    with open(input_file) as in_fh:
        version_link = {}
        version_list = []
        for entry in in_fh.read().split('<pre>')[1].split('\n'):
            if 'Directory' in entry and not 'lookup_service' \
            in entry and not 'users' in entry and not 'old_releases' in entry:
                date_data = entry.split('Directory')[0].strip().replace(':', ' ').split(' ')
                year = int(date_data[0])
                month = int(month_dict[date_data[1]])
                date = int(date_data[2])
                try:
                    time = int(date_data[3])
                except IndexError:
                    time = 0
                version = entry.split('/</a>')[0].split('">')[-1]
                version_link[DT(year, month, date, time)] = version
                version_list.append(DT(year, month, date, time))
        latest_version = max(version_list)
        print("Current version: %s" % version_link[latest_version])
        with open(output_file, 'w') as out_fh:
            out_fh.write(version_link[latest_version])

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    read_html_file(input_file, output_file)
