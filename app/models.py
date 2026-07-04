# Zironlink -- public redacted build. Full source in the private repo.

from __future__ import annotations
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class TrackInfo(BaseModel):
    identifier: str
    isSeekable: bool
    author: str
    length: int
    isStream: bool
    position: int = 0
    title: str
    uri: Optional[str] = None
    artworkUrl: Optional[str] = None
    isrc: Optional[str] = None
    sourceName: str = 'youtube'

class Track(BaseModel):
    encoded: str
    info: TrackInfo
    pluginInfo: Dict[str, Any] = Field(default_factory=dict)
    userData: Dict[str, Any] = Field(default_factory=dict)

class PlaylistInfo(BaseModel):
    name: str
    selectedTrack: int = -1

class Playlist(BaseModel):
    info: PlaylistInfo
    pluginInfo: Dict[str, Any] = Field(default_factory=dict)
    tracks: List[Track]

class LoadResult(BaseModel):
    loadType: str
    data: Any = None

class VoiceState(BaseModel):
    token: str
    endpoint: str
    sessionId: str
    channelId: Optional[str] = None
    knownUserIds: Optional[List[str]] = None

class FilterConfig(BaseModel):
    volume: Optional[float] = None
    equalizer: Optional[List[Dict[str, float]]] = None
    karaoke: Optional[Dict[str, float]] = None
    timescale: Optional[Dict[str, float]] = None
    tremolo: Optional[Dict[str, float]] = None
    vibrato: Optional[Dict[str, float]] = None
    rotation: Optional[Dict[str, float]] = None
    distortion: Optional[Dict[str, float]] = None
    channelMix: Optional[Dict[str, float]] = None
    lowPass: Optional[Dict[str, float]] = None
    bassboost: Optional[float] = None
    lofi: Optional[float] = None
    slowmo: Optional[float] = None
    pluginFilters: Dict[str, Any] = Field(default_factory=dict)

class PlayerState(BaseModel):
    time: int
    position: int
    connected: bool
    ping: int

class PlayerUpdateRequest(BaseModel):
    track: Optional[Dict[str, Any]] = None
    position: Optional[int] = None
    endTime: Optional[int] = None
    volume: Optional[int] = None
    paused: Optional[bool] = None
    filters: Optional[FilterConfig] = None
    voice: Optional[VoiceState] = None
    knownUserIds: Optional[List[str]] = None

class PlayerResponse(BaseModel):
    guildId: str
    track: Optional[Track] = None
    volume: int = 100
    paused: bool = False
    state: PlayerState
    voice: Optional[VoiceState] = None
    filters: Dict[str, Any] = Field(default_factory=dict)
    queueLength: int = 0

class QueueAddRequest(BaseModel):
    encoded: Optional[str] = None
    identifier: Optional[str] = None

class QueueTrackResponse(BaseModel):
    track: Track
    position: int

class QueueListResponse(BaseModel):
    guildId: str
    length: int
    maxSize: int
    tracks: List[Track]

class SessionUpdateRequest(BaseModel):
    resuming: Optional[bool] = None
    timeout: Optional[int] = None

class ExceptionObj(BaseModel):
    message: Optional[str]
    severity: str = 'common'
    cause: str = 'unknown'
