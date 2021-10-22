from flask import Flask, render_template,request,Response
import pika
import uuid


app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('homePage.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=="POST":
         message = sentimentAnalysis.call(request.form['Message'])
    #response = sentimentAnalysis.call(message)
    return Response( message)


class SentimentRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return (self.response)

sentimentAnalysis = SentimentRpcClient()



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')