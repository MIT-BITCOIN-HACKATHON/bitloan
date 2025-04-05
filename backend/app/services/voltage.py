import requests
import json

class Voltage:
    """
    Service class for interacting with the Voltage API.
    Provides methods to retrieve node information from Voltage Cloud.
    """
    
    def __init__(self, api_key=None, organization_id=None):
        """
        Initialize the Voltage service with authentication credentials.
        
        Args:
            api_key (str, optional): Voltage API key for authentication
            organization_id (str, optional): Default organization ID to use for requests
        """
        self.api_key = api_key
        self.organization_id = organization_id
        self.base_url = "https://api.voltage.cloud"
        
    def get_nodes(self, organization_id=None):
        """
        Retrieve a list of all nodes for the specified organization.
        
        Args:
            organization_id (str, optional): Organization ID to use, falls back to the default if not provided
            
        Returns:
            dict: JSON response containing the list of nodes from Voltage API
            
        Raises:
            ValueError: If no organization ID is available
        """
        org_id = organization_id or self.organization_id
        if not org_id:
            raise ValueError("Organization ID is required")
            
        url = f"{self.base_url}/organizations/{org_id}/nodes"
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-VOLTAGE-AUTH': self.api_key
        }
        
        response = requests.request("GET", url, headers=headers)
        return response.json()
        
    def get_node(self, node_id, organization_id=None):
        """
        Retrieve details for a specific node by its ID.
        
        Args:
            node_id (str): ID of the node to retrieve
            organization_id (str, optional): Organization ID to use, falls back to the default if not provided
            
        Returns:
            dict: JSON response containing the specific node details from Voltage API
            
        Raises:
            ValueError: If no organization ID is available or node_id is not provided
        """
        org_id = organization_id or self.organization_id
        if not org_id:
            raise ValueError("Organization ID is required")
        if not node_id:
            raise ValueError("Node ID is required")
            
        url = f"{self.base_url}/organizations/{org_id}/nodes/{node_id}"
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-VOLTAGE-AUTH': self.api_key
        }
        
        response = requests.request("GET", url, headers=headers)
        return response.json()
        
    def create_node(self, node_data, organization_id=None):
        """
        Create a new node with the specified configuration.
        
        Args:
            node_data (dict): Configuration for the new node with keys:
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
            organization_id (str, optional): Organization ID to use, falls back to the default if not provided
            
        Returns:
            dict: JSON response containing the created node details from Voltage API
            
        Raises:
            ValueError: If no organization ID is available or required node data is missing
        """
        org_id = organization_id or self.organization_id
        if not org_id:
            raise ValueError("Organization ID is required")
        
        # Validate required fields
        required_fields = ['name', 'network', 'type']
        for field in required_fields:
            if field not in node_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        url = f"{self.base_url}/organizations/{org_id}/nodes"
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-VOLTAGE-AUTH': self.api_key
        }
        
        response = requests.request("POST", url, headers=headers, data=json.dumps(node_data))
        return response.json()