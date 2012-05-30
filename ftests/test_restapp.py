# -*- coding: iso-8859-15 -*-
"""restapp FunkLoad test
"""
import unittest
import simplejson as json
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import Data


class Restapp(FunkLoadTestCase):
    """This test use a configuration file Restapp.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.server_url = self.conf_get('main', 'url')

    def test_Restapp(self):
        server_url = self.server_url
        # begin of test ---------------------------------------------
        # self.setHeader('Accept-encoding', 'gzip')
        self.get(server_url, description="Get /")
        self.get(server_url + '/instances/', description="List instances")
        self.post(server_url + '/instances/',
                  params=Data('application/json', '{"app_node": "app1", "db_node": "db1"}'),
                  ok_codes=[201, ], description="Add a new instance")
        instance = json.loads(self.getBody())
        self.put(server_url + '/instances/%s' % instance['id'],
                 params=Data('application/json', '{"app_node": "appX"}'),
                 description="Update node")
        self.get(server_url + '/instances/', description="List instances")
        self.delete(server_url + '/instances/%s' % instance['id'],
                    description="Delete node")

        # end of test -----------------------------------------------


if __name__ in ('main', '__main__'):
    unittest.main()
