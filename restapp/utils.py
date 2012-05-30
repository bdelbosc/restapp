#!/usr/bin/env python
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2011 Nuxeo SA <http://nuxeo.com>"
import re
import simplejson as json
import datetime
import iso8601
from . import app
from model import Instance

# 2011-10-25T12:37:15.330644
ISO8601_RE = re.compile(r'/(\d{4})-(\d{2})-(\d{2})T(\d{2})')


class RESTAPPDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(RESTAPPDecoder, self).__init__(*args, **kwargs)
        self.object_hook = self.hook

    def hook(self, obj):
        # print "YYYZZZZ %s" % obj
        if 'app_node' in obj:
            return Instance(**obj)
        for key, val in obj.iteritems():
            if isinstance(val, basestring) and (ISO8601_RE.match(val)):
                try:
                    obj[key] = iso8601.parse_date(val)
                except ValueError:
                    pass
        return obj


def json_hook(obj):
    # find a better way
    if 'app_node' in obj:
        return Instance(**obj)
    # this does not work so far
    for key, val in obj.iteritems():
        if isinstance(val, basestring) and (ISO8601_RE.match(val)):
            try:
                return iso8601.parse_date(val)
            except ValueError:
                pass


def json_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, Instance):
        return obj.to_dict()
    return None


def json_dumps(obj):
    """Dumps that handle datetime and instance object."""
    return json.dumps(obj, default=json_handler)


def json_loads(s):
    #return json.loads(s, cls=RESTAPPDecoder)
    return json.loads(s, object_hook=json_hook)


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET', 'POST'])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                       methods=['GET', 'PUT', 'DELETE'])
