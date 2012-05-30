#!/usr/bin/env python
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2011 Nuxeo SA <http://nuxeo.com>"
from fabric.api import put, run, local, cd, env

# the user to use for the remote commands
env.user = 'restapp'
# the servers where the commands are executed
env.hosts = ['localhost']


def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)


def deploy():
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/restapp.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir /tmp/restapp')
    with cd('/tmp/restapp'):
        run('tar xzf /tmp/restapp.tar.gz')
    with cd('/tmp/restapp/%s' % dist):
        # now setup the package with our virtual environment's
        # python interpreter
        run('/var/www/restapp/env/bin/pip install /tmp/restapp.tar.gz')  # setup.py install')
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/restapp /tmp/restapp.tar.gz')
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    run('touch /var/www/restapp/restapp.wsgi')
