FROM ubuntu:22.04

RUN apt-get update && apt install build-essential -y && apt install protobuf-compiler libprotobuf-dev python3-pip -y && apt install python3-protobuf -y

#COPY . /
