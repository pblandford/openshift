dow=$(date -u +%w)
hour=$(date -u +%H)
if [ $dow -eq 6 ]
then
	exit
fi
if [ $dow -eq 5 -a $hour -gt 21 ]
then
	exit
fi
if [ $dow -eq 0 -a $hour -lt 22 ]
then
	exit
fi
cd ${OPENSHIFT_REPO_DIR}; ./manage.py updatefeed
