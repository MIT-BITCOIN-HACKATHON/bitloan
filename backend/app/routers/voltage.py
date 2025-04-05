from fastapi import APIRouter, Request
from app.services.voltage import Voltage

router = APIRouter()

@router.get('https://api.voltage.cloud/organizations/:organization_id/nodes')
async def get_nodes(organization_id: str):
    
