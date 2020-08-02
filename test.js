let taichi = require('./taichi.js');
let mpm88 = new taichi.Taichi(require('./mpm88.py.js'));

let init = mpm88.get('init_c6_0');
let substep = mpm88.get('substep_c4_0');
let matrix_to_ext_arr = mpm88.get('matrix_to_ext_arr_c20_0');

mpm88.ready(function() {
    init();
    substep();
    let extr = mpm88.set_ext_arr(0, [8192, 2]);
    matrix_to_ext_arr();
    console.log(extr);
});
