# import trimesh
# import trimesh.viewer
# import base64
# import tempfile
# import os
# import json

# with open("lift_result.json","r") as f:
#     txt = f.read()

# start = txt.find('{"hulls"')
# txt = txt[start:]

# data = json.loads(txt)

# scene = trimesh.Scene()

# mesh_groups = data["meshes"]

# for group_name, parts in mesh_groups.items():

#     if not isinstance(parts, list):
#         continue



#     for part in parts:
        

#         if not isinstance(part, dict):
#             continue

#         glb_b64 = part.get("mesh")
#         if glb_b64 is None:
#             continue

#         glb_bytes = base64.b64decode(glb_b64)

#         with tempfile.NamedTemporaryFile(
#             suffix=".glb",
#             delete=False
#         ) as tmp:

#             tmp.write(glb_bytes)
#             tmp_path = tmp.name

#         tm = trimesh.load(tmp_path)

#         if isinstance(tm, trimesh.Scene):
#             tm = tm.dump(
#                 concatenate=True
#             )


#         scene.add_geometry(tm)

#         os.remove(tmp_path)

# # browser viewer
# scene.show()




import trimesh
import base64
import tempfile
import os
import json
import numpy as np
#연구용
with open("outputs/total_result_office_chair.json", "r") as f:
    txt = f.read()
#데모용
# import argparse
# import json

# parser = argparse.ArgumentParser()

# parser.add_argument(
#     "--json",
#     required=True
# )

# args = parser.parse_args()

# with open(
#     args.json,
#     "r",
#     encoding="utf-8"
# ) as f:
#     data = json.load(f)



#연구용
start = txt.find('{"hulls"')
data = json.loads(txt[start:])

scene = trimesh.Scene()
mesh_groups = data["meshes"]

def add_part(part, color=None):
    glb_b64 = part.get("mesh")
    if glb_b64 is None:
        return

    glb_bytes = base64.b64decode(glb_b64)

    with tempfile.NamedTemporaryFile(suffix=".glb", delete=False) as tmp:
        tmp.write(glb_bytes)
        tmp_path = tmp.name

    tm = trimesh.load(tmp_path)

    if isinstance(tm, trimesh.Scene):
        tm = tm.dump(concatenate=True)

    if color is not None:
        tm.visual.face_colors = color

    scene.add_geometry(tm)
    os.remove(tmp_path)

# non-select body
for part in mesh_groups["non_select_obj"]:
    add_part(part, color=[180, 180, 180, 255])

# selected boxes
# for box_id, parts in mesh_groups["select_objs"].items():
#     for part in parts:
#         add_part(part, color=[255, 0, 0, 255])
# affordance colors
# AFF_COLORS = {

#     "lift":
#         [255, 0, 0, 255],          # red

#     "grasp":
#         [0, 0, 255, 255],          # blue

#     "contain":
#         [0, 255, 0, 255],          # green

#     "openable":
#         [255, 165, 0, 255],        # orange

#     "default":
#         [255, 255, 0, 255]         # yellow
# }
AFF_COLORS = {
    "handle_grasp": [1.0, 0.0, 0.0],   # Red (빨강)

    "default":        [0.8, 0.8, 0.8],   # Light Gray (연회색)

    "grasp":       [1.0, 0.0, 0.0],   # Red (빨강)
    "contain":     [0.0, 1.0, 0.0],   # Green (초록)
    "lift":        [0.0, 0.0, 1.0],   # Blue (파랑)
    "openable":    [1.0, 1.0, 0.0],   # Yellow (노랑)

    "support":     [1.0, 0.5, 0.0],   # Orange (주황)
    "wrap_grasp":  [0.6, 0.0, 1.0],   # Purple (보라)

    "pourable":    [0.0, 1.0, 1.0],   # Cyan (시안 - 하늘)

    "pushable":    [0.4, 0.4, 0.4],   # Gray (회색)
    "pull":        [0.5, 0.25, 0.0],  # Brown (갈색)

    "listen":      [0.0, 0.0, 0.5],   # Navy (남색)

    "wear":        [1.0, 0.4, 0.7],   # Pink (분홍)

    "press":       [0.4, 0.8, 1.0],   # Sky Blue (하늘색)

    "cut":         [0.0, 0.0, 0.0],   # Black (검정)

    "stab":        [1.0, 1.0, 1.0],   # White (흰색)

    "layable":   [1.0, 0.0, 1.0],   # Magenta (자홍)
    "sittable":  [0.0, 0.8, 0.8],   # Teal Cyan (청록)

    "move":      [0.0, 0.6, 1.0],   # Deep Sky Blue (진한 하늘색)
    "display":   [1.0, 0.0, 0.5],   # Hot Pink (진분홍)
}
#AFF_COLORS = {"default": [0.8, 0.8, 0.8]}  # 모든 affordance를 연회색으로 통일

