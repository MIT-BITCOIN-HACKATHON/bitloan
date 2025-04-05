from fastapi import APIRouter, Request
from app.services.node import Node

router = APIRouter()

@router.get("/nodes")
async def get_nodes(request: Request):
