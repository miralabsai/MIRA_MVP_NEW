import secrets

key = secrets.token_urlsafe(32)  # generates a random URL-safe key
print(key)
