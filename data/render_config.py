import numpy as np
import json
import math
import os


class RenderConfig:
    def __init__(self, config_file=None):
        if not config_file:
            self.config = dict()
            # Background
            self.config["bg_color"] = np.asarray([0.3, 0.8, 0.9, 1]).tolist()

            # Object
            self.config["object"] = dict()
            self.config["object"]["offset"] = \
                [0, 0, -50e-2]
            self.config["object"]["rand_trans"] = \
                [[-5e-2, 5e-2],
                 [-5e-2, 5e-2],
                 [-5e-2, 5e-2]]
            self.config["object"]["rand_rot"] = \
                [[-math.pi, math.pi],
                 [-math.pi, math.pi],
                 [-math.pi, math.pi]]
            
            # Lighting
            light_arr = []
            light_1 = dict()
            light_1["type"] = "directional"
            light_1["color"] = [1, 0.9, 1]
            light_1["intensity"] = 3e1
            light_arr.append(light_1)

            light_2 = dict()
            light_2["type"] = "spot"
            light_2["cone_angle"] = np.pi / 3
            light_2["intensity"] = 1
            light_arr.append(light_2)

            self.config["lighting"] = light_arr
        else:
            with open(config_file, 'r') as f:
                self.config = json.load(f)


    def write_to_file(self, config_file):
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=4)


    def get_config(self):
        return self.config


if __name__ == "__main__":
    file_dir = os.path.dirname(__file__)
    config_file = f'{file_dir}/../configs/default_render_config.json'

    config = RenderConfig()
    config.write_to_file(config_file)

    config_2 = RenderConfig(config_file)
    print(config_2.get_config())