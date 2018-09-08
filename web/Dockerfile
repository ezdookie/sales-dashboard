FROM python:3.6.4
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y

RUN apt-get install -y ruby-full build-essential rubygems
RUN gem install sass

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD wait-for-it.sh /app/
RUN chmod +x ./wait-for-it.sh
