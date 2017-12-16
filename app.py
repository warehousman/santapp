from flask import Flask
import postgresql

app = Flask(__name__)
db = postgresql.open('pq://dmwonkomseluvu:056095e637408a79a7afd2a510829bb8071a69a237c9aa48d4e7af7831980c17@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/d5frennvu4ie97')


@app.route("/")
def hello():
    a = db.query("SELECT name FROM santa LIMIT 1")
    b = a[0]
    return b


if __name__ == '__main__':
    app.run(debug=True)
