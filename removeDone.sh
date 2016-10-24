#!/bin/bash
for line in `cat ListFiles.log`
do
	BB=`basename ${line} | awk -F"_" '{print $1}'`
	FULL="raw/turin/separated/.done_20150304_${BB}"
	FULL2="turin_tmp_20150304/${BB}_${BB}"
	FULL3="turin_tmp_20150304/.done_20150304_${BB}_${BB}"
	FULL4="turin_out_20150305/${BB}_${BB}"
	rm ${FULL} ${FULL2} ${FULL3} ${FULL4}
done
