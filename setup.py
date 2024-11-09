#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

from setuptools import setup, find_packages
from torch import cuda
from torch.utils.cpp_extension import CUDAExtension, BuildExtension
import os

packages_dust3r = ['dust3r'] + ["dust3r." + package for package in find_packages(where="dust3r")]
packages_croco = ["croco", "croco.utils", "croco.models", "croco.models.curope"]

cxx_compiler_flags = []
nvcc_compiler_flags = []

# compile for all possible CUDA architectures
all_cuda_archs = cuda.get_gencode_flags().replace('compute=', 'arch=').split()
# alternatively, you can list cuda archs that you want, eg:
# all_cuda_archs = [
#     '-gencode', 'arch=compute_70,code=sm_70',
#     '-gencode', 'arch=compute_75,code=sm_75',
#     '-gencode', 'arch=compute_80,code=sm_80',
#     '-gencode', 'arch=compute_86,code=sm_86'
# ]

if os.name == 'nt':
    cxx_compiler_flags.append("/wd4624")
    nvcc_compiler_flags.append("-allow-unsupported-compiler")

setup(
    name="dust3r",
    packages=packages_dust3r + packages_croco,
    package_dir={
        'dust3r': 'dust3r',
        'croco': 'croco'
    },
    ext_modules=[
        CUDAExtension(
            name='croco.models.curope.curope',
            sources=[
                "croco/models/curope/curope.cpp",
                "croco/models/curope/kernels.cu",
            ],
            extra_compile_args=dict(
                nvcc=nvcc_compiler_flags+['-O3', '--ptxas-options=-v', "--use_fast_math"]+all_cuda_archs,
                cxx=['-O3'])
        )
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)
