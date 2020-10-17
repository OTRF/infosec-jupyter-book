# Docker

I prefer to share a standardized and working environment via docker images to focus more on the capabilities of the application rather than spend time troubleshooting the server installation.

## Pre-Requirements

* [Docker Community Edition](https://docs.docker.com/install/linux/docker-ce/binaries/)

You just have to install the community edition of Docker, so that you can pull and run ready-to-run Docker images containing Jupyter applications and interactive computing tools. You can use a stack image to do any of the following (and more):

* Start a personal Jupyter Notebook server in a local Docker container
* Run JupyterLab servers for a team using JupyterHub
* Write your own project Dockerfile

**Community Docker Images**

* [Jupyter Docker Stacks](https://github.com/jupyter/docker-stacks)_
* [Jupyter Docker Base Image](https://hub.docker.com/r/jupyter/base-notebook/)
* [Hunters Forge Images](https://github.com/hunters-forge/notebooks-forge)


![](../images/JUPYTER_DOCKER_GH_MINIMAL.png)


## Downloading and Running a Jupyter Notebook Server

```bash
docker run -p 8888:8888 jupyter/minimal-notebook:latest
```


![](../images/JUPYTER_DOCKER_MINIMAL_RUN.png)


### Demo Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/KVR1_cVlLRE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Using Open Threat Research (OTRF) Docker Images

### Running Latest Images

You can simply download and run a docker image already created by the OTR Community. The Docker images are under the following account: [https://hub.docker.com/u/cyb3rward0g](https://hub.docker.com/u/cyb3rward0g). Look for the docker image names that start with `jupyter-`. If we want to download and run the `jupyter-base` image, you can do it with the following command:

```bash
docker run -p 8888:8888 cyb3rward0g/jupyter-base:latest
```

### Building Latest Images

Clone OTR notebooks-forge repository

```bash
git clone https://github.com/OTRF/notebooks-forge
```

Build & Run Docker Image

```bash
cd notebooks-forge/docker/jupyter-base
docker build -t jupyter-base .
docker run -d -ti -p 8888:8888 --name jupyter-base jupyter-base
```

### Get Notebook Server Link

```bash
docker exec -i jupyter-base jupyter notebook list

Currently running servers:
http://0.0.0.0:8888/?token=bcd90816a041fa1f966829d1d46027e4524f40d97b96b8e0 :: /opt/jupyter/notebooks
```

### Browse to Link

![](../images/JUPYTER_NOTEBOOK_SERVER.png)
