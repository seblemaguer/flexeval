#!/bin/bash

OUTDIR=./tests/TEST_VIDEO_LSF/
rm -rf $OUTDIR
python ./generator.py -o $OUTDIR -j ./input/TEST_VIDEO_LSF.json -t ./input/TEST_VIDEO_LSF.tpl -c input/completed.tpl -i input/index.tpl -e input/export.tpl -s ./input/lsf0.csv systemA ./input/lsf1.csv systemB  -n
ret=$?
if [ $ret == 0 ]; then
	mkdir $OUTDIR/static
	cp -rf ./input/static/* $OUTDIR/static
fi
