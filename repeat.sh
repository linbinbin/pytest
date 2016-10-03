#!/bin/sh
for i in `seq 0 1000`
do
sh DOCXML_004.sh;
if [ $? -ne 0 ] ; then
break; 
fi
done
