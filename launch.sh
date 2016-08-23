#!/bin/bash

#turin
DANTIMESTART="20150304"
DANTIMESTOP="20150305"
if [ $2 == "turin" ]
then
	./toolchain_20160713.py $1 True 44.8 7.3 45.22 8 ${DANTIMESTART} ${DANTIMESTOP} turin
elif [ $2 == "rome" ]
then
	./toolchain_20160713.py $1 True 40 11 43 13 ${DANTIMESTART} ${DANTIMESTOP} rome
elif [ $2 == "newyork" ]
then
	./toolchain_20160713.py $1 True 39.5 -75 42 -72 20131204 20131205 nyc
fi
