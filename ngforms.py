import re

class Form(object) 

  def build(self):

  def validate(self):

  def fields(self):
    raise NotImplemented()

  def validations(self):
    raise NotImplemented()


# ----------------------------------------

class Validation(object)
  def __init__(self, name, message, attr):
    self.name = name
    self.message = message
    self.attr = attr

  def validate(self):
    raise NotImplemented()

class MinLength(Validation)
  def __init__(self, min, message):
    self.min = min
    super(MinLength, self).__init__("MinLength", message, 
        {"ng-minlength" : min})

  def validate(self, value):
    return len(value) >= min

class MaxLength(Validation)
  def __init__(self, max, message):
    self.max = max
    super(MaxLength, self).__init__("MaxLength", message,
        {"ng-maxlength" : max})

  def validate(self, value):
    return len(value) =< max

class Required(Validation)
  def __init__(self, field, message):
    self.field = field
    super(Required, self).__init__("Required", message, {"required"})

  def validate(self, field):
    return len(field)>0

class Email(Validation)
  def __init__(self, email, message):
    self.email = email
    super(Email, self).__init__("Email", message, {})

  def validate(self, email):
    if not re.match("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$", email):
      return False
    else:
      return True
      
