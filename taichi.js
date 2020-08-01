class Taichi {
    constructor(module) {
        this.module = module;
    }

    set_ext_arr(index, shape) {
        let earg_base = this.module._Ti_earg/4 + index * 8;
        let extr_base = this.module._Ti_extr/4;
        let args_base = this.module._Ti_args/4 + index;
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
        if (ret === undefined) {
            // ...
        }
        return function() {
            return ret(this.module._Ti_ctx);
        }.bind(this);
    }

    ready(cb) {
        this.module.onRuntimeInitialized = cb;
    }
}
