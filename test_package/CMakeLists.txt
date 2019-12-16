project(PackageTest C)
cmake_minimum_required(VERSION 3.14)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

# Position-independent code helps make dladdr() return correct symbol information.
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Executables are built with relative RPATH support, so the dynamic libs are
# found either together with the executable, or in the adjacent lib directory.
# This aligns with the Filesystem Hierarchy Standard.
# Necessary so that if building with dynamic libraries, the tests work.
# See: https://docs.conan.io/en/latest/howtos/manage_shared_libraries/rpaths.html#different-approaches
# See: https://gitlab.kitware.com/cmake/community/wikis/doc/cmake/RPATH-handling
# See: http://www.pathname.com/fhs/pub/fhs-2.3.html
conan_basic_setup(KEEP_RPATHS)
if (APPLE)
  set(CMAKE_INSTALL_RPATH "@executable_path;@executable_path/../lib")
else()
  set(CMAKE_INSTALL_RPATH "$ORIGIN;$ORIGIN/../lib")
endif()
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)

add_executable(test_qr_code_generator_package test_qr_code_generator_package.c)
target_link_libraries(test_qr_code_generator_package ${CONAN_LIBS})

# On platforms that have a dynamic load library (like Linux), include it.
find_library(LIBDL dl)
if(LIBDL)
  target_link_libraries(test_qr_code_generator_package ${LIBDL})
endif()
