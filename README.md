# GFactors

### How to Run:
## Way1:
At first, install the whole code into your local device. Also, one needs to install all the dependencies first, listed inside "requirements.txt" file.
Open up the "final-task" named folder and in 2 different cmd/powershell window, run both python files namely "sender.py" and "worker.py", simultaneously. You can find both files beneath folders "server" and "worker" respectively.
On the terminal where "sender.py" is running, you can find the url of localhost, on clicking it will redirect you to the default browser, where there's present a simple UI to put your test, and the text will get processed by worker and the sentiment of that text will be shown to you.

Note: I'm expecting rabbitmq is installed locally on your device, in case you are using rabbitmq image based container, on both "sender.py" and "worker.py" files, under line number 24 and 13 respectively, change the string "localhost" to "rabbitmq" first.

## Way2:
I tried to dockerize everything using docker-compose.yml. I wasn't able to test it becuase of not having the preferred configuration on my device, so may be running this can throw error.

Install the whole code into your local device. And on your Powershell window, hit command:
docker-compose up -d

This will run all three images, first image is for rabbitmq:3.6-management-alpine, second for worker(to process the text and return sentiment), and third for server.
