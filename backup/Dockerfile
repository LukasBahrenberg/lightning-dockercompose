FROM debian:stable-slim
  
# install wget
RUN apt update \
  && apt -y install wget unzip inotify-tools

RUN	wget https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -O awscliv2.zip
RUN	unzip awscliv2.zip && ./aws/install 
RUN rm awscliv2.zip

# remove wget
RUN apt-get remove -y wget unzip

# this profile config step might need to be updated depending on your s3 provider 
RUN ((printf "%s\n" "${S3ACCESSKEY}" "${S3SECRETKEY}" "" "") && cat) | aws configure --profile eu2 

CMD while true; do inotifywait /root/.lnd/data/chain/bitcoin/${NETWORK}/channel.backup \ 
  && aws --profile eu2 --endpoint-url ${S3URL} s3 cp /root/.lnd/data/chain/bitcoin/${NETWORK}/channel.backup s3://${BUCKETNAME}/channel.backup; \
  done