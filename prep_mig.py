import subprocess
import os
from dotenv import load_dotenv
import getpass
from requests import get

# load environment variables
load_dotenv()
network = os.getenv('NETWORK')
s3accesskey = os.getenv('S3ACCESSKEY')
s3secretkey = os.getenv('S3SECRETKEY')
s3url = os.getenv('S3URL')
s3bucketname = os.getenv('S3BUCKETNAME')

# get user name
user = getpass.getuser()

# stop docker containers
subprocess.run('sudo docker compose down', shell=True)

# delete certificates etc.
subprocess.run('sudo rm -rf ../.lnd/tls.cert', shell=True)
subprocess.run('sudo rm -rf ../.lnd/tls.key', shell=True)
subprocess.run('sudo rm -rf ../.lnd/v3_onion_private_key', shell=True)
subprocess.run('sudo rm -rf ../.lit/tls.cert', shell=True)
subprocess.run('sudo rm -rf ../.lit/tls.key', shell=True)
subprocess.run('sudo rm -rf ../.lit/letsencrypt', shell=True)

# install aws cli tool
subprocess.run('wget https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -O awscliv2.zip', shell=True)
subprocess.run('unzip awscliv2.zip && sudo ./aws/install --update', shell=True)
subprocess.run('((printf \"%s\n\" \"{}\" \"{}\" \"\" \"\") && cat) | sudo aws configure --profile eu2'.format(s3accesskey, s3secretkey), shell=True)

# create backups
subprocess.run('sudo aws --profile eu2 --endpoint-url {} s3 sync /home/{}/.lnd s3://{}/.lnd'.format(s3url, user, s3bucketname), shell=True)
subprocess.run('sudo aws --profile eu2 --endpoint-url {} s3 sync /home/{}/.lit s3://{}/.lit'.format(s3url, user, s3bucketname), shell=True)
subprocess.run('sudo aws --profile eu2 --endpoint-url {} s3 cp /home/{}/lightning-dockercompose/.env s3://{}/lightning-dockercompose/.env'.format(s3url, user, s3bucketname), shell=True)