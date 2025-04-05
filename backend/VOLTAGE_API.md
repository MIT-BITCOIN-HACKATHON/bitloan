# Voltage API Integration

This document describes the integration with Voltage Cloud API in the BitLoan application.

## Overview

The integration allows the application to fetch information about Lightning Network nodes hosted on Voltage Cloud. The implementation follows a service-oriented architecture with:

- A service layer (`app/services/voltage.py`) that handles direct API communication
- A router layer (`app/routers/voltage.py`) that exposes these services as REST endpoints

## Configuration

To use the Voltage API integration, you need to configure the following environment variables in the `.env` file:

```
VOLTAGE_API_KEY=your_voltage_api_key_here
VOLTAGE_ORG_ID=your_organization_id_here
```

You can obtain these values from your Voltage Cloud account dashboard.

## Available Endpoints

### Get All Nodes

**Endpoint**: `GET /voltage/nodes`

**Optional Query Parameters**:
- `organization_id`: Override the default organization ID from the environment variables

**Response**: JSON list of all nodes for the organization

**Example**:
```
GET /voltage/nodes
```

### Get Specific Node

**Endpoint**: `GET /voltage/nodes/{node_id}`

**Path Parameters**:
- `node_id`: The ID of the node to retrieve

**Optional Query Parameters**:
- `organization_id`: Override the default organization ID from the environment variables

**Response**: JSON object with detailed information about the specified node

**Example**:
```
GET /voltage/nodes/abc123
```

### Create New Node

**Endpoint**: `POST /voltage/nodes`

**Request Body**:
```json
{
  "name": "node-name",
  "network": "mainnet",
  "type": "standard",
  "settings": {
    "autopilot": false,
    "grpc": true,
    "rest": true,
    "keysend": true,
    "whitelist": [],
    "alias": "node-alias",
    "color": "#FF5000"
  }
}
```

**Optional Query Parameters**:
- `organization_id`: Override the default organization ID from the environment variables

**Required Request Body Fields**:
- `name`: Name of the node
- `network`: Network type (e.g., 'mainnet', 'testnet')
- `type`: Node type (e.g., 'standard')

**Optional Request Body Fields**:
- `settings`: Node configuration settings

**Response**: JSON object with details about the newly created node

**Example**:
```
POST /voltage/nodes
Content-Type: application/json

{
  "name": "my-lightning-node",
  "network": "mainnet",
  "type": "standard",
  "settings": {
    "autopilot": false,
    "grpc": true,
    "rest": true,
    "keysend": true,
    "whitelist": [],
    "alias": "My Lightning Node",
    "color": "#FF5000"
  }
}
```

## Error Handling

The API endpoints handle the following errors:

- **400 Bad Request**: When required parameters are missing (e.g., organization ID)
- **500 Internal Server Error**: When the Voltage API key is not configured or for other unexpected errors

All error responses include a descriptive message in the `detail` field.

## Implementation Details

The implementation uses a dependency injection pattern in FastAPI to provide the Voltage service to route handlers. This makes the code more testable and maintainable.

Authentication is handled automatically by including the API key in the request headers to the Voltage API.

## Future Improvements

Potential future improvements to the Voltage API integration:

1. Add caching for node information to reduce API calls
2. Implement additional Voltage API endpoints (e.g., node deletion, updates)
3. Add pagination support for large node lists
4. Implement request rate limiting to avoid hitting Voltage API limits 