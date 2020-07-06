import pika
import sys


# connect to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declare the exchange in case it doesn't already exist
channel.exchange_declare(exchange='topic_messages', exchange_type='fanout')

# declare a queue which gets deleted whenever the consumer process ends
# let RabbitMQ automatically assign the queue an unused name
new_queue = channel.queue_declare(exclusive=True)
queue_name = new_queue.method.queue

# get the binding keys from command line arguments
binding_keys = sys.arg[1:]
if not binding_keys:
    sys.stderr.write(f'Add binding keys with spaces between them: {sys.argv[0]} [binding_key]...\n')
    sys.exit(1)

# add the binding keys to the queue
for binding_key in binding_keys:
    channel.queue_bind(queue_name, exchange='topic_messages', routing_key=binding_key)

print('[*] Waiting to get message from sender. To exit press CTRL+C')

# define the callback function
def callback_func(ch, method, properties, text):
    print(f'[X] Received message from sender: {method.routing_key}:{text}')

channel.basic_consume(queue=queue_name, on_message_callback=callback_func, auto_ack=True)
channel.start_consuming()