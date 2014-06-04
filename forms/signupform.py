from wtforms import Form, StringField, validators
from wtforms.validators import ValidationError
from foo.models.auth import UserMgr


def is_already_taken(form, field):
    if not field.data:
        raise ValidationError('Insert your email')
    exists = UserMgr.get(email=field.data)
    if exists:
        raise ValidationError('The user has already signed up.')


class SignupForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35),
        validators.Email(message=u'That\'s not a valid email address.'), is_already_taken ])
