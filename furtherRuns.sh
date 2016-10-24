#!/bin/bash
for file in `ls raw/beijing/`
do
	NUMBER=`echo ${file} | sed 's/\.txt//g'`
	if [ ! -f beijing_out_20080206/${NUMBER}.txt_${NUMBER}.csv ]
	then
		rm raw/beijing/.done_20080205_${file}
	fi
done
