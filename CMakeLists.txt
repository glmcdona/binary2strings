cmake_minimum_required(VERSION 2.8.12)
project(binary2strings)
# Set source directory
set(SOURCE_DIR "src/binary2strings")
# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})
set(SOURCES "${SOURCE_DIR}/string_extract.hpp" "${SOURCE_DIR}/crc64.hpp")
# Generate Python module
add_subdirectory(lib/pybind11)
pybind11_add_module(binary2strings ${SOURCES} "${SOURCE_DIR}/bindings.cpp")