#########################
#   Cmd projet Django   #
#########################

all:
	python manage.py syncdb

start:
	open /Applications/MAMP/MAMP.app
	sudo ln -s /applications/MAMP/tmp/mysql/mysql.sock /tmp/mysql.sock

clean:
	find -L . -name "*~" -exec rm -fr {} \;
	find -L . -name "*.pyc" -exec rm -fr {} \;
	find -L . -name ".DS_Store" -exec rm -fr {} \;

ignore:
	svn propset svn:ignore settings.py .
	svn propset svn:ignore "*.pyc" "*~" ".DS_Store" $$(find -type d | egrep -v \.svn)

runserver:
	python manage.py runserver

cp:
	cp ./settings.py ./settings.py.exemple
