import os

import postgresql
from flask import Flask, jsonify
from flask import abort
from flask import request

SELECT_PARTY = """SELECT name, party FROM santa WHERE name = $1"""
SELECT_CANDIDATE = """SELECT name FROM santa WHERE has_party ISNULL AND name != $1 ORDER BY uuid LIMIT 1"""
UPDATE_PARTY = """UPDATE santa SET party = $1 WHERE name = $2"""
UPDATE_CANDIDATE = """UPDATE santa SET has_party = true WHERE name = $1"""

app = Flask(__name__)
db = postgresql.open('pq://dmwonkomseluvu:056095e637408a79a7afd2a510829bb8071a69a237c9aa48d4e7af7831980c17@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/d5frennvu4ie97')


def get_party(user):
    cur_party = db.prepare(SELECT_PARTY)
    return cur_party(user)


def get_candidate_for_santa(user):
    cur_candidate = db.prepare(SELECT_CANDIDATE)
    return cur_candidate(user)


def assign_candidate(candidate, user):
    cur_party = db.prepare(UPDATE_PARTY)
    cur_party(candidate, user)
    cur_candidate = db.prepare(UPDATE_CANDIDATE)
    cur_candidate(candidate)
    return None


@app.route("/", methods=['POST'])
def name():
    assert request.json, abort(400)
    assert 'name' in request.json, abort(400)

    party = get_party(request.json['name'])

    assert len(party), abort(404)

    if party[0]['party']:
        resp = jsonify({'buddy': party[0]['party']})
    else:
        candidate = get_candidate_for_santa(request.json['name'])

        assert len(candidate), abort(404)

        try:
            assign_candidate(candidate[0]['name'], request.json['name'])
        except Exception as e:
            print(e)
            abort(400)
        resp = jsonify({'buddy': candidate[0]['name']})
    return resp


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
