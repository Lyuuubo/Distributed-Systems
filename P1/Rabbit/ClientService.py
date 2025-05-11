import pika
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='request_queue')

# Declare response queue
response = channel.queue_declare(queue='', exclusive=True)
response_queue = response.method.queue

insults= ['Perro','Tonto','Inutil','Feo','Gordo']

for insult in insults:
    channel.basic_publish(exchange='', routing_key='request_queue', body=insult)
    print(f" [x] Sent '{insult}'")

# Start broadcast
message = 'X2'
channel.basic_publish(exchange='', routing_key='request_queue', body=message)
print(f" [x] Sent '{message}'")
time.sleep(20)

# Stop broadcast
message = 'X3'
channel.basic_publish(exchange='', routing_key='request_queue', body=message)
print(f" [x] Sent '{message}'")

for i in range(9):
    message = 'X1'
    channel.basic_publish(exchange='', 
                        routing_key='request_queue', 
                        properties=pika.BasicProperties(reply_to=response_queue),
                        body=message)
    print(f" [x] Sent '{message}'")
time.sleep(2)

# Get the insults of the list
while True:
    method_frame, header_frame, body = channel.basic_get(queue=response_queue, auto_ack=True)
    if method_frame:
        print("Messagee:", body.decode())
    else:
        print("Not more message")
        break



# Close connection
connection.close()