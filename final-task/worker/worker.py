import pika
import time
import tensorflow as tf
import tensorflow_hub as hub



sleepTime = 10
print(' [*] Sleeping for ', sleepTime, ' seconds.')
model = tf.keras.models.load_model('sentiment_model.h5',custom_objects={'KerasLayer':hub.KerasLayer})

print(' [*] Connecting to server ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print(' [*] Waiting for messages.')


def callback(ch, method, props, body):
    print(" [x] Received %s" % body)
    cmd = body.decode()

    array=[]
    sentiment=''
    array.append(cmd)
    ans=model.predict(array)
    if ans>0.5:
        sentiment="Sentiment is postive."
    else:
        sentiment="Sentiment is negative."

    response = sentiment
    print (sentiment, ans)
    print(" [x] Done")

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()