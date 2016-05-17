#!/usr/bin/env python 
import sys
import re
import time

def read_html_file(input_file, output_file):
    month_dict = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6, 'Jul' : 7,
                  'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12}
    all_versions = {}
    with open(input_file) as in_fh:
        if 'ipr_info.html'in input_file:
            for entry in in_fh.read().split('<pre>')[1].split('\n'):
                list1 = []
                for each in entry.split(' '):
                    if not each == '':
                        list1.append(each)
                try:
                    date = "%s/%s/%s" % (list1[2], month_dict[list1[1]], list1[0])
                    newdate = time.strptime(date, "%d/%m/%Y")
                    try:
                        all_versions[newdate] = list1[-1].split('>5.')[1].split('/<')[0]
                    except IndexError:
                        pass
                except IndexError:
                    pass
            with open(output_file, 'w') as out_fh:
                out_fh.write('5.'+all_versions[max(all_versions.keys())])
                
        elif 'ipr_flatfile.html' in input_file:
            with open(output_file, 'w') as out_fh:
                for entry in in_fh.read().split('<pre>')[1].split('\n'):
                    if '>Current</a> -> ' in entry:
                        out_fh.write(entry.split('>Current</a> -> ')[1])

if __name__ == '__main__':
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    read_html_file(input_file, output_file)