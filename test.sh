if [ $1 = "rm" ]
then
	echo "suppression des anciennes bases de données"
	rm databases/*.db
fi
python script.py toto