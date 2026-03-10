from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from .backend import OpportunityStore


def _build_store(app: Flask) -> OpportunityStore:
    return OpportunityStore(Path(app.root_path).parent / app.config["DATA_FILE"])


def _sample_csv_path(app: Flask) -> Path:
    return Path(app.root_path).parent / "src" / "importers" / "examples" / "opportunities.csv"


def init_app(app: Flask) -> None:
    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/opportunities")
    def list_opportunities():
        store = _build_store(app)
        status = request.args.get("status")
        min_score = request.args.get("min_score", type=float)
        search = request.args.get("search")
        items = store.list_items(status=status, min_score=min_score, search=search)
        return jsonify(items)

    @app.get("/api/opportunities/<item_id>")
    def get_opportunity(item_id: str):
        store = _build_store(app)
        item = store.get_item(item_id)
        if not item:
            return jsonify({"error": "not found"}), 404
        return jsonify(item)

    @app.post("/api/opportunities/<item_id>/triage")
    def triage(item_id: str):
        payload = request.get_json(silent=True) or {}
        action = payload.get("action", "")
        note = payload.get("note", "")
        store = _build_store(app)
        try:
            item = store.triage(item_id, action, note)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        if not item:
            return jsonify({"error": "not found"}), 404
        return jsonify(item)

    @app.post("/api/import-csv")
    def import_csv():
        file = request.files.get("file")
        store = _build_store(app)

        if not file:
            summary = store.import_csv(_sample_csv_path(app))
            return jsonify(summary)

        upload_dir = Path(app.root_path).parent / "data" / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        target = upload_dir / file.filename
        file.save(target)

        summary = store.import_csv(target)
        return jsonify(summary)

    @app.post("/api/import-sample")
    def import_sample():
        store = _build_store(app)
        summary = store.import_csv(_sample_csv_path(app))
        return jsonify(summary)

    @app.get("/api/settings")
    def settings_placeholder():
        store = _build_store(app)
        items = store.list_items()
        latest_update = max([i.get("updated_at", "") for i in items], default="")
        return jsonify(
            {
                "cron_status": "not-configured",
                "last_import_time": latest_update,
                "test_command": "pytest -q",
                "cwd": os.getcwd(),
            }
        )
