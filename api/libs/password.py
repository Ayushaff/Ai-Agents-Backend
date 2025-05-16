
import base64
import binascii
import hashlib
import re

password_pattern = r"^(?=.*[a-zA-Z])(?=.*\d).{8,}$"


def valid_password(password):
    # Define a regex pattern for password rules
    pattern = password_pattern
    # Check if the password matches the pattern
    if re.match(pattern, password) is not None:
        return password

    raise ValueError("Password must contain letters and numbers, and the length must be greater than 8.")


def hash_password(password_str, salt_byte):
    dk = hashlib.pbkdf2_hmac("sha256", password_str.encode("utf-8"), salt_byte, 10000)
    return binascii.hexlify(dk)


def compare_password(password_str, password_hashed_base64, salt_base64):
    # compare password for login
    try:
        print(f"Comparing password: length={len(password_str)}")
        print(f"Salt base64 length: {len(salt_base64)}")
        print(f"Password hash base64 length: {len(password_hashed_base64)}")

        # Decode the salt from base64
        salt_bytes = base64.b64decode(salt_base64)
        print(f"Decoded salt length: {len(salt_bytes)}")

        # Hash the provided password with the salt
        hashed_input = hash_password(password_str, salt_bytes)
        print(f"Generated hash length: {len(hashed_input)}")

        # Decode the stored password hash from base64
        stored_hash = base64.b64decode(password_hashed_base64)
        print(f"Stored hash length: {len(stored_hash)}")

        # Compare the hashes
        result = hashed_input == stored_hash
        print(f"Password match result: {result}")

        return result
    except Exception as e:
        print(f"Error comparing password: {str(e)}")
        # If there's an error in comparison, return False for security
        return False