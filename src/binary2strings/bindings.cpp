#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdint.h>
#include "string_extract.hpp"
#include "crc64.hpp"

namespace py = pybind11;

PYBIND11_MODULE(binary2strings, m)
{
    m.doc() = "Python module for extracting strings from binary data input.";

    m.def("extract_all_strings", [](py::bytes &buffer, int min_chars, bool only_uncommon) {
        py::buffer_info info(py::buffer(buffer).request());

        if(info.ndim != 1)
            throw std::runtime_error("Only 1-dimensional arrays are supported");

        const unsigned char *data = reinterpret_cast<const unsigned char *>(info.ptr);
        
        return extract_all_strings(data, info.shape[0], min_chars, only_uncommon);
    },"Extract all strings at least min_chars or longer from the input bytes string. Returns an array of tuples.",
    py::arg("buffer"),
    py::arg("min_chars")=4,
    py::arg("only_uncommon")=false);

    m.def("extract_string", [](py::bytes &buffer, int min_chars, bool only_uncommon) {
        py::buffer_info info(py::buffer(buffer).request());

        if(info.ndim != 1)
            throw std::runtime_error("Only 1-dimensional arrays are supported");

        const unsigned char *data = reinterpret_cast<const unsigned char *>(info.ptr);
        return try_extract_string_tuple(data, info.shape[0], 0, min_chars, only_uncommon);
    },"Tries to extract a single string at least min_chars or longer from the start of the input bytes string. Returns a single of tuple. If it fails to parse a string from the start of the buffer it will return a tuple containing a zero-length string.",
    py::arg("buffer"),
    py::arg("min_chars")=4,
    py::arg("only_uncommon")=false);

    m.def("_crc64", [](uint64_t crc, py::bytes &buffer) {
        py::buffer_info info(py::buffer(buffer).request());

        if(info.ndim != 1)
            throw std::runtime_error("Only 1-dimensional arrays are supported");

        const unsigned char *data = reinterpret_cast<const unsigned char *>(info.ptr);

        return crc64(crc, data, info.shape[0]);
    },"Internal function to calculate crc64 of a bytes string.",py::arg("crc"),py::arg("buffer"));
}