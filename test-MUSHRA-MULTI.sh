#!/bin/bash

OUTDIR=./tests/TEST_MUSHRA_MULTI/
rm -rf $OUTDIR
python ./generator.py -o $OUTDIR -j ./input/MUSHRA-MULTI.json -t ./input/MUSHRA-MULTI.tpl -c input/completed.tpl -i input/index.tpl -e input/export.tpl -s ./input/sys0.csv systemA ./input/sys1.csv systemB ./input/sys2.csv systemC -n
ret=$?
if [ $ret == 0 ]; then
	mkdir $OUTDIR/static
	cp -rf ./input/static/* $OUTDIR/static
fi
