from flask import Blueprint, request, jsonify
from services.event_service import EventService

bp = Blueprint("budget", __name__)
event_service = EventService()

@bp.route("/update_budget", methods=["POST"])
def update_budget():
    data = request.get_json()
    event_id = data.get("event_id")
    try:
        amount = int(data.get("amount", 0))
    except ValueError:
        return jsonify({"error": "Amount must be a valid number"}), 400
    updated_event = event_service.update_budget(event_id, amount)
    if not updated_event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Budget updated", "event": updated_event})

@bp.route("/get_budget", methods=["GET"])
def get_budget():
    event_id = request.args.get("event_id")
    budget = event_service.get_budget(event_id)
    if budget is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"budget": budget})

@bp.route("/edit_budget", methods=["POST"])
def edit_budget():
    data = request.get_json()
    event_id = data.get("event_id")
    try:
        new_budget = int(data.get("new_budget", 0))
    except ValueError:
        return jsonify({"error": "New budget must be a valid number"}), 400
    updated_event = event_service.edit_budget(event_id, new_budget)
    if not updated_event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Budget updated", "event": updated_event})
