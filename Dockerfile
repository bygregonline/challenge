FROM python:3.9.10-slim
RUN apt-get update
RUN apt-get install -y micro \
    python3-pip \
    git \
    neofetch

RUN apt-get autoremove -y
RUN apt-get clean -y