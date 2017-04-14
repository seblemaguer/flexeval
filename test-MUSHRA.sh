#!/bin/bash

OUTDIR=./tests/Test_MOS/
rm -rf $OUTDIR
python ./generator.py -o $OUTDIR -j ./input/MOS.json -t ./input/MOS.tpl -c input/completed.tpl -i input/index.tpl -e input/export.tpl -s ./input/sys0.csv system1 ./input/sys1.csv system2 -n
ret=$?
if [ $ret == 0 ]; then
	mkdir $OUTDIR/static
	cp -rf ./input/static/* $OUTDIR/static
fi