# selected affordance meshes
for key, parts in mesh_groups["select_objs"].items():

    # key = lift_5 / grasp_1 ...
    #affordance = key.split("_")[0]
    affordance = key.rsplit("_", 1)[0]

    color = AFF_COLORS.get(
        affordance,
        AFF_COLORS["default"]
    )

    print(
        key,
        affordance,
        color
    )

    for part in parts:
        add_part(
            part,
            color=color
        )


for key, parts in mesh_groups["select_objs"].items():

    total_faces = 0

    for part in parts:

        glb_b64 = part["mesh"]

        glb_bytes = base64.b64decode(glb_b64)

        with tempfile.NamedTemporaryFile(
            suffix=".glb",
            delete=False
        ) as tmp:

            tmp.write(glb_bytes)
            tmp_path = tmp.name

        tm = trimesh.load(tmp_path)

        if isinstance(tm, trimesh.Scene):
            tm = tm.dump(concatenate=True)

        total_faces += len(tm.faces)

        os.remove(tmp_path)

    print(
        key,
        "parts =", len(parts),
        "faces =", total_faces
    )

scene.show()






# import trimesh
# import base64
# import tempfile
# import os
# import json
# import numpy as np

# with open("lift_raw_result.json","r") as f:
#     txt = f.read()

# start = txt.find('{"hulls"')
# txt = txt[start:]

# data = json.loads(txt)

# scene = trimesh.Scene()
# mesh_groups = data["meshes"]

# # ------------------------------------------------
# # non-select + select 모두 읽기
# # ------------------------------------------------
# for group_name, parts in mesh_groups.items():

#     # select_objs는 dict라서 처리
#     if isinstance(parts, dict):

#         iterable = []

#         for _, plist in parts.items():
#             iterable.extend(plist)

#     elif isinstance(parts, list):

#         iterable = parts

#     else:
#         continue

#     for part in iterable:

#         if not isinstance(part, dict):
#             continue

#         # --------------------------------
#         # mesh 또는 raw_mesh 둘 다 읽기
#         # --------------------------------
#         glb_b64 = (
#             part.get("mesh")
#             or
#             part.get("raw_mesh")
#         )

#         if glb_b64 is None:
#             continue

#         glb_bytes = base64.b64decode(
#             glb_b64
#         )

#         with tempfile.NamedTemporaryFile(
#             suffix=".glb",
#             delete=False
#         ) as tmp:

#             tmp.write(glb_bytes)
#             tmp_path = tmp.name

#         tm = trimesh.load(tmp_path)

#         if isinstance(
#             tm,
#             trimesh.Scene
#         ):
#             tm = tm.dump(
#                 concatenate=True
#             )

#         # --------------------------------
#         # 색 지정
#         # raw = 빨강
#         # vhacd hull = 랜덤
#         # global = 회색
#         # --------------------------------
#         if part.get("origin") == "per-box-raw":

#             tm.visual.face_colors = [
#                 255,0,0,255
#             ]

#         elif part.get("origin") == "per-box":

#             color = np.random.randint(
#                 50,
#                 255,
#                 4
#             )

#             tm.visual.face_colors = color

#         else:

#             tm.visual.face_colors = [
#                 180,180,180,255
#             ]

#         scene.add_geometry(tm)

#         os.remove(tmp_path)

# # browser viewer
# scene.show()


# import trimesh
# import base64
# import tempfile
# import os
# import json
# import numpy as np

# with open("lift_result.json","r") as f:
#     data = json.load(f)

# scene = trimesh.Scene()

# mesh_groups = data["meshes"]

# # ------------------
# # non-select
# # ------------------
# for part in mesh_groups["non_select_obj"]:

#     glb_bytes = base64.b64decode(
#         part["mesh"]
#     )

#     with tempfile.NamedTemporaryFile(
#         suffix=".glb",
#         delete=False
#     ) as tmp:

#         tmp.write(glb_bytes)
#         tmp_path = tmp.name

#     tm = trimesh.load(tmp_path)

#     if isinstance(tm, trimesh.Scene):
#         tm = tm.dump(concatenate=True)

#     tm.visual.face_colors = [
#         np.random.randint(50,255),
#         np.random.randint(50,255),
#         np.random.randint(50,255),
#         255
#     ]

#     scene.add_geometry(tm)
#     os.remove(tmp_path)

# # ------------------
# # select_objs
# # ------------------
# for box_id, parts in mesh_groups["select_objs"].items():

#     for part in parts:

#         glb_bytes = base64.b64decode(
#             part["mesh"]
#         )

#         with tempfile.NamedTemporaryFile(
#             suffix=".glb",
#             delete=False
#         ) as tmp:

#             tmp.write(glb_bytes)
#             tmp_path = tmp.name

#         tm = trimesh.load(tmp_path)

#         if isinstance(tm, trimesh.Scene):
#             tm = tm.dump(
#                 concatenate=True
#             )

#         # 손잡이 빨강
#         tm.visual.face_colors = [
#             255,0,0,255
#         ]

#         scene.add_geometry(tm)
#         os.remove(tmp_path)

# scene.show()






