#!/bin/bash

OUTDIR=./tests/Test_AB/
rm -rf $OUTDIR
python ./generator.py -o $OUTDIR -j ./input/AB.json -t ./input/AB.tpl -c input/completed.tpl -i input/index.tpl -e input/export.tpl -s ./input/sys0.csv system1 ./input/sys1.csv system2 -n
ret=$?
if [ $ret == 0 ]; then
	mkdir $OUTDIR/static
	cp -rf ./input/static/* $OUTDIR/static
fi
