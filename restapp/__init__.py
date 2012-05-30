#!/usr/bin/env python
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2011 Nuxeo SA <http://nuxeo.com>"
import os
import sys
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from logging import getLogger
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from logging import Formatter
from logging import DEBUG, INFO, WARN

app = Flask(__name__)
app.config.from_pyfile('restapp.conf')
app.config.from_envvar('restapp_CONF', silent=True)
db = SQLAlchemy(app)

if 'LOG_DIR' in app.config:
    log_dir = app.config['LOG_DIR']
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file_handler = RotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'restapp.log'))
    if 'LOG_LEVEL' in app.config:
        if app.config['LOG_LEVEL'] == 'INFO':
            file_handler.setLevel(INFO)
        elif app.config['LOG_LEVEL'].startswith('WARN'):
            file_handler.setLevel(WARN)
        elif app.config['LOG_LEVEL'] == 'DEBUG':
            file_handler.setLevel(DEBUG)
    elif app.config['DEBUG']:
        file_handler.setLevel(DEBUG)
    else:
        file_handler.setLevel(INFO)
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
                                        '[in %(pathname)s:%(lineno)d]'))
    for logger in [app.logger, getLogger('sqlalchemy')]:
        logger.handlers = []
        logger.addHandler(file_handler)
else:
    for logger in [app.logger, getLogger('sqlalchemy')]:
        stream_handler = StreamHandler(sys.stdout)
        logger.handlers = []
        logger.addHandler(stream_handler)

from . import views
from . import instances
