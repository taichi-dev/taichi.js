if (typeof require != 'undefined') {
    JsTaichi = require('./taichi.js').JsTaichi;
    myProgram = require('./program.js');
} else {
    myProgram = Module;
}

let ta = new JsTaichi(myProgram);

ta.module.onRuntimeInitialized = function() {
    ta.get('render_c4_0')();
    let extr = ta.set_ext_arr(0, [512, 512, 3]);
    ta.get('matrix_to_ext_arr_c18_0')();
    console.log(extr);
};
