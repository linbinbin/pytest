#!/bin/sh

DATA=`cat $2`
 
echo "----------- read in list $2 -----------"
 
cnt=0
while read line
do
    cnt=`expr $cnt + 1`
    echo "LINE $cnt : $line"
	if [ `find $1 -type f | xargs grep -o "$line" | grep -v "*//*" | wc -l` -eq 0 ]; then
	#if [ tmp -eq '0' ]; then
		echo $line >> $3
	fi
done <<OVER
$DATA
OVER

