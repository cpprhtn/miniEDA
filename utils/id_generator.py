import random
import string
import time

def createId():
  timestamp = int(time.time())
  encoded_timestamp = base36encode(timestamp)
  random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
  id = encoded_timestamp + random_chars

  return id

def base36encode(number):
  base36 = string.digits + string.ascii_lowercase
  encoded = ''

  while number:
    number, remainder = divmod(number, 36)
    encoded = base36[remainder] + encoded

  return encoded
