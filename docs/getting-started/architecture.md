# Architecture

Jupyter Notebooks work with what is called a two-process model based on a kernel-client infrastructure. This model applies a similar concept to the Read-Evaluate-Print Loop (REPL) programming environment that takes a single user’s inputs, evaluates them, and returns the result to the user.

Based on the two-process model concept, we can explain the main components of Jupyter in the following way:

![](../images/JUPYTER_ARCHITECTURE.png)

## Jupyter Client

* It allows a user to send code to the kernel in a form of a Qt Console or a browser via notebook documents.
* From a REPL perspective, the client does the read and print operations.
* Notebooks are hosted by a Jupyter web server which uses Tornado to serve HTTP requests.

## Jupyter Kernel

* It receives the code sent by the client, executes it, and returns the results back to the client for display. A kernel process can have multiple clients communicating with it which is why this model is also referred as the decoupled two-process model.
* From a REPL perspective, the kernel does the evaluate operation.
* kernel and clients communicate via an interactive computing protocol based on an asynchronous messaging library named ZeroMQ (low-level transport layer) and WebSockets (TCP-based)

## Jupyter Notebook Document

* Notebooks are automatically saved and stored on disk in the open source JavaScript Object Notation (JSON) format and with a .ipynb extension.