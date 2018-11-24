import os

import postgresql
from uuid import UUID
from flask import Flask, jsonify
from flask import abort
from flask import request

SELECT_PARTY_BY_ID = """SELECT party FROM santa WHERE uuid = $1"""
SELECT_PARTY = """SELECT santa.uuid, santa.name, santa.party, candidate.real_name
        FROM santa as santa
        LEFT OUTER JOIN santa as candidate on (santa.party = candidate.name)
        WHERE santa.name = $1"""
SELECT_CANDIDATE = """SELECT name, real_name FROM santa WHERE has_party ISNULL AND name != $1
        ORDER BY uuid LIMIT 1"""
UPDATE_PARTY = """UPDATE santa SET party = $1 WHERE name = $2"""
UPDATE_CANDIDATE = """UPDATE santa SET has_party = true WHERE name = $1"""

app = Flask(__name__)
db_url = os.environ.get("DB_URL")
db = postgresql.open(str(db_url))


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


def get_party_by_id(uuid):
    cur_party = db.prepare("SELECT party FROM santa WHERE uuid = $1")
    return cur_party(uuid)


@app.route("/", methods=['POST'])
def postparty():

    # Logs
    print('Request:', request.json)

    assert request.json, abort(400)
    assert 'name' in request.json, abort(400)

    party = get_party(request.json['name'])

    # Logs
    print('Party:', party)

    assert len(party), abort(404)

    if party[0]['party']:
        resp = jsonify({'party': party[0]['real_name'],
                        "your_uuid": party[0]['uuid']})
    else:
        candidate = get_candidate_for_santa(request.json['name'])

        assert len(candidate), abort(404)

        try:
            assign_candidate(candidate[0]['name'], request.json['name'])
        except Exception as e:
            print(e)
            abort(400)
        resp = jsonify({'party': candidate[0]['real_name'],
                        "your_uuid": party[0]['uuid']})
    return resp


@app.route("/<uuid>", methods=['GET'])
def getparty(uuid):
    assert uuid, abort(400)

    try:
        UUID(uuid, version=4)
    except ValueError:
        abort(400)

    party = get_party_by_id(uuid)
    assert len(party), abort(404)

    return jsonify({'your_party': party[0]['party']})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
