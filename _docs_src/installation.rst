.. _installation:

============
Installation
============

Prerequisites
=============
Prerequisites:

- `conda` (included in Miniconda 3 and Anaconda 3 distributions)

Clone the ttt's repository
============================

.. code-block:: bash

    git clone https://github.com/sbugallo/TicTacToe-MDP.git
    cd TicTacToe-MDP

The following instructions assume that you are located in the root of `TicTacToe-MDP'`.

Install requirements
====================

`conda` is the recommended way for installing all the requirements. You can install `conda` from
`this link <https://docs.conda.io/en/latest/miniconda.html>`_. The following instructions assume that you have
conda installed on your system.

Predefined conda environments for different use cases are provided under `./envs`. There are 2
available environments:

- **dev.yml**: for simple execution usage.
- **prod.yml**: to generate docs, test and develope new features.

You can create a new conda environment as follows:

.. code-block:: bash

    conda env create -f ./envs/{dev.yml | prod.yml}


Usage examples:

.. code-block:: bash

    conda env create -f ./envs/dev.yml
    conda env create -f ./envs/prod.yml

Once our environment is installed, we have to activate it running the following:

.. code-block:: bash

    source activate ttt

Assuming that you have the environment activated, we install `ttt` module running:

.. code-block:: bash

    python setup.py install

If you plan to modify de source code, run some tests or generate documentation you should install the module in
development mode:

.. code-block:: bash

    python setup.py develop

This will also install some scripts that can be run directly in your terminal:

- `ttt-human-vs-human`
- `ttt-human-vs-cpu`
- `ttt-cpu-vs-cpu`
- `ttt-train`

To see how they work, please go to :ref:`usage` section

Docker
======

To facilitate the usage, a docker image is available at
`https://hub.docker.com/r/sbugallo/ttt <https://hub.docker.com/r/sbugallo/ttt>`_ .

Prerequisites
-------------

Prerequisites:

 - `docker` (see `https://docs.docker.com/install/ <https://docs.docker.com/install/>`_)
