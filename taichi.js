if (window && window.location.href.startsWith('file://')) {
    alert('Taichi.js could not be functional when accessed from a local '
        + 'file (i.e. file://) due to WASM limitation, please run '
        + '`python server.py` in the project root directory and access '
        + 'this page using http or https instead.');
}

class Taichi {
    constructor(module) {
        this.module = module;
    }

    set_arg_int(index, value) {
        let args_base = this.module._Ti_args/4 + index * 2;
        let args = this.module.HEAP32.subarray(args_base, args_base + 1);

        args[0] = value;
    }

    set_arg_float(index, value) {
        let args_base = this.module._Ti_args/4 + index * 2;
        let args = this.module.HEAPF32.subarray(args_base, args_base + 1);

        args[0] = value;
    }

    set_ext_arr(index, shape) {
        let earg_base = this.module._Ti_earg/4 + index * 8;
        let extr_base = this.module._Ti_extr/4;
        let args_base = this.module._Ti_args/4 + index * 2;
        let earg = this.module.HEAP32.subarray(earg_base, earg_base + 8);
        let args = this.module.HEAP32.subarray(args_base, args_base + 1);

        args[0] = this.module._Ti_extr;

        let size = 1;
        for (let i = 0; i < shape.length; i++) {
            earg[i] = shape[i];
            size *= shape[i];
        }

        let extr = this.module.HEAPF32.subarray(extr_base, extr_base + size);
        return extr;  // let the user fill it instead of our memcpy
    }

    get(name) {
        let ret = this.module['_Tk_' + name];
        if (typeof ret == 'undefined') {
            console.error('Undefined Taichi kernel:', name);
        }
        return function() {
            return ret(this.module._Ti_ctx);
        }.bind(this);
    }

    ready(cb) {
        this.module.onRuntimeInitialized = cb;
    }
}

function taichiAnimation(callback) {
    let fps = 0;
    let last_time = Date.now();

    function wrapped() {
        window.requestAnimationFrame(wrapped);

        if((Date.now() - last_time) >= 1000) {
            console.log(fps, 'FPS');
            last_time = Date.now();
            fps = 0;
        }
        fps++;

        callback();
    }
    wrapped();
}

function taichiSetImage(ctx, image) {
    let imgData = ctx.createImageData(RES, RES);
    for (let y = 0; y < RES; y++) {
        for (let x = 0; x < RES; x++) {
            let i = (y * RES + x) * 4;
            let j = (x * RES + (RES - 1 - y)) * 4;
            imgData.data[i++] = parseInt(image[j++] * 255);
            imgData.data[i++] = parseInt(image[j++] * 255);
            imgData.data[i++] = parseInt(image[j++] * 255);
            imgData.data[i++] = 255 - parseInt(image[j++] * 255);
        }
    }
    ctx.putImageData(imgData, 0, 0);
}
