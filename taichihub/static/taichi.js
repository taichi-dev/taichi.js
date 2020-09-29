if (typeof window != 'undefined') {
    if (window.location.href.startsWith('file://')) {
        alert('Taichi.js could not be functional when accessed from a local '
            + 'file (i.e. file://) due to WASM limitation, please run '
            + '`python server.py` in the project root directory and access '
            + 'this page using http or https instead.');
    }
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

    get_ret_int(index, value) {
        let args_base = this.module._Ti_args/4 + index * 2;
        let args = this.module.HEAP32.subarray(args_base, args_base + 1);

        return args[0];
    }

    get_ret_float(index, value) {
        let args_base = this.module._Ti_args/4 + index * 2;
        let args = this.module.HEAPF32.subarray(args_base, args_base + 1);

        return args[0];
    }

    set_ext_arr(index, shape) {
        let earg_base = this.module._Ti_earg/4 + index * 8;
        let args_base = this.module._Ti_args/4 + index * 2;
        let earg = this.module.HEAP32.subarray(earg_base, earg_base + 8);
        let args = this.module.HEAP32.subarray(args_base, args_base + 1);

        args[0] = this.module._Ti_extr;

        let size = 1;
        for (let i = 0; i < shape.length; i++) {
            earg[i] = shape[i];
            size *= shape[i];
        }

        return size;
    }

    set_ext_arr_float(index, shape) {
        let size = this.set_ext_arr(index, shape);
        let extr_base = this.module._Ti_extr/4;
        let extr = this.module.HEAPF32.subarray(extr_base, extr_base + size);
        return extr;
    }

    set_ext_arr_int(index, shape) {
        let size = this.set_ext_arr(index, shape);
        let extr_base = this.module._Ti_extr/4;
        let extr = this.module.HEAP32.subarray(extr_base, extr_base + size);
        return extr;
    }

    set_ext_arr_uint8(index, shape) {
        let size = this.set_ext_arr(index, shape);
        let extr_base = this.module._Ti_extr;
        let extr = this.module.HEAPU8.subarray(extr_base, extr_base + size);
        return extr;
    }

    get(name) {
        let ret = this.module['_Tk_' + name];
        if (typeof ret == 'undefined') {
            for (let key in this.module) {
                if (key.startsWith('_Tk_' + name)) {
                    ret = this.module[key];
                    this.module['_Tk_' + name] = ret;
                    break;
                }
            }
        }
        if (typeof ret == 'undefined')
            return undefined;
        return function() {
            return ret(this.module._Ti_ctx);
        }.bind(this);
    }

    get_config_int(name) {
        let base = this.module['_Ti_cfg_' + name];
        if (typeof base == 'undefined')
            return undefined;
        return this.module.HEAP32[base/4];
    }

    get_config_float(name) {
        let base = this.module['_Ti_cfg_' + name];
        if (typeof base == 'undefined')
            return undefined;
        return this.module.HEAPF32[base/4];
    }

    get_config_str(name) {
        let base = this.module['_Ti_cfg_' + name];
        if (typeof base == 'undefined')
            return undefined;
        let ret = '';
        for (var i = base; this.module.HEAPU8[i] != 0; i++) {
            ret += String.fromCharCode(this.module.HEAPU8[i]);
        }
        return ret;
    }

    ready(cb) {
        this.module.onRuntimeInitialized = cb;
    }
}

//Taichi.tiAlreadyReady = false;

class TaichiGUI {
    constructor(canvas, resx, resy) {
        this.resx = resx || 512;
        this.resy = resy || this.resx;
        this.canvas = canvas;
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = this.resx;
        this.canvas.height = this.resy;
        this.stopped = false;
    }

    animation(callback) {
        let that = this;
        function wrapped() {
            if (that.stopped) {
                return;
            }

            callback();
            window.requestAnimationFrame(wrapped);
        }
        wrapped();
    }

    set_image_uint8(image) {
        let imgData = this.ctx.createImageData(this.resx, this.resy);
        let data = imgData.data;
        for (let y = 0; y < this.resy; y++) {
            for (let x = 0; x < this.resx; x++) {
                let i = (y * this.resx + x) * 4;
                let j = (x * this.resy + (this.resy - 1 - y)) * 4;
                data[i++] = image[j++];
                data[i++] = image[j++];
                data[i++] = image[j++];
                data[i++] = 255;
            }
        }
        this.ctx.putImageData(imgData, 0, 0);
    }

    set_image(image) {
        let imgData = this.ctx.createImageData(this.resx, this.resy);
        let data = imgData.data;
        for (let y = 0; y < this.resy; y++) {
            for (let x = 0; x < this.resx; x++) {
                let i = (y * this.resx + x) * 4;
                let j = (x * this.resy + (this.resy - 1 - y)) * 4;
                data[i++] = parseInt(image[j++] * 255);
                data[i++] = parseInt(image[j++] * 255);
                data[i++] = parseInt(image[j++] * 255);
                data[i++] = 255;
            }
        }
        this.ctx.putImageData(imgData, 0, 0);
    }

    circles(pos, radius) {
        radius = radius || 2;
        this.ctx.fillStyle = 'black';
        this.ctx.fillRect(0, 0, this.resx, this.resy);
        this.ctx.fillStyle = 'white';
        for (let i = 0; i < pos.length;) {
            let x = pos[i++] * this.resx;
            let y = (1 - pos[i++]) * this.resy;
            this.ctx.beginPath();
            this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
            this.ctx.fill();
        }
    }
}

if (typeof exports != 'undefined') {
    exports.Taichi = Taichi;
}
