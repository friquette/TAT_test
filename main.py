import os
from pathlib import Path
import platform

PROJECT_ROOT = Path("G:\WORK\TAT_test\project")
file_template = "{accessory}_{asset}_{status}_{task}_{version}.{extension}"
work_template = "{accessory}_{asset}/{task}/work"
publish_template = "{accessory}_{asset}/{task}/publish"

representation = {
        "accessory": "A",
        "asset": "Toto",
        "status": "publish",
        "task": "mode",
        "extension": "ma"
    }

def import_assets():
    published_workfile_path = Path(os.path.join(
        PROJECT_ROOT,
        publish_template.format(**representation)
    ))

    latest_published_file, version = get_latest_published_file_and_version(published_workfile_path)
    latest_published_filepath = Path(os.path.join(
        published_workfile_path,
        latest_published_file
    ))
    mode = cmds.file(latest_published_filepath, i=True)

    circle_path = Path(os.path.join(PROJECT_ROOT, "circle.ma"))
    square_path = Path(os.path.join(PROJECT_ROOT, "square.ma"))

    circle_ctrl = cmds.file(circle_path, i=True)
    square_ctrl = cmds.file(square_path, i=True)


def get_latest_published_file_and_version(path):
    published_files = {}
    versions = []
    for workfile in os.listdir(path):
        file_name, extension = os.path.splitext(workfile)
        version = file_name.split("_")[-1][1:]
        versions.append(int(version))
        published_files[int(version)] = workfile

    versions.sort()
    latest_published_file = published_files[versions[-1]]

    return latest_published_file, versions[-1]

import_assets()
