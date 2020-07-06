import pika


# connect to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create a new queue called testqueue
channel.queue_declare(queue='testqueue', durable=1)

# add a message to the testqueue
channel.basic_publish(exchange='', routing_key='testqueue', body='RabbitMQ is cool!')
print('[X] Sent "RabbitMQ is cool!"')

# close the queue connection
connection.close()