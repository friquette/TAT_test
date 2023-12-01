import os
from pathlib import Path
import platform

PROJECT_ROOT = Path("G:\WORK\TAT_test\project")
file_template = "{accessory}_{asset}_{status}_{task}_{version}.{extension}"
work_template = "{accessory}_{asset}/{task}/work"
publish_template = "{accessory}_{asset}/{task}/publish"

def import_assets():
    representation = {
        "accessory": "A",
        "asset": "Toto",
        "status": "publish",
        "task": "mode",
        "extension": "ma"
    }
    workfile_path = Path(os.path.join(PROJECT_ROOT, publish_template.format(**representation)))
    latest_version = get_latest_version(workfile_path)

    representation["version"] = latest_version + 1


def get_latest_version(path):
    versions = []
    for workfile in os.listdir(path):
        file_name, extension = os.path.splitext(workfile)
        version = file_name.split("_")[-1][1:]
        versions.append(int(version))

    versions.sort()
    return versions[-1]


import_assets()