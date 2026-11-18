from datetime import datetime

from core.config import (
    DATE_FORMAT,
    MAX_PHONE_LENGTH,
    MAX_PRICE,
    MAX_QUANTITY,
    MIN_PASSWORD_LENGTH,
    MIN_PHONE_LENGTH,
)


def check_phone(phno):
    if not phno.isdigit():
        return "Phone number must contain digits only"
    if len(phno) < MIN_PHONE_LENGTH or len(phno) > MAX_PHONE_LENGTH:
        return "Phone number must be %d to %d digits" % (
            MIN_PHONE_LENGTH,
            MAX_PHONE_LENGTH,
        )
    return ""


def check_email(email):
    if "@" not in email or "." not in email.split("@")[-1]:
        return "Enter a valid email address"
    return ""


def check_passwords(pass1, pass2):
    if len(pass1) < MIN_PASSWORD_LENGTH:
        return "Password must be at least %d characters" % MIN_PASSWORD_LENGTH  # noqa: UP031
    if pass1 != pass2:
        return "Passwords do not match"
    return ""


def check_not_empty(fields):
    # fields is a dict of label -> value
    for label in fields:
        if fields[label].strip() == "":
            return label + " is required"
    return ""


def to_int(text):
    try:
        return int(text)
    except ValueError:
        return None


def check_quantity(text):
    number = to_int(text)
    if number is None or number <= 0:
        return "Quantity must be a whole number greater than 0"
    if number > MAX_QUANTITY:
        return "Quantity cannot be more than %d" % MAX_QUANTITY  # noqa: UP031
    return ""


def check_price(text):
    number = to_int(text)
    if number is None or number <= 0:
        return "Price must be a whole number greater than 0"
    if number > MAX_PRICE:
        return "Price cannot be more than %d" % MAX_PRICE  # noqa: UP031
    return ""


def check_date(text, label):
    try:
        datetime.strptime(text, DATE_FORMAT)
    except ValueError:
        return "Invalid %s, use YYYY-MM-DD" % label
    return ""


def check_dates(mfg, exp):
    error = check_date(mfg, "manufacture date")
    if error:
        return error
    error = check_date(exp, "expiry date")
    if error:
        return error
    if exp <= mfg:
        return "Expiry date must be after manufacture date"
    return ""
