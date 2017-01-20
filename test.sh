#!/bin/bash

if [ $# = 1 ]
then
	if [ $1 = "rm" ]
	then
		echo "suppression des anciens test"
		rm -rf ./tests/*
	fi
fi
python ./generator.py -j ./input/test.json -t ./input/template.tpl -c input/completed.tpl -i input/index.tpl -e input/export.tpl -s ./input/sys0.csv system1 ./input/sys1.csv system2 ./input/sys2.csv system3 ./input/sys3.csv system4 ./input/sys4.csv system5 -n
cp -rf ./input/static/* ./tests/Perceptual_Test_A/static/
