# This script is designed to be run as root from a brand new Linux installation 
# As root user, commands would not need to be run as sudo. This makes it testable, however, for non-root users and still works for the root user.

import subprocess
import base64
import re
import time
import json
from pprint import pprint
import os
from dotenv import load_dotenv
import getpass
from requests import get

# get user name
user = getpass.getuser()

# load environment variables
load_dotenv()

s3accesskey = os.getenv('S3ACCESSKEY')
s3secretkey = os.getenv('S3SECRETKEY')
s3url = os.getenv('S3URL')
s3bucketname = os.getenv('S3BUCKETNAME')

# install aws cli tool
subprocess.run('wget https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -O awscliv2.zip', shell=True)
subprocess.run('unzip awscliv2.zip && sudo ./aws/install --update', shell=True)
subprocess.run('((printf \"%s\n\" \"{}\" \"{}\" \"\" \"\") && cat) | sudo aws configure --profile eu2'.format(s3accesskey, s3secretkey), shell=True)

# load data from S3 bucket
subprocess.run('sudo aws --profile eu2 --endpoint-url {} s3 sync s3://{}/.lnd /home/{}/.lnd'.format(s3url, user, s3bucketname), shell=True)
subprocess.run('sudo aws --profile eu2 --endpoint-url {} s3 sync s3://{}/.lit /home/{}/.lit'.format(s3url, user, s3bucketname), shell=True)
subprocess.run('sudo aws --profile eu2 --endpoint-url {} s3 cp s3://{}/lightning-dockercompose/.env /home/{}/lightning-dockercompose/.env'.format(s3url, user, s3bucketname), shell=True)

# load environment variables
load_dotenv()

# assign env variables & co
bitcoindversion = os.getenv('BITCOINDVERSION')
litversion = os.getenv('LITVERSION')
initversion = os.getenv('INITVERSION')
rtlversion = os.getenv('RTLVERSION')

network = os.getenv('NETWORK')
nodenumber = os.getenv('NODENUMBER')
domain = os.getenv('DOMAIN')
nodealias = os.getenv('NODEALIAS')
nodeurl = network + '-' + nodenumber + '.' + domain

bitcoindrpcport = os.getenv('BITCOINDRPCPORT')
litrpcport = os.getenv('LITRPCPORT')
rtlrpcport = os.getenv('RTLRPCPORT')
thrpcport = os.getenv('THRPCPORT')

s3backup = os.getenv('S3BACKUP')

# get public ip
ip = get('https://api.ipify.org').content.decode('utf8')
print(ip)

# reset permissions
subprocess.run('sudo chown -R {}:sudo /home/{}'.format(user, user), shell=True)

# set password for wallet, rpc, rtl & save to file
with open('/home/{}/.lnd/walletpassword.txt'.format(user), 'r') as file: # Read in the file
  filedata = file.read()
password = filedata

# determine tor hashed control password
result = subprocess.run('tor --hash-password {}'.format(password), shell=True, capture_output=True, text=True)
torhashedcontrolpassword = result.stdout.strip()

# insert into config files

## tor torrc
with open('/home/{}/lightning-dockercompose/tor/torrc'.format(user), 'r') as file: # Read in the file
  filedata = file.read()
filedata = filedata.replace('HashedControlPassword', 'HashedControlPassword ' + torhashedcontrolpassword) # Replace the target string
with open('/home/{}/lightning-dockercompose/tor/torrc'.format(user), 'w') as file: # Write the file out again
  file.write(filedata)

## bitcoin.conf
with open('/home/{}/lightning-dockercompose/bitcoind/bitcoin.conf'.format(user), 'r') as file: # Read in the file
  filedata = file.read()
filedata = filedata.replace('_NETWORK_', network) # Replace the target string
filedata = filedata.replace('_USER_', user) # Replace the target string
filedata = filedata.replace('_PWD_', password) # Replace the target string
filedata = filedata.replace('_BITCOINDRPCPORT_', bitcoindrpcport) # Replace the target string
with open('/home/{}/lightning-dockercompose/bitcoind/bitcoin.conf'.format(user), 'w') as file: # Write the file out again
  file.write(filedata)

## lit.conf
with open('/home/{}/lightning-dockercompose/lit/lit.conf'.format(user), 'r') as file: # Read in the file
  filedata = file.read()
filedata = filedata.replace('_NETWORK_', network) # Replace the target string
filedata = filedata.replace('_NODEALIAS_', nodealias) # Replace the target string
filedata = filedata.replace('_NODEURL_', nodeurl) # Replace the target string
filedata = filedata.replace('_IP_', ip) # Replace the target string
filedata = filedata.replace('_USER_', user) # Replace the target string
filedata = filedata.replace('_BITCOINDRPCPORT_', bitcoindrpcport) # Replace the target string
filedata = filedata.replace('_PWD_', password) # Replace the target string
with open('/home/{}/lightning-dockercompose/lit/lit.conf'.format(user), 'w') as file: # Write the file out again
  file.write(filedata)

## lit.conf
with open('/home/{}/lightning-dockercompose/lit/Dockerfile'.format(user), 'r') as file: # Read in the file
  filedata = file.read()
filedata = filedata.replace('_PWD_', password) # Replace the target string
with open('/home/{}/lightning-dockercompose/lit/Dockerfile'.format(user), 'w') as file: # Write the file out again
  file.write(filedata)

## rtl conf
with open('/home/{}/lightning-dockercompose/rtl/RTL-Config.json'.format(user), 'r') as file: # Read in the file
  filedata = file.read()
filedata = filedata.replace('_RTLPORT_', rtlrpcport) # Replace the target string
filedata = filedata.replace('_NETWORK_', network) # Replace the target string
filedata = filedata.replace('_PWD_', password) # Replace the target string
with open('/home/{}/lightning-dockercompose/rtl/RTL-Config.json'.format(user), 'w') as file: # Write the file out again
  file.write(filedata)

## thunderhub config.yaml
with open('/home/{}/lightning-dockercompose/thunderhub/config.yaml'.format(user), 'r') as file: # Read in the file
  filedata = file.read()
filedata = filedata.replace('_PWD_', password) # Replace the target string
filedata = filedata.replace('_NETWORK_', network) # Replace the target string
with open('/home/{}/lightning-dockercompose/thunderhub/config.yaml'.format(user), 'w') as file: # Write the file out again
  file.write(filedata)

## thunderhub .env
with open('/home/{}/lightning-dockercompose/thunderhub/.env'.format(user), 'r') as file: # Read in the file
  filedata = file.read()
filedata = filedata.replace('_THRPCPORT_', thrpcport) # Replace the target string
filedata = filedata.replace('_NETWORK_', network) # Replace the target string
filedata = filedata.replace('_URL_', nodeurl) # Replace the target string
with open('/home/{}/lightning-dockercompose/thunderhub/.env'.format(user), 'w') as file: # Write the file out again
  file.write(filedata)

## use backup service
if s3backup=='true': 
  with open('/home/{}/lightning-dockercompose/docker-compose.yaml'.format(user), 'r') as file: # Read in the file
    filedata = file.read()
  filedata = filedata.replace('profiles:', '# profiles:') # Replace the target string
  filedata = filedata.replace('- donotstart', '# - donotstart ') # Replace the target string
  with open('/home/{}/lightning-dockercompose/docker-compose.yaml'.format(user), 'w') as file: # Write the file out again
    file.write(filedata)

# run docker compose
subprocess.run('sudo docker compose up -d --build', shell=True)