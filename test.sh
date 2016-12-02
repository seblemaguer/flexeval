#!/bin/bash
DIR="~/Documents/PROJET/GIT"

if [ $# = 1 ]
then
	if [ $1 = "rm" ]
	then
		echo "suppression des anciens test"
		rm -rf ./tests/*
	fi
fi
python ./generator.py -j ./test.json -t ./test_template.tpl
cp -rf ./static/* ./tests/Test\ AB\ pour\ validation\ du\ XML/static/