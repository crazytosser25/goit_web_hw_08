import sys
import pika
from model import Contact
import mongoconnect
# pylint: disable=no-member


def send_email(contact):
    print(f'Sending email to {contact.name} at {contact.email}')
    return True

def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact:
        if send_email(contact):
            contact.is_sent = True
            contact.save()
            print(f'Email sent to {contact.name}. Status updated in DB.')
            print(properties)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials('user', 'secretpassword')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='email_queue',
        on_message_callback=callback
    )

    print('Waiting for messages.')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
