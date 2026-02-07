import secrets

def generate_django_secret_key():
    """
    Generates a secure Django SECRET_KEY.
    Django's default key length is 50 characters.
    """
    allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(allowed_chars) for _ in range(50))

if __name__ == "__main__":
    secret_key = generate_django_secret_key()
    print("Your new Django SECRET_KEY is:\n")
    print(secret_key)