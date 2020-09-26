Taichi.js
=========

Play Taichi kernels online by Emscripten and Taichi's C backend.


How to setup a TaichiHub server
-------------------------------

1. Install Emscripten SDK according to `their official documentation <https://emscripten.org/docs/getting_started/downloads.html>`_:

.. code-block:: bash

    git clone https://github.com/emscripten-core/emsdk.git
    cd emsdk
    ./emsdk install latest
    ./emsdk activate latest
    source ./emsdk_env.sh
    cd ..
    emcc --version

2. Install Flask and Taichi:

.. code-block:: bash

    python3 -m pip install flask
    python3 -m pip install taichi

3. Clone this repo:

.. code-block:: bash

    git clone https://github.com/taichi-dev/taichi.js.git
    cd taichi.js

4. Build the container for executing user Python code:

.. code-block:: bash

    docker build . -t taichihub

5. Start the server:

.. code-block:: bash

    source /path/to/emsdk/emsdk_env.sh  # add `emcc` to PATH
    python3 -m flask run
