from flask import Blueprint, request, jsonify
from services.event_service import EventService
from datetime import datetime

bp = Blueprint("event", __name__)
event_service = EventService()

@bp.route("/events", methods=["GET"])
def list_events():
    events = event_service.list_events()
    return jsonify(events)

@bp.route("/create_event", methods=["POST"])
def create_event():
    data = request.get_json()
    name = data.get("name")
    date_str = data.get("date")
    budget = data.get("budget", 0)

    if not name or not date_str:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        date = datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        return jsonify({"error": "Date must be in DD-MM-YYYY format"}), 400

    try:
        budget = int(budget)
    except ValueError:
        return jsonify({"error": "Budget must be a valid number"}), 400

    event = event_service.create(name, date, budget)
    return jsonify(event), 201

@bp.route("/edit_event", methods=["POST"])
def edit_event():
    data = request.get_json()
    event_id = data.get("event_id")
    if not event_id:
        return jsonify({"error": "Missing event_id"}), 400
    # Remove o event_id do dicionário para evitar duplicidade
    data.pop("event_id", None)
    event = event_service.update(event_id, **data)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event)

@bp.route("/delete_event", methods=["POST"])
def delete_event():
    data = request.get_json()
    event_id = data.get("event_id")
    if event_service.delete(event_id):
        return jsonify({"message": "Event deleted", "id": event_id})
    return jsonify({"error": "Event not found"}), 404
