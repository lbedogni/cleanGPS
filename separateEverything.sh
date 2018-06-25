#!/bin/bash
# Usage thisfile.sh interp_file file_to_split delta_time_in_sec time_position divide_for_1000 prefix
rm -rf tmp
mkdir final

for interpfile in `find cologne_interpolation_100s -type f`
do
	echo ${interpfile}
	./splitInterpFiles.py $interpfile 7200 1
	for file in `ls tmp/interp_*`
	do
		./splitComputedFile.py ${file} cologne_out_100s/`basename ${interpfile}`_`basename ${interpfile}` 7200 1 False our
	done

	for file in `ls tmp/interp_*`
	do
		cat COLOGNE/calibrated/cologne_gap_100/`basename ${interpfile}` | sed 's/,/ /g' > tmp_their_file
		mv tmp_their_file `basename ${interpfile}`
		./splitComputedFile.py ${file} `basename ${interpfile}` -10800 1 True their
		rm `basename ${interpfile}`
	done

	mv tmp/* final/
done
