import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

from core.settings import sender_settings
from jinja2 import Environment, FileSystemLoader
from orjson import orjson
from storage.models.models import EmailMessage as EmailMessageModel
from storage.src.saver import MessagesSaver

from messages.schema.senders import Senders
from messages.schema.statuses import Statuses


class MessagesSender:

    def __init__(self):
        self.sender = sender_settings.sender
        self.server = smtplib.SMTP(sender_settings.sender_host, sender_settings.sender_port)

    def send(self, recipients: set, message_to_send: dict):
        message = EmailMessage()
        message['From'] = self.sender
        message['Subject'] = message_to_send['content']['subject']

        env = Environment(loader=FileSystemLoader(f'{os.path.dirname(__file__)}'))
        template = env.get_template('templates/base.html')
        output = template.render(**{
            'text': message_to_send['content']['text'],
        })
        message.add_alternative(output, subtype='html')
        for recipient in recipients:
            try:
                self.server.sendmail(self.sender, recipient, message.as_string())
            except smtplib.SMTPException:
                self.save_history(recipients=recipients, message=message_to_send, status=Statuses.FAILED)
            else:
                self.save_history(recipients=recipients, message=message_to_send)

    def close_connection(self):
        self.server.close()

    def save_history(self, recipients: set, message: dict, status: Statuses = Statuses.SENT):
        data = [
            EmailMessageModel(
                created_at=message['created_at'],
                updated_at=datetime.now(),
                status=status.name,
                sender=Senders(message['sender']),
                recipient=recipient,
                content=orjson.dumps(message['content'])
            )
            for recipient in recipients
        ]

        MessagesSaver.save(data=data)
