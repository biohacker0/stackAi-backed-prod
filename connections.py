import requests
import logging
import os
from dotenv import load_dotenv
from auth import getAuthHeaders

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

backend_url = os.getenv("BACKEND_URL")
connection_id = os.getenv("CONNECTION_ID")

def listResources(resource_id=None):
    """List files and folders from Google Drive connection"""
    if not backend_url or not connection_id:
        raise Exception("Environment variables BACKEND_URL and CONNECTION_ID must be set")
        
    headers = getAuthHeaders()
    
    url = f"{backend_url}/connections/{connection_id}/resources/children"
    
    params = {}
    if resource_id:
        params["resource_id"] = resource_id
    
    logger.info(f"Fetching resources: {url} with params: {params}")
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        logger.error(f"Failed to fetch resources: {response.text}")
        return None
    
    data = response.json()
    
    # Handle the nested data structure
    if isinstance(data, dict) and 'data' in data:
        resources = data['data']
    else:
        resources = data
    
    # Format the resources for frontend
    formatted_resources = []
    for resource in resources:
        formatted_resources.append({
            "id": resource["resource_id"],
            "name": resource["inode_path"]["path"],
            "type": resource["inode_type"],
            "size": resource.get("size", 0),
            "mime_type": resource.get("content_mime", ""),
            "indexed_at": resource.get("indexed_at"),
            "status": resource.get("status", "resource")
        })
    
    return formatted_resources

def getConnectionInfo():
    """Get connection details"""
    headers = getAuthHeaders()
    
    url = f"{backend_url}/connections?connection_provider=gdrive&limit=5"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Failed to fetch connections: {response.text}")
        return None
    
    connections = response.json()
    
    # Find our working connection
    for conn in connections:
        if conn["connection_id"] == connection_id:
            return {
                "id": conn["connection_id"],
                "name": conn["name"],
                "created_at": conn["created_at"]
            }
    
    return None