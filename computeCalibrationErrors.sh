#!/bin/bash
#for theirfile in `find COLOGNE/SamplingCologne180-240-300/calibrated/cologne_gap_180/* -type f`
for theirfile in `find cologne_interpolation_100s/* -type f`
do
	./checkErrors.py cologne_interpolation_100s/`basename ${theirfile}` ${theirfile} COLOGNE/sampling_data/cologne_gap_1/`basename ${theirfile}` errors/our_`basename ${theirfile}` errors/interp_`basename ${theirfile}`
done


