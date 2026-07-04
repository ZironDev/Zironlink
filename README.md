# Zironlink

A Lavalink v4-compatible audio node written in Python/FastAPI. It exposes the
same REST + WebSocket surface as [Lavalink](https://lavalink.dev), so most
existing Discord bot client libraries (`lavalink.py`, `Lavalink4NET`, `Shoukaku`,
`Mafic`, etc.) can connect to it with **zero code changes on the bot side** —
you just point them at this node's host/port/password like any other Lavalink
node.

Unlike a pure API mock, this actually joins Discord voice channels and streams
real audio: it performs the Discord voice gateway handshake, UDP IP discovery,
Opus encoding, and `xsalsa20_poly1305`-encrypted RTP packet sending itself.

## Endpoint compatibility (Lavalink v4 protocol)

| Method | Path | Status |
|---|---|---|
| GET | `/version` | ✅ |
| GET | `/v4/info` | ✅ |
| GET | `/v4/stats` | ✅ |
| WS  | `/v4/websocket` | ✅ (ready/playerUpdate/stats/event frames) |
| GET | `/v4/loadtracks?identifier=` | ✅ (YouTube/SoundCloud/HTTP via yt-dlp) |
| GET | `/v4/decodetrack` | ✅ |
| POST | `/v4/decodetracks` | ✅ |
| GET | `/v4/sessions/{id}/players` | ✅ |
| GET/PATCH/DELETE | `/v4/sessions/{id}/players/{guildId}` | ✅ (play/pause/stop/seek/volume/voice) |
| PATCH | `/v4/sessions/{id}` | ✅ (resuming/timeout stored; resume playback continuity not persisted across restarts) |
| Filters | volume | ✅ applied live (no restart). `bassboost`/`lofi`/`slowmo` (Zironlink extensions) ✅ applied via ffmpeg, brief re-seek under the hood. equalizer/timescale/karaoke/etc. | accepted & echoed back, **not yet applied to audio** (stubbed) |
| Route planner endpoints | — | not implemented (single-IP node) |
| Plugins | — | not implemented |

### `encoded` track strings
Real Lavalink uses a proprietary binary track format. This server uses its own
base64(JSON) scheme instead. This is safe because bot libraries treat the
`encoded` field as an opaque token they just pass back to you — they don't
decode it client-side. If your bot code manually decodes tracks with an
official Lavalink-format decoder, that won't work here; use this node's own
`/v4/decodetrack` instead, which understands its own format.

## Requirements

- Python 3.11+ (3.10 also works)
- `ffmpeg` on PATH
- `libopus` — see OS-specific notes below
- `libsodium` (usually a PyNaCl dependency, pulled in automatically on most platforms)

### Windows note: getting libopus working

`opuslib` needs a native `opus.dll` — Windows doesn't ship one, and pip can't
install it for you. Fix:

1. Download a prebuilt DLL — the easiest source is discord.py's bundled binaries:
   - 64-bit Python (most common): https://github.com/Rapptz/discord.py/raw/master/discord/bin/libopus-0.x64.dll
   - 32-bit Python: https://github.com/Rapptz/discord.py/raw/master/discord/bin/libopus-0.x86.dll
2. Rename the downloaded file to **`opus.dll`**.
3. Place it directly in the project root — the same folder as `run.py`.

`run.py` and `app/player.py` already add that folder to the DLL search path
automatically, so nothing else is needed. Not sure if you're 32 or 64-bit
Python? Run `py -c "import struct; print(struct.calcsize('P') * 8)"` — it
prints `64` or `32`.

Also make sure `ffmpeg.exe` is on your PATH (`ffmpeg -version` should work
in the same terminal), or set `FFMPEG_PATH` in `.env` to its full path.


## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # edit password if desired
python run.py
```

The node listens on `2333` by default, same as stock Lavalink.

Point your bot's Lavalink client config at:
```
host: localhost (or wherever you deploy this)
port: 2333
password: youshallnotpass   # from .env
secure: false               # put behind TLS-terminating proxy for wss/https in production
```

## How playback works

1. Your bot library sends Discord's normal voice-state update, gets back a
   `VOICE_SERVER_UPDATE`, and forwards `{token, endpoint, sessionId}` to this
   node via `PATCH /v4/sessions/{id}/players/{guildId}` with a `voice` object —
   exactly like it would with real Lavalink.
2. This node opens its own websocket to Discord's voice gateway, does the
   IP discovery + protocol select handshake, and receives a `secret_key`.
3. On `PATCH .../players/{guildId}` with a `track`, the node resolves a
   direct stream URL via `yt-dlp`, pipes it through `ffmpeg` to raw 48kHz
   stereo PCM, encodes 20ms frames to Opus, and sends them as
   `aead_xchacha20_poly1305_rtpsize`-encrypted RTP packets to Discord —
   pacing frames on a monotonic clock to avoid drift. (Discord discontinued
   the older `xsalsa20_poly1305` family of modes on Nov 18, 2024; this node
   uses the mode every voice gateway is required to support.)
4. `TrackStartEvent` / `TrackEndEvent` / `TrackExceptionEvent` and periodic
   `playerUpdate` frames are pushed back over `/v4/websocket`, matching the
   Lavalink protocol your client library already knows how to parse.

## Troubleshooting

**`Requested format is not available` / tracks fail to play / a "Available Clients" table appears in logs**
YouTube's default "web" player client increasingly requires a PO token to
serve playable audio formats, which yt-dlp can't obtain on its own. This
node already forces yt-dlp to try `android`/`ios` clients first, which
usually don't hit that wall. If it still fails:
```bash
pip install -U yt-dlp
```
yt-dlp ships fixes for YouTube's extraction changes frequently — an
outdated version is the most common cause of this.

**Voice connection drops after a while**
Check the server log for a line like `Voice gateway closed for guild ...
(code=... reason=...)`. Common causes: the bot left the voice channel,
Discord's voice session simply expired, or the token from a stale
`VOICE_SERVER_UPDATE` was reused. Full auto-reconnect/resume on the Discord
voice websocket isn't implemented yet — if this happens, have your bot
re-send the voice state update to re-establish it.

## Filters

Send these in the `filters` object of `PATCH /v4/sessions/{id}/players/{guildId}`,
same as any other Lavalink filter:

```json
{
  "filters": {
    "volume": 1.0,
    "bassboost": 1.0,
    "lofi": 0.5,
    "slowmo": 0.85
  }
}
```

- **volume** — standard Lavalink filter (multiplier, `1.0` = 100%). Applied
  live per-frame in Python, so it changes instantly with no glitch.
- **bassboost** *(Zironlink extension)* — `0.0` (off) to `5.0` (extreme).
  `1.0` is a reasonable "on". Adds an ffmpeg low-shelf boost around 100Hz.
- **lofi** *(Zironlink extension)* — `0.0` (off) to `1.0` (max). Lowpass +
  highpass + bitcrush + a little vibrato wobble, for a muffled/tape feel.
- **slowmo** *(Zironlink extension)* — playback rate multiplier, `1.0` =
  normal. Values below `1.0` slow down *and* drop pitch (the "slowed"
  sound), above `1.0` speeds up and raises pitch. Clamped to `0.5`-`2.0`.

`bassboost`/`lofi`/`slowmo` are baked into ffmpeg's filter graph, which
can't be hot-swapped mid-stream — changing any of them briefly restarts
the ffmpeg pipeline at the current playback position (same mechanism as a
seek). `volume` alone never triggers this. These three are additive,
non-standard fields on top of the regular Lavalink v4 `filters` object, so
bot clients that don't know about them can simply never send them.

## Connection logging

Every rejected connection attempt is logged with a reason - this used to be
silent in a few places, which made debugging painful:

- **REST requests** with a bad/missing password → `401` + a
  `[UNAUTHORIZED]` line with the IP, path, and user-agent.
- **`/v4/websocket` handshakes** with a bad password or missing `User-Id`
  header → the socket is closed (`4001`/`4002`) and a `[REJECTED]` line is
  logged with the IP, user-agent, and reason. Successful connects/resumes
  and disconnects are logged too (`[NEW]`/`[RESUMED]`/`[CLOSED]`).
- **Discord voice gateway connection attempts** (per-guild) that fail —
  DNS/TLS errors, connect timeout, or Discord closing the socket before a
  session is established — log a `connection attempt REJECTED` warning
  with the guild ID, endpoint, and the specific reason/close code (see
  `VOICE_CLOSE_CODES` in `app/voice/gateway.py`), and the failing
  `PATCH /v4/sessions/{id}/players/{guildId}` now returns a `502` with
  that reason instead of an opaque `500`.
- **UDP IP discovery** (part of the voice handshake) now times out after 5s
  instead of hanging forever if the discovery packet is dropped by a
  firewall/NAT, and logs why.

## DAVE (End-to-End Encryption)

This node speaks Discord's DAVE protocol (MLS-based E2EE) using
[`dave.py`](https://github.com/DisnakeDev/dave.py), Python bindings for
Discord's own `libdave`. It identifies with the highest DAVE version the
bindings support, does the MLS handshake (external sender, key package,
proposals/commit/welcome, epoch transitions), and encrypts outgoing Opus
frames at the media layer before the existing transport-layer
(`aead_xchacha20_poly1305_rtpsize`) encryption wraps them - both layers
apply, same as official clients.

**Status: implemented but unverified against a live voice gateway.**
`dave.py` ships with no documentation beyond its type stub, so the opcode
handling in `app/voice/gateway.py` and `app/voice/dave_session.py` is built
from the type stub, the DAVE whitepaper, and empirical testing of the
bindings in isolation - not from a working session. Known soft spots,
flagged inline with `# UNVERIFIED:`:
- The `group_id` argument to `Session.init()` isn't documented; a local
  incrementing counter is used.
- The exact byte layout of `transition_id` inside the binary OP29/OP30
  payloads is inferred, not confirmed against a capture.
- `process_proposals()`'s return value is assumed to be the ready-to-send
  OP28 "commit welcome" blob; there's no separate commit/welcome getter in
  the bindings, so this is the best-fitting reading of the API surface.
- Incoming-audio decryption (`DaveSession.decrypt`) is wired up but unused,
  since this node only sends audio and never processes received RTP.
- `recognized_user_ids` (used to validate MLS Add proposals) is only ever
  as complete as the `OP_SPEAKING` frames we've seen - there's no
  member-list source wired in yet.

If DAVE negotiation fails for a call, the node still works as before via
`OP_DAVE_PREPARE_TRANSITION`'s downgrade path (falls back to transport-only
encryption) - the bug would only show up as Discord dropping the connection
or other clients being unable to decode this bot's audio, not a crash.
Turn on debug logging (`voice.gateway` / `voice.dave` loggers) when
diagnosing.

