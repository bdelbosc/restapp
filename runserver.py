#!/usr/bin/env python
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2011 Nuxeo SA <http://nuxeo.com>"
from restapp import app
from restapp import db

if __name__ == '__main__':
    db.create_all()
    app.logger.info('Starting')
    app.run()
