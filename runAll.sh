rm outfile.csv
for file in `ls $1`
do
	./getTimes.py $1/$file
done
