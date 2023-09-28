import os
import argparse
import synthetic_data_generator as syn
import cv2 as cv
from tqdm import tqdm
import shutil


def safe_delete_check(dir):
    proceed = input(f'{dir} already exists, proceeding '\
                    f'will delete all files currently in this '\
                    f'directory, continue? (y/N): ')
    return proceed.lower() == 'y'


def safe_delete_contents(dir):
    for _, subdirs, files in os.walk(dir):
        for subdir in subdirs:
            shutil.rmtree(os.path.join(dir, subdir))
        for file in files:
            os.remove(os.path.join(dir, file))


def ensure_dir(dir):
    if os.path.exists(dir):
        if not safe_delete_check(dir):
            return False
        
        safe_delete_contents(dir)
    else:
        os.makedirs(dir)

    return True


def main(args):
    sdg = syn.SyntheticDataGenerator(args.render_cfg,
                                     args.camera_cfg,
                                     args.model_file)
    
    out_dir = args.output_dir
    images_dir = os.path.join(out_dir, 'images')
    masks_dir = os.path.join(out_dir, 'masks')

    if not ensure_dir(images_dir):
        print('Aborting')
        return
    
    if not ensure_dir(masks_dir):
        print('Aborting')
        return
        
    for i in tqdm(range(200)):
        rgb, depth = sdg.get()
        filename = f'img_{i:05d}.png'

        cv.imwrite(os.path.join(images_dir, filename), rgb)
        cv.imwrite(os.path.join(masks_dir, filename), depth)

        cv.imshow('Test', rgb)
        k = cv.waitKey(33)
        if k == 'q':
            break


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    parser = argparse.ArgumentParser(description='Generate images from 3D models')
    parser.add_argument('-r', '--render_cfg', help='Path to render config file',
                        default=f'{script_dir}/configs/default_render_config.json')
    parser.add_argument('-c', '--camera_cfg', help='Path to camera config',
                        default=f'{script_dir}/configs/camera.json')
    parser.add_argument('-m', '--model_file', help='Path to 3D model file', required=True)
    parser.add_argument('-o', '--output_dir', help='Output directory', required=True)

    args = parser.parse_args()
    main(args)