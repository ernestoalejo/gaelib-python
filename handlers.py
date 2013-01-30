
import webapp2

import os

class Base(webapp2.RequestHandler):
  def render(self, name, *args, **kwargs):
    template = jinja_environment.get_template(os.path.join("templates", 
        ('%s.html' % name) ))
    self.response.out.write(template.render(*args, **kwargs))
