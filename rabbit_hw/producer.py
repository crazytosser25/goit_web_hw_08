import pika
from faker import Faker
from model import Contact
import mongoconnect
# pylint: disable=no-member


fake = Faker()

def create_fake_contact():
    contact = Contact(
        name=fake.name(),
        email=fake.email(),
    )
    contact.save()
    return contact

def send_contact_to_queue(contact_id):
    # parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
    credentials = pika.PlainCredentials('user', 'secretpassword')
    connection = pika.BlockingConnection(
        # parameters
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials,
            connection_attempts=3,
            retry_delay=5
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')

    channel.basic_publish(
        '',  # exchange
        'email_queue',  # routing_key
        str(contact_id),  # body
        # pika.BasicProperties(
        #     content_type='text/plain',
        #     delivery_mode=pika.DeliveryMode.Transient
        # )
    )

    connection.close()

def main():
    number_of_contacts = 10
    for _ in range(number_of_contacts):
        contact = create_fake_contact()
        send_contact_to_queue(contact.id)
        print(f'Contact {contact.name} added to queue.')

if __name__ == '__main__':
    main()
