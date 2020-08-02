# Taichi.js

Running compiled Taichi kernels in Javascript (powered by WASM)


## 1. Compile

To compile a existing Taichi/Python program, say `mpm88.py`, into Javascript:

```bash
./compile.py mpm88.py
```

A GUI will shows up, please **close it** after showing a image so that the process could continue.

After the process complete, the following files will be created:

- `mpm88.py.yml`
- `mpm88.py.c`
- `mpm88.py.js`
- `mpm88.py.wasm`

`mpm88.py.js` and `mpm88.py.wasm` are the final output files, make sure **include both of them** when distrubute.


## 2. Programming

The compiled program in ``mpm88.py.js`` contains all the **Taichi kernels** in ``mpm88.py``.
It can be loaded in either Node.js or any modern browser (requires ES6).

The kernel names in compiled program, is not like what they were in the ``mpm88.py`` due to Taichi's kernel naming rule, e.g.:
`substep` maybe `substep_c6_0` or `substep_c4_0`. You may checkout `mpm88.py.c` to find your desired kernel name.

### 2.1. Node.js

```js
let taichi = require('./taichi.js');
let mpm88 = new taichi.Taichi(require('./mpm88.py.js'));

let init = mpm88.get('init_c4_0');
let substep = mpm88.get('substep_c6_0');

mpm88.ready(function() {
    init();
    ...
});
```


### 2.2. Browser Javascript

```html
<script src="./taichi.js"></script>
<script src="./mpm88.py.js"></script>
<script>
let mpm88 = new Taichi(Module);

let init = mpm88.get('init_c4_0');
let substep = mpm88.get('substep_c6_0');

mpm88.ready(function() {
    init();
    ...
});
</script>
```

## 3. Visualizing

You need to set up a basic HTTP server to make WASM functional:

```bash
python server.py
```

It will shows an URL, open it in the browser, and you will browse several ``xxx.py.html``'s, choose the one you desire to play, and enjoy!
