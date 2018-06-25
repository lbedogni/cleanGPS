#!/bin/bash

#turin
DANTIMESTART="20150304"
DANTIMESTOP="20150305"
touch ${2}.cache.nearest.csv
if [ $2 == "turin" ]
then
	./toolchain_20160713.py $1 True 44.8 7.3 45.22 8 ${DANTIMESTART} ${DANTIMESTOP} turin
elif [ $2 == "rome" ]
then
	./toolchain_20160713.py $1 True 40 11 43 13 ${DANTIMESTART} ${DANTIMESTOP} rome
elif [ $2 == "newyork" ]
then
	./toolchain_20160713.py $1 True 39.5 -75 42 -72 20131204 20131205 nyc
elif [ $2 == "milan" ]
then
	./toolchain_20160713.py $1 True 45 8.5 46 10 ${DANTIMESTART} ${DANTIMESTOP} milan
elif [ $2 == "bari" ]
then
	./toolchain_20160713.py $1 True 40.8 16.5 41.2 17.1 ${3} ${4} bari
elif [ $2 == "palermo" ]
then
	./toolchain_20160713.py $1 True 38 13 38.5 13.5 ${DANTIMESTART} ${DANTIMESTOP} palermo
elif [ $2 == "sanfrancisco" ]
then
	./toolchain_20160713.py $1 True 37 -122.6 38 -122 20080528 20080529 sf
elif [ $2 == "beijing" ]
then
	./toolchain_20160713.py $1 True 39.3 115.2 41.1 117.6 20080205 20080206 beijing
elif [ $2 == "cologne" ]
then
	./toolchain_20160713.py $1 True 50.85 6.78 51.031 7.184 20100505 20100506 cologne
elif [ $2 == "shanghai" ]
then
	./toolchain_20160713.py $1 True 30.5 120.5 32 122.2 20070220 20070221 shanghai
elif [ $2 == "shenzen" ]
then
	echo "Shenzen"
	./toolchain_20160713.py $1 True 22.447 113.747 22.779 114.662 20131022 20131023 shenzen
fi
