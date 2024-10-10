import uuid
from django.core.cache import cache


def generate_delete_token(item_id):
    token = str(uuid.uuid4())
    cache.set(f'delete_token_{item_id}', token, timeout=600)
    return token

def validate_delete_token(item_id, token):
    cached_token = cache.get(f'delete_token_{item_id}')
    return cached_token == token

