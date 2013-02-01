
import webapp2
from webapp2_extras import json

import os


class Base(webapp2.RequestHandler):
  def render(self, name, *args, **kwargs):
    template = jinja_environment.get_template(os.path.join("templates", 
        ('%s.html' % name) ))
    self.response.out.write(template.render(*args, **kwargs))

  def json(self, value):
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    self.response.out.write(json.encode(value))
