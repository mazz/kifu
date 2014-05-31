from wtforms import Form, BooleanField, StringField, validators


class SignupForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
