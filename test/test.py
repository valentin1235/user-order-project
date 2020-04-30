import bcrypt, jwt
from datetime import datetime, timedelta

from config import SECRET
payload = {'id': 1, 'exp': datetime.utcnow() + timedelta(minutes=1)}
token = jwt.encode(payload, SECRET['secret_key'], algorithm=SECRET['algorithm'])

payload = jwt.decode(token, SECRET['secret_key'], algorithm=SECRET['algorithm'])

print(payload)