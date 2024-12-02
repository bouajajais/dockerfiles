# dockerfiles

This Docker image allows you to build base images for your custom images and dev images for a Docker devcontainer environment for VSCode. These images add a non root user to existing base images. Additional features are installed on top of base images to provide you with ready to use images (like docker-python or cuda-poetry).

## Available tags

Only `latest` tag is available.

## Usage

### Step 1: Pull and edit `config.json`

1. Run the following command to pull the default `config.json` locally: (make sure your local `config.json` file exists)
    ```bash
    docker run --rm -it -e USER_UID=$(id -u) -e USER_GID=$(id -g) -v /var/run/docker.sock:/var/run/docker.sock -v /path/to/config.json:/app/config/config.json ismailbouajaja/dockerfiles config
    ```

    Here's the default `config.json`:
    ```json
    {
        "partial_args": {
            "docker_user": "ismailbouajaja",
            "target": ["prod", "dev"],
            "base_image": [""],
            "docker_tag": ["27.3.1-cli"],
            "poetry_version": ["1.8"],
            "python_version": ["3.10", "3.11", "3.12"],
            "python_type": ["", "slim"],
            "python_os": [""],
            "cuda_version": ["12.4.1", "12.5.1", "12.6.2"],
            "cuda_cudnn": ["", "cudnn"],
            "cuda_type": ["devel"],
            "cuda_os": ["ubuntu22.04"]
        },
        "target_images": []
    }
    ```

2. Edit the `config.json` to your liking. (see `config.json` specifications below)

### Step 2: Initialize your project

3. Run the following command :

    ```bash
    docker run --rm -it -e USER_UID=$(id -u) -e USER_GID=$(id -g) -v /var/run/docker.sock:/var/run/docker.sock -v ~/.docker/config.json:/root/.docker/config.json -v /path/to/config.json:/app/config/config.json -v /optional/path/to/logs/folder:/app/data/logs ismailbouajaja/dockerfiles
    ```

    This assumes that you have docker installed on your computer and that you have already logged in to your account for running docker commands locally and that the authentication informations are in `~/.docker/config.json`, otherwise you should change that volume path in the `docker run` command.

4. Run the updates:

    The container will tell you what are all the images that will be built and published in the process.

    If everything's good, type `y` and enter. 
    
### Step 3: Check the logs for failures

5. Read the logs to verify if all images were successfully built. Every succesfully built and published image is logged with the keyword `SUCCESS` while every failure is logged with the keyword `ERROR`. The logs are output to the terminal you run the container in. They are also optionally created in the logs folder if you mounted its corresponding volume when running the container.

## `config.json` specifications

### - `partial_args`:

This field is an object that contains different arguments that are combined together to produce different combinations of images and tags.

#### -- `docker_user`: `"ismailbouajaja"`

This field is a string that corresponds to the `hub.docker` account where the images will be pushed and it defaults to `"ismailbouajaja"`.

`"ismailbouajaja"` is currently the only possible value.

#### -- `target`: `["prod", "dev"]`

This field is an array containing any combination of the two values: `"prod"` and `"dev"`.

It represents the build target of each Dockerfile.

Both targets have non-root users added to the base image. `"dev"` target installs additional features like `sudo` and `git`.

#### -- `base_image`: `[]`

This field is an array of publicly available docker images (like `"python:3.10"`).

Fill this field to build and publish `ismailbouajaja/base:{base_image_owner}__{base_image_name}__{base_image_tag}` images.

## dockerfiles

#### NOTE

I'll use `to_tag` to replace images in the format:
- `owner/basename:tag` to `owner__basename__tag`
- `basename:tag` to `basename__tag`

### Image Naming

Here is the general rule used to name images:
- The owner is `ismailbouajaja`
- The name of the image is chosen on the spot
- The tag is constructed as follow:
We start with the names used in the image basename then with the remaining args and if the target is `"dev"` then we add `"dev"` at the end. All of these chunks are separated with a double dash `"--"`

#### Example

For example, the image `cuda-poetry` has 3 arguments: `CUDA_TAG`, `POETRY_VERSION` AND `PYTHON_VERSION`.

Since `cuda` and `poetry` are part of the image basename `cuda-poetry`, we start with these two names in that order then we add the remaining args which in this case is `python` alone.

We consider in this example that the target is `"dev"`.

Therefore the tag is: `nvidia__cuda__{CUDA_TAG}--poetry__{POETRY_VERSION}--python__{PYTHON_VERSION}--dev`

The final image name would be: `ismailbouajaja/cuda-poetry:nvidia__cuda__{CUDA_TAG}--poetry__{POETRY_VERSION}--python__{PYTHON_VERSION}--dev`

### Images

Here are the different images that are built and published:

### ismailbouajaja/base

It uses:
- `docker_user = partial_args["docker_user"]`
- `base_image = partial_args["base_image"]`

It depends on: `partial_args["base_image"]`

It builds and publishes: `{docker_user}/base:{base_image_owner}__{base_image_name}__{base_image_tag}`

## Clone repository

To clone the github repository, follow these steps :

1. Clone the repository:
    ```bash
    git clone https://github.com/bouajajais/setup-devcontainer.git
    ```

2. Navigate to the project directory:
    ```bash
    cd setup-devcontainer
    ```

### Build and run the Dockerfile
3. Build the Docker image using the provided Dockerfile:
    ```bash
    docker build --build-arg USER_UID=$(id -u) --build-arg USER_GID=$(id -g) -t setup-devcontainer .
    ```

    The `docker build` command accepts the following arguments:
    - `ARG PYTHON_TAG=3.10-slim-buster`: The Python tag to use.
    - `ARG POETRY_VERSION=1.8.*`: The Poetry version to install.

4. Run the Docker container to generate `config.json`: (make sure your local `config.json` file exists)
    ```bash
    docker run --rm -it -e USER_UID=$(id -u) -e USER_GID=$(id -g) -v /path/to/config.json:/app/config/config.json setup-devcontainer config
    ```

5. Run the Docker container to initialize a project:
    ```bash
    docker run --rm -it -e USER_UID=$(id -u) -e USER_GID=$(id -g) -v /optional/path/to/config.json:/app/config/config.json -v /path/to/project/folder:/app/data/target setup-devcontainer
    ```

### Docker compose up

3. Create a `.env` file next to the file `compose.yaml` and define the following environment variables inside :
    ```bash
    CONFIG_FILEPATH=/path/to/config.json
    DATA_PATH=/optional/path/to/project/folder
    ```

4. Run the following commands :
    ```bash
    chmod +x ./set_user_guid.sh
    ./set_user_guid.sh
    docker compose run --rm dockerfiles
    ```




## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.