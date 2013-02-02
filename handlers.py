
import webapp2
from webapp2_extras import json

import os
import datetime


class Base(webapp2.RequestHandler):
  @webapp2.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def render(self, template, **kwargs):
    self.response.headers.add('X-UA-Compatible', 'chrome=1')
    self.response.headers.add('Content-Type', 'text/html; charset=utf-8')

    resp = self.jinja2.render_template(template, **kwargs)
    self.response.write(resp)

  def json(self, data):
    self.response.headers.add('Content-Type', 'application/json; charset=utf-8')
    self.response.out.write(")]}',\n")

    def serializer(obj):
      if isinstance(obj, datetime.datetime):
        return obj.isoformat()
      return None

    self.response.write(json.encode(data, default=serializer))

  def long_id(self, num):
    try:
      n = long(num)
      if n == 0:
        self.abort(403, detail='valid numeric id expected')
        return n
    except ValueError:
      self.abort(403, detail='numeric id expected')
