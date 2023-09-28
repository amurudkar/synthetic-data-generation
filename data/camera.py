import json
import numpy as np


class Camera:
    def __init__(self, json_path):
        with open(json_path, 'r') as json_data:
            data = json.load(json_data)
            self.width = data['width']
            self.height = data['height']
            self.fx = data['fx']
            self.fy = data['fy']
            self.cx = data['cx']
            self.cy = data['cy']
            
        self.intrinsics = np.eye(3, dtype=np.float32)
        self.intrinsics[0,0] = self.intrinsics[1,1] = self.fx
        self.intrinsics[0,2] = self.cx
        self.intrinsics[1,2] = self.cy
        self.intrinsics.setflags(write=False)


    def get_resolution(self):
        return self.width, self.height


    def get_params(self):
        return self.fx, self.fy, self.cx, self.cy
        

    def get_intrinsics(self):
        return self.intrinsics