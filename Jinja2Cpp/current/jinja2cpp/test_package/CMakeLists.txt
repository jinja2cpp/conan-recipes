cmake_minimum_required(VERSION 2.8.0)
project(Jinja2CppTestPackage)

set(CMAKE_CXX_STANDARD 14)

find_package(jinja2cpp REQUIRED)

add_executable(jinja2cpp-test-package main.cpp)
target_link_libraries(jinja2cpp-test-package PRIVATE jinja2cpp::jinja2cpp)
