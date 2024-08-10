"""Producer"""
import os
import pika
from dotenv import load_dotenv
from faker import Faker
import model as mm
# pylint: disable=no-member


fake = Faker()

load_dotenv()
pika_user = os.getenv('pika_user')
pika_pass = os.getenv('pika_pass')
pika_host = os.getenv('pika_host')
pika_port = os.getenv('pika_port')


def create_fake_contact() -> object:
    """Creates a fake contact and saves it to the database.

    This function generates a fake name and email using the Faker library,
    creates a `Contact` object, and saves it to the MongoDB database.

    Returns:
        object: The created `Contact` object.
    """
    contact = mm.Contact(
        name=fake.name(),
        email=fake.email(),
    )
    contact.save()
    return contact

def send_contact_to_queue(contact_id) -> None:
    """Sends the contact ID to the RabbitMQ queue.

    This function establishes a connection to a RabbitMQ server, declares
    a queue named 'email_queue', and publishes the given contact ID to
    the queue.

    Args:
        contact_id (str): The ID of the contact to send to the queue.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=pika_host,
            port=pika_port,
            credentials=pika.PlainCredentials(
                pika_user,
                pika_pass
            ),
            connection_attempts=3,
            retry_delay=5
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=str(contact_id),
    )
    connection.close()

def main(number_of_contacts):
    """Creates multiple fake contacts and sends them to the queue.

    This function creates the specified number of fake contacts using
    `create_fake_contact`, and then sends each contact's ID to the RabbitMQ
    queue using `send_contact_to_queue`.

    Args:
        number_of_contacts (int): The number of fake contacts to create.
    """
    for _ in range(number_of_contacts):
        contact = create_fake_contact()
        send_contact_to_queue(contact.id)
        print(f'Contact {contact.name} added to queue.')


if __name__ == '__main__':
    try:
        task = int(input('Enter number of contacts to create: '))
    except ValueError:
        print('Must be integer!')
    main(task)
