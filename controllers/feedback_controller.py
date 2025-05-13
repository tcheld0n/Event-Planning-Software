from flask import Blueprint, request, jsonify
from services.feedback_service import FeedbackService

bp = Blueprint("feedback", __name__)
feedback_service = FeedbackService()

@bp.route("/add_feedback", methods=["POST"])
def add_feedback():
    data = request.get_json()
    event_id = data.get("event_id")
    content = data.get("feedback")
    if not event_id or not content:
        return jsonify({"error": "Missing event_id or feedback"}), 400
    # Agora usamos 'create' para feedback
    feedback = feedback_service.create(event_id, content)
    if not feedback:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Feedback added", "feedback": feedback})
