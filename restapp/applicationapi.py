#!/usr/bin/env python
"""
   application api
   ~~~~~~~~~~~~~~~~

"""
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2011 Nuxeo SA <http://nuxeo.com/>"
import simplejson as json
from flask.views import MethodView
from flask import request
from flask import abort
from sqlalchemy.exc import IntegrityError
from utils import register_api
from utils import json_dumps
from model import Application
from . import db
from . import app


class ApplicationAPI(MethodView):
    """Application API"""
    def get(self, id):
        """Get an application."""
        if id is None:
            # list all
            app.logger.info('List all application')
            ret = Application.query.all()
            return json_dumps(ret)
        app.logger.info('Get application: %s' % id)
        application = Application.query.filter_by(id=id).first_or_404()
        return application.to_json()

    def post(self, id):
        """Create an application, expecting a json content."""
        application = Application.from_json(request.data)
        app.logger.info('Creating new application: %s' % request.data)
        db.session.add(application)
        try:
            db.session.commit()
        except IntegrityError, error:
            app.logger.warning(error)
            abort(409)
        app.logger.info('Created new application: %s' % application.to_json())
        return application.to_json(), 201

    def delete(self, id):
        """Delete an application."""
        application = Application.query.filter_by(id=id).first_or_404()
        app.logger.info('Delete application: %s' % id)
        db.session.delete(application)
        db.session.commit()
        return json.dumps({'id': id, 'status': 'deleted'})

    def put(self, id):
        """Update an application."""
        application = Application.query.filter_by(id=id).first_or_404()
        app.logger.info('Update application: %s' % id)
        target = Application.from_json(request.data)
        application.merge(target)
        db.session.commit()
        return application.to_json()


register_api(ApplicationAPI, 'application_api', '/application/', pk='id',
             pk_type='string')
