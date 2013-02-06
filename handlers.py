
import webapp2
from webapp2_extras import json, sessions, jinja2

import os
import datetime

from endarch.models.user import User


class Base(webapp2.RequestHandler):
  def dispatch(self):
      session_store = User.get_session_store()
      self.session = User.get_session()
      try:
          super(Base, self).dispatch()
      finally:
          session_store.save_sessions(self.response)

  @webapp2.cached_property
  def jinja2(self):
    return jinja2.Jinja2(app=self.app, config={
      'template_path': '.',
    })

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

  
