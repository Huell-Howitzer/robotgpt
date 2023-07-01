import os
def generate_secret_key():
    """Generate a random secret key"""
    return os.urandom(24)