FROM ubuntu:18.04

COPY ./opensmile /app/

WORKDIR /app/

RUN apt-get update && apt-get install -y \
    automake \
    autoconf \
    gcc \
    g++ \
    libasound2-dev \
    make \
    patch \
    libx11-dev \
    build-essential \
    libtool \
    m4



RUN ./buildStandalone.sh