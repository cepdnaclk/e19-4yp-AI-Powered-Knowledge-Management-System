from flask import Blueprint, request, jsonify
from services.profile_service import create_or_update, get as get_profile

bp = Blueprint("profiles", __name__, url_prefix="/api/profile")


@bp.route("/<user_id>", methods=["GET"])
def fetch_profile(user_id):
    prof = get_profile(user_id)
    if not prof:
        return jsonify({"success": False, "message": "Profile not found"}), 404
    return jsonify({"success": True, "profile": prof.as_dict()}), 200


@bp.route("", methods=["POST"])
def upsert_profile():
    data = request.get_json(force=True)
    try:
        user_id = data["user_id"]
        role = data["role"]
        interests = data.get("interests", [])
    except KeyError as missing:
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Missing field {missing.args[0]} in body",
                }
            ),
            400,
        )

    prof = create_or_update(user_id, role, interests)
    return jsonify({"success": True, "profile": prof.as_dict()}), 200
