import subprocess

# create new user
result = subprocess.run('openssl rand -base64 40', shell=True, capture_output=True, text=True)
password = result.stdout.strip()

# set user password
result = subprocess.run('printf \'{}\' | mkpasswd --stdin --method=sha-256'.format(password), shell=True, capture_output=True, text=True)
passwordhash = result.stdout.strip()

print(password)
print(passwordhash)