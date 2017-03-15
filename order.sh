#!/bin/bash
for file in `find ${1}`
do
	cat ${file} | sort -n -k 4 > .tmpfile
	mv .tmpfile ${file}
done
