let tai = require('../taichi/program.js');

function set_ext_arr(index, shape) {
    let earg_base = tai._Ti_earg/4 + index * 8;
    let extr_base = tai._Ti_extr/4;
    let args_base = tai._Ti_args/4 + index;
    let earg = tai.HEAP32.subarray(earg_base, earg_base + 8);
    let args = tai.HEAP32.subarray(args_base, args_base + 1);

    let size = 1;
    for (let i = 0; i < shape.length; i++) {
        earg[i] = shape[i];
        size *= shape[i];
    }
    console.log(earg);

    args[0] = tai._Ti_extr;

    let extr = tai.HEAPF32.subarray(extr_base, extr_base + size);

    return extr;  // let the user fill it instead of our memcpy
}

tai.onRuntimeInitialized = function() {
    tai._Tk_render_c4_0(tai._Ti_ctx);
    let extr = set_ext_arr(0, [512, 512, 3]);
    tai._Tk_matrix_to_ext_arr_c18_0(tai._Ti_ctx);
    console.log(extr);
};
