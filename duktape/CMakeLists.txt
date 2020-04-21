cmake_minimum_required(VERSION 3.0)

project(DUKTAPE C)

set(CMAKE_LEGACY_CYGWIN_WIN32 OFF)

if (POLICY CMP0054)
    cmake_policy(SET CMP0054 NEW)
endif()

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

option(BUILD_SHARED_LIBS "Build shared libraries" OFF)
option(DUKTAPE_INSTALL "Generate installation target" ON)


if (MSVC)
    option(USE_MSVC_RUNTIME_LIBRARY_DLL "Use MSVC runtime library DLL" ON)
endif()

if (BUILD_SHARED_LIBS)
    set(DUKTAPE_BUILD_DLL 1)
endif()

set(DUKTAPE_LIB_NAME duktape)




#--------------------------------------------------------------------
# Set compiler specific flags
#--------------------------------------------------------------------
if (MSVC)

    if (NOT USE_MSVC_RUNTIME_LIBRARY_DLL)
        foreach (flag CMAKE_C_FLAGS
                      CMAKE_C_FLAGS_DEBUG
                      CMAKE_C_FLAGS_RELEASE
                      CMAKE_C_FLAGS_MINSIZEREL
                      CMAKE_C_FLAGS_RELWITHDEBINFO)

            if (${flag} MATCHES "/MD")
                string(REGEX REPLACE "/MD" "/MT" ${flag} "${${flag}}")
            endif()
            if (${flag} MATCHES "/MDd")
                string(REGEX REPLACE "/MDd" "/MTd" ${flag} "${${flag}}")
            endif()

        endforeach()
    endif()
endif()

if (MINGW)
    # Workaround for legacy MinGW not providing XInput and DirectInput
    include(CheckIncludeFile)


    # Enable link-time exploit mitigation features enabled by default on MSVC
    include(CheckCCompilerFlag)

endif()



set(duktape_HEADERS 
	"duktape/src/duktape.h"
	"duktape/src/duk_config.h"
	"duktape/extras/logging/duk_logging.h"
	"duktape/extras/module-duktape/duk_module_duktape.h"
	"duktape/extras/print-alert/duk_print_alert.h"
	"duktape/extras/console/duk_console.h"
)
set(duktape_SOURCES 
	"duktape/src/duktape.c" 
	"duktape/extras/logging/duk_logging.c"
	"duktape/extras/module-duktape/duk_module_duktape.c"
	"duktape/extras/print-alert/duk_print_alert.c"
	"duktape/extras/console/duk_console.c"
)
if (APPLE)
    # For some reason, CMake doesn't know about .m
    set_source_files_properties(${duktape_SOURCES} PROPERTIES LANGUAGE C)
endif()


add_library(duktape ${duktape_SOURCES} ${duktape_HEADERS})
set_target_properties(duktape PROPERTIES
                      OUTPUT_NAME ${DUKTAPE_LIB_NAME}
                      VERSION 1
                      SOVERSION 2
                      POSITION_INDEPENDENT_CODE ON
                      FOLDER "DUKTAPE")

#target_compile_definitions(duktape PRIVATE _GLFW_USE_CONFIG_H)
target_include_directories(duktape PUBLIC
                           "duktape/src")
target_include_directories(duktape PRIVATE
                           "duktape/src"
                           "duktape/extras/logging"
                           "duktape/src")


if (BUILD_SHARED_LIBS)
    if (WIN32)
        if (MINGW)
            # Remove the lib prefix on the DLL (but not the import library)
            set_target_properties(duktape PROPERTIES PREFIX "")

            # Add a suffix to the import library to avoid naming conflicts
            set_target_properties(duktape PROPERTIES IMPORT_SUFFIX "dll.a")
        else()
            # Add a suffix to the import library to avoid naming conflicts
            set_target_properties(duktape PROPERTIES IMPORT_SUFFIX "dll.lib")
        endif()
    elseif (APPLE)
        # Add -fno-common to work around a bug in Apple's GCC
        target_compile_options(duktape PRIVATE "-fno-common")

        set_target_properties(duktape PROPERTIES
                              INSTALL_NAME_DIR "${CMAKE_INSTALL_LIBDIR}")
    elseif (UNIX)
        # Hide symbols not explicitly tagged for export from the shared library
        target_compile_options(duktape PRIVATE "-fvisibility=hidden")
    endif()

    target_compile_definitions(duktape INTERFACE GLFW_DLL)
    target_link_libraries(duktape PRIVATE ${glfw_LIBRARIES})
else()
    target_link_libraries(duktape INTERFACE ${glfw_LIBRARIES})
endif()

if (MSVC)
    target_compile_definitions(duktape PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()



#--------------------------------------------------------------------
# Install files other than the library
# The library is installed by src/CMakeLists.txt
#--------------------------------------------------------------------
if (DUKTAPE_INSTALL)
	INSTALL(FILES ${duktape_HEADERS} DESTINATION include)
    
	INSTALL(TARGETS duktape
		RUNTIME DESTINATION bin
		LIBRARY DESTINATION lib
		ARCHIVE DESTINATION lib)
endif()

