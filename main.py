import mysql.connector
import flask
import tomllib
import apt

with open("mirror.toml", "rb") as f:
    config = tomllib.load(f)

app = flask.Flask(
    __name__,
    static_url_path="",
    static_folder="./mirror",
    template_folder="./templates",
)
db = mysql.connector.connect(
    host=config["DB_HOST"], user=config["DB_USER"], password=config["DB_PASSWORD"]
)
db_cursor = db.cursor()
db_cursor.execute("USE debian")
mirror = apt.mirror(
    config["mirror"], db, [apt.distro(d) for d in config["distributions"]]
)
mirror.syncdb()


@app.route("/")
def index():
    return "test"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
