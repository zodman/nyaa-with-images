from dotenv import load_dotenv
import dataset
import os
import flask
import json

load_dotenv()

dir_path = os.path.dirname(os.path.realpath(__file__))
app = flask.Flask(__name__, )


@app.route("/")
def index():
    db = dataset.connect(
        os.environ.get("DATABASE_URL", f'sqlite:///{dir_path}/database.db'))
    table = db["entry"]
    entries = []
    for i in table.all(order_by="now", _limit=75):
        i["jikan"] = json.loads(i["jikan"])
        i["guessit"] = json.loads(i["guessit"])
        if i["jikan"]:
            entries.append(i)
    context = {'entries': entries}

    return flask.render_template("index.html", **context)
