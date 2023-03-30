# set alpine as the base image of the Dockerfile
FROM debian:stable-slim

# update the package repository and install Tor
RUN apt-get update \
  && apt-get install -y tor \
  && apt-get clean 

CMD tor -f /etc/tor/torrc