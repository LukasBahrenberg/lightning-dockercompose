FROM debian:stable-slim

RUN apt-get update \
  && apt-get install -y curl \
  && apt-get install -y bash \
  && apt-get install -y apt-utils  \
  && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt update \
  && apt install -y nodejs \
  && apt-get install -y git \
  && cd /root \
  && git clone https://github.com/apotdevin/thunderhub.git \
  && cd thunderhub \
  && npm install \
  && npm run build \
  && apt-get remove -y curl \ 
  && apt-get remove -y git 

CMD cd /root/thunderhub && npm start