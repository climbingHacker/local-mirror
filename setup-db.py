import mysql.connector
import tomllib

with open("mirror.toml", "rb") as f:
    config = tomllib.load(f)

db = mysql.connector.connect(
    host=config["DB_HOST"],
    user=config["DB_USER"],
    password=config["DB_PASSWORD"]
)
db_cursor = db.cursor()
db_cursor.execute("CREATE DATABASE IF NOT EXISTS debian")
db_cursor.execute("USE debian")
db_cursor.execute("""-- sql
        CREATE TABLE IF NOT EXISTS distros (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            distro VARCHAR(255),
            amd64 BOOLEAN NOT NULL,
            i386 BOOLEAN NOT NULL,
            arm64 BOOLEAN NOT NULL,
            armhf BOOLEAN NOT NULL,
            riscv64 BOOLEAN NOT NULL,
            armel BOOLEAN NOT NULL,
            loong64 BOOLEAN NOT NULL,
            ppc64el BOOLEAN NOT NULL,
            s390x BOOLEAN NOT NULL
        ) WITH SYSTEM VERSIONING
    """)

db_cursor.execute("""-- sql
    CREATE TABLE IF NOT EXISTS packages (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        package VARCHAR(255),
        distro ENUM({distros}),
        arch ENUM({architectures}),
        component VARCHAR(255),
        version VARCHAR(255),
        filename VARCHAR(255),
        size BIGINT,
        sha256sum VARCHAR(64)
    ) WITH SYSTEM VERSIONING""".format(
        distros=",".join([f"'{d}'" for d in config["distributions"]]),
        architectures=",".join([f"'{a}'" for a in config["architectures"]])))


# for distro in config["distributions"]:
#     for arch in config["architectures"]:
#         for component in config["components"]:
#             db_cursor.execute("""-- sql
#                 CREATE TABLE IF NOT EXISTS {distro}_{arch}_{component} (
#                     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#                     package VARCHAR(255),
#                     version VARCHAR(255),
#                     filename VARCHAR(255),
#                     size BIGINT,
#                     sha256sum VARCHAR(64)
#                 ) WITH SYSTEM VERSIONING""".format(distro=distro, arch=arch, component=component.replace("-", "")))