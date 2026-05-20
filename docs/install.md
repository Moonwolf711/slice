# Install Guide

## 1. Prereqs

- **Ableton Live 12.x Suite** (any 12.3.x build)
- **Max for Live** (built into Suite)
- **Python 3.10+**
- **Node.js + Claude Code CLI**: `npm install -g @anthropic-ai/claude-code`
- **Anthropic API key** with credits
- **AbletonOSC** Remote Script: clone https://github.com/ideoforms/AbletonOSC into your Live "MIDI Remote Scripts" folder

## 2. AbletonOSC setup

```
# Windows
C:\ProgramData\Ableton\Live 12 Suite\Resources\MIDI Remote Scripts\AbletonOSC\

# Mac
/Applications/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/AbletonOSC/
```

Make sure the `logs/` subfolder is writable by your user (not just admin).
On Windows: `icacls "...\AbletonOSC\logs" /grant Users:(OI)(CI)F /T`

In Live → Preferences → Link/MIDI → pick **AbletonOSC** for any Control Surface slot,
leave Input/Output as None. Restart Live so the script binds UDP 11000.

Verify:
```bash
python bridge/osc.py live/song/get/tempo
# {"address": "/live/song/get/tempo", "args": [124.0]}
```

## 3. Python deps

```bash
pip install anthropic "python-socketio[client]" eventlet
```

## 4. Anthropic credentials

Create `~/.env`:
```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

The bridge loads this on startup. Never commit `.env`.

## 5. Run

Terminal 1: local Collab-Hub relay
```bash
python bridge/server.py
```

Terminal 2: the bridge
```bash
python bridge/bridge.py
```

## 6. Generate agents

```bash
python agents/build.py
```

This reads your Ableton template (path is configurable in the script) and writes
one channel-specialist agent into `~/.claude/agents/` per unique track name.

## 7. Install ClaudeBar device

Copy `device/ClaudeBar.amxd` into your Ableton User Library:
```
User Library/Presets/MIDI Effects/Max MIDI Effect/ClaudeBar.amxd
```

Drag it onto any MIDI track. The chat bar appears in the device strip.
It connects to the local relay over websocket on `127.0.0.1:3000`.

## 8. Try it

Type in the bar:
- `hello` — fast Haiku chat
- `/full` — switch to Sonnet + tools
- `set tempo to 124` — should change the transport tempo
- `delegate to track-kick: program a 2-step drop pattern` — spawns the agent

## Troubleshooting

- **bar shows offline** → bridge/server not running, check ports 3000 + 11000
- **session ID in use** → bridge bug, restart `bridge.py`
- **AbletonOSC silent** → toggle Control Surface dropdown off+on, or restart Live
- **bridge prints "API err: 401"** → `.env` missing or has wrong key
- **clips not landing** → make sure `--allowed-tools` includes `mcp__ableton-mcp__*`
