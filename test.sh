if [ $# = 1 ]
then
	if [ $1 = "rm" ]
	then
		echo "suppression des anciens test"
		rm -rf ./tests/*
	else
		python script.py $1
	fi
elif [ $# = 2 ]
then
	if [ $2 = "rm" ]
	then
		echo "suppression des anciens test"
		rm -rf ./tests/*
		echo "nouveau test $1"
		python script.py $1
	else
		echo "NOTHING TO DO!"
	fi
else
	python script.py newTest
fi