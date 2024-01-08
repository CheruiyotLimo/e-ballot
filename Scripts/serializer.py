import secrets
import string

def generate_alphanumeric_sequence():
    alphanumeric_chars = string.ascii_letters + string.digits
    sequence = ''.join(secrets.choice(alphanumeric_chars) for _ in range(14))
    return sequence