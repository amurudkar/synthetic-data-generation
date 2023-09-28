import cv2 as cv
import numpy as np
import open3d as o3d


def draw_3d_box(img, box_points):
    box_int = box_points.astype(int)
    for i in range(4):
        img = cv.line(img, box_int[:2, i], box_int[:2, i + 4], (255, 0, 0), 2)
        img = cv.line(img, box_int[:2, i], box_int[:2, (i + 1) % 4], (0, 255, 0), 2)
        img = cv.line(img, box_int[:2, i + 4], box_int[:2, ((i + 1) % 4) + 4], (0, 0, 255), 2)


def project_3d_points(K, W, P, X):
    if X.shape[0] != 4:
        print(X.shape)
        X = np.vstack(X, np.ones((1, X.shape[1])))
        
    X_proj = K @ W @ P @ X
    X_proj = (X_proj / X_proj[2,:])
    X_proj = X_proj[:2,:]
    return X_proj


# Columns = coord, rows = dims
def bounds3d_2_corners(bounds):
    rmin = bounds[:,0:1]
    fmax = bounds[:,1:2]

    rmax = fmax.copy()
    rmax[2] = rmin[2]

    fmin = rmin.copy()
    fmin[2] = fmax[2]
    
    f_coords = bounds2d_2_corners(np.hstack((fmin, fmax)))
    r_coords = bounds2d_2_corners(np.hstack((rmin, rmax)))

    return f_coords, r_coords


def bounds2d_2_corners(bounds):
    bl = bounds[:,0:1]
    tr = bounds[:,1:2]

    # print(bl, tr)

    # Bounds to 4 corners
    # 
    #   ------------------------- X
    #  |  tl                *tr*
    #  |    ----------------
    #  |   |                |
    #  |   |                |
    #  |   |                |
    #  |    ----------------
    #  | *bl*               br
    #  |
    #  Y
    
    br = bl.copy()
    br[0] = tr[0]

    tl = tr.copy()
    tl[0] = bl[0]

    return bl, br, tr, tl


def pyrender_node_bounds(node):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(node.mesh.primitives[0].positions)
    pcd.transform(node.matrix)
    pcd_box = pcd.get_axis_aligned_bounding_box()
    bounds = np.vstack((pcd_box.min_bound, pcd_box.max_bound)).transpose()
    return bounds


