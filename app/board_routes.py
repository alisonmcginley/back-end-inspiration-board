from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"], strict_slashes=False)
def create_board():
    request_body = request.get_json()

    if "title" not in request_body.keys() and
    "owner" not in request_body.keys():
        return {},400

    new_board = Board(title = request_body["title"], owner = request_body["owner"])
    db.session.add(new_board)
    db.session.commit()

    return {
        "title": new_board.to_json(),
        "owner": new_board.to_json()
    }, 201

