for file in `find SHENZEN/truck_*`
do
	cat $file | sed 's/\*\*\*\*-\*\*/2013-10/g' > .aaa
	mv .aaa $file
done
