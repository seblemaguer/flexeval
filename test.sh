#!/bin/bash

if [ $# = 1 ]
then
	if [ $1 = "rm" ]
	then
		echo "suppression des anciens test"
		rm -rf ./tests/*
	fi
fi
python ./generator.py -j ./test.json -t ./template.tpl -s ./sys0.csv system1 ./sys1.csv system2 -n
cp -rf ./static/* ./tests/Test\ grandeur\ nature/static/