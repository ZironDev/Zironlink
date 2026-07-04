# Zironlink

A Lavalink v4-compatible audio node, built from scratch in Python — with
Discord end-to-end voice encryption (DAVE), server-side queueing, and custom
DSP filters that stock Lavalink doesn't have.

It speaks the same REST + WebSocket API as [Lavalink](https://lavalink.dev),
so existing Discord bot libraries (`lavalink.py`, `Lavalink4NET`, `Shoukaku`,
`Mafic`, etc.) can point at it like any other Lavalink node — **no changes
needed on the bot side.**

Unlike a mock/API shim, this actually joins Discord voice channels and streams
real audio: it does the Discord voice gateway handshake, UDP IP discovery,
Opus encoding, and encrypted RTP packet sending itself.

> ### ⚠️ This is a public, redacted build
> This repo shows the project's architecture, API surface, and scope of
> work — it is **not the full source** and won't run as-is. Core
> implementation logic (the voice gateway / DAVE encryption handling, the
> ffmpeg → Opus → RTP playback pipeline, DSP filter construction, queueing,
> track resolution, and related routers) has been stripped from the affected
> files. Signatures, docstrings, and structure are kept so the design is
> visible; function bodies are replaced with a redaction marker.
>
> Want to actually run Zironlink? Grab the **prebuilt Windows release**
> below — no source, no setup, no Python required.

## 📦 Download (Windows)

A prebuilt `.exe` release is available under
[**Releases**](../../releases) — no Python, `ffmpeg`, or `opus.dll` wrangling
required, everything's bundled.

1. Grab the latest `Zironlink-x.x.x-win64.exe` from the Releases page.
2. Run it. It listens on `2333` by default, same as stock Lavalink.
3. Point your bot's Lavalink client config at:
   ```
   host: localhost (or wherever you're running it)
   port: 2333
   password: youshallnotpass   (or whatever you set in the config)
   secure: false               (put behind TLS-terminating proxy for wss/https in production)
   ```

Building from this source instead? See [Setup](#setup-from-source) below —
but keep in mind this public copy is redacted and won't actually play audio.

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
| Filters | volume ✅ live, no restart. `bassboost`/`lofi`/`slowmo` (Zironlink extensions) ✅ via ffmpeg. equalizer/timescale/karaoke/etc. accepted & echoed, not yet applied to audio |
| Route planner endpoints | — | not implemented (single-IP node) |
| Plugins | — | not implemented |

## Highlights

- **DAVE (End-to-End Encryption)** — speaks Discord's MLS-based DAVE
  protocol: identifies with the highest supported DAVE version, performs the
  MLS handshake (external sender, key package, proposals/commit/welcome,
  epoch transitions), and encrypts outgoing Opus frames at the media layer
  before transport-layer (`aead_xchacha20_poly1305_rtpsize`) encryption wraps
  them — same as official clients. Falls back cleanly to transport-only
  encryption if DAVE negotiation fails.
- **Server-side queue** *(Zironlink extension)* — real per-guild queueing on
  top of the protocol, entirely optional and additive. Add/list/clear/shuffle/
  skip endpoints, auto-advance on track end, configurable per-guild size cap.
- **DSP filters** *(Zironlink extension)* — `bassboost`, `lofi`, and `slowmo`,
  layered on top of the standard Lavalink `filters` object. Bot clients that
  don't know about them simply never send them.
- **Soundboard support** *(Zironlink extension)* — resolve a guild's Discord
  soundboard sounds into normal loadable tracks, playable through the same
  pipeline as everything else.
- **Multi-guild by design** — one node instance serves every guild your bot
  is in, each with its own fully isolated voice connection, ffmpeg pipeline,
  filters, and queue.

## Filters

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

- **volume** — standard Lavalink filter (`1.0` = 100%), applied live per-frame.
- **bassboost** — `0.0`–`5.0`. Low-shelf boost around 100Hz.
- **lofi** — `0.0`–`1.0`. Lowpass + highpass + bitcrush + wobble, for a
  muffled/tape feel.
- **slowmo** — playback rate multiplier, `0.5`–`2.0`. Below `1.0` slows down
  and drops pitch (the "slowed" sound), above speeds up and raises pitch.

## Queue

| Method | Path | Description |
|---|---|---|
| GET | `/v4/sessions/{id}/players/{guildId}/queue` | List the guild's queue |
| POST | `/v4/sessions/{id}/players/{guildId}/queue` | Add a track |
| DELETE | `/v4/sessions/{id}/players/{guildId}/queue` | Clear the queue |
| DELETE | `/v4/sessions/{id}/players/{guildId}/queue/{index}` | Remove one queued track |
| POST | `/v4/sessions/{id}/players/{guildId}/queue/shuffle` | Shuffle the queue |
| POST | `/v4/sessions/{id}/players/{guildId}/queue/skip` | Skip to the next queued track |

## Soundboard

| Method | Path | Description |
|---|---|---|
| GET | `/v4/soundboard/{guildId}` | List the guild's soundboard sounds |
| GET | `/v4/soundboard/{guildId}/{soundId}/loadtrack` | Resolve a sound to a loadable track |

## Setup (from source)

> Reminder: this public source is redacted and will not actually play audio
> end-to-end. This is here to show setup shape / for anyone building
> against it as a reference — for a working node, use the Windows release
> above.

**Requirements:** Python 3.11+ (3.10 works too), `ffmpeg` on PATH, `libopus`,
`libsodium` (usually pulled in via PyNaCl automatically).

```bash
pip install -r requirements.txt
cp .env.example .env   # edit password if desired
python run.py
```

### Windows: libopus

`opuslib` needs a native `opus.dll`, which Windows doesn't ship and pip can't
install. Drop a prebuilt `opus.dll` (e.g. from discord.py's bundled binaries)
into the project root, next to `run.py` — it's picked up automatically.

## Known limitations

- Single-node only — no clustering/route-planner/IP rotation.
- DSP filters beyond volume/bassboost/lofi/slowmo aren't applied to audio yet.
- No plugin system.
- In-memory session/player state — restarting drops all players.
- Source/format support depends entirely on yt-dlp's extractors.
- DAVE support is implemented against the protocol spec + bindings, not yet
  verified end-to-end against a live session in every edge case.

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
  ws_manager.py    /v4/websocket client session registry + event emission
  state.py         session/player registry
  voice/
    gateway.py     Discord voice websocket (identify/select-protocol/session-description)
    dave_session.py  DAVE (MLS E2EE) session handling
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

## License / contact

This project is shared for portfolio/demo purposes. If you're interested in
the full implementation, licensing, or contributing, reach out to the author
directly rather than opening a PR against redacted code.
