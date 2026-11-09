import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "pharmacy.db")
SECRET_KEY = os.environ.get("SECRET_KEY", "add-your-secret-key")

# Validation limits
MIN_PASSWORD_LENGTH = 4
MIN_PHONE_LENGTH = 10
MAX_PHONE_LENGTH = 15
MAX_QUANTITY = 100000
MAX_PRICE = 1000000
DATE_FORMAT = "%Y-%m-%d"

# Order IDs start from 1000
ORDER_ID_START = 1000

# Account types shown on the login page
ACCOUNT_TYPES = {"customer": "Customer", "seller": "Seller"}
