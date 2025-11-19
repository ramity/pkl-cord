FROM python:slim

WORKDIR /code

RUN apt update
RUN apt upgrade -y
RUN apt install -y build-essential

RUN pip install --upgrade pip
RUN pip install discord.py
RUN pip install matplotlib

ENTRYPOINT sleep infinity
