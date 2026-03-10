const THEME_KEY = 'artopp-theme';
let selectedId = null;

function applyTheme(theme) {
  document.body.classList.toggle('dark', theme === 'dark');
}

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY) || 'light';
  applyTheme(saved);

  const toggle = document.getElementById('theme_toggle');
  if (!toggle) return;
  toggle.checked = saved === 'dark';
  toggle.onchange = () => {
    const nextTheme = toggle.checked ? 'dark' : 'light';
    localStorage.setItem(THEME_KEY, nextTheme);
    applyTheme(nextTheme);
  };
}

async function loadItems() {
  const status = document.getElementById('status').value;
  const minScore = document.getElementById('min_score').value;
  const search = document.getElementById('search').value;
  const params = new URLSearchParams();
  if (status) params.set('status', status);
  if (minScore) params.set('min_score', minScore);
  if (search) params.set('search', search);

  const res = await fetch(`/api/opportunities?${params.toString()}`);
  const items = await res.json();
  const tbody = document.getElementById('items');
  tbody.innerHTML = '';

  for (const item of items) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${item.title}</td><td>${item.city}</td><td>${item.discipline}</td><td>${item.status}</td><td>${item.score_total ?? ''}</td>`;
    tr.onclick = () => showDetail(item.id);
    tbody.appendChild(tr);
  }
}

async function showDetail(id) {
  selectedId = id;
  const res = await fetch(`/api/opportunities/${id}`);
  const item = await res.json();
  document.getElementById('detail_json').textContent = JSON.stringify(item, null, 2);
}

async function triage(action) {
  if (!selectedId) return alert('Select an item first.');
  if (!confirm(`Confirm ${action}?`)) return;

  const note = document.getElementById('triage_note').value;
  const res = await fetch(`/api/opportunities/${selectedId}/triage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action, note }),
  });
  if (!res.ok) {
    const err = await res.json();
    alert(err.error || 'Triage failed');
    return;
  }
  await showDetail(selectedId);
  await loadItems();
}

async function importCsv() {
  const input = document.getElementById('csv_file');

  if (!input.files.length) {
    const sampleRes = await fetch('/api/import-sample', { method: 'POST' });
    const sampleResult = await sampleRes.json();
    document.getElementById('import_result').textContent = JSON.stringify(sampleResult);
    await loadItems();
    return;
  }

  const form = new FormData();
  form.append('file', input.files[0]);
  const res = await fetch('/api/import-csv', { method: 'POST', body: form });
  const result = await res.json();
  document.getElementById('import_result').textContent = JSON.stringify(result);
  await loadItems();
}

async function importSample() {
  const res = await fetch('/api/import-sample', { method: 'POST' });
  const result = await res.json();
  document.getElementById('import_result').textContent = JSON.stringify(result);
  await loadItems();
}

document.getElementById('refresh').onclick = loadItems;
document.getElementById('import_btn').onclick = importCsv;
document.getElementById('import_server_btn').onclick = importSample;
document.querySelectorAll('[data-action]').forEach((btn) => {
  btn.onclick = () => triage(btn.dataset.action);
});

initTheme();
loadItems();
