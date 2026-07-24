"""
Storage Layer

Unified storage access for all AI modules.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path


class Storage:

    def __init__(self, root="."):

        self.root = Path(root)

        self.database = (
            self.root /
            "database"
        )

        self.database.mkdir(
            parents=True,
            exist_ok=True
        )


    def path(self, filename):

        return self.database / filename


    def exists(self, filename):

        return self.path(
            filename
        ).exists()


    def load(
        self,
        filename,
        default=None
    ):

        file = self.path(
            filename
        )

        if not file.exists():

            return default if default is not None else {}

        try:

            return json.loads(
                file.read_text()
            )

        except Exception:

            return default if default is not None else {}


    def save(
        self,
        filename,
        data
    ):

        file = self.path(
            filename
        )

        file.write_text(

            json.dumps(
                data,
                indent=4
            )

        )

        return str(file)


    def delete(
        self,
        filename
    ):

        file = self.path(
            filename
        )

        if file.exists():

            file.unlink()

            return True

        return False


    def list(self):

        return sorted(

            [

                f.name

                for f in self.database.glob(
                    "*.json"
                )

            ]

        )


    def backup(
        self,
        filename
    ):

        file = self.path(
            filename
        )

        if not file.exists():

            return None

        backup_dir = (
            self.database /
            "backup"
        )

        backup_dir.mkdir(
            exist_ok=True
        )

        backup = (

            backup_dir /

            f"{file.stem}_"

            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            ".json"

        )

        shutil.copy2(
            file,
            backup
        )

        return str(backup)
