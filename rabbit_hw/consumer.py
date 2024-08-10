"""Consumer"""
import os
import sys
import pika
from dotenv import load_dotenv
import model as mm
# pylint: disable=no-member


load_dotenv()
pika_user = os.getenv('pika_user')
pika_pass = os.getenv('pika_pass')
pika_host = os.getenv('pika_host')
pika_port = os.getenv('pika_port')

def send_email(contact) -> bool:
    """Simulates sending an email to a contact.

    Args:
        contact (mm.Contact): The contact object containing the recipient's
        information.

    Returns:
        bool: Returns True if the email was "sent" successfully.
    """
    print(f'Sending email to {contact.name} at {contact.email}')
    return True

def callback(ch, method, properties, body) -> None:
    """Callback function to process messages from the RabbitMQ queue.

    This function is triggered for each message in the 'email_queue'. It
    decodes the message, retrieves the corresponding contact from the database,
    sends an email to the contact, and updates the contact's `is_sent` status
    in the database.

    Args:
        ch (pika.channel.Channel): The channel object.
        method (pika.spec.Basic.Deliver): Method frame with delivery details.
        properties (pika.spec.BasicProperties): Properties of the message.
        body (bytes): The message body, expected to contain the contact ID.
    """
    contact_id = body.decode()
    contact = mm.Contact.objects(id=contact_id).first()
    if contact:
        if send_email(contact):
            contact.is_sent = True
            contact.save()
            print(
                f'{properties}\n',
                f'Email sent to {contact.name}. Status updated in DB.\n',
                '- - - - -'
            )

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main() -> None:
    """Main function to set up the RabbitMQ consumer.

    This function establishes a connection to RabbitMQ, declares the
    'email_queue', and starts consuming messages from it. Each message
    triggers the `callback` function.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=pika_host,
            port=pika_port,
            credentials=pika.PlainCredentials(
                pika_user,
                pika_pass
            )
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='email_queue',
        on_message_callback=callback
    )
    print('Waiting for messages to send.')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\tSending e-mails stopped.')
        sys.exit(0)
