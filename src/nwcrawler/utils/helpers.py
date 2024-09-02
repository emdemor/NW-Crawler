import hashlib


def create_hash(texto, method="md5"):
    if method not in hashlib.algorithms_available:
        raise Exception(
            f"method '{method}' not recognized. Available methods are {hashlib.algorithms_available}"
        )
    hash_object = getattr(hashlib, method)()
    hash_object.update(texto.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex
