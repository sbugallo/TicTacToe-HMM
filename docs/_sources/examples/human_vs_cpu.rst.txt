Play human vs CPU
=================

To play a game against a CPU simply run the following command:

.. code:: bash

    ttt-human-vs-cpu \
    --cpu_weights_path <path from where to load weights | str> \
    --cpu_mode <random or best | str>

Example:

.. code:: bash

    ttt-human-vs-cpu \
    --cpu_weights_path /home/sbugallo/Documents/weights.json \
    --cpu_mode best