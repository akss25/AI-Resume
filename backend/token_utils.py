import jwt
import datetime
from flask import current_app as app

def generate_token(email):
    """Generate a JWT token."""
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Token expires in 1 day
            'iat': datetime.datetime.utcnow(),  # Issued at
            'sub': email  # Subject of the token (user ID)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    except Exception as e:
        print(f"Error generating token: {e}")
        return None

def verify_token(token):
    """Verify the JWT token and return the user ID if valid."""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']  # Return the user ID
    except jwt.ExpiredSignatureError:
        print("Token expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None
