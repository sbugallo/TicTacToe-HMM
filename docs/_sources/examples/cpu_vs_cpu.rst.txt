Play CPU vs CPU
=================

To make 2 CPU agents play a game, run the following command:

.. code:: bash

    ttt-cpu-vs-cpu \
    ---cpu_1_weights_path <path from where to load weights | str> \
    ---cpu_1_mode <random or best | str> \
    ---cpu_2_weights_path <path from where to load weights | str> \
    ---cpu_2_mode <random or best | str> \
    ---num_rounds <number of rounds to be played | int> \
    ---display_board <whether to display the board with each move | bool | Default: True

Example:

.. code:: bash

    ttt-cpu-vs-cpu \
    ---cpu_1_weights_path /home/sbugallo/Documents/weights_1.json \
    ---cpu_1_mode best \
    ---cpu_2_weights_path /home/sbugallo/Documents/weights_2.json \
    ---cpu_2_mode best \
    ---num_rounds 5 \
    ---display_board True