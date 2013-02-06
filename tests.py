
import webapp2
from webapp2_extras import json

import unittest

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util
from google.appengine.api import mail


class Base(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
 
    self.init()
    self.addCleanup(self.finish)
    self.addCleanup(self.testbed.deactivate)

  def init(self):
    pass
 
  def finish(self):
    pass
 
  def login(self, admin=False):
    pass

  def init_datastore(self, full=True):
    if full:
      policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=1)
    else:
      policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
 
    self.testbed.init_datastore_v3_stub(consistency_policy=policy)
    self.testbed.init_memcache_stub()
 
  def init_taskqueue(self):
    """Helper to init the taskqueue stub.
 
    We abstract the fact that we should provide the root path to the application
    in order to work correctly when reading cron.yaml. It provides an easy way
    to access the stub from the tests too.
    """
    self.testbed.init_taskqueue_stub(root_path='.')
    self.taskqueue = self.testbed.get_stub('taskqueue')

  def init_mail(self):
    self.testbed.init_mail_stub()
    self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

  def json_request(self, url, data):
    r = webapp2.Request.blank(url)
    r.method = 'POST'
    r.body = json.encode(data)
    return r