## Multi-guild support

Like real Lavalink, a single node instance serves every guild your bot is
in at once. Players are keyed by `(session_id, guild_id)` (see
`app/state.py`), so each guild gets its own fully independent `Player`:
its own voice gateway connection, its own ffmpeg pipeline, its own filters,
and - with the queue feature below - its own queue. Playing/pausing/
skipping in one guild never touches another guild's playback, and there's
no artificial cap on how many guilds one node can drive concurrently beyond
your machine's CPU/bandwidth for however many simultaneous ffmpeg/Opus
pipelines you're running.

## Queue (Zironlink extension)

Upstream Lavalink has no server-side queue at all - queueing is entirely a
bot-side concern, normally implemented in the client library. This node
adds an optional real queue per guild on top, in the same additive spirit
as the `bassboost`/`lofi`/`slowmo` filters: existing bot clients that don't
know about it can keep managing their own queue exactly as before and never
notice this exists.

| Method | Path | Description |
|---|---|---|
| GET | `/v4/sessions/{id}/players/{guildId}/queue` | List the guild's queue |
| POST | `/v4/sessions/{id}/players/{guildId}/queue` | Add a track (`{"encoded": ...}` or `{"identifier": ...}`). Starts playing immediately if the player is idle, otherwise appends. |
| DELETE | `/v4/sessions/{id}/players/{guildId}/queue` | Clear the queue |
| DELETE | `/v4/sessions/{id}/players/{guildId}/queue/{index}` | Remove one queued track by its 0-based index |
| POST | `/v4/sessions/{id}/players/{guildId}/queue/shuffle` | Shuffle the queue order |
| POST | `/v4/sessions/{id}/players/{guildId}/queue/skip` | Stop the current track and start the next queued one |

