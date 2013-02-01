
import unittest

from google.appengine.ext import testbed


class Base(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()

    if 'init' in self.__class__.__dict__:
      self.init()

  def tearDown(self):
    self.testbed.deactivate()

  def login(self, admin=False):
    self.testbed.setup_env(
      USER_EMAIL='test@example.com',
      USER_ID='123',
      USER_IS_ADMIN='1' if admin else '0',
      overwrite=True
    )
