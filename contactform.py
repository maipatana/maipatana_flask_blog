from wtforms import Form,  StringField, TextAreaField, validators

class ContactForm(Form):
  name = StringField("Name", [validators.Length(min=3, max=30)])
  email = StringField("Email", [validators.Length(min=5, max=35)])
  subject = StringField("Subject", [validators.Length(min=5, max=40)])
  message = TextAreaField("Message", [validators.Length(min=5, max=1000)])

