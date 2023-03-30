FROM debian:stable-slim

ARG LITVERSION
ARG INITVERSION
ARG NETWORK

# LIT
ENV FILENAME lightning-terminal-linux-amd64-v${LITVERSION}
ENV FILE ${FILENAME}.tar.gz
ENV DOWNLOAD_URL https://github.com/lightninglabs/lightning-terminal/releases/download/v${LITVERSION}/${FILE}

# LNDINIT
ENV INIT_FILENAME lndinit-linux-amd64-v${INITVERSION}
ENV INIT_FILE ${INIT_FILENAME}.tar.gz
ENV INIT_DOWNLOAD_URL https://github.com/lightninglabs/lndinit/releases/download/v${INITVERSION}/${INIT_FILE}

RUN apt-get update \
  && apt-get install -y wget \
  
  # LNDINIT
  && mkdir lndinit_tmp \
  && cd lndinit_tmp \
  && wget $INIT_DOWNLOAD_URL \
  && tar xzvf $INIT_FILE \
  && mv $INIT_FILENAME/lndinit /usr/local/bin/ \
  && cd .. \
  && rm -rf lndinit_tmp \
  
  # LND
  && mkdir lnd_tmp \
  && cd lnd_tmp \
  && wget $DOWNLOAD_URL \
  && tar xzvf $FILE \
  && mv $FILENAME/litd /usr/local/bin/ \
  && mv $FILENAME/lncli /usr/local/bin/ \
  && mv $FILENAME/litcli /usr/local/bin/ \
  && mv $FILENAME/frcli /usr/local/bin/ \
  && mv $FILENAME/pool /usr/local/bin/ \
  && mv $FILENAME/loop /usr/local/bin/ \
  && cd .. \
  && rm -rf lnd_tmp \
  
  # remove wget
  && apt-get remove -y wget

CMD if [ ! -f /root/.lnd/seed.txt ]; then lndinit gen-seed > /root/.lnd/seed.txt ; fi \  
  && if [ ! -f /root/.lnd/data/chain/bitcoin/${NETWORK} ]; then lndinit -v init-wallet --secret-source=file --file.seed=/root/.lnd/seed.txt --file.wallet-password=/root/.lnd/walletpassword.txt --init-file.output-wallet-dir=/root/.lnd/data/chain/bitcoin/${NETWORK} --init-file.validate-password ; fi \  
  && litd --uipassword=_PWD_ \