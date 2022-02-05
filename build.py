import os
import subprocess
import errno    
import sys
import platform


# USAGE: python daw-deps/build.py [build-directory] [install-path]

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

script_path = os.path.dirname(os.path.abspath( __file__ ))

sysargs = sys.argv[:]

if len(sysargs) < 3:
	sysargs = [__file__, "./build", "./install"]


CMDLINE_EXTRA_ARGS = None
if len(sysargs) > 3:
    CMDLINE_EXTRA_ARGS=" "+(" ".join(sysargs[3:]))+" "

PRINT_CMDS_ONLY = False
# PRINT_CMDS_ONLY = True

PATH_DEPS_REPO=script_path
PATH_DEPS_BUILD_DIR = os.path.abspath(sysargs[1])
PATH_DEPS_INSTALL_DIR = os.path.abspath(sysargs[2])
print("PATH_DEPS_REPO %s"%PATH_DEPS_REPO)
print("PATH_DEPS_BUILD_DIR %s"%PATH_DEPS_BUILD_DIR)
print("PATH_DEPS_INSTALL_DIR %s"%PATH_DEPS_INSTALL_DIR)


BUILD_TYPE_RELEASE=0
BUILD_TYPE_DEBUG=1
LINK_MODE_STATIC=0
LINK_MODE_SHARED=1

IS_MSVC = 'VisualStudioVersion' in os.environ

COMPILER_NAME = "clang" if not IS_MSVC else 'msvc'
BUILD_TYPE_STRING = ["Release", "Debug"]
LINK_MODE_STRING = ["static", "shared"]
BUILD_FILE_GENERATOR = '-G"Ninja Multi-Config"'

if COMPILER_NAME == "msvc":
    BUILD_FILE_GENERATOR = ""

execution_environ = os.environ


def buildLibrary(linkMode, name, cmakeConfig):
    BUILD_LOCATION = f'{PATH_DEPS_BUILD_DIR}{os.path.sep}build-{COMPILER_NAME}-{LINK_MODE_STRING[linkMode]}{os.path.sep}{name}'
    SRC_LOCATION = f'{PATH_DEPS_REPO}{os.path.sep}{name}'

    # print("SRC_LOCATION %s"%SRC_LOCATION)
    # print("BUILD_LOCATION %s"%BUILD_LOCATION)
    
    SHARED_LIBS = 'Off' if linkMode==LINK_MODE_STATIC else 'On'
    
    
    CMD_CMAKE_CONFIGURE = f'cmake {BUILD_FILE_GENERATOR} -S"{SRC_LOCATION}" -B"{BUILD_LOCATION}" -DBUILD_SHARED_LIBS:BOOL={SHARED_LIBS} '

    if cmakeConfig: CMD_CMAKE_CONFIGURE += cmakeConfig
    if CMDLINE_EXTRA_ARGS: CMD_CMAKE_CONFIGURE += CMDLINE_EXTRA_ARGS
    
    print("%s"%CMD_CMAKE_CONFIGURE)
    if not PRINT_CMDS_ONLY:
      mkdir_p(BUILD_LOCATION)
      ret = subprocess.call(CMD_CMAKE_CONFIGURE, stderr=subprocess.STDOUT, shell=True, env=execution_environ)
      if 0 != ret:
          raise Exception("subprocess call returned %d"%ret)


    for buildType in range(2):
        INSTALL_LOCATION = f'{PATH_DEPS_INSTALL_DIR}{os.path.sep}lib-{COMPILER_NAME}-{BUILD_TYPE_STRING[buildType].lower()}-{LINK_MODE_STRING[linkMode]}{os.path.sep}{name}'
        print("INSTALL_LOCATION %s"%INSTALL_LOCATION)

        CMD_CMAKE_SET_INSTALL_LOCATION = f'cmake "{BUILD_LOCATION}" -DCMAKE_INSTALL_PREFIX:PATH="{INSTALL_LOCATION}" '

        print("%s"%CMD_CMAKE_SET_INSTALL_LOCATION)
        
        if not PRINT_CMDS_ONLY:
          mkdir_p(INSTALL_LOCATION)

          ret = subprocess.call(CMD_CMAKE_SET_INSTALL_LOCATION, stderr=subprocess.STDOUT, shell=True, env=execution_environ)
          if 0 != ret:
              raise Exception("subprocess call returned %d"%ret)
        
        CMD_CMAKE_BUILD_AND_INSTALL = f'cmake --build "{BUILD_LOCATION}" --config {BUILD_TYPE_STRING[buildType]} --target install'
        print("%s"%CMD_CMAKE_BUILD_AND_INSTALL)


        if not PRINT_CMDS_ONLY:
          ret = subprocess.call(CMD_CMAKE_BUILD_AND_INSTALL, stderr=subprocess.STDOUT, shell=True, env=execution_environ)
          if 0 != ret:
            raise Exception("subprocess call returned %d"%ret)
        
        print('\n')




