from distutils.core import setup, Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("cadsolver",
                         ["cadsolver.pyx",
                          "cadical_wrapper.cpp"],
                         language="c++",
                         extra_compile_args=["-fPIC"],
                         extra_objects=["libcadical.a"])]

for e in ext_modules:
    e.cython_directives = {'language_level': "3"}

setup(ext_modules=ext_modules,
      include_dirs = ['.'],
      cmdclass = {'build_ext': build_ext},
      name = 'cadsolver',
      version = '0.1'
)
