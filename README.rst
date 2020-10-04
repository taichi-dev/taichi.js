Taichi.js
=========

Play Taichi kernels online by Emscripten and Taichi's C backend.


TaichiHub
---------

TaichiHub is a website where you can create and share your creativity by writting
shaders using `the Taichi programming langurage <https://github.com/taichi-dev/taichi>`_.

If you're familiar with `Shadertoy <https://shadertoy.com>`_, then
**Taichihub is to Taichi just as Shadertoy is to GLSL**.

Preview it online at https://142857.red:3389/.

.. warning::

    As the port abuse of ``:3389`` suggested, the server is still at its early development stage.
    So there's no warranty, it might be buggy, and may temporary shutdown for maintainance.

.. note::

    Your browser needs to support WebAssembly (WASM) to make this site functional.

How to browse and edit artworks?
++++++++++++++++++++++++++++++++

Entering the website, you'll see several artworks created by users. Hovering on them to preview
the animation. Click one of them and you'll be redirected to its 'EDIT' page.

The source code is on the left side, and the result is on the right side. You may edit the source
code, then press the 'RUN' button to get the new result (may take a couple of time to compile).

Or, if you'd like to create a new artwork from scratch, press the 'CREATE NEW' button to get a
blank one. It should gives you a pre-written template rendering a colorful animation.

Once your artwork is done, press the 'SAVE' button, give your artwork a 'title', and it will be
displayed on the homepage.

.. note::

    In fact till now there're only administrator's artworks in the database...
    so please feel free to create and share your own one if you'd like to :)

Difference between TaichiHub and ordinary Taichi
++++++++++++++++++++++++++++++++++++++++++++++++

Directly copy-and-paste an ordinary Taichi program in https://github.com/taichi-dev/taichi/tree/master/examples
won't work, cause they're using Taichi's builtin GUI event loop, which is deeply embed in Python.
However TaichiHub is hosted on the web, its frontend is Javascript..

Background
::::::::::

As we all know, Taichi is a langurage embed in Python, while the browsers only support Javascript.
But with the power of Taichi's C backend, we can export Taichi kernels to C source, and then compile
them into Javascript and WebAssembly using `Emscripten <https://github.com/emscripten-core/emscripten>`_.

But **we can only export the computations in Taichi-scope, not Python-scope** this way.
So computations *must* resides in Taichi kernels to write a functional TaichiHub artwork.
The code in Python-scope are only executed on compile-time, only Taichi-scope code are called on run-time.

Kernels
:::::::

So, in order to let the compiler know *what kernels shall I export*, we need to invoke the kernels
to trigger JIT compilation. To do this, please invoke all the kernels required at runtime.

Or, equivalently, we provide a handy decorator to execute the kernel right after declaration:

.. code-block:: python

    import hub

    @hub.kernel
    def render():
        ...

    # is equivalent to:

    @ti.kernel
    def render():
        ...

    render()

You could replace all ``@ti.kernel`` to ``@hub.kernel`` while porting a program from ordinary Taichi
to TaichiHub shaders.

Kernel names
::::::::::::

TaichiHub will search kernels by name, for example:

- ``reset()`` will be called on initialization, or when 'RESET' button pressed.
- ``render(t: float)`` will be called on each frame, ``t`` is the current time in seconds.
- ``substep()`` will be called ``n``-times per frame before ``render``, ``hub.substep_nr(n)`` to specify ``n``.
- ``onclick(x: float, y: float)`` will be called when LMB is clicked, ``x``, ``y`` is the mouse position.

Rendering
:::::::::

So, we've pre-built the frontend GUI system and logic infrastructure in Javascript, which render the
**HTML5 canvas** instead of Taichi GUI which is not available in browsers. Some changes are required
to adapt to it:

1. To render **images**:

Ordinary:

.. code-block:: python

    img = ti.Vector.field(3, float, (512, 512))
    ...

    while gui.running:
        ...
        gui.set_image(img)
        gui.show()

TaichiHub:

.. code-block:: python

    import hub

    img = ti.Vector.field(3, float, (512, 512))
    ...

    hub.bind_image(img)

2. To render **particles**:

Ordinary:

.. code-block:: python

    pos = ti.Vector.field(2, float, 8192)

    while gui.running:
        ...
        gui.circles(pos.to_numpy())
        gui.show()

TaichiHub:

.. code-block:: python

    import hub

    pos = ti.Vector.field(2, float, 8192)
    ...

    hub.bind_particles(pos)


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

2. Install requirements:

.. code-block:: bash

    python3 -m pip install pymongo
    python3 -m pip install flask
    python3 -m pip install taichi
    apt install mongodb

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
    cd taichihub
    python3 -m flask run -h 0.0.0.0 -p 80


Acknowledgements
----------------

`MDUI <https://github.com/zdhxiong/mdui>`_ and `jQuery <http://jquery.com>`_ are used in frontend page design.

`Codemirror <http://codemirror.net>`_ is used for the source editor.

`BootCDN <bootcdn.cn>`_ is used for hosting and accelerating their Javascript / CSS.

Flask is used as an infrastructure for a HTTP server.

MongoDB is used for storing database and artworks.

`Emscripten <https://github.com/emscripten-core/emscripten>`_ is used for compiling C source emitted ny Taichi.

Docker is used for creating secure container executing user code.

`Shadertoy <https://shadertoy.com>`_ is taken as a good reference for TaichiHub.
