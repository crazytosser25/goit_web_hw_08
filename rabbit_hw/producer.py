import os
import pika
from faker import Faker
from dotenv import load_dotenv
from mongoengine import connect
from rabbit_hw.models import Contact


load_dotenv()
mongo_user = os.getenv('user')
mongodb_pass = os.getenv('pass')
db_name = os.getenv('db_name')
domain = os.getenv('domain')

connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}"""
)

fake = Faker()

def create_fake_contact():
    contact = Contact(
        full_name=fake.name(),
        email=fake.email(),
    )
    contact.save()
    return contact

def send_contact_to_queue(contact_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')

    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=str(contact_id)
    )

    connection.close()

def main():
    number_of_contacts = 10
    for _ in range(number_of_contacts):
        contact = create_fake_contact()
        send_contact_to_queue(contact.name)
        print(f'Contact {contact.name} added to queue.')

if __name__ == '__main__':
    main()
