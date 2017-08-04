#!/usr/bin/env python
# Description = Stores user provided keywords in files.


def keyword_domains_files(kw_file_path, keywords):
    with open(kw_file_path+'/keywords_for_domain_selection.txt',
              'w') as out_fh:
        try:
            if ',' in keywords:
                for each_kw in keywords.split(','):
                    if ' ' in each_kw:
                        each_kw.replace(' ', '-')
                    out_fh.write('%s\n' % each_kw)
            else:
                out_fh.write(keywords)
                print("------\nSingle keyword for domain selection "
                      "has been given.")
                print("Multiple keywords can be provided as comma separated "
                      "list.\n------")
        except:
            print("Please provide the keywords for domain selection using the flag -kw")

def keyword_class_files(kw_file_path, keywords):
    with open(kw_file_path+'/keywords_for_result_classification.txt',
              'w') as out_fh:
        if ',' in keywords:
            out_fh.write('\n'.join(keywords.split(',')))
        else:
            out_fh.write(keywords)
            print("------\nSingle keyword for result "
                  "classification has been given.")
            print("Multiple keywords can be provided as "
                  "comma separated list.\n------")
