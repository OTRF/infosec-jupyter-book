# BinderHub

Another way to interact with a Jupyter Notebook server is by leveraging the BinderHub public computing infrastructure and a Binder Repository (i.e A Dockerfile). If you want to learn more about this, you can read the [MyBinder](https://mybinder.readthedocs.io/en/latest/index.html) and [BinderHub](https://binderhub.readthedocs.io/en/latest/overview.html) docs.


* Released on May, 2016
* Updated 2.0 on November, 2019
* The Binder Project is an open community that makes it possible to create shareable, interactive, reproducible environments.
* The main technical product that the community creates is called BinderHub, and one deployment of a BinderHub exists at mybinder.org.
* Who is it for?:
    * Researchers, Educators, people analyzing data and people trying to communicate the data analysis to others!!

BinderHub connects several services together to provide on-the-fly creation and registry of Docker images. It utilizes the following tools:

* A cloud provider such Google Cloud, Microsoft Azure, Amazon EC2, and others
* Kubernetes to manage resources on the cloud
* Helm to configure and control Kubernetes
* Docker to use containers that standardize computing environments
* A BinderHub UI that users can access to specify Git repos they want built
* BinderHub to generate Docker images using the URL of a Git repository
* A Docker registry (such as gcr.io) that hosts container images
* JupyterHub to deploy temporary containers for users

![](../images/Binderhub-Architecture.png)

This website was built via the [Jupyter Books](https://jupyterbook.org/intro.html) project. An open source project for building beautiful, publication-quality books and documents from computational material. Therefore, you can test the creation of a Jupyter Notebook server via Binderhub by running the server that can be used to host the content of this projects. Click on the following badge:

* [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/OTRF/infosec-jupyter-book/master)


Right after that you will see the following Binder page preparing and launching the Jupyter Notebook server:

That's it! Now you will be able to use the notebooks available in this project! The advantage of this service is that you can share your notebooks this way with others without deploying or installing a Jupyter notebook server.