When the current track ends naturally (not on manual `stop()`/seek/DSP
restart), the player automatically pulls the next track off this guild's
queue and starts it - matching how a bot-side queue implementation would
normally behave, just moved server-side. `GET .../players/{guildId}` and
`GET .../players` also report a non-standard `queueLength` field.

Each guild's queue is capped at `LAVALINK_QUEUE_LIMIT` tracks (env var,
default **100**) - adding past the limit returns `409 Conflict`. Set it in
`.env`:
```
LAVALINK_QUEUE_LIMIT=100
```

## Soundboard sounds (Zironlink extension)

Discord's guild soundboard sounds are just `.ogg` files on Discord's CDN.
This node can look up a guild's soundboard via Discord's own REST API
(needs `DISCORD_BOT_TOKEN` in `.env` - your bot's normal token, separate
from `LAVALINK_PASSWORD`) and resolve a sound to a normal, loadable track -
but playback always goes through the same yt-dlp-based pipeline as every
other source. There's no separate soundboard-specific audio backend; this
is purely "fetch the URL via Discord's API, then hand it to the existing
loader," which keeps queueing, filters, and events working identically
regardless of where a track came from.

| Method | Path | Description |
|---|---|---|
| GET | `/v4/soundboard/{guildId}` | List the guild's soundboard sounds (proxies Discord's API) |
| GET | `/v4/soundboard/{guildId}/{soundId}/loadtrack` | Resolve one sound to a `track` object via yt-dlp, ready to `PATCH .../players/{guildId}` or `POST .../queue` |

