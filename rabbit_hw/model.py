"""Connection to MongoDB and model."""
import os
from mongoengine import Document, connect
from mongoengine.fields import StringField, EmailField, BooleanField
from dotenv import load_dotenv


load_dotenv()
m_user = os.getenv('mongo_user')
m_pass = os.getenv('mongo_pass')
m_domain = os.getenv('mongo_domain')
db_name = os.getenv('mongo_db_name')

connect(
    host=f"""mongodb+srv://{m_user}:{m_pass}@{m_domain}/{db_name}"""
)


class Contact(Document):
    """Represents a contact in the database.

    This class defines the schema for storing contact information
    in the MongoDB database. It inherits from the `Document` class
    provided by MongoEngine.

    Attributes:
        name (StringField): The name of the contact. This field is required and
                            has a maximum length of 200 characters.
        email (EmailField): The email address of the contact. This field is required
                            and must be unique in the database.
        is_sent (BooleanField): A flag indicating whether the contact's email has
                                been sent. Defaults to False.
    """
    name = StringField(required=True, max_length=200)
    email = EmailField(required=True, unique=True)
    is_sent = BooleanField(default=False)
