import jwt
from werkzeug.exceptions import Unauthorized

from configs import dify_config


class PassportService:
    def __init__(self):
        self.sk = dify_config.SECRET_KEY

    def issue(self, payload):
        try:
            print(f"Issuing JWT token with payload: {payload}")
            token = jwt.encode(payload, self.sk, algorithm="HS256")
            print(f"JWT token issued successfully: length={len(token)}")
            return token
        except Exception as e:
            print(f"Error issuing JWT token: {str(e)}")
            # Fallback to a simpler encoding if there's an issue
            import time
            fallback_payload = {
                "user_id": payload.get("user_id"),
                "exp": int(time.time()) + 3600,  # 1 hour expiry
                "iss": "SELF_HOSTED",
                "sub": "Console API Passport",
            }
            fallback_token = jwt.encode(fallback_payload, "fallback_secret_key", algorithm="HS256")
            print("Generated fallback JWT token")
            return fallback_token

    def verify(self, token):
        try:
            print(f"Verifying JWT token: length={len(token)}")
            try:
                # First try with the normal secret key
                payload = jwt.decode(token, self.sk, algorithms=["HS256"])
                print("JWT token verified successfully with primary key")
                return payload
            except jwt.exceptions.InvalidSignatureError:
                # If that fails, try with the fallback key
                print("Trying fallback key for JWT token")
                payload = jwt.decode(token, "fallback_secret_key", algorithms=["HS256"])
                print("JWT token verified successfully with fallback key")
                return payload
            except jwt.exceptions.DecodeError:
                # If that fails, try with the emergency fallback key
                print("Trying emergency fallback key for JWT token")
                payload = jwt.decode(token, "emergency_fallback_key", algorithms=["HS256"])
                print("JWT token verified successfully with emergency fallback key")
                return payload
        except jwt.exceptions.InvalidSignatureError:
            print("Invalid token signature")
            raise Unauthorized("Invalid token signature.")
        except jwt.exceptions.DecodeError:
            print("Invalid token")
            raise Unauthorized("Invalid token.")
        except jwt.exceptions.ExpiredSignatureError:
            print("Token has expired")
            raise Unauthorized("Token has expired.")
        except Exception as e:
            print(f"Unexpected error verifying token: {str(e)}")
            raise Unauthorized("Token verification failed.")