#!/bin/bash
#for i in 10 20 30 60 100 180 240 300
for i in 100
do
	rm -rf errors_final_${i}
	mkdir errors_final_${i}
	for file in `ls final_${i}/interp*`
	do
		./computeErrorsFromDistance.py ${file}
	done
	cat total_errors.csv | awk '{print $1 " " $2}' > total_errors_LI_${i}.csv
	cat total_errors.csv | awk '{print $1 " " $3}' > total_errors_TH_${i}.csv
	cat total_errors.csv | awk '{print $1 " " $4}' > total_errors_OU_${i}.csv
	rm total_errors.csv
done		
