import re


class Form(object) 

  def build(self):

  def validate(self):

  def fields(self):
    raise NotImplemented()

  def validations(self):
    raise NotImplemented()

  def field(self, name):
    return ""


class Validation(object):
  """The name of the field containing the value"""
  input = ""

  def __init__(self, name, message, attr):
    self.name = name
    self.message = message
    self.attr = attr

  def validate(self, form):
    raise NotImplemented()


class MinLength(Validation)
  def __init__(self, min, message):
    super(MinLength, self).__init__("minlength", message, 
        {"ng-minlength" : min})
    self.min = min

  def validate(self, form):
    return len(form.field(self.input)) >= min


class MaxLength(Validation)
  def __init__(self, max, message):
    super(MaxLength, self).__init__("maxLength", message,
        {"ng-maxlength" : max})
    self.max = max

  def validate(self, form):
    return len(form.field(self.input)) =< max


class Required(Validation)
  def __init__(self, message):
    super(Required, self).__init__("required", message, {"required"})

  def validate(self, form):
    return len(form.field(self.input)) > 0


class Email(Validation)
  def __init__(self, message):
    super(Email, self).__init__("email", message, {})

  def validate(self, form):
    return re.match("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$", 
        form.field(self.input)) 
        is not None


class Match(Validation)
  def __init__(self, value, message):
    super(Match, self).__init__("match", message, {})
    self.value = value

    def validate(self, form):
      return value == form.field(self.input)


class Pattern(Validation)
  def __init__(self, pattern, message):
    super(Pattern, self).__init__("pattern", message, 
        {"pattern" : pattern})
    self.pattern = pattern

    def validate(self, form):
      return re.match(pattern,form.field(self.input)) is not None
