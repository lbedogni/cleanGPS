#!/bin/bash

#turin
DANTIMESTART="20150304"
DANTIMESTOP="20150305"
if [ $2 == "turin" ]
then
	./toolchain_20160713.py $1 True 7.3 44.8 8 45.22 ${DANTIMESTART} ${DANTIMESTOP} turin
elif [ $2 == "rome" ]
then
	./toolchain_20160713.py $1 True 11 40 13 43 ${DANTIMESTART} ${DANTIMESTOP} rome
fi
