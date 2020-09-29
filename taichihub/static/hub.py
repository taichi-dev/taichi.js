import taichi as ti
import numpy as np
import atexit

ti.init()


def kernel(foo):
    from taichi.lang.kernel import _kernel_impl
    foo = _kernel_impl(foo, level_of_class_stackframe=3)
    nargs = foo._primal.func.__code__.co_argcount
    args = [0 for i in range(nargs)]
    foo(*args)
    return foo


@ti.func
def cook_color(x):
    return min(255, max(0, int(x * 255)))


@ti.func
def uncook_color(x):
    return x / 255


def bind_image(img):
    @ti.kernel
    def hub_get_image(imgout: ti.ext_arr()):
        for I in ti.grouped(img):
            if ti.static(isinstance(img, ti.Matrix)):
                for j in ti.static(range(img.n)):
                    imgout[I, j] = cook_color(img[I][j])
            else:
                val = cook_color(img[I])
                for j in ti.static(range(3)):
                    imgout[I, j] = val

    imgout = np.empty((*img.shape, 4), dtype=np.uint8)
    hub_get_image(imgout)


def substep_nr(num):
    @ti.kernel
    def hub_get_substep_nr() -> int:
        return num

    hub_get_substep_nr()


def link_texture(img, url):
    @ti.kernel
    def hub_load_texture(imgin: ti.ext_arr()):
        for I in ti.grouped(img):
            for j in ti.static(range(img.n)):
                img[I][j] = uncook_color(imgin[I, j])

    imgin = np.zeros((*img.shape, 4), dtype=np.uint8)
    hub_load_texture(imgin)

    if '/' not in url:
        url = '/' + url
    ti.record_action_config('hub_texture_url', url)


def bind_particles(pos, num=None):
    if num is None:
        num = pos.shape[0]

    @ti.kernel
    def hub_get_num_particles() -> int:
        if ti.static(isinstance(num, int)):
            return num
        else:
            return num[None]

    @ti.kernel
    def hub_get_particles(posout: ti.ext_arr()):
        for I in ti.grouped(pos):
            for j in ti.static(range(2)):
                posout[I, j] = pos[I][j]

    posout = np.empty((*pos.shape, 2), dtype=np.float32)
    hub_get_num_particles()
    hub_get_particles(posout)



import hub

__all__ = [
    'hub',
    'ti',
]
