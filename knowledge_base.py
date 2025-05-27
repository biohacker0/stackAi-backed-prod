import requests
import logging
from auth import getAuthHeaders, getOrgId
import json

logger = logging.getLogger(__name__)

backend_url = "https://api.stack-ai.com"
connection_id = "e171b021-8c00-4c3f-8a93-396095414f57"

def createKnowledgeBase(name, description, resource_ids):
    """Create a new knowledge base with selected resources"""
    headers = getAuthHeaders()
    
    data = {
        "connection_id": connection_id,
        "connection_source_ids": resource_ids,
        "name": name,
        "description": description,
        "indexing_params": {
            "ocr": False,
            "unstructured": True,
            "embedding_params": {
                "embedding_model": "text-embedding-ada-002",
                "api_key": None
            },
            "chunker_params": {
                "chunk_size": 1500,
                "chunk_overlap": 500,
                "chunker": "sentence"
            },
        },
        "org_level_role": None,
        "cron_job_id": None,
    }
    
    response = requests.post(
        f"{backend_url}/knowledge_bases",
        headers=headers,
        json=data
    )
    
    if response.status_code not in [200, 201]:
        logger.error(f"Failed to create KB: {response.text}")
        return None
    
    kb_data = response.json()
    return {
        "id": kb_data["knowledge_base_id"],
        "name": kb_data["name"],
        "created_at": kb_data["created_at"],
        "is_empty": kb_data["is_empty"]
    }

def syncKnowledgeBase(kb_id):
    """Trigger sync for knowledge base"""
    headers = getAuthHeaders()
    org_id = getOrgId()
    
    if not org_id:
        logger.error("No org_id available")
        return False
    
    url = f"{backend_url}/knowledge_bases/sync/trigger/{kb_id}/{org_id}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Failed to sync KB: {response.text}")
        return False
    
    return True

def listKnowledgeBaseResources(kb_id, resource_path="/"):
    """List resources in a knowledge base"""
    headers = getAuthHeaders()
    
    url = f"{backend_url}/knowledge_bases/{kb_id}/resources/children"
    params = {"resource_path": resource_path}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        logger.error(f"Failed to list KB resources: {response.text}")
        return None
    
    data = response.json()
    
    # Handle nested data structure
    if isinstance(data, dict) and 'data' in data:
        resources = data['data']
    else:
        resources = data
    
    formatted_resources = []
    for resource in resources:
        path = resource['inode_path']['path'] if isinstance(resource['inode_path'], dict) else resource['inode_path']
        formatted_resources.append({
            "id": resource["resource_id"],
            "name": path,
            "type": resource["inode_type"],
            "status": resource.get("status", "unknown"),
            "indexed_at": resource.get("indexed_at")
        })
    
    return formatted_resources

def deleteResourceFromKB(kb_id, resource_path):
    """Remove a file from knowledge base (de-index)"""
    headers = getAuthHeaders()
    
    url = f"{backend_url}/knowledge_bases/{kb_id}/resources"
    params = {"resource_path": resource_path}
    
    response = requests.delete(url, headers=headers, params=params)
    
    if response.status_code not in [200, 204]:
        logger.error(f"Failed to delete resource: {response.text}")
        return False
    
    return True
