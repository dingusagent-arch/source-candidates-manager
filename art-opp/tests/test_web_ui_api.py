from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest

from app import create_app


@pytest.fixture()
def client(tmp_path: Path):
    app = create_app({"TESTING": True, "DATA_FILE": str(tmp_path / "opps.json")})
    return app.test_client()


def _upload_example_csv(client):
    csv_path = Path("src/importers/examples/opportunities.csv")
    data = {
        "file": (BytesIO(csv_path.read_bytes()), "opportunities.csv"),
    }
    return client.post("/api/import-csv", data=data, content_type="multipart/form-data")


def test_import_and_list(client):
    resp = _upload_example_csv(client)
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload["total"] > 0

    list_resp = client.get("/api/opportunities")
    assert list_resp.status_code == 200
    items = list_resp.get_json()
    assert len(items) == payload["total"]
    assert "score_total" in items[0]


def test_detail_and_triage(client):
    _upload_example_csv(client)
    items = client.get("/api/opportunities").get_json()
    item_id = items[0]["id"]

    detail = client.get(f"/api/opportunities/{item_id}")
    assert detail.status_code == 200

    triage = client.post(
        f"/api/opportunities/{item_id}/triage",
        json={"action": "approve", "note": "Good fit"},
    )
    assert triage.status_code == 200
    updated = triage.get_json()
    assert updated["status"] == "approved"
    assert updated["notes"] == "Good fit"


def test_filters(client):
    _upload_example_csv(client)

    filtered = client.get("/api/opportunities?min_score=999")
    assert filtered.status_code == 200
    assert filtered.get_json() == []

    bad = client.post("/api/opportunities/does-not-exist/triage", json={"action": "approve"})
    assert bad.status_code == 404
