# Zironlink -- public redacted build. Full source in the private repo.

import asyncio
import logging
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import settings
from app.logging_setup import setup_logging, print_banner, client_ip, log_http_unauthorized, log_http_request
from app.routers import info, loadtracks, decodetrack, sessions, players, websocket, soundboard
from app.state import players as player_registry
from app.ws_manager import ws_manager
setup_logging(level=logging.DEBUG if settings.DEBUG else logging.INFO)
log = logging.getLogger('main')
app = FastAPI(title='Zironlink', version=settings.LAVALINK_SEMVER)
OPEN_PATHS = {'/version', '/docs', '/openapi.json', '/redoc'}

@app.middleware('http')
async def access_log_middleware(request: Request, call_next):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@app.middleware('http')
async def auth_middleware(request: Request, call_next):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')

@app.middleware('http')
async def add_version_header(request: Request, call_next):
    """[core implementation redacted for the public release -- see private repo]"""
    raise NotImplementedError('core implementation redacted for the public release -- see private repo')
app.include_router(info.router)
app.include_router(loadtracks.router)
app.include_router(decodetrack.router)
app.include_router(sessions.router)
app.include_router(players.router)
app.include_router(soundboard.router)
app.include_router(websocket.router)

@app.on_event('startup')
async def startup_event():
    """[core implementation redacted for the public release -- see private repo]"""

async def _stats_broadcast_loop():
    """[core implementation redacted for the public release -- see private repo]"""
