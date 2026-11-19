import requests
import mysql.connector
import gzip


class mirror:
    def __checkdb(self):
        if not self.db:
            raise ValueError("No database")
            return 0
        return 1

    def __init__(self, url, db=None, distros=None):
        """
        Initializes a new instance of the mirror class.
        Args:
            name (str): The name of the mirror
            url (str): The URL of the mirror
            db (mysql.connector.MySQLConnection, optional): The database connection. Defaults to None.
            distros (list, optional): The list of supported distributions. Defaults to None.
        """
        self.url = url
        self.db = db
        self.db_cursor = db.cursor() if db else None
        self.distros = distros

    def syncdb(self):
        if not self._mirror__checkdb:
            return 0
        sql_query = f"""-- sql
                                    INSERT INTO packages (package, distro, arch, component, version, filename, size, sha256sum) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        data = []
        for distro in self.distros:
            for arch in distro.architectures:
                for component in distro.components:
                    response = requests.get(
                        f"{self.url}/dists/{distro.name}/{component}/binary-{arch}/Packages.gz"
                    )
                    print(f"Downloaded: {distro.name}-{arch}")
                    if response.status_code == 200:
                        response.raw.decode_content = True
                        f = gzip.decompress(
                            response.content
                        )  # Decompress the response content
                        f = f.decode("utf-8")  # Decode the decompressed content

                        for line in f.splitlines():
                            if line.startswith("Package:"):
                                package = line.split(":")[1].strip()
                            elif line.startswith("Version:"):
                                version = line.split(":")[1].strip()
                            elif line.startswith("Filename:"):
                                filename = line.split(":")[1].strip()
                            elif line.startswith("Size:"):
                                size = int(line.split(":")[1].strip())
                            elif line.startswith("SHA256:"):
                                sha256sum = line.split(":")[1].strip()
                                data.append(
                                    [
                                        package,
                                        distro.name,
                                        arch,
                                        component,
                                        version,
                                        filename,
                                        size,
                                        sha256sum,
                                    ]
                                )
                print(f"Parsed {distro.name}")
                self.db_cursor.executemany(sql_query, data)
                self.db.commit()
                print(f"Inserrted {distro.name}")
                data = []
        return self

    def package_tracked(self, name):
        if not self._mirror__checkdb:
            return 0
        self.db_cursor.execute(
            "SELECT * FROM packages_tracked WHERE package = %s", ([name])
        )
        if self.db_cursor.fetchone():
            return True
        return False

    def track_package(self, name):
        if not self._mirror__checkdb:
            return 0
        self.db_cursor.execute(
            "INSERT INTO packages_tracked (package) VALUES (%s)", ([name])
        )
        self.db.commit()
        return True


class distro:
    components = ["main", "contrib", "non-free", "non-free-firmware"]
    architectures = ["all", "amd64", "i386", "arm64", "armhf"]

    def __init__(self, name, architectures=None, components=None):
        self.name = name
        self.architectures = architectures or self.architectures
        self.components = components or self.components


class component:

    def __init__(self, name):
        self.name = name
        return self


class architecture:
    def __init__(self, arch):
        self.arch = arch
