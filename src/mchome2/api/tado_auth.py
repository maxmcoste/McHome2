"""Tado OAuth device-code flow and zone listing endpoints."""

import asyncio

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PyTado.interface import Tado

from mchome2.config import settings, save_settings
from mchome2.hardware.tado.client import get_tado_client

router = APIRouter(prefix="/api/tado", tags=["tado"])

# Pending Tado instance during auth flow (in-memory, single-user)
_pending_tado: Tado | None = None


class AuthStartResponse(BaseModel):
    url: str
    user_code: str | None = None


class AuthCompleteResponse(BaseModel):
    success: bool


class ZoneInfo(BaseModel):
    id: int
    name: str
    type: str


@router.post("/auth/start", response_model=AuthStartResponse)
async def start_auth():
    """Start Tado device-code OAuth flow."""
    global _pending_tado
    _pending_tado = await asyncio.to_thread(Tado)
    url = _pending_tado.device_verification_url()
    if not url:
        raise HTTPException(status_code=500, detail="Failed to start Tado device flow")
    return AuthStartResponse(url=url)


@router.post("/auth/complete", response_model=AuthCompleteResponse)
async def complete_auth():
    """Complete Tado device-code OAuth flow after user authorizes in browser."""
    global _pending_tado
    if _pending_tado is None:
        raise HTTPException(status_code=400, detail="No pending auth flow. Call /auth/start first.")

    try:
        await asyncio.to_thread(_pending_tado.device_activation)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Activation failed: {exc}")

    token = _pending_tado.get_refresh_token()
    if not token:
        raise HTTPException(status_code=500, detail="No refresh token received")

    # Persist to settings
    settings.tado_refresh_token = token
    save_settings({"tado_refresh_token": token})

    _pending_tado = None
    return AuthCompleteResponse(success=True)


@router.get("/zones", response_model=list[ZoneInfo])
async def list_zones():
    """List Tado zones using the stored refresh token."""
    if not settings.tado_refresh_token:
        raise HTTPException(status_code=400, detail="Tado not connected. Complete setup first.")

    try:
        client = get_tado_client(settings.tado_refresh_token)
        zones = await asyncio.to_thread(client.getZones)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to fetch zones: {exc}")

    return [
        ZoneInfo(id=z["id"], name=z["name"], type=z.get("type", "UNKNOWN"))
        for z in zones
    ]
