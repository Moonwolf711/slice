// claude_cursor.js — moves Ableton's selection to wherever Claude is editing.
// Input: ["cursor", kind, idx, idx2]  (from jweb's max.outlet)
// kind: track | clip | scene | tempo | transport | browser

autowatch = 1;
inlets = 1;
outlets = 0;

function log(s) { post("[cursor] " + s + "\n"); }

function selectTrack(idx) {
    try {
        var t = new LiveAPI(null, "live_set tracks " + idx);
        if (!t || !t.id) { log("no track " + idx); return; }
        var view = new LiveAPI(null, "live_set view");
        view.set("selected_track", "id " + t.id);
        log("track " + idx);
    } catch (e) { log("err: " + e); }
}

function selectClip(track, slot) {
    try {
        var t = new LiveAPI(null, "live_set tracks " + track);
        var view = new LiveAPI(null, "live_set view");
        view.set("selected_track", "id " + t.id);
        if (slot >= 0) {
            var cs = new LiveAPI(null, "live_set tracks " + track + " clip_slots " + slot);
            if (cs && cs.id) view.set("highlighted_clip_slot", "id " + cs.id);
        }
        log("clip " + track + "/" + slot);
    } catch (e) { log("err: " + e); }
}

function selectScene(idx) {
    try {
        var sc = new LiveAPI(null, "live_set scenes " + idx);
        var view = new LiveAPI(null, "live_set view");
        view.set("selected_scene", "id " + sc.id);
        log("scene " + idx);
    } catch (e) { log("err: " + e); }
}

function cursor(kind, idx, idx2) {
    idx  = parseInt(idx,  10); if (isNaN(idx))  idx  = -1;
    idx2 = parseInt(idx2, 10); if (isNaN(idx2)) idx2 = -1;
    switch (String(kind)) {
        case "track":     if (idx >= 0) selectTrack(idx); break;
        case "clip":      if (idx >= 0) selectClip(idx, idx2); break;
        case "scene":     if (idx >= 0) selectScene(idx); break;
        case "tempo":     log("(tempo)"); break;
        case "transport": log("(transport)"); break;
        case "browser":   log("(browser)"); break;
        default:          log("unknown kind: " + kind);
    }
}

function anything() {
    // Accept either: "cursor kind idx idx2"  OR  raw "kind idx idx2"
    var args = arrayfromargs(messagename, arguments);
    if (args[0] === "cursor") args.shift();
    cursor(args[0], args[1], args[2]);
}

post("claude_cursor.js loaded\n");
