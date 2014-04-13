django_boilerplate
==================

apt-get install apache2 apache2-mpm-worker libapache2-mod-wsgi python-pip git mercurial mysql-client libmysqlclient-dev python-dev build-essential graphviz libgraphviz-dev pkg-config sensible-mda libxml2-dev libxslt1-dev mysql-server

pip install virtualenv

cd /opt/git

git clone https://github.com/pianojet/django_boilerplate.git

cd django_boilerplate

./bootstrap.py

source venv/bin/activate

export DJANGO_SETTINGS_MODULE=ufe.settings.dev

pip install -r requirements.debug.txt

sudo ln -s /opt/git/django_boilerplate/apache/vhost.development.conf /etc/apache2/sites-available/django_boilerplate

sudo a2ensite django_boilerplate
