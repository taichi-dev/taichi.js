import taichi as ti
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
    gui = ti.GUI(show_gui=False)
    gui.set_image(img)


def bind_particles(pos):
    gui = ti.GUI(show_gui=False)
    gui.circles(pos.to_numpy())



import hub

__all__ = [
    'hub',
    'ti',
]
