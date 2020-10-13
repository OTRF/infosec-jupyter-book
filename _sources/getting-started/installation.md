# Installation

I am sure you are anxious to install Jupyter and start exploring its capabilities, but first you have to decide if you want to install the Jupyter Notebook server directly on your system or host it on a virtual machine or a docker container.

I believe it is important to give you the options so that you feel comfortable running the tool however you feel like it. If you want to do a classic install directly on your system, follow the [official Jupyter Install documents](https://jupyter.org/install).

## Manual Install

**Prerequisite:** Python

While Jupyter runs code in many programming languages, Python is a requirement (Python 3.3 or greater, or Python 2.7) for installing the JupyterLab or the classic Jupyter Notebook.

### Using Conda

```bash
conda install -c conda-forge notebook
```

### Using PIP

```bash
pip install notebook
```

Once Jupyter Notebook is installed, you can run it with the following command:

```
jupyter notebook
```
