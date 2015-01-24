dow=$(date +%w)
hour=$(date +%H)
if [ $dow -eq 6 ]
then
	exit
fi
if [ $dow -eq 5 -a $hour -gt 9 ]
then
	exit
fi
if [ $dow -eq 0 -a $hour -lt 10 ]
then
	exit
fi
cd ${OPENSHIFT_REPO_DIR}; ./manage.py updatefeed
