FROM python:3.9.10-slim
USER root
RUN apt-get update
RUN apt-get install -y micro \
    python3-pip \
    git \
    neofetch \
    procps

RUN apt-get autoremove -y
RUN apt-get clean -y

WORKDIR /root
RUN git clone https://github.com/bygregonline/challenge.git
WORKDIR /root/challenge
RUN pip3 install -r requirements.txt
WORKDIR /root/challenge/mainsite
RUN python3  manage.py makemigrations deliverect
RUN python3  manage.py migrate
RUN python3  manage.py test
RUN chmod 777 run_gunicorn.sh
ENTRYPOINT [ "run_gunicorn.sh" ]
EXPOSE 8888

