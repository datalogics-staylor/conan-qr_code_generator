import os
from conans import ConanFile, CMake, tools


class QrcodegeneratorConan(ConanFile):
    name = "qr_code_generator"
    license = "MIT"
    url = "https://github.com/nayuki/QR-Code-generator"
    description = "This project aims to provide the best and clearest QR Code generator library."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [False],
               'verbose': [False, True]}
    default_options = {"shared": False,
                       'verbose': False}
    generators = "cmake"
    exports_sources = 'CMakeLists.txt'

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        url = self.conan_data["sources"][self.version]["url"]
        archive_name = os.path.basename(os.path.dirname(os.path.dirname(url))) + '-' + self.version
        os.rename(archive_name, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self,
                      # You can specify the following verbosity levels: q[uiet], m[inimal], n[ormal], d[etailed], and diag[nostic].
                      msbuild_verbosity="normal" if self.options.verbose else "minimal")

        cmake.definitions['CMAKE_VERBOSE_MAKEFILE'] = str(self.options.verbose).upper()
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        cmake.test()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

    def package_id(self):
        # Verbosity doesn't affect the package ID
        del self.info.options.verbose

    def configure(self):
        del self.settings.compiler.libcxx
