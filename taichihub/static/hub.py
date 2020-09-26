import taichi as ti
import numpy as np
import atexit

ti.init()


kernels = []

def kernel(foo):
    from taichi.lang.kernel import _kernel_impl
    foo = _kernel_impl(foo, level_of_class_stackframe=3)
    kernels.append(foo)
    return foo

def finalize():
    for foo in kernels:
        nargs = foo._primal.func.__code__.co_argcount
        args = [0 for i in range(nargs)]
        foo(*args)

atexit.register(finalize)


def bind_image(img):
    @ti.kernel
    def hub_get_image(imgout: ti.ext_arr()):
        for I in ti.grouped(img):
            if ti.static(isinstance(img, ti.Matrix)):
                for j in ti.static(range(img.n)):
                    imgout[I, j] = img[I][j]
            else:
                for j in ti.static(range(4)):
                    imgout[I, j] = img[I]

    imgout = np.empty((*img.shape, 4), dtype=np.float32)
    hub_get_image(imgout)


def substep_nr(num):
    @ti.kernel
    def hub_get_substep_nr() -> int:
        return num

    hub_get_substep_nr()


def bind_particles(pos, num=None):
    if num is None:
        num = pos.shape[0]

    @ti.kernel
    def hub_get_particles(posout: ti.ext_arr()) -> int:
        for I in ti.grouped(pos):
            for j in ti.static(range(2)):
                posout[I, j] = pos[I][j]
        return num if isinstance(num, int) else num[None]

    posout = np.empty((*pos.shape, 2), dtype=np.float32)
    hub_get_particles(posout)



import hub

__all__ = [
    'hub',
    'ti',
]
