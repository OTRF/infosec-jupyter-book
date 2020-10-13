# Docker

I prefer to share a standardized and working environment via docker images to focus more on the capabilities of the application rather than spend time troubleshooting the server installation.

## Pre-Requirements

* [Docker Community Edition](https://docs.docker.com/install/linux/docker-ce/binaries/)

You just have to install the community edition of Docker, so that you can pull and run ready-to-run Docker images containing Jupyter applications and interactive computing tools. You can use a stack image to do any of the following (and more):

* Start a personal Jupyter Notebook server in a local Docker container
* Run JupyterLab servers for a team using JupyterHub
* Write your own project Dockerfile

**Community Docker Images**

* Jupyter Docker Stacks: https://github.com/jupyter/docker-stacks
* Jupyter Docker Base Image: https://hub.docker.com/r/jupyter/base-notebook/
* Hunters Forge Images: https://github.com/hunters-forge/notebooks-forge

## Downloading and Running a Jupyter Notebook Server

```bash
docker run -p 8888:8888 jupyter/minimal-notebook:3b1f4f5e6cc1
```

### Demo Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/KVR1_cVlLRE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Using Hunters Forge Docker Images

```bash
git clone https://github.com/hunters-forge/notebooks-forge
```

### Build & Run Docker Image

```bash
cd notebooks-forge/blob/master/docker/jupyter-base
docker-compose -f docker-compose.yml up --build -d
```

### Get Notebook Server Link

```bash
docker exec -i jupyter-base jupyter notebook list
```

### Browse to Link

![](../images/JUPYTER_NOTEBOOK_SERVER.png)
