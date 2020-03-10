#!/usr/bin/env bash

cat ../../ling073-div-corpus/div.corpus.basic.txt | hfst-proc ../div.automorf.hfst | sed 's/\$ /\$\n/g' > __temp.txt

cat __temp.txt | sort | uniq -c | sort | grep '\*'

TOTAL=`cat __temp.txt | wc -l`
KNOWN=`cat __temp.txt | grep -v '\*' | wc -l`
UNKNOWN=`cat __temp.txt | grep '\*' | wc -l`

PERCENTAGE=`calc $KNOWN/$TOTAL | sed 's/[\s\t]//g'`

echo "coverage: $KNOWN / $TOTAL ($PERCENTAGE)"
echo "remaining unknown forms: $UNKNOWN"

rm __temp.txt
