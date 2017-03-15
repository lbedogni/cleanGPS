#!/bin/bash
for file in `ls raw/milano/`
do
	NUMBER=`echo ${file} | sed 's/\.txt//g'`
	if [ ! -f milan_out_20150305/${NUMBER}.txt_${NUMBER}.csv ]
	then
		NUM=`cat raw/milano/${file} | grep "02-05" | wc -l`
#		echo ${NUM}
		if [ $NUM -gt 1 ]
		then
#		echo "${NUMBER},"
		echo ${NUMBER}
#		if [ -f beijing_tmp_20080205/${NUMBER}.txt_${NUMBER}.csv ]
#		then
#			rm raw/beijing/.done_20080205_${NUMBER}.txt
#		else
#			touch raw/beijing/.done_20080205_${NUMBER}.txt
		fi
#		else
#			rm beijing_tmp_20080205/.done_20080205_${NUMBER}.txt_${NUMBER}.csv
#		fi
	fi
done
