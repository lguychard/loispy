import sys; sys.path.append("..")
import flask
from interpreter.analysis import eval
from interpreter.utils import to_string


# -------
# GLOBALS
# -------

app = flask.Flask(__name__)


# ----------
# APP ROUTES
# ----------


@app.route("/")
def app_index():
    return flask.render_template("index.html")


@app.route("/eval_string/", methods=["POST"])
def eval_string():
    s = flask.request.form["string"]
    try:
        val = eval(s)
        return flask.jsonify(retval=to_string(val))
    except Exception as e:
        return flask.jsonify(error=e)


@app.route("/get_env_info/", methods=["GET"])
def get_env_info():
    raise NotImplementedError


# -------------
# PARTY STARTER
# -------------


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
