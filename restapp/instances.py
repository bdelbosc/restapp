#!/usr/bin/env python
"""
   instance api
   ~~~~~~~~~~~~

"""
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2011 Nuxeo SA <http://nuxeo.com>"
import simplejson as json
from flask.views import MethodView
from flask import request
from flask import abort
from sqlalchemy.exc import IntegrityError
from utils import register_api
from utils import json_dumps
from model import Instance
from . import db
from . import app


class InstanceAPI(MethodView):
    """API to manipulate instance
    """
    def get(self, id):
        """Get an instance."""
        if id is None:
            # list all
            app.logger.info('List instances')
            ret = Instance.query.all()
            return json_dumps(ret)
        app.logger.info('Get instance: %s' % id)
        instance = Instance.query.filter_by(id=id).first_or_404()
        return instance.to_json()

    def post(self, id):
        """Create an instance, expecting a json content."""
        instance = Instance.from_json(request.data)
        app.logger.info('Creating new instance: %s' % request.data)
        db.session.add(instance)
        try:
            db.session.commit()
        except IntegrityError, error:
            app.logger.warning(error)
            abort(409)
        app.logger.info('Created new instance: %s' % instance.to_json())
        return instance.to_json(), 201

    def delete(self, id):
        """Delete an instance."""
        instance = Instance.query.filter_by(id=id).first_or_404()
        app.logger.info('Delete instance: %s' % id)
        db.session.delete(instance)
        db.session.commit()
        return json.dumps({'id': id, 'status': 'deleted'})

    def put(self, id):
        """Update an instance."""
        instance = Instance.query.filter_by(id=id).first_or_404()
        app.logger.info('Update instance: %s' % id)
        target = Instance.from_json(request.data)
        instance.merge(target)
        db.session.commit()
        return instance.to_json()


register_api(InstanceAPI, 'instance_api', '/instances/', pk='id',
             pk_type='string')
