Train an agent
==============

To train an agent simply run the following command:

.. code:: bash

    ttt-train \
    --output_path <path where to save weights | str>\
    --lr <learning rate | float | Default: 0.1>\
    --exploration_iterations <number of games to be played during exploration phase | int | Default: 2500> \
    --exploitation_iterations <number of games to be played during exploitation phase | int | Default: 1500> \
    --exploration_exploitation_iterations <number of games to be played during exploration-exploitation phase | int | Default: 1000>

Example:

.. code:: bash

    ttt-train \
    --output_path /home/sbugallo/Documents/weights.json \
    --lr 0.1 \
    --exploration_iterations 2500 \
    --exploitation_iterations 1500 \
    --exploration_exploitation_iterations 1000
