inpath='documentation'
outpath='source'

for files in $inpath/*.md
do
	filename=$(basename `echo $files | cut -d '.' -f 1`)
	pandoc --from=markdown --to=rst --output=source/$filename.rst $files
done
