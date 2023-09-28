import pyrender as pyr
import trimesh
import numpy as np
import data.camera as camera


def load_camera(json_path):
    cam = camera.Camera(json_path)
    pycam = pyr.camera.IntrinsicsCamera(*cam.get_params())
    return cam, pycam


def load_model(model_file):
    fuze_trimesh = trimesh.load(model_file)
    return pyr.Mesh.from_trimesh(fuze_trimesh)


def load_lights(config):
    lights = []
    
    for l in config["lighting"]:
        l_type = l["type"]
        
        intensity = l["intensity"] if "intensity" in l else 1e0
        color = l["color"] if "color" in l else [255, 255, 255]
        cone_angle = l["cone_angle"] if "cone_angle" in l else np.pi / 4

        light = None

        if l_type == 'directional':
            light = pyr.DirectionalLight(color=color, intensity=intensity)
        elif l_type == 'spot':
            light = pyr.SpotLight(color=color, outerConeAngle=cone_angle, intensity=intensity)

        if light:
            lights.append(light)

    return lights


def get_cam_pose(config):
    pose = np.eye(4, dtype=np.float32)
    pose[:3,3] = config["object"]["offset"]
    return pose
