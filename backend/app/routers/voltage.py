from fastapi import APIRouter, Request, Depends, HTTPException, Body
from app.services.voltage import Voltage
from typing import Optional, Dict, List, Any
import os

# Router for Voltage API endpoints
router = APIRouter(prefix="/voltage", tags=["voltage"])

def get_voltage_service():
    """
    Dependency function to create a configured Voltage service instance.
    
    Retrieves API key and organization ID from environment variables
    and creates a Voltage service instance with these credentials.
    
    Returns:
        Voltage: A configured Voltage service instance
        
    Raises:
        HTTPException: If the Voltage API key is not configured
    """
    api_key = os.environ.get("VOLTAGE_API_KEY")
    organization_id = os.environ.get("VOLTAGE_ORG_ID")
    if not api_key:
        raise HTTPException(status_code=500, detail="Voltage API key not configured")
    return Voltage(api_key=api_key, organization_id=organization_id)

@router.get("/nodes")
async def get_nodes(organization_id: Optional[str] = None, voltage: Voltage = Depends(get_voltage_service)):
    """
    Retrieve a list of all nodes from the Voltage API.
    
    Args:
        organization_id (str, optional): Organization ID to use for the request.
            If not provided, uses the default from environment variables.
        voltage (Voltage): Voltage service instance (injected by FastAPI)
    
    Returns:
        dict: JSON response containing the list of nodes
        
    Raises:
        HTTPException: With appropriate status code and error message if request fails
    """
    try:
        return voltage.get_nodes(organization_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting nodes: {str(e)}")

@router.get("/nodes/{node_id}")
async def get_node(node_id: str, organization_id: Optional[str] = None, voltage: Voltage = Depends(get_voltage_service)):
    """
    Retrieve details for a specific node by its ID from the Voltage API.
    
    Args:
        node_id (str): ID of the node to retrieve
        organization_id (str, optional): Organization ID to use for the request.
            If not provided, uses the default from environment variables.
        voltage (Voltage): Voltage service instance (injected by FastAPI)
    
    Returns:
        dict: JSON response containing the node details
        
    Raises:
        HTTPException: With appropriate status code and error message if request fails
    """
    try:
        return voltage.get_node(node_id, organization_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting node: {str(e)}")

@router.post("/nodes")
async def create_node(
    node_data: Dict[str, Any] = Body(...),
    organization_id: Optional[str] = None,
    voltage: Voltage = Depends(get_voltage_service)
):
    """
    Create a new node with the specified configuration.
    
    Args:
        node_data (Dict[str, Any]): Configuration for the new node with keys:
            - name (str): Name of the node
            - network (str): Network type (e.g., 'mainnet', 'testnet')
            - type (str): Node type (e.g., 'standard')
            - settings (dict): Node settings including:
                - autopilot (bool): Whether to enable autopilot
                - grpc (bool): Whether to enable gRPC
                - rest (bool): Whether to enable REST API
                - keysend (bool): Whether to enable keysend
                - whitelist (list): List of whitelisted IPs
                - alias (str): Node alias
                - color (str): Node color (hex format)
        organization_id (str, optional): Organization ID to use for the request.
            If not provided, uses the default from environment variables.
        voltage (Voltage): Voltage service instance (injected by FastAPI)
    
    Returns:
        dict: JSON response containing the created node details
        
    Raises:
        HTTPException: With appropriate status code and error message if request fails
    """
    try:
        return voltage.create_node(node_data, organization_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating node: {str(e)}")
    
