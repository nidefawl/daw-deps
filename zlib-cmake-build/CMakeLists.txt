cmake_minimum_required(VERSION 3.21)
project(zlib LANGUAGES C VERSION 1.2.13)
include(CheckTypeSize)
include(CheckFunctionExists)
include(CheckIncludeFile)
include(CheckCSourceCompiles)

check_include_file(sys/types.h HAVE_SYS_TYPES_H)
check_include_file(stdint.h    HAVE_STDINT_H)
check_include_file(stddef.h    HAVE_STDDEF_H)

#
# Check to see if we have large file support
#
set(CMAKE_REQUIRED_DEFINITIONS -D_LARGEFILE64_SOURCE=1)
# We add these other definitions here because CheckTypeSize.cmake
# in CMake 2.4.x does not automatically do so and we want
# compatibility with CMake 2.4.x.
if(HAVE_SYS_TYPES_H)
    list(APPEND CMAKE_REQUIRED_DEFINITIONS -DHAVE_SYS_TYPES_H)
endif()
if(HAVE_STDINT_H)
    list(APPEND CMAKE_REQUIRED_DEFINITIONS -DHAVE_STDINT_H)
endif()
if(HAVE_STDDEF_H)
    list(APPEND CMAKE_REQUIRED_DEFINITIONS -DHAVE_STDDEF_H)
endif()
check_type_size(off64_t OFF64_T)
if(HAVE_OFF64_T)
   add_definitions(-D_LARGEFILE64_SOURCE=1)
endif()
set(CMAKE_REQUIRED_DEFINITIONS) # clear variable

#
# Check for fseeko
#
check_function_exists(fseeko HAVE_FSEEKO)
if(NOT HAVE_FSEEKO)
    add_definitions(-DNO_FSEEKO)
endif()

#
# Check for unistd.h
#
check_include_file(unistd.h Z_HAVE_UNISTD_H)
set(ZLIB_SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../zlib")

if(NOT ZLIB_SRC_DIR STREQUAL CMAKE_CURRENT_BINARY_DIR)
    # If we're doing an out of source build and the user has a zconf.h
    # in their source tree...
    if(EXISTS ${ZLIB_SRC_DIR}/zconf.h)
        message(STATUS "Renaming")
        message(STATUS "    ${ZLIB_SRC_DIR}/zconf.h")
        message(STATUS "to 'zconf.h.included' because this file is included with zlib")
        message(STATUS "but CMake generates it automatically in the build directory.")
        file(RENAME ${ZLIB_SRC_DIR}/zconf.h ${ZLIB_SRC_DIR}/zconf.h.included)
  endif()
endif()

configure_file(	${ZLIB_SRC_DIR}/zconf.h.cmakein
		${CMAKE_CURRENT_BINARY_DIR}/dist/zconf.h @ONLY)
# copy zlib.h to dist/
configure_file(	${ZLIB_SRC_DIR}/zlib.h
        ${CMAKE_CURRENT_BINARY_DIR}/dist/zlib.h COPYONLY)

#============================================================================
# zlib
#============================================================================

set(ZLIB_PRIVATE_HDRS
    crc32.h
    deflate.h
    gzguts.h
    inffast.h
    inffixed.h
    inflate.h
    inftrees.h
    trees.h
    zutil.h
)
set(ZLIB_SRCS
    adler32.c
    compress.c
    crc32.c
    deflate.c
    gzclose.c
    gzlib.c
    gzread.c
    gzwrite.c
    inflate.c
    infback.c
    inftrees.c
    inffast.c
    trees.c
    uncompr.c
    zutil.c
)

list(TRANSFORM ZLIB_PUBLIC_HDRS PREPEND "${ZLIB_SRC_DIR}/")
list(TRANSFORM ZLIB_PRIVATE_HDRS PREPEND "${ZLIB_SRC_DIR}/")
list(TRANSFORM ZLIB_SRCS PREPEND "${ZLIB_SRC_DIR}/")
set(ZLIB_PUBLIC_HDRS
    ${CMAKE_CURRENT_BINARY_DIR}/dist/zconf.h
    ${CMAKE_CURRENT_BINARY_DIR}/dist/zlib.h
)

add_library(zlib STATIC)
target_sources(zlib PRIVATE ${ZLIB_SRCS} ${ZLIB_PRIVATE_HDRS})
target_sources(zlib PUBLIC ${ZLIB_PUBLIC_HDRS})
set_target_properties(zlib PROPERTIES
    UNITY_BUILD OFF
    POSITION_INDEPENDENT_CODE ON
    PUBLIC_HEADER "${ZLIB_PUBLIC_HDRS}"
)
target_include_directories(zlib PRIVATE ${ZLIB_SRC_DIR})
target_include_directories(zlib PUBLIC ${CMAKE_CURRENT_BINARY_DIR}/dist)
if(MSVC)
    target_compile_definitions(zlib PRIVATE -D_CRT_SECURE_NO_DEPRECATE -D_CRT_NONSTDC_NO_DEPRECATE)
else()
    target_compile_options(zlib PRIVATE -Wno-deprecated-non-prototype)
endif()

if(HAVE_OFF64_T)
    target_compile_definitions(zlib PRIVATE -D_LARGEFILE64_SOURCE=1)
endif()
if(NOT HAVE_FSEEKO)
    target_compile_definitions(zlib PRIVATE -DNO_FSEEKO)
endif()
