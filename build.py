#!/usr/bin/env python3
"""
Dependencies install script
USAGE: python daw-deps/build.py [build-directory] [install-path]
"""

import os
import platform
import subprocess
import sys

OPTION_SANITIZE=None
OPTION_RELEASE_FLAGS_GCC_CLANG='-DNDEBUG -O3 -march=x86-64-v3 -mtune=corei7 -ffunction-sections -fdata-sections'
OPTION_RELEASE_FLAGS_MSVC=None

script_path = os.path.dirname(os.path.abspath(__file__))

sysargs = sys.argv[:]

if len(sysargs) > 1 and sysargs[1][0:1] == '-':
    sysargs = [__file__, './build', './install', *sysargs[1:]]
elif len(sysargs) < 3:
    sysargs = [__file__, './build', './install']

build_types = []
for arg in sysargs[3:]:
    if '-debug' in arg:
        build_types.append('Debug')
        sysargs.remove(arg)
    if '-release' in arg:
        build_types.append('Release')
        sysargs.remove(arg)

if len(build_types) == 0:
    build_types = ['Debug', 'Release']

CMDLINE_LOG_ARGS = ' --log-level=WARNING -Wno-dev '
# CMDLINE_LOG_ARGS = ''

CMDLINE_EXTRA_ARGS = None
if len(sysargs) > 3:
    CMDLINE_EXTRA_ARGS = ' '+(' '.join(sysargs[3:]))+' '

PRINT_CMDS_ONLY = False
# PRINT_CMDS_ONLY = True

PATH_DEPS_REPO = script_path
PATH_DEPS_BUILD_DIR = os.path.abspath(sysargs[1])
PATH_DEPS_INSTALL_DIR = os.path.abspath(sysargs[2])

print('PATH_DEPS_REPO', PATH_DEPS_REPO)
print('PATH_DEPS_BUILD_DIR', PATH_DEPS_BUILD_DIR)
print('PATH_DEPS_INSTALL_DIR', PATH_DEPS_INSTALL_DIR)


IS_WINDOWS = 'Windows' == platform.system()
IS_MSVC = 'VisualStudioVersion' in os.environ

COMPILER_NAME = 'clang' if not IS_MSVC else 'msvc'
if 'CC' in os.environ and os.environ['CC'] == 'gcc':
    COMPILER_NAME = 'gnu'

LINK_MODE_STRING = ['static', 'shared']
BUILD_FILE_GENERATOR = '-GNinja'

if COMPILER_NAME == 'msvc':
    BUILD_FILE_GENERATOR = ''

execution_environ = os.environ


def buildLibrary(libraryName, cmakeConfig, buildConfigs, appendPostfix=True):
    SRC_LOCATION = f'{PATH_DEPS_REPO}{os.path.sep}{libraryName}'

    for CMD_BUILD_CONFIG_TYPE in buildConfigs:
        BUILD_LOCATION = os.path.join(PATH_DEPS_BUILD_DIR, CMD_BUILD_CONFIG_TYPE, libraryName)
        INSTALL_LOCATION = os.path.join(PATH_DEPS_INSTALL_DIR)
        CMD_CMAKE_CONFIGURE = f'cmake {BUILD_FILE_GENERATOR} -S"{SRC_LOCATION}" -B"{BUILD_LOCATION}" '
        CMD_CMAKE_CONFIGURE += f' -DCMAKE_BUILD_TYPE={CMD_BUILD_CONFIG_TYPE}'
        CMD_CMAKE_CONFIGURE += f' -DCMAKE_INSTALL_PREFIX:PATH="{INSTALL_LOCATION}"'
        if appendPostfix:
            CMD_CMAKE_CONFIGURE += ' -DCMAKE_DEBUG_POSTFIX=_debug -DCMAKE_RELEASE_POSTFIX=_release'
        CMD_CMAKE_REL_FLAGS = OPTION_RELEASE_FLAGS_MSVC if IS_MSVC else OPTION_RELEASE_FLAGS_GCC_CLANG
        if CMD_CMAKE_REL_FLAGS is not None:
            CMD_CMAKE_CONFIGURE += f' -DCMAKE_C_FLAGS_RELEASE_INIT="{CMD_CMAKE_REL_FLAGS}"'
            CMD_CMAKE_CONFIGURE += f' -DCMAKE_CXX_FLAGS_RELEASE_INIT="{CMD_CMAKE_REL_FLAGS}"'
            CMD_CMAKE_CONFIGURE += f' -DCMAKE_C_FLAGS_RELWITHDEBINFO_INIT="{CMD_CMAKE_REL_FLAGS}"'
            CMD_CMAKE_CONFIGURE += f' -DCMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT="{CMD_CMAKE_REL_FLAGS}"'
        if OPTION_SANITIZE is not None:
            if IS_MSVC:
                CMD_CMAKE_CONFIGURE += f' -DCMAKE_C_FLAGS_DEBUG_INIT="/fsanitize={OPTION_SANITIZE}"'
                CMD_CMAKE_CONFIGURE += f' -DCMAKE_CXX_FLAGS_DEBUG_INIT="/fsanitize={OPTION_SANITIZE}"'
            else:
                CMD_CMAKE_CONFIGURE += f' -DCMAKE_C_FLAGS_DEBUG="-fsanitize={OPTION_SANITIZE} -fno-omit-frame-pointer"'
                CMD_CMAKE_CONFIGURE += f' -DCMAKE_CXX_FLAGS_DEBUG="-fsanitize={OPTION_SANITIZE} -fno-omit-frame-pointer"'
        if cmakeConfig:
            CMD_CMAKE_CONFIGURE += f' {cmakeConfig}'
        if CMDLINE_EXTRA_ARGS:
            CMD_CMAKE_CONFIGURE += f' {CMDLINE_EXTRA_ARGS}'
        if CMDLINE_LOG_ARGS:
            CMD_CMAKE_CONFIGURE += f' {CMDLINE_LOG_ARGS}'
        print(CMD_CMAKE_CONFIGURE)
        if not PRINT_CMDS_ONLY:
            ret = subprocess.call(CMD_CMAKE_CONFIGURE, stderr=subprocess.STDOUT, shell=True, env=execution_environ)
            if 0 != ret:
                raise Exception(f'subprocess call returned {ret}')

        CMD_CMAKE_BUILD_AND_INSTALL = f'cmake --build "{BUILD_LOCATION}" --config {CMD_BUILD_CONFIG_TYPE} --target install'
        print(CMD_CMAKE_BUILD_AND_INSTALL)
        if not PRINT_CMDS_ONLY:
            ret = subprocess.call(CMD_CMAKE_BUILD_AND_INSTALL, stderr=subprocess.STDOUT, shell=True, env=execution_environ)
            if 0 != ret:
                raise Exception(f'subprocess call returned {ret}')
        print('\n')


