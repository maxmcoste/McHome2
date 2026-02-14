"""Shared Tado client manager — one client per refresh token."""

from PyTado.interface import Tado

_clients: dict[str, Tado] = {}


def get_tado_client(refresh_token: str) -> Tado:
    """Return a connected Tado client, reusing cached instances."""
    if refresh_token not in _clients:
        client = Tado(saved_refresh_token=refresh_token)
        _clients[refresh_token] = client
    return _clients[refresh_token]
