rm ${2}_speeds.csv
for file in `find $1`
do
	echo $file
	./getSpeeds.py $file ${2}
done
