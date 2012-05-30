#!/usr/bin/env python
"""
   restapp.model
   ~~~~~~~~~~~~~~

   This module contains the data models for the RESTAPP.
"""
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2011 Nuxeo SA <http://nuxeo.com>"
import datetime
from . import db
import simplejson as json

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None


class Instance(db.Model):
    """The data model for an instance.
    """
    __tablename__ = "instances"
    #: The Auto increment integer id
    id = db.Column(db.Integer, db.Sequence('instance_id_seq'), primary_key=True)
    #: Application node
    app_node = db.Column(db.String(64))
    #: Database node
    db_node = db.Column(db.String(64))
    #: Instance port
    http_port = db.Column(db.Integer)
    #: Database port
    db_port = db.Column(db.Integer)
    #: Creation datetime
    created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, **kwargs):
        keys = Instance.columns()
        for key in kwargs.keys():
            if key in keys:
                value = kwargs.get(key, None)
                if value:
                    setattr(self, key, value)

    def __repr__(self):
        return self.to_json()

    @classmethod
    def columns(cls):
        """List the column of the table."""
        return [column.name for column in Instance.__table__.columns]

    def to_dict(self):
        """Return a dict representing the data model."""
        ret = {}
        for column in Instance.columns():
            value = getattr(self, column, None)
            if value:
                ret[column] = getattr(self, column)
        return ret

    def to_json(self):
        """Return a json representation of a data model."""
        return json.dumps(self.to_dict(), default=dthandler)

    @classmethod
    def from_json(cls, jsonstr):
        """Return an instance from a json representation."""
        obj = json.loads(jsonstr)
        ret = cls(**obj)
        return ret

    def merge(self, target):
        """Merge the instance with another.

        :param target: the instance that override the current one."""
        for key in Instance.columns():
            # keep some properties immutable
            if key in ['id', 'created']:
                continue
            value = getattr(target, key, None)
            if value:
                setattr(self, key, value)
