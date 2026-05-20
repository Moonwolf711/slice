"""Build ClaudeBar.amxd — a thin M4L MIDI Effect device with a jweb chat UI."""
import json
import os
import struct

SLICE_ROOT = os.environ.get(
    "SLICE_ROOT",
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)
OUT = os.path.join(SLICE_ROOT, "device", "ClaudeBar.amxd")
HTML_FILE = os.path.join(SLICE_ROOT, "device", "claude-chat.html").replace("\\", "/")
CURSOR_JS = os.path.join(SLICE_ROOT, "device", "claude_cursor.js").replace("\\", "/")
HTML_URL = "file:///" + HTML_FILE

patcher = {
    "patcher": {
        "fileversion": 1,
        "appversion": {"major": 9, "minor": 0, "revision": 10, "architecture": "x64", "modernui": 1},
        "classnamespace": "box",
        "rect": [40.0, 100.0, 900.0, 500.0],
        "openrect": [0.0, 0.0, 570.0, 160.0],
        "openinpresentation": 1,
        "default_fontsize": 10.0,
        "default_fontname": "Arial",
        "gridsize": [8.0, 8.0],
        "boxanimatetime": 0,
        "devicewidth": 570.0,
        "description": "SLICE chat bar — talks to local Collab-Hub server.",
        "digest": "SLICE",
        "tags": "slice claude chat",
        "boxes": [
            {"box": {"id": "obj-1", "maxclass": "newobj", "numinlets": 1, "numoutlets": 3,
                     "outlettype": ["", "", ""], "patching_rect": [20.0, 20.0, 110.0, 22.0],
                     "text": "live.thisdevice"}},
            {"box": {"id": "obj-dbg", "maxclass": "newobj", "numinlets": 1, "numoutlets": 0,
                     "patching_rect": [150.0, 20.0, 130.0, 22.0],
                     "text": "node.debug 9229"}},
            {"box": {"id": "obj-comment", "maxclass": "comment", "numinlets": 1, "numoutlets": 0,
                     "patching_rect": [20.0, 60.0, 540.0, 22.0],
                     "text": "SLICE — jweb UI talks via socket.io to 127.0.0.1:3000/hub"}},
            {"box": {
                "id": "obj-web", "maxclass": "jweb",
                "numinlets": 1, "numoutlets": 1, "outlettype": [""],
                "patching_rect": [20.0, 100.0, 560.0, 150.0],
                "presentation": 1,
                "presentation_rect": [0.0, 0.0, 570.0, 155.0],
                "url": HTML_URL,
                "background": 1,
            }},
            {"box": {"id": "obj-cursor", "maxclass": "newobj", "numinlets": 1, "numoutlets": 0,
                     "patching_rect": [320.0, 280.0, 280.0, 22.0],
                     "text": "js " + CURSOR_JS}},
            {"box": {"id": "obj-min",  "maxclass": "newobj", "numinlets": 1, "numoutlets": 1,
                     "outlettype": [""], "patching_rect": [20.0, 280.0, 50.0, 22.0],
                     "text": "midiin"}},
            {"box": {"id": "obj-mout", "maxclass": "newobj", "numinlets": 1, "numoutlets": 0,
                     "patching_rect": [20.0, 320.0, 50.0, 22.0],
                     "text": "midiout"}},
        ],
        "lines": [
            {"patchline": {"source": ["obj-min", 0], "destination": ["obj-mout", 0]}},
            {"patchline": {"source": ["obj-web", 0], "destination": ["obj-cursor", 0]}},
        ],
    }
}


def build():
    js = json.dumps(patcher, separators=(',', ' : ')).encode('utf-8')
    out = bytearray()
    out += b'ampf' + struct.pack('<I', 4)
    out += b'mmmmmeta' + struct.pack('<I', 4)
    out += struct.pack('<I', 1)
    out += b'ptch' + struct.pack('<I', len(js))
    out += js
    with open(OUT, 'wb') as f:
        f.write(out)
    print(f"wrote {OUT} ({len(out)} bytes)")


if __name__ == "__main__":
    build()