```
DISCORD_BOT_TOKEN=your.bots.token.here
```

## Windows: ffmpeg pipe "WinError 6" / "I/O operation on closed pipe" noise

If you saw tracebacks like:
```
ERROR | asyncio | Exception in callback _ProactorBasePipeTransport._call_connection_lost(None)
...
OSError: [WinError 6] The handle is invalid
```
```
Exception ignored in: <function _ProactorBasePipeTransport.__del__ ...>
...
ValueError: I/O operation on closed pipe
```
this is a long-standing CPython/Windows issue (bpo-39232) with
`ProactorEventLoop`'s pipe transports for subprocesses - it happens after
ffmpeg is killed and a new one is spawned right away (track skip, seek, DSP
filter change), which this node does often. Both exceptions fire *after*
the process/pipe are already gone, so there's no playback impact - just log
noise. `app/winfix.py` patches exactly those two code paths to swallow
exactly that known-benign error (applied automatically on Windows, from
`run.py`, before the event loop starts); `Player.stop()` also now properly
`wait()`s for ffmpeg to exit instead of firing `kill()` and immediately
dropping the reference, which is what triggered the race in the first
place.



- Single-node only — no clustering/route-planner/IP rotation.
- DSP filters beyond volume/bassboost/lofi/slowmo (equalizer, timescale,
  karaoke, tremolo, etc.) are accepted in the API but not yet applied to
  the audio pipeline.
- No plugin system.
- In-memory session/player state — restarting the process drops all players
  (resume semantics are accepted at the API level but playback isn't
  reconstructed from a saved state).
- SoundCloud/HTTP source support depends entirely on yt-dlp's extractors.

## Project layout

```
app/
  main.py          FastAPI app, auth middleware, stats broadcast loop
  config.py        env-driven settings
  models.py        Pydantic schemas matching the Lavalink v4 REST contract
  track_codec.py   encode/decode for the `encoded` track string
  track_loader.py  yt-dlp based search/resolve
  queue.py         per-guild playback queue (Zironlink extension)
  soundboard.py    Discord soundboard lookup -> yt-dlp identifier (Zironlink extension)
  winfix.py        Windows-only asyncio Proactor pipe-close error suppression
  player.py        per-guild playback state machine (ffmpeg -> Opus -> RTP)
  ws_manager.py     /v4/websocket client session registry + event emission
  state.py         session/player registry
  voice/
    gateway.py     Discord voice websocket (identify/select-protocol/session-description)
    udp.py         UDP IP discovery + encrypted RTP framing
  routers/
    info.py        /version, /v4/info, /v4/stats
    loadtracks.py  /v4/loadtracks
    decodetrack.py /v4/decodetrack(s)
    sessions.py    /v4/sessions/{id}
    players.py     /v4/sessions/{id}/players[/{guildId}] + queue endpoints
    soundboard.py  /v4/soundboard/{guildId}[/{soundId}/loadtrack]
    websocket.py   /v4/websocket
```
