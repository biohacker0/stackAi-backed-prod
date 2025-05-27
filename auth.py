import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

supabase_url = os.getenv("SUPABASE_URL")
anon_key = os.getenv("SUPABASE_ANON_KEY")

print(f"Supabase URL: {supabase_url}")
print(f"Anon Key: {anon_key}")

# Store token in memory
auth_token = None
org_id = None

def login(email, password):
    global auth_token, org_id
    
    if not supabase_url or not anon_key:
        raise Exception("Environment variables SUPABASE_URL and SUPABASE_ANON_KEY must be set")
    
    url = f"{supabase_url}/auth/v1/token?grant_type=password"
    
    response = requests.post(
        url,
        json={
            "email": email,
            "password": password,
            "gotrue_meta_security": {},
        },
        headers={
            "Content-Type": "application/json",
            "Apikey": anon_key,
        },
        timeout=10,
    )
    
    if response.status_code != 200:
        logger.error(f"Login failed: {response.text}")
        return None
    
    auth_token = response.json()["access_token"]
    logger.info("Login successful")
    
    # Get org_id
    headers = getAuthHeaders()
    org_response = requests.get(
        "https://api.stack-ai.com/organizations/me/current",
        headers=headers
    )
    
    if org_response.status_code == 200:
        org_id = org_response.json()["org_id"]
        logger.info(f"Got org_id: {org_id}")
    
    return auth_token

def getAuthHeaders():
    if not auth_token:
        raise Exception("Not authenticated")
    return {"Authorization": f"Bearer {auth_token}"}

def getOrgId():
    return org_id