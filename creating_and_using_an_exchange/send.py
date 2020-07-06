import pika
import sys


# connect to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create a new fanout exchange called messages
channel.exchange_declare(exchange='messages', exchange_type='fanout')

# send a new message to the exchange
message = ' '.join(sys.argv[1:]) or 'info: RabbitMQ is Cool!'
channel.basic_publish(exchange='message', routing_key='', body=message)

print(f'[X] Send {message}')

# close the queue connection
connection.close()