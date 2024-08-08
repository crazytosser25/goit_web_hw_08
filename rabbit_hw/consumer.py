# consumer.py
import pika
from rabbit_hw.models import Contact
# pylint: disable=no-member



def send_email(contact):
    print(f'Sending email to {contact.full_name} at {contact.email}')
    return True

def callback(ch, method, body):
    contact_name = body.decode()
    contact = Contact.objects(contact_name).first()

    if contact:
        if send_email(contact):
            contact.is_sent = True
            contact.save()
            print(f'Email sent to {contact.name}. Status updated in DB.')

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
