import os

import postgresql
from flask import Flask, jsonify
from flask import abort
from flask import request

app = Flask(__name__)
db = postgresql.open('pq://dmwonkomseluvu:056095e637408a79a7afd2a510829bb8071a69a237c9aa48d4e7af7831980c17@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/d5frennvu4ie97')


@app.route("/", methods=['POST'])
def postparty():
    if not request.json or not 'name' in request.json:
        abort(400)
    user = request.json['name']
    sql = db.prepare("SELECT party FROM santa WHERE name = $1")
    checkparty = sql(user)
    if checkparty != [(None,)]:
        a = checkparty[0][0]
        sqlrn = db.prepare("SELECT real_name FROM santa WHERE name = $1")
        c = sqlrn(a)
        e = c[0][0]
        resp = jsonify({'party': e})
    else:
        sel = db.prepare("SELECT name FROM santa WHERE has_party ISNULL AND name != $1 ORDER BY uuid LIMIT 1")
        r = sel(user)
        print (r)
        z=r[0]
        x=z[0]
        print(x)
        pupd = db.prepare("UPDATE santa SET party = $1 WHERE name = $2")
        pupd(x,user)
        upd = db.prepare("UPDATE santa SET has_party = true WHERE name = $1")
        upd(x)
        getname = db.prepare("SELECT real_name FROM santa WHERE name = $1")
        realname = getname(x)
        getuid = db.prepare("SELECT uuid FROM santa WHERE name = $1")
        guid = getuid(user)
        resp = jsonify({'party': realname, "uuid": guid})
    return resp

@app.route("/<uuid>", methods=['GET'])
def getparty(uuid):
    if not uuid:
        abort(400)
    getp = db.prepare("SELECT party FROM santa WHERE uuid = $1")
    h = getp(uuid)
    j = h[0]
    k = j[0]
    return jsonify({'your party': k})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)