GLFW_ARGS = [
    '',
    'GLFW_BUILD_DOCS:BOOL=OFF',
    'GLFW_BUILD_TESTS:BOOL=OFF',
    'GLFW_BUILD_EXAMPLES:BOOL=OFF',
    'BUILD_SHARED_LIBS:BOOL=OFF',
]
buildLibrary("glfw", ' -D'.join(GLFW_ARGS), build_types)

SQLITECPP_ARGS = [
    '',
    'SQLITECPP_RUN_CPPCHECK:BOOL=OFF',
    'SQLITECPP_RUN_CPPLINT:BOOL=OFF',
    'SQLITECPP_INTERNAL_SQLITE:BOOL=ON',
    'SQLITECPP_USE_STATIC_RUNTIME:BOOL=OFF',
    'SQLITE_ENABLE_COLUMN_METADATA:BOOL=OFF',
    'SQLITE_ENABLE_JSON1:BOOL=OFF',
    'SQLITE_OMIT_JSON:BOOL=ON',
    'SQLITECPP_USE_STACK_PROTECTION:BOOL=OFF',
    'BUILD_SHARED_LIBS:BOOL=OFF',
]
buildLibrary("SQLiteCpp", ' -D'.join(SQLITECPP_ARGS), build_types)

SOXR_ARGS = [
    '',
    'BUILD_EXAMPLES:BOOL=OFF',
    'BUILD_TESTS:BOOL=OFF',
    'WITH_OPENMP:BOOL=OFF',
    'WITH_LSR_BINDINGS:BOOL=OFF',
    'BUILD_SHARED_RUNTIME:BOOL=ON',
    'BUILD_SHARED_LIBS:BOOL=ON',
    f'CMAKE_RELEASE_POSTFIX="-{COMPILER_NAME}-release"',
    f'CMAKE_DEBUG_POSTFIX="-{COMPILER_NAME}-debug"',
]
buildLibrary("soxr", ' -D'.join(SOXR_ARGS), ['Release'])

PORTAUDIO_ARGS = [
    '',
    'PA_DLL_LINK_WITH_STATIC_RUNTIME:BOOL=OFF',
    'PA_ENABLE_DEBUG_OUTPUT:BOOL=OFF',
    'BUILD_SHARED_LIBS:BOOL=OFF',
]
if platform.system() == "Windows":
    PORTAUDIO_ARGS.append('PA_USE_ASIO:BOOL=ON')

buildLibrary('portaudio', ' -D'.join(PORTAUDIO_ARGS), build_types)

buildLibrary('portmidi', ' -DBUILD_SHARED_LIBS:BOOL=OFF -DPM_USE_STATIC_RUNTIME=OFF -DPM_CHECK_ERRORS=OFF', build_types)

buildLibrary('pybind11', ' -DBUILD_SHARED_LIBS:BOOL=OFF -DPYBIND11_TEST:BOOL=OFF -DPYBIND11_INSTALL:BOOL=On', ['Release'])

KISSFFT_ARGS = [
    '',
    'KISSFFT_TEST=OFF',
    'KISSFFT_OPENMP=0',
    'KISSFFT_DATATYPE=float',
    'KISSFFT_TOOLS=OFF',
    'KISSFFT_USE_ALLOCA=OFF',
    'KISSFFT_PKGCONFIG=OFF',
    'KISSFFT_STATIC=ON',
    'BUILD_SHARED_LIBS:BOOL=OFF',
]

buildLibrary('kissfft', ' -D'.join(KISSFFT_ARGS), build_types)

BENCHMARK_ARGS = [
    '',
    'BENCHMARK_ENABLE_TESTING=OFF',
    'BENCHMARK_INSTALL_DOCS=OFF',
    'BUILD_SHARED_LIBS:BOOL=OFF',
]

buildLibrary('google-benchmark', ' -D'.join(BENCHMARK_ARGS), build_types)

# Note about libarchive + libz:
# libarchive cannot be built static-only (no switch provided)
# That means we need to provide a dynamic libz version for it to build successfully.
# On windows the dynamic libz is not needed, so we can just build it static-only.

ZLIB_ARGS = [
    'BUILD_SHARED_LIBS:BOOL=' + ('OFF' if IS_WINDOWS else 'ON'),
]
buildLibrary('zlib', ' -D'.join(ZLIB_ARGS), build_types, appendPostfix=True)
