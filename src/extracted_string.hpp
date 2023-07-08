// Class for extracted strings
#pragma once
#include <string>
#define _SILENCE_ALL_CXX17_DEPRECATION_WARNINGS
#include <codecvt>
#include "string_model.hpp"
#include <unordered_set>
#include <cmath>
#include <locale>

using namespace std;

enum STRING_TYPE
{
	TYPE_UNDETERMINED,
	TYPE_UTF8,
	TYPE_WIDE_STRING
};



class extracted_string
{
private:
	STRING_TYPE m_type;
	std::string m_string; // Supports Utf8
	size_t m_size_in_bytes;
	size_t m_offset_start;
	size_t m_offset_end;

public:
	extracted_string();
	extracted_string(const char* string, size_t size_in_bytes, STRING_TYPE type, size_t offset_start, size_t offset_end);
	extracted_string(const char16_t* string, size_t size_in_bytes, STRING_TYPE type, size_t offset_start, size_t offset_end);

	float get_proba_interesting();
	size_t get_size_in_bytes();
	string get_string();
	STRING_TYPE get_type();
	string get_type_string();
	size_t get_offset_start();
	size_t get_offset_end();

	bool is_interesting();

	~extracted_string();
};
