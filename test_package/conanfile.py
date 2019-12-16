import os

from conans import ConanFile, CMake, tools


class QrcodegeneratorTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {'verbose': [False, True]}
    default_options = {'verbose': False}

    def build(self):
        cmake = CMake(self,
                      # You can specify the following verbosity levels: q[uiet], m[inimal], n[ormal], d[etailed], and diag[nostic].
                      msbuild_verbosity="normal" if self.options.verbose else "minimal")

        cmake.definitions['CMAKE_VERBOSE_MAKEFILE'] = str(self.options.verbose).upper()
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run(".%stest_qr_code_generator_package" % os.sep)

    def package_id(self):
        # Verbosity doesn't affect the package ID
        del self.info.options.verbose

    def configure(self):
        del self.settings.compiler.libcxx
