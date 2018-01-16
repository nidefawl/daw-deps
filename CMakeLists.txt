cmake_minimum_required(VERSION 3.3)
project(DAW-dependencies)
include(ExternalProject)

set(GLFW_BUILD_PATH ${CMAKE_BINARY_DIR}/tmp/glfw)
set(GLFW_OUTPUT_PATH ${CMAKE_BINARY_DIR}/lib/glfw)
set(GLFW_ROOT ${CMAKE_SOURCE_DIR}/glfw)
ExternalProject_Add(glfw
                    PREFIX ${GLFW_BUILD_PATH}
                    SOURCE_DIR ${GLFW_ROOT}
                    INSTALL_DIR ${GLFW_OUTPUT_PATH}
                    CMAKE_CACHE_ARGS -DGLFW_BUILD_DOCS:BOOL=OFF -DGLFW_BUILD_TESTS:BOOL=OFF -DGLFW_BUILD_EXAMPLES:BOOL=OFF -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>)

set(SQLiteCPP_BUILD_PATH ${CMAKE_BINARY_DIR}/tmp/sqlitecpp)
set(SQLiteCPP_OUTPUT_PATH ${CMAKE_BINARY_DIR}/lib/sqlitecpp)
set(SQLiteCPP_ROOT ${CMAKE_SOURCE_DIR}/sqlitecpp)
ExternalProject_Add(sqlitecpp
                    PREFIX ${SQLiteCPP_BUILD_PATH}
                    SOURCE_DIR ${SQLiteCPP_ROOT}
                    INSTALL_DIR ${SQLiteCPP_OUTPUT_PATH}
                    CMAKE_CACHE_ARGS -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>)

