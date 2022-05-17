#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "string_extract.hpp"

namespace py = pybind11;

PYBIND11_PLUGIN(binary2strings)
{
    py::module m("binary2strings");
    m.def("extract_all_strings", [](py::bytes &buffer, int min_chars) {
        py::buffer_info info(py::buffer(buffer).request());

        if(info.ndim != 1)
            throw std::runtime_error("Only 1-dimensional arrays are supported");

        const unsigned char *data = reinterpret_cast<const unsigned char *>(info.ptr);
        return extract_all_strings(data, info.shape[0], min_chars);
    });

    m.def("extract_string", [](py::bytes &buffer, int min_chars) {
        py::buffer_info info(py::buffer(buffer).request());

        if(info.ndim != 1)
            throw std::runtime_error("Only 1-dimensional arrays are supported");

        const unsigned char *data = reinterpret_cast<const unsigned char *>(info.ptr);
        return try_extract_string_tuple(data, info.shape[0], 0, min_chars);
    });
    
    return m.ptr();
}