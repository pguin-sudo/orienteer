from flask import jsonify

from core.data.sponsor_data import SponsorData


def sponsor_info(user_id):
    if not user_id or user_id == "00000000-0000-0000-0000-000000000000":
        return "", 404
    elif SponsorData().get_info(user_id) is not None:
        return jsonify(SponsorData().get_info(user_id))
    else:
        return "", 404