linkMode=LINK_MODE_STATIC

GLFW_ARGS=[
  '',
  'GLFW_BUILD_DOCS:BOOL=OFF',
  'GLFW_BUILD_TESTS:BOOL=OFF',
  'GLFW_BUILD_EXAMPLES:BOOL=OFF'
]
# buildLibrary(linkMode, "glfw" , ' -D'.join(GLFW_ARGS))

SQLITECPP_ARGS=[
  '',
  'SQLITECPP_RUN_CPPCHECK:BOOL=OFF',
  'SQLITECPP_RUN_CPPLINT:BOOL=OFF',
  'SQLITECPP_INTERNAL_SQLITE:BOOL=ON',
  'SQLITECPP_USE_STATIC_RUNTIME:BOOL=OFF',
  'SQLITECPP_USE_STACK_PROTECTION:BOOL=OFF',
]
# buildLibrary(linkMode, "SQLiteCpp" , ' -D'.join(SQLITECPP_ARGS))

SOXR_ARGS=[
  '',
  'BUILD_EXAMPLES:BOOL=OFF',
  'BUILD_TESTS:BOOL=OFF',
  'WITH_OPENMP:BOOL=OFF',
  'BUILD_SHARED_LIBS:BOOL=ON',
 f'CMAKE_RELEASE_POSTFIX="-{COMPILER_NAME}-release"',
 f'CMAKE_DEBUG_POSTFIX="-{COMPILER_NAME}-debug"',
]
buildLibrary(linkMode, "soxr" , ' -D'.join(SOXR_ARGS))

PORTAUDIO_ARGS = [
  '',
 'PA_DLL_LINK_WITH_STATIC_RUNTIME:BOOL=OFF',
 'PA_ENABLE_DEBUG_OUTPUT:BOOL=OFF'
]
if platform.system() == "Windows":
  PORTAUDIO_ARGS.append('PA_USE_ASIO:BOOL=ON')

# buildLibrary(linkMode, "portaudio" , ' -D'.join(PORTAUDIO_ARGS))

# buildLibrary(linkMode, "portmidi", " -DPM_USE_STATIC_RUNTIME=OFF")

# buildLibrary(linkMode, "pybind11", " -DPYBIND11_TEST:BOOL=OFF -DPYBIND11_INSTALL:BOOL=On")

KISSFFT_ARGS = [
  '',
  'KISSFFT_TEST=OFF',
  'KISSFFT_OPENMP=0',
  'KISSFFT_DATATYPE=float',
  'KISSFFT_TOOLS=OFF',
  'KISSFFT_USE_ALLOCA=OFF',
  'KISSFFT_PKGCONFIG=OFF',
  'KISSFFT_STATIC=' + ('ON' if linkMode==LINK_MODE_STATIC else 'OFF')
]

# buildLibrary(linkMode, "kissfft", ' -D'.join(KISSFFT_ARGS))
