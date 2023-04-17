import subprocess
import re
import base64
import os
import time
from requests import get
import getpass
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# assign env variables & co
network = os.getenv('NETWORK')
nodenumber = os.getenv('NODENUMBER')
domain = os.getenv('DOMAIN')
nodealias = os.getenv('NODEALIAS')
nodeurl = network + '-' + nodenumber + '.' + domain

# credentials
user = getpass.getuser()

# macaroons in hex
print('')
print('admin macaroon:')
subprocess.run('sudo xxd -p -c2000 /home/{}/.lnd/data/chain/bitcoin/{}/admin.macaroon'.format(user, network), shell=True)
print('')
print('readonly macaroon:')
subprocess.run('sudo xxd -p -c2000 /home/{}/.lnd/data/chain/bitcoin/{}/readonly.macaroon'.format(user, network), shell=True)
print('')
print('invoice macaroon:')
subprocess.run('sudo xxd -p -c2000 /home/{}/.lnd/data/chain/bitcoin/{}/invoice.macaroon'.format(user, network), shell=True)
print('')

# certs in hex
def remove(rem, my_string):
  return re.sub(".*" + rem + ".*\n?", "", my_string)
with open('/home/{}/.lnd/tls.cert'.format(user), 'r') as file: # Read in the file
  tls_cert = file.read()
# print(tls_cert)
tls_cert = remove('-----BEGIN CERTIFICATE-----', tls_cert)
tls_cert = remove('-----END CERTIFICATE-----', tls_cert)
tls_cert_hex = base64.b64decode(tls_cert).hex()
print('tls cert:')
print(tls_cert_hex + '\n')

# get macaroon
subprocess_result = subprocess.run('sudo xxd -p -c2000 /home/{}/.lnd/data/chain/bitcoin/{}/admin.macaroon'.format(user, network), shell=True, capture_output=True, text=True)
admin_macaroon = subprocess_result.stdout.strip()

# create lit LNC session
subprocess_result = subprocess.run('sudo docker exec lit litcli --network {} --tlscertpath /root/.lit/tls.cert sessions add --label="default" --type=admin'.format(network), shell=True)
