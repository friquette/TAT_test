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


def build_speed_rig():
    mesh = cmds.ls(exactType="mesh", long=True)[0]
    mesh = mesh.split('|')[1]
    new_name_mesh = f"{representation['asset']}_msh"
    cmds.rename(mesh, new_name_mesh)

    circle_path = os.path.join(PROJECT_ROOT, "circle.ma")
    square_path = os.path.join(PROJECT_ROOT, "square.ma")
    circle_ctrl_01 = cmds.file(circle_path, i=True)
    circle_ctrl_02 = cmds.file(circle_path, i=True)
    square_ctrl = cmds.file(square_path, i=True)

    controlers = cmds.ls(type="nurbsCurve", long=True)
    controlers_name = ["world_ctrl", "fly_ctrl", "global_ctrl"]
    for controler, name in zip(controlers, controlers_name):
        controler = controler.split('|')[1]
        cmds.rename(controler, name)

    objects = controlers_name + [new_name_mesh]
    for object in objects:
        cmds.select(object)
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        cmds.xform(cp=True)

    root_group = cmds.group(name="ROOT", empty=True)
    geo_group = cmds.group(new_name_mesh, name='geo', parent=root_group)
    cmds.group('world_ctrl', name='ctrl')
    cmds.parent('global_ctrl', 'world_ctrl')

    bbox = cmds.exactWorldBoundingBox(new_name_mesh)
    width = bbox[3] - bbox[0]
    height = bbox[4] - bbox[1]
    depth = bbox[5] - bbox[2]
    cmds.scale(width, height, depth, 'fly_ctrl')
    cmds.parent('fly_ctrl', 'global_ctrl')

    cmds.select(clear=True)
    root_joint = cmds.joint(name='root')
    skin_cluster = cmds.skinCluster(root_joint, new_name_mesh, toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1)[0]
    cmds.skinPercent(skin_cluster, new_name_mesh, transformValue=[root_joint, 1.0])

    cmds.select(clear=True)
    cmds.group(root_joint, name='jnt')
    cmds.parent('jnt', 'ctrl')
    cmds.parent('ctrl', 'ROOT')


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
build_speed_rig()
