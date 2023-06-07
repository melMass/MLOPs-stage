import hou
import datetime
import json

from pprint import pprint
from pathlib import Path

from PySide2 import QtWidgets

IGNORED_PARM = [hou.parmTemplateType.Button, hou.parmTemplateType.FolderSet]

def get_json_path(save=False):
    if file_path := hou.ui.selectFile(
        title="JSON File", file_type=hou.fileType.Any, pattern="*.json"
    ):
        if not save:
            return Path(file_path).resolve().as_posix()

        file_path = Path(file_path).with_suffix(".json").as_posix()
        res_path = hou.text.expandString(file_path)
        if Path(res_path).exists():
            return (
                None
                if (
                    hou.ui.displayMessage(
                        f"File {file_path} already exists, do you want to overwrite it?",
                        buttons=("Yes", "No"),
                        help="This action cannot be undone",
                        title="File already exists",
                    )
                )
                else res_path
            )


# - SERIALIZE MULTIPARM
def serialize_multiparm(parm, skip_defaults=False):
    if not parm.isMultiParmParent():
        raise ValueError("Parm is not a multiparm parent")

    out = {}
    for m in parm.multiParmInstances():
        if m.parmTemplate().type() not in IGNORED_PARM:
            index = m.multiParmInstanceIndices()[0]
            parmout = out.get(index, [])
            if skip_defaults and m.isAtDefault():
                continue

            parmout.append(serialize_parm(m))
            out[index] = parmout

    return out


# - SERIALIZE PARM
def serialize_parm(parm):
    """Serialize a parm to a dict. Return None if:
    - it's in the ignore list
    - it's a multiparm parent
    """
    if parm.parmTemplate().type() in IGNORED_PARM or parm.isMultiParmParent():
        raise ValueError(
            f"Parm {parm.name()} is not serializable because it's a multiparm parent or one of the ignored types"
        )

    value_type = "value"
    if parm.isShowingExpression():
        value_type = "expression"
    elif parm.isAtDefault():
        value_type = "default"

    return {
        "name": parm.name(),
        "value_type": value_type,
        "value": parm.expression() if parm.isShowingExpression() else str(parm.eval()),
    }


# - LOAD PARMS FROM JSON
def deserialize_node_state(node, dry=False):
    file_path = get_json_path(save=False)

    if not file_path:
        return

    res_path = Path(hou.text.expandString(file_path))

    if not res_path.exists():
        hou.ui.displayMessage(f"File {file_path} does not exist")
        return

    print("Loading JSON from:", file_path)
    data = None
    # load the json
    with open(res_path, "r") as f:
        data = json.load(f)

    if not data:
        return

    if data["node"] != node.type().name() and hou.ui.displayMessage(
                f"Node type mismatch: {data['node']} != {node.type().name()}. Continue?",
                buttons=("Yes", "No"),
                title="Node type mismatch",
            ):
        return

    # load the parms
    def set_parm(serialized_parm):
        parm = node.parm(serialized_parm["name"])
        valtype = serialized_parm["value_type"]
        val = serialized_parm["value"]
        print(
            f"Setting parm {parm.name()} to {valtype} {val} parm is of type {parm.parmTemplate().type().name()}"
        )
        if valtype == "value":
            if dry:
                print(f"Would set {parm['name']} to {parm['value']}")
            else:
                if parm.parmTemplate().type().name() == "Menu":
                    parm.set(parm.menuItems()[int(val)])
                else:
                    parm.set(val)
        elif valtype == "expression":
            if dry:
                print(f"Would set {parm['name']} to expression {parm['value']}")
            else:
                parm.setExpression(val)
        elif valtype == "default":
            if dry:
                print(f"Would revert {parm['name']} to default")
            else:
                parm.revertToDefaults()

    for parm in data["parms"]:
        set_parm(parm)

    for mp_name, mp_parms in data["multiparms"].items():
        mp = node.parm(mp_name)
        if not dry:
            mp.set(len(mp_parms))
        for _, mp_parm in mp_parms.items():
            for parm in mp_parm:
                set_parm(parm)

# - SERIALIZE NODE
def serialize_node_state(node, pretty=False, skip_defaults=False):
    """Save all parms in a node to a JSON file"""

    json_path = get_json_path(save=True)

    if not json_path:
        print("Operation aborted")
        return

    multiparms = []
    out = {
        "node": node.type().name(),
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "houdini_version": hou.applicationVersionString(),
        "parms": [],
        "multiparms": {},
    }

    for parm in node.parms():
        if parm.parmTemplate().type() not in IGNORED_PARM:
            if parm.isMultiParmInstance() or (skip_defaults and parm.isAtDefault()):
                continue
            elif parm.isMultiParmParent():
                multiparms.append(parm)
            else:
                out["parms"].append(serialize_parm(parm))

    for multiparm in multiparms:
        multiparm_name = multiparm.name()
        out["multiparms"][multiparm_name] = serialize_multiparm(
            multiparm, skip_defaults=skip_defaults
        )

    with open(json_path, "w") as f:
        if pretty:
            json.dump(out, f, indent=4)
        else:
            json.dump(out, f)

    print(f"Saved to {json_path}")


# - HScript to link new instances (works only for newly created instances)
# opmultiparm /obj/sd_solve/SD_from_scene/SceneToControlNet "camerapath#" "../camerapath#" "projmode#" "../projmode#" "nearclip#" "../nearclip#" "active#" "../active#" "minangle#" "../minangle#" "maxangle#" "../maxangle#" "bg_distance#" "../bg_distance#" "uv_distance#" "../uv_distance#"

# Some methods to look into:
# ----------------------------
# - insertMultiParmInstance
# - isMultiParmInstance
# - isMultiParmParent
# - multiParmInstanceIndices #-return the current index of the parm as a tuple (1,)
# - multiParmInstances
# - multiParmInstancesCount
# - multiParmInstancesPerItem #-return the number of "child" per parm group
# - multiParmStartOffset
# - parentMultiParm
# - removeMultiParmInstance
