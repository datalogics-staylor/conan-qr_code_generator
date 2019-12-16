cmake_minimum_required(VERSION 3.15 FATAL_ERROR)
project(qr_code_generator C)
enable_testing()

if(EXISTS ${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo_multi.cmake)
  include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo_multi.cmake)
else()
  include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
endif()

# Executables are built with relative RPATH support, so the dynamic libs are
# found either together with the executable, or in the adjacent lib directory.
# This aligns with the Filesystem Hierarchy Standard.
# Necessary so that if building with dynamic libraries, the tests work.
# See: https://docs.conan.io/en/latest/howtos/manage_shared_libraries/rpaths.html#different-approaches
# See: https://gitlab.kitware.com/cmake/community/wikis/doc/cmake/RPATH-handling
# See: http://www.pathname.com/fhs/pub/fhs-2.3.html
conan_basic_setup(TARGETS KEEP_RPATHS)
if (APPLE)
  set(CMAKE_INSTALL_RPATH "@executable_path;@executable_path/../lib")
else()
  set(CMAKE_INSTALL_RPATH "$ORIGIN;$ORIGIN/../lib")
endif()
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)

# We include some of the static libraries in dynamic libraries, so always make
# position independent code.
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(QR_CODE_C_FOLDER ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/c)
add_library(qr_code_generator ${QR_CODE_C_FOLDER}/qrcodegen.c)
target_include_directories(qr_code_generator PRIVATE ${QR_CODE_C_FOLDER})

# It comes with a test, so let's test it!
# Needs the qrcodegen.c file compiled with QRCODEGEN_TEST
add_executable(qrcodegen-test
  ${QR_CODE_C_FOLDER}/qrcodegen-test.c
  ${QR_CODE_C_FOLDER}/qrcodegen.c)
target_include_directories(qrcodegen-test PRIVATE ${QR_CODE_C_FOLDER})
target_compile_definitions(qrcodegen-test PRIVATE QRCODEGEN_TEST)
target_link_libraries(qrcodegen-test PRIVATE qr_code_generator)
add_test(NAME qrcodegen-test COMMAND qrcodegen-test)

install(TARGETS qr_code_generator
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib)

install(FILES ${QR_CODE_C_FOLDER}/qrcodegen.h DESTINATION include)
