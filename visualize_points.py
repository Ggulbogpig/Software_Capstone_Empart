import numpy as np
import open3d as o3d

# # load sampled points
# #points = np.load("testing/data/models/motor_points.npy")
# points = np.load("D:/Software_Capstone/ICLR25-3D_ADLLM/Knife_1be1aa66cd8674184e09ebaf49b0cb2f_grasp.npy")
# print(points.shape)

# # point cloud
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(points)

# # optional color
# pcd.paint_uniform_color(
#     [0.2, 0.7, 1.0]
# )

# # visualize
# o3d.visualization.draw_geometries(
#     [pcd],
#     window_name="Motor Point Cloud"
# )



# import numpy as np
# import open3d as o3d

# #points = np.load("D:/Software_Capstone/ICLR25-3D_ADLLM/Knife_1be1aa66cd8674184e09ebaf49b0cb2f_grasp.npy")
# points = np.load("D:/Software_Capstone/ICLR25-3D_ADLLM/all_points_with_mask.npy")
# print(points.shape)

# # xyz만 추출
# xyz = points[:, :3]

# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(xyz)
# pcd.paint_uniform_color([0.2, 0.7, 1.0])

# o3d.visualization.draw_geometries(
#     [pcd],
#     window_name="Knife Point Cloud"
# )



##colored affordance point visualization
# # visualize_local.py
# import numpy as np
# import open3d as o3d

# data = np.load("D:/Software_Capstone/ICLR25-3D_ADLLM/all_points_with_mask.npy")
# #data = np.load("testing/data/models/cup_points.npy")
# points = data[:, :3]
# mask = data[:, 3]
# scores = data[:, 4]

# # 마스크 결과
# colors = np.zeros((len(points), 3))
# colors[mask == 1] = [1, 0, 0]    # 빨강 = grasp 영역
# colors[mask == 0] = [0, 0.5, 1.0]  # 파랑 = 나머지

# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(points)
# pcd.colors = o3d.utility.Vector3dVector(colors)

# o3d.visualization.draw_geometries(
#     [pcd],
#     window_name="Knife Grasp Affordance (Red=Grasp Area)",
#     width=1200,
#     height=800,
# )


import numpy as np
import open3d as o3d

# =====================================================
# LOAD NPY
# =====================================================

points = np.load("testing/data/models/mug8555_points_shaped_2048.npy")

print("shape:", points.shape)
print("min:", points.min(axis=0))
print("max:", points.max(axis=0))

# =====================================================
# POINT CLOUD
# =====================================================

pcd = o3d.geometry.PointCloud()

pcd.points = o3d.utility.Vector3dVector(
    points[:, :3]
)

# =====================================================
# AXIS
# =====================================================

axis = o3d.geometry.TriangleMesh.create_coordinate_frame(
    size=0.1
)

# =====================================================
# VISUALIZE
# =====================================================

o3d.visualization.draw_geometries(
    [pcd, axis]
)



# import numpy as np
# import open3d as o3d

# data = np.load("D:/Software_Capstone/ICLR25-3D_ADLLM/Knife_1be1aa66cd8674184e09ebaf49b0cb2f_grasp.npy")
# points = data[:, :3]
# gt_mask = data[:, 5]

# print("GT 마스크 1 개수:", gt_mask.sum())

# colors = np.zeros((len(points), 3))
# colors[gt_mask == 1] = [1, 0, 0]
# colors[gt_mask == 0] = [0, 0.5, 1.0]

# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(points)
# pcd.colors = o3d.utility.Vector3dVector(colors)

# o3d.visualization.draw_geometries(
#     [pcd],
#     window_name="GT Grasp Affordance (Red=Grasp Area)",
#     width=1200,
#     height=800,
# )