import uuid


def make_id(prefix):
    suffix = uuid.uuid4().hex
    return f'{prefix}_{suffix}'
