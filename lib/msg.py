"""Create and send messages to users

"""
import logging
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pyramid.settings import asbool
from pyramid_mailer.message import Message
import pyramid_mailer
from os import path
from pyramid.paster import bootstrap


LOG = logging.getLogger(__name__)

# notification statuses
# might have pending, sent, failed
MSG_STATUS = {
    'pending': 0,
    'sent': 1,
    'failed': 2,
    'not_sent': 3,
    'error': 4,
}

app_settings = bootstrap(path.join(path.dirname(path.dirname(path.dirname(__file__))), "development.ini"))['registry'].settings

class Msg(object):
    """This is a base email message we can then tweak"""

    def __init__(self, to, subject, settings):
        """Start up a basic message"""
        self.to = to
        self.subject = subject
        self.settings = settings

        self.from_addr = settings.get('email.from', None)

        # need ot setup/override in the extending classes
        self.message_file = None

    def _get_message_body(self, template_file, message_data):
        """Return the completed message template body

        """
        return "Test email message from bookie"
        # lookup = config['pylons.app_globals'].mako_lookup
        # template = lookup.get_template(template_file)

        # # template vars are a combo of the obj dict and the extra dict
        # template_vars = {'data': message_data}
        # return template.render(**template_vars)

    def send(self, message_data=None):
        """Send the message with the given subject

        body can be sent as part of send() or it can be set to the object as
        msg.body = "xxx"

        """

        self.body = self._get_message_body(self.message_file, message_data)

        msg = MIMEMultipart('related')
        msg['Subject'] = self.subject
        msg['From'] = self.from_addr

        msg['To'] = self.to

        plain_text = MIMEText(self.body, 'plain', _charset="UTF-8")
        msg.attach(plain_text)

        LOG.debug('msg: ' + repr(msg))

        mailer = pyramid_mailer.mailer.Mailer.from_settings(app_settings)
        message = Message(subject=msg['Subject'],
                          recipients=[msg['To']],
                          body=self.body)

        mailer.send_immediately(message, fail_silently=False)
        return MSG_STATUS['sent']

class ReactivateMsg(Msg):
    """Send an email for a reactivation email"""

    def _get_message_body(self, template_file, message_data):
        """Return the completed message template body

        """
        return """
Hello {username}:

Please activate your app account by clicking on the following url:

{url}

---
From Us""".format(**message_data)
        # lookup = config['pylons.app_globals'].mako_lookup
        # template = lookup.get_template(template_file)

        # # template vars are a combo of the obj dict and the extra dict
        # template_vars = {'data': message_data}
        # return template.render(**template_vars)

class SignupMsg(Msg):
    """Send an email that you've been invited to the system"""
    def _get_message_body(self, template_file, message_data):
        """Return the completed message template body

        """
        return """
Someone signed-up for an account at ~~~PROJNAME~~~(possibly you).

Please click the link below to activate your account.

{0}

---
From Us""".format(message_data)

class ResetMsg(Msg):
    """Send an email that you've been invited to the system"""
    def _get_message_body(self, template_file, message_data):
        """Return the completed message template body

        """
        return """
Someone requested to reset the password for your account at ~~~PROJNAME~~~(possibly you).

Please click the link below to reset your password.

If this wasn't you, then simply ignore this message.

{0}

---
From Us""".format(message_data)



class InvitationMsg(Msg):
    """Send an email that you've been invited to the system"""
    def _get_message_body(self, template_file, message_data):
        """Return the completed message template body

        """
        return """
You've been invited to The Site!

Please click the link below to activate your account.

{0}

---
From Us""".format(message_data)


class ImportFailureMessage(Msg):
    """Send an email that the import has failed."""

    def _get_message_body(self, template_file, message_data):
        """Build the email message body."""

        msg = """
The import for user {username} has failed to import. The path to the import
is:

{file_path}

Error:

{exc}

""".format(**message_data)
        return msg


class UserImportFailureMessage(Msg):
    """Send an email to the user their import has failed."""

    def _get_message_body(self, template_file, message_data):
        """Build the email message body."""

        msg = """
Your import has failed. The error is listed below. Please file a bug at
https://github.com/mitechie/bookie/issues if this error continues. You may
also join #bookie on freenode irc if you wish to aid in debugging the issue.
If the error pertains to a specific bookmark in your import file you might try
removing it and importing the file again.

Error
----------

{exc}

A copy of this error has been logged and will be looked at.

---
From Us""".format(**message_data)
        return msg


class UserImportSuccessMessage(Msg):
    """Send an email to the user after a successful import."""

    def _get_message_body(self, template_file, message_data):
        """Build the email message body."""

        msg = """
Your bookmark import is complete! We've begun processing your bookmarks to
load their page contents and fulltext index them. This process might take a
while if you have a large number of bookmarks. Check out your imported
bookmarks at https://bmark.us/{username}/recent.

---
From Us""".format(**message_data)
        return msg
