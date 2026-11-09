import mysql.connector
import flask
import tomllib

with open("mirror.toml", "rb") as f:
    config = tomllib.load(f)

app = flask.Flask(__name__,
    static_url_path='',
    static_folder='./mirror',
    template_folder='./templates')


@app.route("/")
def index():
    return "test"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
