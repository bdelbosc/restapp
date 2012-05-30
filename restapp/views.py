#!/usr/bin/env python
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2011 Nuxeo SA <http://nuxeo.com>"
from . import app


@app.route('/')
def index():
    return 'Hello restapp World!'
