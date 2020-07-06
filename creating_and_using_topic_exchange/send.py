import pika
import sys


# connect to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create a new topic exchange called messages
channel.exchange_declare(exchange='topic_messages', exchange_type='topic')

# specify the message routing key and body
routing_key = sys.argv[1] if len(sys.argv) >= 2 else 'big.red.truck'
message = ' '.join(sys.argv[2:]) or 'info: RabbitMQ is Cool!'

# send the message and routing key to the topic exchange
channel.basic_publish(exchange='topic_messages', routing_key=routing_key, body=message)

print(f'[X] Send {routing_key}:{message}')

# close the queue connection
connection.close()