
import trimesh
import numpy as np

#mesh = trimesh.load("testing/data/models/motor.glb")
#손잡이 달린 컵 메시 데이터
#mesh = trimesh.load("D:/Software_Capstone/archive (1)/ShapeNetCore.v2/ShapeNetCore.v2/03797390/3a7439cfaa9af51faf1af397e14a566d/models/model_normalized.ply")
#mesh = trimesh.load("D:/Software_Capstone/archive (1)/ShapeNetCore.v2/ShapeNetCore.v2/03797390/1a97f3c83016abca21d0de04f408950f/models/model_normalized.ply")

# target_id = "71ead7f072106c63ed13f430b2941481" #손잡이 있는 가방 - 02773838
# folder = "mask_outputs"

# mesh_path = "D:/Software_Capstone/archive (1)/ShapeNetCore.v2/ShapeNetCore.v2/02773838/" + target_id + "/models/model_normalized.ply"
# mesh = trimesh.load(mesh_path)
#mesh = trimesh.load("Chair.ply")
#mesh = trimesh.load("D:/Software_Capstone/EmpartACD/empart/Mug/Mug/models/8555.obj")
mesh = trimesh.load(r"D:\Software_Capstone\EmpartACD\empart\Microwave\Microwave\models\3465.obj")
# GLB가 Scene이면 mesh로 합치기
if isinstance(mesh, trimesh.Scene):
    mesh = mesh.dump(concatenate=True)

print(
    type(mesh),
    len(mesh.vertices),
    len(mesh.faces)
)

# surface point sampling
points, face_idx = trimesh.sample.sample_surface(
    mesh,
    2048
)

print(points.shape)

np.save(
    "testing/data/models/microwave3465_points_shaped_2048.npy",
    points
)