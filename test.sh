if [ $# = 1 ]
then
	if [ $1 = "rm" ]
	then
		echo "suppression des anciens test"
		rm -rf ./tests/*
	fi
fi
python generator.py -j test.json -t template.tpl
