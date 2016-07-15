#!/bin/sh
xxd -c 32 $1 | sed -e "s/^.*0: //" -e "s/  .*//" -e "s/ //g" > tmp
sed -e "s/^/\$data\.=\"/" -e "s/$/\";/" tmp > res

echo "perl -e '" > data
cat res >> data
echo "@yy = pack(\"H*\", \$data); printf \"@yy\";'" >> data
