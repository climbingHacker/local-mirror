import mysql.connector
import flask
import tomllib
import apt
import requests
from pathlib import Path
import os
from flask import stream_with_context

CHUNK = 1024 * 1024

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
# mirror.syncdb()


@app.route("/")
def index():
    return "test"


@app.route("/debian/pool/<component>/<letter>/<package>/<filename>")
def package(component, letter, package, filename):
    if (mirror.package_tracked(package)
        and Path("mirror/pool/{component}/{letter}/{package}/{filename}").exists()
    ):
        with open(f"mirror/pool/{component}/{letter}/{package}/{filename}", "rb") as p:
            return flask.send_file(p)
    req = requests.get(
        config["mirror"] + f"/pool/{component}/{letter}/{package}/{filename}",
        stream=True,
        timeout=(10, None),
    )
    req.raw.decode_content = True
    folder_path = Path(
        os.getcwd() + os.path.join(f"mirror/pool/{component}/{letter}/{package}")
    )  # define folder structure
    if not os.path.exists(folder_path):  # create folders if not exists
        os.makedirs(folder_path)

    local = open(
        f"mirror/pool/{component}/{letter}/{package}/{filename}.part",
        "wb+",
    )

    @stream_with_context
    def generator():
        try:
            for chunk in req.iter_content(chunk_size=CHUNK):
                if not chunk:  # keep-alive/empty chunks
                    continue
                local.write(chunk)
                yield chunk
        finally:
            local.close()
            req.close()
            os.replace(
                "mirror/pool/{component}/{letter}/{package}/{filename}.part}",
                "mirror/pool/{component}/{letter}/{package}/{filename}",
            )
            mirror.track_package(package)

    if req.status_code == 200:
        return flask.Response(generator())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
