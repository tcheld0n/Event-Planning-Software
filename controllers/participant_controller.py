from flask import Blueprint, request, jsonify
from services.participant_service import ParticipantService

bp = Blueprint("participant", __name__)
participant_service = ParticipantService()

@bp.route("/register_participant", methods=["POST"])
def register_participant():
    data = request.get_json()
    event_id = data.get("event_id")
    name = data.get("name")
    if not event_id or not name:
        return jsonify({"error": "Missing event_id or name"}), 400
    # Usa o método 'create'
    participant = participant_service.create(event_id, name)
    if not participant:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Participant registered", "participant": participant})

@bp.route("/attendees", methods=["GET"])
def get_attendees():
    event_id = request.args.get("event_id")
    attendees = participant_service.get_attendees(event_id)
    if attendees is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"participants": attendees})

@bp.route("/edit_participant", methods=["POST"])
def edit_participant():
    data = request.get_json()
    participant_id = data.get("participant_id")
    new_name = data.get("new_name")
    if not participant_id or not new_name:
        return jsonify({"error": "Missing participant_id or new_name"}), 400
    # Usa o método 'update'
    participant = participant_service.update(participant_id, new_name)
    if not participant:
        return jsonify({"error": "Participant not found"}), 404
    return jsonify({"message": "Participant updated", "participant": participant})
