import uuid
import random
import string


def make_id():
    """Generates a string with uuid4 hex"""
    return uuid.uuid4().hex


def sample_id(size=6, chars=string.ascii_uppercase + string.digits):
    """Returns a simple uppercase alphanumeric id """
    return ''.join(random.choice(chars) for _ in range(size))


def sample_email():
    """Return a randomly generated email address"""
    return f'{sample_id(size=10)}@{sample_id(size=5)}.{sample_id(size=3)}'
