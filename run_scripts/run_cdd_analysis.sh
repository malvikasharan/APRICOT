#!/usr/bin/env sh
#AUTHOR: Malvika Sharan {malvikasharan@gmail.com}
#Date: 2015-08-07

DB_PATH=$1
UP_FASTA_PATH=$2
DOMAIN_PREDICTION=$3

main(){
    cdd_analysis
}

cdd_analysis(){
    echo "########"
    for fasta in $(ls $UP_FASTA_PATH)
    do
        FILE_PATH=$UP_FASTA_PATH/$fasta
        rps_file=$(echo $fasta | cut -d '.' -f 1)
        if [ ! -f $DOMAIN_PREDICTION/$rps_file.txt ]
        then
            echo RPS-BLAST analysis for $rps_file is running...
            rpsblast -i $FILE_PATH -d $DB_PATH/Cdd \
            -o $DOMAIN_PREDICTION/$rps_file.txt 
        else
            echo CDD based analysis result for $rps_file exists.
        fi
    done
    echo Finished running RPS-BLAST analysis.
}

main