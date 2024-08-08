from mongoengine import Document
from mongoengine.fields import StringField, EmailField, BooleanField


class Contact(Document):
    name = StringField(required=True, max_length=200)
    email = EmailField(required=True, unique=True)
    is_sent = BooleanField(default=False)
