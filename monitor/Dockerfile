FROM python:3.11-slim

WORKDIR /app
ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get update
RUN apt-get install -y openssh-client

EXPOSE 80

CMD ["python", "monitor.py"]
