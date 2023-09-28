# Synthetic Data Generation
A python module to generate synthetic images from 3D models, for use in image detection/segmentation tasks.

## Usage
1. Clone the repo
    ```bash
    git clone https://github.com/amurudkar/synthetic-data-generation.git
    cd synthetic-data-generation
    ```

1. Setup your conda or pip environment
    ```bash
    conda env create -f environment.yml
    ```

    ***or***

    Create a virtual environment using [this guide](https://virtualenv.pypa.io/en/latest/user_guide.html) (optional), then install packages using:
    
    ```bash
    python -m pip install -r requirements.txt
    ```

1. Run the *generate.py* script
    ```bash
    python ./generate.py -m <path_to_obj_file> -o <output_dir>
    ```

## Configuration
- Render settings can be configured using the [default_render_config.json](./configs/default_render_config.json) as a template.
- Additionally, camera properties can be changed by using [camera.json](./configs/camera.json) file as a template.
- The script uses the files mentioned above as default but different files can be provided using command line arguments. Run `python ./generate.py -h` to get a full list of arguments.
