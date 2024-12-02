# syntax=docker/dockerfile:1

# Set the CUDA version to install
ARG CUDA_TAG=12.6.2-cudnn-devel-ubuntu22.04

# Set the Python version to install
ARG PYTHON_VERSION=3.10

#################### PROD IMAGE with non-root user ####################

FROM ismailbouajaja/cuda:nvidia__cuda__${CUDA_TAG} AS prod

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set environment variables to avoid user prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

ARG PYTHON_VERSION

# Install system packages
RUN apt-get update \
    # Install the software-properties-common package to add new repositories (ppa:deadsnakes/ppa for Python)
    && apt-get install -y software-properties-common \
    # Add the deadsnakes PPA to install Python
    && add-apt-repository ppa:deadsnakes/ppa \
    # Update the package list to include the new repository
    && apt-get update \
    # Install the Python ${PYTHON_VERSION} interpreter and essential tools
    && apt-get install -y \
    # Essential tools for building software (gcc, g++, make)
    build-essential \
    # Cross-platform tool for managing the build process
    cmake \
    # Version control system
    git \
    # Command-line utility for downloading files
    wget \
    # Tool for transferring data with URLs
    curl \
    # Common CA certificates to ensure HTTPS connections work
    ca-certificates \
    # Python ${PYTHON_VERSION} interpreter
    python${PYTHON_VERSION} \
    # Header files and a static library for Python C extensions
    python${PYTHON_VERSION}-dev \
    # Tool for creating isolated Python environments
    python3-venv \
    # Download get-pip.py and install pip for Python ${PYTHON_VERSION}
    && wget https://bootstrap.pypa.io/get-pip.py \
    && python${PYTHON_VERSION} get-pip.py \
    # Clean up the package list to reduce the image size
    && rm -rf /var/lib/apt/lists/* \
    && rm get-pip.py

# Set Python ${PYTHON_VERSION} as the default python and pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1

#################### DEV IMAGE with non-root user ################

FROM ismailbouajaja/cuda:nvidia__cuda__${CUDA_TAG}--dev AS dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set environment variables to avoid user prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

ARG PYTHON_VERSION

# Install system packages
RUN apt-get update \
    # Install the software-properties-common package to add new repositories (ppa:deadsnakes/ppa for Python)
    && apt-get install -y software-properties-common \
    # Add the deadsnakes PPA to install Python
    && add-apt-repository ppa:deadsnakes/ppa \
    # Update the package list to include the new repository
    && apt-get update \
    # Install the Python ${PYTHON_VERSION} interpreter and essential tools
    && apt-get install -y \
    # Essential tools for building software (gcc, g++, make)
    build-essential \
    # Cross-platform tool for managing the build process
    cmake \
    # Version control system
    git \
    # Command-line utility for downloading files
    wget \
    # Tool for transferring data with URLs
    curl \
    # Common CA certificates to ensure HTTPS connections work
    ca-certificates \
    # Python ${PYTHON_VERSION} interpreter
    python${PYTHON_VERSION} \
    # Header files and a static library for Python C extensions
    python${PYTHON_VERSION}-dev \
    # Tool for creating isolated Python environments
    python3-venv \
    # Download get-pip.py and install pip for Python ${PYTHON_VERSION}
    && wget https://bootstrap.pypa.io/get-pip.py \
    && python${PYTHON_VERSION} get-pip.py \
    # Clean up the package list to reduce the image size
    && rm -rf /var/lib/apt/lists/* \
    && rm get-pip.py

# Set Python ${PYTHON_VERSION} as the default python and pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1