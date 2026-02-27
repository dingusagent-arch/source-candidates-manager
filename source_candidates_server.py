#!/usr/bin/env python3
import datetime as dt
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")
CANDIDATES_PATH = os.path.join(DATA_DIR, "art_sources_candidates.json")
HOST = "127.0.0.1"
PORT = 8011


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def ensure_store() -> dict:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CANDIDATES_PATH):
        payload = {
            "notes": "Brave-discovered source queue. status: proposed|approved|rejected|paused",
            "candidates": [],
        }
        with open(CANDIDATES_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return payload

    with open(CANDIDATES_PATH, "r", encoding="utf-8") as f:
        try:
            payload = json.load(f)
        except Exception:
            payload = {"notes": "auto-recovered", "candidates": []}
    if not isinstance(payload, dict):
        payload = {"notes": "auto-recovered", "candidates": []}
    payload.setdefault("candidates", [])
    return payload


def save_store(payload: dict) -> None:
    with open(CANDIDATES_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def normalize_url(url: str) -> str:
    text = (url or "").strip()
    if not text.startswith(("http://", "https://")):
        raise ValueError("url must start with http:// or https://")
    return text


HTML = """<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Source Candidates Manager</title>
<style>
  :root {
    --bg: #0f1115;
    --card: #171a21;
    --text: #e8ecf1;
    --muted: #9aa5b1;
    --border: #2a3240;
    --btn: #222a38;
    --btn-text: #e8ecf1;
    --link: #80b8ff;
  }
  body.light {
    --bg: #f7f9fc;
    --card: #ffffff;
    --text: #1c2430;
    --muted: #5f6b7a;
    --border: #d8e0ea;
    --btn: #eef3fa;
    --btn-text: #1c2430;
    --link: #0a58ca;
  }
  body {
    font-family: Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    max-width: 1000px;
    margin: 0 auto;
    padding: 1rem;
  }
  .card { border: 1px solid var(--border); border-radius: 8px; padding: .75rem; margin: .5rem 0; background: var(--card); }
  .row { display: grid; grid-template-columns: 1fr 1fr; gap: .5rem; }
  .muted { color: var(--muted); font-size: .9em; }
  button { margin-right: .4rem; background: var(--btn); color: var(--btn-text); border: 1px solid var(--border); border-radius: 6px; padding: .35rem .6rem; cursor: pointer; }
  input, select { background: var(--card); color: var(--text); border: 1px solid var(--border); border-radius: 6px; padding: .35rem; width: 100%; box-sizing: border-box; }
  a { color: var(--link); }
  .topbar { display: flex; justify-content: space-between; align-items: center; }
</style>
</head>
<body>
<div class='topbar'>
  <h1>Source Candidates Manager</h1>
  <button id='themeBtn' type='button'>☀️ Light</button>
</div>
<p class='muted'>Standalone tool (outside art-catalog project). Approved sources are picked up by scout cron.</p>

<div class='card'>
  <h3>Add Candidate</h3>
  <form id='f'>
    <div class='row'>
      <label>URL <input id='url' required placeholder='https://example.org/events'></label>
      <label>Name <input id='name' placeholder='Example Arts'></label>
      <label>Type <input id='type' value='unknown'></label>
      <label>Coverage <input id='coverage' value='unknown'></label>
      <label>Source <input id='source' value='brave'></label>
      <label>Notes <input id='notes'></label>
    </div>
    <p><button type='submit'>Add</button> <span id='msg' class='muted'></span></p>
  </form>
</div>

<label>Filter
  <select id='filter'>
    <option value=''>All</option>
    <option>proposed</option>
    <option>approved</option>
    <option>rejected</option>
    <option>paused</option>
  </select>
</label>
<div id='list'></div>

<script>
const THEME_KEY='source_mgr_theme';
function applyTheme(theme){
  document.body.classList.toggle('light', theme==='light');
  localStorage.setItem(THEME_KEY, theme);
  const btn=document.getElementById('themeBtn');
  btn.textContent = theme==='light' ? '🌙 Dark' : '☀️ Light';
}
(function initTheme(){
  const saved=localStorage.getItem(THEME_KEY);
  applyTheme(saved||'dark');
})();
document.getElementById('themeBtn').onclick=()=>{
  const isLight=document.body.classList.contains('light');
  applyTheme(isLight?'dark':'light');
};

async function req(path, opts={}){
  const r=await fetch(path,{headers:{'Content-Type':'application/json'},...opts});
  const t=await r.text();
  let d={};
  try{d=JSON.parse(t)}catch{}
  if(!r.ok) throw new Error(d.detail||t||r.statusText);
  return d;
}
function esc(s){return String(s||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}

async function load(){
  const st=document.getElementById('filter').value;
  const d=await req('/api/candidates'+(st?('?status='+encodeURIComponent(st)):''));
  const list=document.getElementById('list');
  list.innerHTML='';
  if(!d.items.length){list.innerHTML='<p class=muted>No candidates.</p>';return;}
  for(const i of d.items){
    const el=document.createElement('div');
    el.className='card';
    el.innerHTML=`<div><strong>${esc(i.name||i.url)}</strong></div><div><a href='${esc(i.url)}' target='_blank'>${esc(i.url)}</a></div><div class='muted'>type=${esc(i.type)} | coverage=${esc(i.coverage)} | source=${esc(i.source)}</div><div class='muted'>status=<b>${esc(i.status)}</b> | updated=${esc(i.updated_at||'')}</div><div class='muted'>notes=${esc(i.notes||'')}</div>`;
    const p=document.createElement('p');
    for(const s of ['proposed','approved','rejected','paused']){
      const b=document.createElement('button');
      b.textContent=s;
      b.disabled=i.status===s;
      b.onclick=async()=>{await req('/api/candidates/status',{method:'PATCH',body:JSON.stringify({url:i.url,status:s})});await load();};
      p.appendChild(b);
    }
    el.appendChild(p);
    list.appendChild(el);
  }
}

document.getElementById('f').onsubmit=async(e)=>{
  e.preventDefault();
  const payload={url:url.value.trim(),name:name.value.trim(),type:type.value.trim(),coverage:coverage.value.trim(),source:source.value.trim(),notes:notes.value.trim()};
  try{
    await req('/api/candidates',{method:'POST',body:JSON.stringify(payload)});
    msg.textContent='Added';
    e.target.reset();
    type.value='unknown'; coverage.value='unknown'; source.value='brave';
    await load();
  }catch(err){ msg.textContent=err.message; }
};
filter.onchange=()=>load();
load();
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, data, content_type="application/json"):
        body = data.encode("utf-8") if isinstance(data, str) else json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            return self._send(200, HTML, "text/html; charset=utf-8")
        if u.path == "/api/candidates":
            payload = ensure_store()
            items = payload.get("candidates", [])
            q = parse_qs(u.query)
            status = (q.get("status", [""])[0] or "").strip().lower()
            if status:
                items = [i for i in items if str(i.get("status", "")).lower() == status]
            return self._send(200, {"count": len(items), "items": items})
        return self._send(404, {"detail": "not found"})

    def do_POST(self):
        if self.path != "/api/candidates":
            return self._send(404, {"detail": "not found"})
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8"))
            url = normalize_url(data.get("url", ""))
        except Exception as e:
            return self._send(422, {"detail": str(e)})

        payload = ensure_store()
        for i in payload.get("candidates", []):
            if i.get("url") == url:
                return self._send(409, {"detail": "Candidate URL already exists"})

        item = {
            "name": (data.get("name") or urlparse(url).netloc.replace("www.", "") or "Unnamed Source").strip(),
            "url": url,
            "type": (data.get("type") or "unknown").strip() or "unknown",
            "coverage": (data.get("coverage") or "unknown").strip() or "unknown",
            "status": "proposed",
            "source": (data.get("source") or "manual").strip() or "manual",
            "notes": (data.get("notes") or "").strip(),
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        payload.setdefault("candidates", []).append(item)
        save_store(payload)
        return self._send(HTTPStatus.CREATED, {"ok": True, "item": item})

    def do_PATCH(self):
        if self.path != "/api/candidates/status":
            return self._send(404, {"detail": "not found"})
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8"))
            url = normalize_url(data.get("url", ""))
            status = (data.get("status") or "").strip().lower()
            if status not in {"proposed", "approved", "rejected", "paused"}:
                raise ValueError("invalid status")
        except Exception as e:
            return self._send(422, {"detail": str(e)})

        payload = ensure_store()
        for item in payload.get("candidates", []):
            if item.get("url") == url:
                item["status"] = status
                item["updated_at"] = now_iso()
                if "notes" in data and data["notes"] is not None:
                    item["notes"] = str(data["notes"])
                save_store(payload)
                return self._send(200, {"ok": True, "item": item})
        return self._send(404, {"detail": "candidate not found"})


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Source manager running at http://{HOST}:{PORT}")
    server.serve_forever()
