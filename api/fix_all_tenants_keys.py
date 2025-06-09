import os
import sys
import opendal
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from flask import Flask

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions.ext_database import db
from models.account import Tenant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mohitsql@localhost:5432/dify'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def generate_and_save_keys(tenant_id):
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Get the public key
    public_key = private_key.public_key()
    
    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Create OpenDAL operator
    op = opendal.Operator(scheme="fs", root="storage")
    
    # Create tenant directory path
    tenant_dir = f"tenant/{tenant_id}"
    
    # Ensure the directory exists
    os.makedirs(os.path.join("storage", "tenant", tenant_id), exist_ok=True)
    
    # Save private key
    private_key_path = f"{tenant_dir}/private_key.pem"
    op.write(private_key_path, private_pem)
    print(f"Private key saved to: {private_key_path}")
    
    # Save public key
    public_key_path = f"{tenant_dir}/public_key.pem"
    op.write(public_key_path, public_pem)
    print(f"Public key saved to: {public_key_path}")
    
    print(f"RSA keys generated for tenant {tenant_id}")

with app.app_context():
    # Get all tenants
    tenants = db.session.query(Tenant).all()
    if tenants:
        for tenant in tenants:
            tenant_id = tenant.id
            print(f"Found tenant ID: {tenant_id}")
            generate_and_save_keys(tenant_id)
    else:
        print("No tenants found in the database")