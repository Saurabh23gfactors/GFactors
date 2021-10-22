# init a base image(Alpine, small linux distro)
FROM python:3.8

#define present working directory
WORKDIR /server

#Copy contents into working dir
ADD . /server

#Install dependencies 
RUN pip install -r requirements.txt

#define command to build the image
CMD ["python", "sender.py"]
