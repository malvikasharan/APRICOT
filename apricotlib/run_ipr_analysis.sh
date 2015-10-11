#!/usr/bin/env sh
#AUTHOR: Malvika Sharan {malvikasharan@gmail.com}
#Date: 2015-08-07

DB_PATH=$1
UP_FASTA_PATH=$2
DOMAIN_PREDICTION=$3

main(){
    run_ipr_analysis
}

run_ipr_analysis(){
    for fasta in $(ls $UP_FASTA_PATH)
    do
        FILE_PATH=$UP_FASTA_PATH/$fasta
        ipr_file=$(echo $fasta | cut -d '.' -f 1)        
        if [ ! -f $DOMAIN_PREDICTION/$ipr_file.tsv ]
        then
            echo InterProScan analysis for $ipr_file is running...
            bash $DB_PATH/interproscan.sh \
            -i $FILE_PATH -b $DOMAIN_PREDICTION/$ipr_file \
            -f tsv -dp -goterms
        else
            echo InterPro based analysis result for $ipr_file exists.
        fi
    done
    echo Finished running InterProScan analysis.
}

main