import os
import sys
import opendal
from flask import Flask

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions.ext_database import db
from models.account import Tenant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mohitsql@localhost:5432/dify'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Get all tenants
    tenants = db.session.query(Tenant).all()
    if tenants:
        for tenant in tenants:
            tenant_id = tenant.id
            print(f"Checking tenant ID: {tenant_id}")
            
            # Create OpenDAL operator
            op = opendal.Operator(scheme="fs", root="storage")
            
            # Check if keys exist
            private_key_path = f"privkeys/{tenant_id}/private.pem"
            
            private_key_exists = op.exists(private_key_path)
            
            print(f"  Private key exists: {private_key_exists}")
            
            if private_key_exists:
                print(f"  Private key exists for tenant {tenant_id}.")
                
                # Check if public key is in the database
                tenant_obj = db.session.query(Tenant).filter(Tenant.id == tenant_id).first()
                if tenant_obj and tenant_obj.encrypt_public_key:
                    print(f"  Public key exists in database for tenant {tenant_id}.")
                else:
                    print(f"  Public key is missing in database for tenant {tenant_id}.")
            else:
                print(f"  Private key is missing for tenant {tenant_id}. Please check the paths and permissions.")
    else:
        print("No tenants found in the database")