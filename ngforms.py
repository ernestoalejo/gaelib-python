import re

import webapp2
from webapp2_extras import json


class Form(object):
  field_values = {} 

  def build(self):
    fields = ''.join([f.build(self) for f in self.fields])

    return """
      <form class="form-horizontal" name="f" novalidate ng-init="val = false;"
        ng-submit="f.$valid && submit()"><fieldset>%s</fieldset></form>
    """ % fields

  def validate(self):
    request = webapp2.get_request()
    data = json.decode(request.body)

    for f in self.fields:
      vals = self.validations[f.id]

      try:
        value = data[f.id]
      except KeyError:
        value = ''

      field_values[f.id] = value
      for val in vals:
        if not val.validate(self):    
          request.abort(403)

  @property
  def fields(self):
    raise NotImplemented()

  @property
  def validations(self):
    raise NotImplemented()

  def field(self, id):
    return field_values[id]


class Validation(object):
  input = ""

  def __init__(self, name, message, attrs):
    self.name = name
    self.message = message
    self.attrs = attrs

  def validate(self, form):
    raise NotImplemented()


class MinLength(Validation):
  def __init__(self, min, message):
    super(MinLength, self).__init__("minlength", message, 
        {"ng-minlength" : min})
    self.min = min

  def validate(self, form):
    return len(form.field(self.input)) >= min


class MaxLength(Validation):
  def __init__(self, max, message):
    super(MaxLength, self).__init__("maxlength", message,
        {"ng-maxlength" : max})
    self.max = max

  def validate(self, form):
    return len(form.field(self.input)) <= max


class Required(Validation):
  def __init__(self, message):
    super(Required, self).__init__("required", message, {"required": ''})

  def validate(self, form):
    return len(form.field(self.input)) > 0


class Email(Validation):
  def __init__(self, message):
    super(Email, self).__init__("email", message, {})

  def validate(self, form):
    return not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$', 
        form.field(self.input)) is None


class Match(Validation):
  def __init__(self, field, message):
    super(Match, self).__init__("match", message, {'match': field})
    self.field = field

    def validate(self, form):
      return form.field(field) == form.field(self.input)


class Pattern(Validation):
  def __init__(self, pattern, message):
    super(Pattern, self).__init__("pattern", message, {"pattern" : pattern})
    self.pattern = pattern

    def validate(self, form):
      return not re.match(pattern,form.field(self.input)) is None


class Field(object):
  def __init__(self, id, name):
    self.id = id
    self.name = name

  def build(self, form):
    vals = form.validations[self.id]
    errs = " || ".join(['f.%s.$error.%s' % (self.id, val.name) for val in vals])

    attrs = {}
    for val in vals:
      attrs.update(val.attrs)

    messages = []
    for v in vals:
      messages.append('<span ng-show="f.%s.$error.%s">%s</span>' % 
          (self.id, v.name, v.message))
    messages = ''.join(messages)

    if len(self.name) == 0:
      return attrs, """
        <div class="control-group" ng-class="val && (%s) && 'error'">
          %%s
          <p class="help-block error" ng-show="val && f.%s.$invalid">
            %s
          </p>
        </div>
      """ % (errs, self.id, messages)
    
    return attrs, """
      <div class="control-group" ng-class="val && (%s) && 'error'">
        <label class="control-label" for="%s">%s</label>
        <div class="controls">%%s
          <p class="help-block error" ng-show="val && f.%s.$invalid">
            %s
          </p>
        </div>
      </div>
    """ % (errs, self.id, self.name, self.id, messages)


class InputField(Field):
  def __init__(self, id, cls, name, type='text', placeholder=''):
    super(InputField, self).__init__(id, name)

    self.type = type
    self.placeholder = placeholder
    self.cls = cls

  def build(self, form):
    attrs = {
      "type": self.type,
      "id": self.id,
      "name": self.name,
      "placeholder": self.placeholder,
      "class": ' '.join(self.cls),
      "ng-model": 'data.%s' % self.id, 
    }
    
    (at, tmpl) = super(InputField, self).build(form)
    attrs.update(at)
    
    input = [' %s="%s"' % (k, v) for k,v in attrs.iteritems()]
    input = '<input%s>' % ''.join(input)

    return tmpl % input
