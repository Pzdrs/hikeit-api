import os
from datetime import datetime
from enum import Enum

from flask import Flask, request, jsonify

app = Flask(__name__)


class Goal:
    class Type(Enum):
        STEPS = 'steps'
        DISTANCE = 'distance'

    def __init__(self, goal_id: int, label: str, deadline: datetime, goal_type: Type, value: float):
        self.id = goal_id
        self.label = label
        self.deadline = deadline
        self.type = goal_type
        self.value = value

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'deadline': self.deadline,
            'type': self.type.value,
            'value': self.value,
        }


goals: list[Goal] = []

AUTH_TOKEN = os.getenv("AUTH_TOKEN")


def token_required(f):
    def middleware(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        # Check if the Authorization header is present and contains a bearer token
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header with Bearer token is required"}), 401

        # Extract the token (everything after 'Bearer ')
        token = auth_header.split(" ")[1]

        # Example token check (replace this with your own validation)
        if token != AUTH_TOKEN:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    middleware.__name__ = f.__name__
    return middleware


@app.route('/')
def hello_world():  # put application's code here
    return 'This is the backend API for the HikeIt native android application (https://github.com/Pzdrs/hikeithttps://github.com/Pzdrs/hikeit).'


@app.route('/api/v1/goals')
def all_goals():
    return [goal.to_dict() for goal in goals]


@app.route('/api/v1/goals', methods=['POST'])
@token_required
def create_goal():
    req = request.json

    try:
        goal = Goal(
            len(goals),
            req['label'],
            datetime.fromtimestamp(req['deadline']),
            Goal.Type(req['type']),
            req['value']
        )
        goals.append(goal)
        return goal.to_dict(), 201
    except KeyError:
        return {'error': 'Invalid request'}, 400


@app.route('/api/v1/goals/<int:goal_id>/finish', methods=['POST'])
@token_required
def finish_goal(goal_id):
    for goal in goals:
        if goal.id == goal_id:
            goals.remove(goal)
            return goal.to_dict()
    return {'error': 'Goal not found'}, 404


if __name__ == '__main__':
    app.run()
