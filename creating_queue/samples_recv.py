import pika


# connect to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declare the queue in case it doesn't already exist
channel.queue_declare(queue='testqueue')

def callback_func(ch, method, properties, text):
    print(f'[X] Received message from sender: {text}')

channel.basic_consume(queue='testqueue', on_message_callback=callback_func, auto_ack=True)
print('[*] Waiting to get message from sender. To exit press CTRL+C')
channel.start_consuming()