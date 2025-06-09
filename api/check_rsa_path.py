import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from libs import rsa
from models.account import Tenant
from flask import Flask
from extensions.ext_database import db

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
            
            # Get the filepath that rsa.py is looking for
            filepath = f"privkeys/{tenant_id}/private.pem"
            print(f"RSA module is looking for: {filepath}")
            
            # Check if the directory exists
            privkeys_dir = os.path.join("storage", "privkeys", tenant_id)
            if not os.path.exists(privkeys_dir):
                print(f"Directory does not exist: {privkeys_dir}")
                os.makedirs(privkeys_dir, exist_ok=True)
                print(f"Created directory: {privkeys_dir}")
    else:
        print("No tenants found in the database")