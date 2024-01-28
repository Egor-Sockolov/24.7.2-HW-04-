import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv('email')
password = os.getenv('password')
invalid_email = os.getenv('invalid_email')
invalid_password = os.getenv('invalid_password')
invalid_auth_key = os.getenv('invalid_auth_key')