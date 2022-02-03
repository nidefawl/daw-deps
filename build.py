import os
import subprocess
import errno    
import sys
import platform

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

script_path = os.path.dirname(os.path.abspath( __file__ ))
print("script path %s"%script_path)
sysargs = sys.argv[:]

if len(sysargs) < 3:
	sysargs = [__file__, "./build", "./install"]
	#raise ValueError("python daw-deps/build.py <build-directory> <install-path>")
extraArgs = ""
if len(sysargs) > 3:
    extraArgs=" "+(" ".join(sysargs[3:]))+" "



PATH_DEPS_REPO=script_path
PATH_DEPS_BUILD_DIR = os.path.abspath(sysargs[1])
PATH_DEPS_INSTALL_DIR = os.path.abspath(sysargs[2])
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

# # build path to vcvarsall.bat file
# vcvarsall = os.path.join(vspath, "VC", "Auxiliary", "Build", "vcvarsall.bat")

# # vcvarsall.bat changes the current directory to the one specified
# # by the environment variable %VSCMD_START_DIR%
my_env = os.environ
# my_env["VSCMD_START_DIR"] = build_dir

# set up the environment and then call cmake with Ninja generator


def buildLibrary(linkMode, name, extraArgs, optionalCmakeArgs=""):
    BUILD_LOCATION = f'{PATH_DEPS_BUILD_DIR}{os.path.sep}build-{COMPILER_NAME}-{LINK_MODE_STRING[linkMode]}{os.path.sep}{name}'
    SRC_LOCATION = f'{PATH_DEPS_REPO}{os.path.sep}{name}'

    # print("SRC_LOCATION %s"%SRC_LOCATION)
    # print("BUILD_LOCATION %s"%BUILD_LOCATION)
    
    SHARED_LIBS = 'Off' if linkMode==LINK_MODE_STATIC else 'On'
    
    CMD_CMAKE_CONFIGURE = f'cmake {BUILD_FILE_GENERATOR} -S"{SRC_LOCATION}" -B"{BUILD_LOCATION}" -DBUILD_SHARED_LIBS:BOOL={SHARED_LIBS} {extraArgs} {optionalCmakeArgs}'
    
    mkdir_p(BUILD_LOCATION)
    
    print("%s"%CMD_CMAKE_CONFIGURE)
    ret = subprocess.call(CMD_CMAKE_CONFIGURE, stderr=subprocess.STDOUT, shell=True, env=my_env)
    if 0 != ret:
        raise Exception("subprocess call returned %d"%ret)
        
        
    for buildType in range(2):
        INSTALL_LOCATION = f'{PATH_DEPS_INSTALL_DIR}{os.path.sep}lib-{COMPILER_NAME}-{BUILD_TYPE_STRING[buildType].lower()}-{LINK_MODE_STRING[linkMode]}{os.path.sep}{name}'
        print("INSTALL_LOCATION %s"%INSTALL_LOCATION)
    
        mkdir_p(INSTALL_LOCATION)
        
        
        CMD_CMAKE_SET_INSTALL_LOCATION = f'cmake -DCMAKE_INSTALL_PREFIX:PATH="{INSTALL_LOCATION}" "{BUILD_LOCATION}"'
        # print("%s"%CMD_CMAKE_SET_INSTALL_LOCATION)
        ret = subprocess.call(CMD_CMAKE_SET_INSTALL_LOCATION, stderr=subprocess.STDOUT, shell=True, env=my_env)
        if 0 != ret:
            raise Exception("subprocess call returned %d"%ret)
        
        CMD_CMAKE_BUILD_AND_INSTALL = f'cmake --build "{BUILD_LOCATION}" --config {BUILD_TYPE_STRING[buildType]} --target install'
        
        # print("%s"%CMD_CMAKE_BUILD_AND_INSTALL)
        ret = subprocess.call(CMD_CMAKE_BUILD_AND_INSTALL, stderr=subprocess.STDOUT, shell=True, env=my_env)
        if 0 != ret:
            raise Exception("subprocess call returned %d"%ret)
    



linkMode=LINK_MODE_STATIC
buildLibrary(linkMode, "glfw" , extraArgs=extraArgs, optionalCmakeArgs=" -DGLFW_BUILD_DOCS:BOOL=OFF -DGLFW_BUILD_TESTS:BOOL=OFF -DGLFW_BUILD_EXAMPLES:BOOL=OFF")
buildLibrary(linkMode, "SQLiteCpp" , extraArgs=extraArgs, optionalCmakeArgs=" -DSQLITECPP_RUN_CPPCHECK:BOOL=OFF -DSQLITECPP_RUN_CPPLINT:BOOL=OFF -DSQLITECPP_INTERNAL_SQLITE:BOOL=ON ")
buildLibrary(linkMode, "soxr" , extraArgs=extraArgs, optionalCmakeArgs=" -DBUILD_EXAMPLES:BOOL=OFF -DBUILD_TESTS:BOOL=OFF -DWITH_OPENMP:BOOL=OFF")
optionalCmakeArgsPortAudio=" -DPA_DLL_LINK_WITH_STATIC_RUNTIME:BOOL=OFF -DPA_ENABLE_DEBUG_OUTPUT:BOOL=Off"
if (linkMode == LINK_MODE_STATIC):
    optionalCmakeArgsPortAudio += " -DPA_BUILD_SHARED:BOOL=Off"
    optionalCmakeArgsPortAudio += " -DPA_BUILD_STATIC:BOOL=On"
else:
    optionalCmakeArgsPortAudio += " -DPA_BUILD_SHARED:BOOL=On"
    optionalCmakeArgsPortAudio += " -DPA_BUILD_STATIC:BOOL=Off"

buildLibrary(linkMode, "portaudio" , extraArgs=extraArgs, optionalCmakeArgs=optionalCmakeArgsPortAudio)
buildLibrary(linkMode, "portmidi", extraArgs=extraArgs)
buildLibrary(linkMode, "pybind11", extraArgs=extraArgs, optionalCmakeArgs=" -DPYBIND11_TEST:BOOL=Off -DPYBIND11_INSTALL:BOOL=On")
    