from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"], strict_slashes=False)
def create_board():
    request_body = request.get_json()

    if "title" not in request_body.keys() or "owner" not in request_body.keys():
        return {"details": "Invalid data"},400

    new_board = Board(title = request_body["title"], owner = request_body["owner"])
    db.session.add(new_board)
    db.session.commit()

    return {
        "title": new_board.to_json(),
        "owner": new_board.to_json()
    }, 201

@boards_bp.route("", methods=["GET"], strict_slashes=False)
def get_board():
    title_from_url = request.args.get("title")

    if title_from_url:
        boards = Board.query.filter_by(title = title_from_url)

    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append(board.to_json())

    return jsonify(boards_response), 200   

@boards_bp.route("<board_id>/cards", methods=["GET"], strict_slashes=False)
def get_cards(board_id):

    board =Board.query.get_or_404(board_id)

    cards = []
    for card in board.cards:
        cards.append(card.to_json())

    return board.to_json_with_cards(cards), 200



