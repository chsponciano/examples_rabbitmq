import pika


# connect to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declare the exchange in case it doesn't already exist
channel.exchange_declare(exchange='messages', exchange_type='fanout')

# declare a queue which gets deleted whenever the consumer process ends
# let RabbitMQ automatically assign the queue an unused name
new_queue = channel.queue_declare(exclusive=True)
queue_name = new_queue.method.queue

# bind the newly created queue to the exchange
channel.queue_bind(exchange='messages', queue=queue_name)

print('[*] Waiting to get message from sender. To exit press CTRL+C')

# define the callback function
def callback_func(ch, method, properties, text):
    print(f'[X] Received message from sender: {text}')

channel.basic_consume(queue=queue_name, on_message_callback=callback_func, auto_ack=True)
channel.start_consuming()