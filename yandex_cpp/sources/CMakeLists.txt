cmake_minimum_required(VERSION 2.8)
project(yandex_cpp)

set(CXX)

if (${CMAKE_BUILD_TYPE} MATCHES DEBUG)
    MESSAGE("Building DEBUG version: -O0 is used")
    add_compile_options(-O0 -m64 -std=c++0x -fopenmp -ggdb3)
else()
    MESSAGE("Building RELEASE version: -O3 is used")
    add_compile_options(-Ofast -m64 -std=c++0x -fopenmp)
endif()


include_directories()
link_directories()

file(GLOB sources "*.cpp")
file(GLOB sourceheaders "*.hpp")
file(GLOB headers "*.h")

add_library(yandex STATIC ${sources} ${headers} ${sourceheaders})
add_executable(yandex-app main.cpp)
target_link_libraries(yandex-app LINK_PUBLIC gomp yandex)

