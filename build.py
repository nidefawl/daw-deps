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
if len(sys.argv) < 3:
        raise ValueError("python daw-deps/build.py <build-directory> <install-path>")
extraArgs = ""
if len(sys.argv) > 3:
    extraArgs=" "+(" ".join(sys.argv[3:]))+" "



PATH_DEPS_REPO=script_path
PATH_DEPS_BUILD_DIR=sys.argv[1]
PATH_DEPS_INSTALL_DIR=sys.argv[2]
PATH_DEPS_BUILD_DIR = os.path.abspath(sys.argv[1])
PATH_DEPS_INSTALL_DIR = os.path.abspath(sys.argv[2])
print("PATH_DEPS_BUILD_DIR %s"%PATH_DEPS_BUILD_DIR)
print("PATH_DEPS_INSTALL_DIR %s"%PATH_DEPS_INSTALL_DIR)


BUILD_TYPE_RELEASE=0
BUILD_TYPE_DEBUG=1
LINK_MODE_STATIC=0
LINK_MODE_SHARED=1

CMAKE_CXX_COMPILER_ID = "clang"
BUILD_TYPE_STRING = ["Release", "Debug"]
LINK_MODE_STRING = ["static", "shared"]




# # build path to vcvarsall.bat file
# vcvarsall = os.path.join(vspath, "VC", "Auxiliary", "Build", "vcvarsall.bat")

# # vcvarsall.bat changes the current directory to the one specified
# # by the environment variable %VSCMD_START_DIR%
my_env = os.environ
# my_env["VSCMD_START_DIR"] = build_dir

# set up the environment and then call cmake with Ninja generator


def buildLibrary(buildType, linkMode, name, extraArgs, optionalCmakeArgs=""):
    BUILD_PATH_SUFFIX = CMAKE_CXX_COMPILER_ID + "-" + BUILD_TYPE_STRING[buildType] + "-" + LINK_MODE_STRING[linkMode]
    BUILD_PATH_SUFFIX = BUILD_PATH_SUFFIX.lower()
    DEPS_BUILD_FOLDER_LIBS = "lib-" + BUILD_PATH_SUFFIX
    DEPS_BUILD_FOLDER_TMP = "tmp-" + BUILD_PATH_SUFFIX
    PATH_DEPS_BUILD_FOLDER_LIBS = PATH_DEPS_INSTALL_DIR + "/" + DEPS_BUILD_FOLDER_LIBS
    PATH_DEPS_BUILD_FOLDER_TMP = PATH_DEPS_BUILD_DIR + "/" + DEPS_BUILD_FOLDER_TMP

    pathSrc = PATH_DEPS_REPO + "/" + name
    pathBuild = PATH_DEPS_BUILD_FOLDER_TMP + "/" + name
    pathInstall = PATH_DEPS_BUILD_FOLDER_LIBS + "/" + name
    print("pathSrc %s"%pathSrc)
    print("pathBuild %s"%pathBuild)
    print("pathInstall %s"%pathInstall)
    makeFileType = " "
    print("%s"%platform.system())
    if platform.system() == "Windows":
        makeFileType = '-G "Ninja" '
    cmd = 'cd "'+pathBuild+'" && cmake '+makeFileType + pathSrc
    cmdInstall = 'cd "'+pathBuild+'" && cmake --build . --target install'
    if (buildType == BUILD_TYPE_DEBUG):
      cmd += " -DCMAKE_BUILD_TYPE:String=Debug"
      cmdInstall += " --config Debug"
    else:
      cmd += " -DCMAKE_BUILD_TYPE:String=Release"
      cmdInstall += " --config Release"
    if (linkMode == LINK_MODE_STATIC):
      cmd += " -DBUILD_SHARED_LIBS:BOOL=Off"
    else:
      cmd += " -DBUILD_SHARED_LIBS:BOOL=On"
    if len(extraArgs) > 0:
        cmd += extraArgs
    cmd += " -DCMAKE_INSTALL_PREFIX="+pathInstall
      
    cmd += optionalCmakeArgs

    mkdir_p(pathBuild)
    print("%s"%cmd)
    ret = subprocess.call(cmd, stderr=subprocess.STDOUT, shell=True, env=my_env)
    if 0 != ret:
        raise Exception("subprocess call returned %d"%ret)
    mkdir_p(pathInstall)
    print("%s"%cmdInstall)
    ret = subprocess.call(cmdInstall, stderr=subprocess.STDOUT, shell=True, env=my_env)
    if 0 != ret:
        raise Exception("subprocess call returned %d"%ret)
    



for buildType in range(2):
    linkMode=LINK_MODE_STATIC
    buildLibrary(buildType, linkMode, "glfw" , extraArgs=extraArgs, optionalCmakeArgs=" -DGLFW_BUILD_DOCS:BOOL=OFF -DGLFW_BUILD_TESTS:BOOL=OFF -DGLFW_BUILD_EXAMPLES:BOOL=OFF")
    buildLibrary(buildType, linkMode, "SQLiteCpp" , extraArgs=extraArgs, optionalCmakeArgs=" -DSQLITECPP_RUN_CPPCHECK:BOOL=OFF -DSQLITECPP_RUN_CPPLINT:BOOL=OFF -DSQLITECPP_INTERNAL_SQLITE:BOOL=ON ")
    buildLibrary(buildType, linkMode, "soxr" , extraArgs=extraArgs, optionalCmakeArgs=" -DBUILD_EXAMPLES:BOOL=OFF -DBUILD_TESTS:BOOL=ON -DWITH_OPENMP:BOOL=OFF -DBUILD_SHARED_LIBS:BOOL=ON")
    optionalCmakeArgsPortAudio=" -DPA_DLL_LINK_WITH_STATIC_RUNTIME:BOOL=OFF -DPA_ENABLE_DEBUG_OUTPUT:BOOL=Off"
    if (linkMode == LINK_MODE_STATIC):
        optionalCmakeArgsPortAudio += " -DPA_BUILD_SHARED:BOOL=Off"
        optionalCmakeArgsPortAudio += " -DPA_BUILD_STATIC:BOOL=On"
    else:
        optionalCmakeArgsPortAudio += " -DPA_BUILD_SHARED:BOOL=On"
        optionalCmakeArgsPortAudio += " -DPA_BUILD_STATIC:BOOL=Off"

    buildLibrary(buildType, linkMode, "portaudio" , extraArgs=extraArgs, optionalCmakeArgs=optionalCmakeArgsPortAudio)
    buildLibrary(buildType, linkMode, "portmidi", extraArgs=extraArgs)
    buildLibrary(buildType, linkMode, "pybind11", extraArgs=extraArgs, optionalCmakeArgs=" -DPYBIND11_TEST:BOOL=Off -DPYBIND11_INSTALL:BOOL=On")
    buildLibrary(buildType, linkMode, "duktape", extraArgs=extraArgs)
    