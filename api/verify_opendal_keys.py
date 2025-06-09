import os
import sys
import opendal
from flask import Flask

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions.ext_database import db
from models.account import Tenant  # Changed from models.tenant to models.account

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mohitsql@localhost:5432/dify'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Get the current tenant ID
    tenant = db.session.query(Tenant).first()
    if tenant:
        tenant_id = tenant.id
        print(f"Found tenant ID: {tenant_id}")
        
        # Create OpenDAL operator
        op = opendal.Operator(scheme="fs", root="storage")
        
        # Check if keys exist
        private_key_path = f"tenant/{tenant_id}/private_key.pem"
        public_key_path = f"tenant/{tenant_id}/public_key.pem"
        
        private_key_exists = op.exists(private_key_path)
        public_key_exists = op.exists(public_key_path)
        
        print(f"Private key exists: {private_key_exists}")
        print(f"Public key exists: {public_key_exists}")
        
        if private_key_exists and public_key_exists:
            print("Both keys exist. The issue should be resolved.")
        else:
            print("Keys are missing. Please check the paths and permissions.")
    else:
        print("No tenant found in the database")
