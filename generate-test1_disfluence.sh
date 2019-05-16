#!/bin/bash

OUTDIR=./tests/TEST1_DISFLUENCE/
rm -rf $OUTDIR
python ./generator.py -o $OUTDIR -j ./input/TEST1_DISFLUENCE.json -t ./input/TEST1_DISFLUENCE.tpl -c input/completed.tpl -i input/index.tpl -e input/export.tpl -s ./input/sys0.csv systemA ./input/sys1.csv systemB ./input/sys2.csv systemC ./input/sys3.csv systemD -n
ret=$?
if [ $ret == 0 ]; then
	mkdir $OUTDIR/static
	cp -rf ./input/static/* $OUTDIR/static
fi
