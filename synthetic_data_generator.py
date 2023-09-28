import data.camera as camera
import data.render_config as rconfig
import utils.render_utils as rutils
import pyrender as pyr
import numpy as np
import time
import open3d as o3d


class SyntheticDataGenerator:
    def __init__(self, render_cfg, camera_cfg, model_file):
        np.random.seed(time.localtime())
        print('Loading render config from: ', render_cfg)
        self.config = rconfig.RenderConfig(render_cfg).get_config()
        self.scene = pyr.Scene(bg_color=self.config["bg_color"])

        print('Loading camera config from: ', camera_cfg)
        self.cam, self.render_cam = rutils.load_camera(camera_cfg)
        
        print('Loading model file from: ', model_file)
        self.model = rutils.load_model(model_file)
        self.lights = rutils.load_lights(self.config)

        # cam_pose = rutils.get_cam_pose(self.config)
        self.scene.add(self.render_cam, np.eye(4, 4)) #, pose=cam_pose)
        print('Adding lights')
        for light in self.lights:
            print(f'\t{type(light).__name__} {light.intensity}, color = {light.color * 255}')
            self.scene.add(light)

        self.mesh_node = self.scene.add(self.model)
        self.renderer = pyr.OffscreenRenderer(*self.cam.get_resolution())


    def _process_depth(depth):
        # Normalize
        out = depth / np.max(depth)

        # Threshold
        out[out >= 0.2] = 255
        out[out < 0.2] = 0

        # Return in uint8 format
        return out.astype(np.uint8)


    def get(self):
        self.randomize_pose()
        rgb, depth = self.renderer.render(self.scene)
        return rgb[:,:,::-1], SyntheticDataGenerator._process_depth(depth)
    

    def randomize_pose(self):
        # Generate random translation and rotation vectors
        rand_pose = self.get_rand_pose()

        for node in self.scene.mesh_nodes:
            self.scene.set_pose(node, rand_pose)


    def get_rand_pose(self):
        t_ranges = self.config["object"]["rand_trans"]
        r_ranges = self.config["object"]["rand_rot"]

        rand_t = np.zeros((3, 1))
        rand_r = np.zeros((3, 1))

        for i in range(len(t_ranges)):
            rand_t[i] = np.random.uniform(*t_ranges[i])
            rand_r[i] = np.random.uniform(*r_ranges[i])

        # Add translation offset to object
        rand_t = self.config["object"]["offset"] + rand_t.T
        # Convert XYZ rotations to R matrix
        rand_r = o3d.geometry.get_rotation_matrix_from_xyz(rand_r)

        # Copy to pose
        pose = np.eye(4, dtype=np.float64)
        pose[:3, :3] = rand_r
        pose[:3, 3] = rand_t

        return pose
