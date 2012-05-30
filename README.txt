=============================
Rest Application Template
=============================

A sample rest server using flask, apache and more.

Installation
---------------

Requirements
~~~~~~~~~~~~~~~~

- python 2.x>=2.6::

    sudo aptitude install python2.6

- setuptools >= 0.6c6::

    curl -O http://peak.telecommunity.com/dist/ez_setup.py
    sudo python ez_setup.py -U setuptools

- virtualenv::

    sudo easy_install virtualenv

Setup
~~~~~~~~

Go to the restapp source directory, then

- Get dependencies to virtualenv::

    make env

- Activate the virtual env::

    source env/bin/activate

Configuration file
---------------------

The default configuration `restapp/restapp.conf` can be overriden using a
`RESTAPP_CONF` environment variable::

  RESTAPP_CONF=/path/to/myrestapp.conf ./runserver.py

Configuration keys
~~~~~~~~~~~~~~~~~~~~

- DEBUG = True
- TESTING = True
- SQLALCHEMY_ECHO = False
- SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
- LOG_DIR = '/tmp/restapp'
- LOG_LEVEL = 'INFO'


API
-----

Return code
~~~~~~~~~~~~

- 200 OK: ok for GET/DELETE/PUT.
- 201 Created: ok for POST.
- 401 Unauthorized: if you are not a recognized user.
- 403 Forbidden: if the user is not authorized to access/create.
- 404 Not Found: if the resource does not exist.
- 409 Conflict: if you try and create an existing resource.


Deploying
-------------

Standalone server
~~~~~~~~~~~~~~~~~~~

Start the server::

  ./runserver.py

Apache wsgi
~~~~~~~~~~~~~

- Installing mod_wsgi::

    apt-get install libapache2-mod-wsgi

- Create a restapp user and home::
    
    sudo adduser restapp
    # accept ssh users
    ssh-copy-id restapp@localhost
    sudo mkdir -p /var/www/restapp
    sudo chown restapp.restapp /var/www/restapp
    sudo su -l restapp -c "(cd /var/www/restapp; virtualenv --distribute env)"


- Setup a virtual host::

    # Add a /etc/apache2/sites-available/restapp
    <VirtualHost api.restapp.com:*>
        ServerName api.restapp.com
        WSGIDaemonProcess restapp user=restapp group=restapp processes=2 threads=5
        WSGIScriptAlias / /var/www/restapp/restapp.wsgi
        WSGIScriptReloading On
        WSGIRestrictEmbedded On 
        <Directory /var/www/restapp>
            WSGIProcessGroup restapp
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
        ErrorLog /var/log/apache2/restapp_error.log
        CustomLog /var/log/apache2/restapp_access.log combined
    </VirtualHost>


- Enable new virtual host::

   sudo a2ensite restapp
   sudo invoke-rc.d apache2 reload

- Setup a restapp.wsgi file take model of the restapp.wsgi::
  
    sudo su -l restapp -c "vi /var/www/restapp/restapp.wsgi"

- Setup a restapp.conf file::
  
    sudo su -l restapp -c "vi  /var/www/restapp/restapp.conf"

- Deploy the application::

    make deploy-apache

- Reset env::
  
    sudo rm -rf /var/www/restapp/env &&  sudo su -l restapp -c "(cd /var/www/restapp; virtualenv --distribute env)" && make deploy-apache
    

Create a PostgreSQL database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new user and database::

  sudo su -l postgres -c "createuser -P restapp"
  sudo su -l postgres -c "createdb restapp -O restapp"

Then setup the restapp.conf with::
   
  SQLALCHEMY_DATABASE_URI = 'postgresql://restapp:secret@localhost/restapp'



Testing
------------

Unit tests
~~~~~~~~~~~

- Run the test suite::

   make test

- Launching a single test::

   nosetests -v -s test_restapp.py:JsonTestCase.test_json


Curl basic tests
~~~~~~~~~~~~~~~~~

- Add a new instance::

   curl -X POST -H "Content-Type: application/json" -d '{"app_node": "app1", "db_node": "db1"}' http://localhost:5000/instances/
  

- List all instances::

   curl http://localhost:5000/instances/

- List a single instances::

   curl http://localhost:5000/instances/1

- Update an instance::
 
    curl -X PUT -H "Content-Type: application/json" -d '{"app_node": "app2"}' http://localhost:5000/instances/1

- Delete an instance::

    curl -X DELETE http://localhost:5000/instances/1


FunkLoad tests
~~~~~~~~~~~~~~~~

You need to install funkload (http://funkload.org/install.html)

- Testing::


    make

- Benching::

    make bench

- Remote tests::

   make URL=http://localhost:5000


Building documentation
-----------------------

You need to install python-sphinx (deb pacakge is fine), then::
    
    make doc


Known limitation and errors
------------------------------

- Missing virtualenv activation::

    AttributeError: 'SQLAlchemy' object has no attribute 'relationship'

  This is because you have an old sqlalchemy package remove it and activate virtualenv::

    sudo aptitude remove python-sqlalchemy
    source env/bin/activate

- On restart/reload in wsgi mode KeyError in threading

  This happens even with `WSGIRestrictEmbedded On`, So far there are no impact on application
  problem is described here:
  http://groups.google.com/group/modwsgi/browse_thread/thread/ba82b2643564d2dd

  Error message::
  
    [error] Exception KeyError: KeyError(-1217366272,) in <module 'threading' from '/usr/lib/python2.6/threading.pyc'> ignored


- In wsgi multi process and multi thread with sqlite
  experiencing some db lock on deleting load, using postgresql no pb.

.. Local Variables:
.. mode: rst
.. End:
.. vim: set filetype=rst:
