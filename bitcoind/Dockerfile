FROM debian:stable-slim

ENV FILENAME bitcoin-${BITCOINDVERSION}-x86_64-linux-gnu.tar.gz
ENV DOWNLOAD_URL https://bitcoincore.org/bin/bitcoin-core-${BITCOINDVERSION}/${FILENAME}

RUN apt-get update \
  && apt-get install -y  wget \
  && wget $DOWNLOAD_URL \
  && apt-get remove -y wget \
  && tar xzvf /bitcoin-${BITCOINDVERSION}-x86_64-linux-gnu.tar.gz \
  && mkdir /root/.bitcoin \
  && mv /bitcoin-${BITCOINDVERSION}/bin/* /usr/local/bin/ \
  && rm -rf /bitcoin-${BITCOINDVERSION}/ \
  && rm -rf /bitcoin-${BITCOINDVERSION}-x86_64-linux-gnu.tar.gz 

CMD bitcoind