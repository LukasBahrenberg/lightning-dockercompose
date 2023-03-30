FROM debian:stable-slim

ARG RTLVERSION

ENV FILENAME v${RTLVERSION}.tar.gz
ENV DOWNLOAD_URL https://github.com/Ride-The-Lightning/RTL/archive/refs/tags/v${RTLVERSION}/${FILENAME}

RUN apt-get update \
  && apt-get install -y wget \
  && apt-get install -y curl \
  && apt-get install -y bash \
  && apt-get install -y apt-utils  \
  && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt update \
  && apt install -y nodejs \
  && mkdir rtl_tmp \
  && cd rtl_tmp \
  && wget $DOWNLOAD_URL \
  && tar xvf $FILENAME \
  && mv RTL-${RTLVERSION} RTL \
  && mv RTL /root \
  && cd .. \
  && rm -rf rtl_tmp \
  && cd /root/RTL \
  && apt-get remove -y wget \
  && apt-get remove -y curl \
  && npm install --omit=dev 

CMD node /root/RTL/rtl