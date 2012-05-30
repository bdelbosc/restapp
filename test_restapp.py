#!/usr/bin/env python
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2011 Nuxeo SA <http://nuxeo.com>"
import datetime
from unittest import TestCase
from unittest import main
import simplejson as json
from restapp import app
from restapp import db
from restapp.model import Instance
from restapp.utils import json_dumps
from restapp.utils import json_loads


class JsonTestCase(TestCase):
    def test_json(self):
        obj = [datetime.datetime.now(),
               Instance(app_node="foo", http_port=1234),
               "some string", 3124]
        s = json_dumps(obj)
        new_obj = json_loads(s)
        self.assertTrue(isinstance(new_obj[1], Instance), type(new_obj[1]))
        # TODO: fix datetime decoding
        # self.assertTrue(isinstance(new_obj[0], datetime.datetime), type(new_obj[0]))
        # self.assertEquals(obj[0].year, new_obj[0].year)
        # self.assertEquals(obj[0].second, new_obj[0].second)
        self.assertEquals(obj[1].to_dict(), new_obj[1].to_dict())


class restappTestCase(TestCase):

    def setUp(self):
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"  # in-memory
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_instance(self, id):
        return Instance('appnode1', 'dbnode1').to_json()

    # testing functions
    def test_root(self):
        rv = self.client.get('/')
        self.assertTrue('Hello' in rv.data, rv.data)

    def test_instances(self):
        rv = self.client.get('/instances/')
        self.assertTrue('[]' in rv.data, rv.data)
        self.assertEquals(rv.status_code, 200)
        instances = json_loads(rv.data)
        self.assertEquals(0, len(instances))
        # create
        foo = Instance(app_node='appnode1', db_node='dbnode1', http_port=8380)
        rv = self.client.post('/instances/', data=foo.to_json(),
                              follow_redirects=True)
        self.assertEquals(rv.status_code, 201)
        foo = Instance.from_json(rv.data)
        self.assertEquals(foo.http_port, 8380)
        self.assertTrue(foo.id)
        # list
        rv = self.client.get('/instances/')
        self.assertTrue('appnode1' in rv.data, rv.data)

        instances = json_loads(rv.data)
        self.assertEquals(1, len(instances))
        self.assertEquals(foo.id, instances[0].id)
        # get
        rv = self.client.get('/instances/%s' % foo.id)
        self.assertEquals(rv.status_code, 200)
        bar = Instance.from_json(rv.data)
        self.assertEquals(foo.id, bar.id)
        self.assertEquals(foo.app_node, bar.app_node)
        # update
        foo.app_node = "appnode2"
        rv = self.client.put('/instances/' + str(foo.id), data=foo.to_json(),
                             follow_redirects=True)
        self.assertTrue("appnode2" in rv.data, rv.data)
        # delete
        rv = self.client.delete('/instances/' + str(foo.id))
        self.assertEquals(rv.status_code, 200)
        # list
        rv = self.client.get('/instances/')
        instances = json_loads(rv.data)
        self.assertEquals(0, len(instances))

    def test_instances_404(self):
        rv = self.client.delete('/instances/1')
        self.assertEquals(rv.status_code, 404)
        rv = self.client.get('/instances/1')
        self.assertEquals(rv.status_code, 404)
        foo = Instance(app_node="foo", db_node="bar")
        rv = self.client.put('/instances/1', data=foo.to_json(),
                             follow_redirects=True)
        self.assertEquals(rv.status_code, 404)
        rv = self.client.delete('/instances/1', data=foo.to_json(),
                                follow_redirects=True)
        self.assertEquals(rv.status_code, 404)

    def test_instances_integrity(self):
        foo = Instance(id=1, app_node="foo", db_node="bar")
        rv = self.client.post('/instances/', data=foo.to_json(),
                              follow_redirects=True)
        self.assertEquals(rv.status_code, 201)
        # TODO disable logging
        rv = self.client.post('/instances/', data=foo.to_json(),
                              follow_redirects=True)
        self.assertEquals(rv.status_code, 409)

if __name__ == '__main__':
    main()
