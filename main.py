from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv
import auth
import connections
import knowledge_base

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Get CORS origins from environment
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Stack AI Backend API"}

## Authentication endpoints

@app.post("/auth/login")
def login(body: dict):
    email = body.get("email")
    password = body.get("password")
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    token = auth.login(email, password)
    
    if not token:
        raise HTTPException(status_code=401, detail="Login failed")
    
    return {"success": True, "message": "Logged in successfully"}

@app.get("/auth/status")
def auth_status():
    try:
        headers = auth.getAuthHeaders()
        return {"authenticated": True}
    except:
        return {"authenticated": False}
    

## Connection endpoints    

@app.get("/connections/info")
def get_connection_info():
    info = connections.getConnectionInfo()
    if not info:
        raise HTTPException(status_code=404, detail="Connection not found")
    return info

@app.get("/connections/resources")
def list_resources(resource_id: str = None):
    resources = connections.listResources(resource_id)
    if resources is None:
        raise HTTPException(status_code=500, detail="Failed to fetch resources")
    return {"data": resources}



## knowledge base endpoints

@app.post("/knowledge-bases")
def create_knowledge_base(body: dict):
    name = body.get("name")
    description = body.get("description", "")
    resource_ids = body.get("resource_ids", [])
    
    if not name or not resource_ids:
        raise HTTPException(status_code=400, detail="Name and resource_ids required")
    
    kb = knowledge_base.createKnowledgeBase(name, description, resource_ids)
    
    if not kb:
        raise HTTPException(status_code=500, detail="Failed to create knowledge base")
    
    return kb

@app.post("/knowledge-bases/{kb_id}/sync")
def sync_knowledge_base(kb_id: str):
    success = knowledge_base.syncKnowledgeBase(kb_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to sync knowledge base")
    
    return {"success": True, "message": "Sync initiated"}

@app.get("/knowledge-bases/{kb_id}/resources")
def list_kb_resources(kb_id: str, resource_path: str = "/"):
    resources = knowledge_base.listKnowledgeBaseResources(kb_id, resource_path)
    
    if resources is None:
        raise HTTPException(status_code=500, detail="Failed to fetch resources")
    
    return {"data": resources}

@app.delete("/knowledge-bases/{kb_id}/resources")
def delete_kb_resource(kb_id: str, resource_path: str):
    success = knowledge_base.deleteResourceFromKB(kb_id, resource_path)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete resource")
    
    return {"success": True, "message": "Resource deleted"}



