from conans import ConanFile, CMake, tools
import os
import shutil
import textwrap
import re
from conans.errors import ConanInvalidConfiguration


class Jinja2cppConan(ConanFile):
    name = "jinja2cpp"
    version = "1.0.0"
    license = "MIT"
    url = "https://jinja2cpp.dev/"
    description = "Jinja2 C++ (and for C++) almost full-conformance template engine implementation"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
    }
    default_options = {'shared': False}
    generators = "cmake_find_package"
    requires = (
        "variant-lite/[1.2.1]@nonstd-lite/stable",
        "expected-lite/[0.3.0]@nonstd-lite/stable",
        "optional-lite/[3.2.0]@nonstd-lite/stable",
        "boost/1.69.0@conan/stable",
        "string-view-lite/[~=1]@nonstd-lite/testing",
        "fmt/[>=5.3]@bincrafters/stable"
    )

    def configure(self):
        cppstd = self.settings.get_safe("compiler.cppstd")
        if cppstd:
            cppstd_pattern = re.compile(r'^(gnu)?(?P<cppstd>\d+)$')
            m = cppstd_pattern.match(cppstd)
            cppstd_profile = int(m.group("cppstd"))
            if cppstd_profile < 14:
                raise ConanInvalidConfiguration("Minimum C++ Standard required is 14 (provided '{}')".format(cppstd))

    def source(self):
        git = tools.Git(folder=self.name)
        git.clone("https://github.com/jinja2cpp/Jinja2Cpp.git", "release_1_0_prep")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["JINJA2CPP_BUILD_TESTS"] = False
        cmake.definitions["JINJA2CPP_DEPS_MODE"] = "conan-build"
        compiler = self.settings.get_safe("compiler")
        if compiler == 'Visual Studio':
            runtime = self.settings.get_safe("compiler.runtime")
            cmake.definitions["JINJA2CPP_MSVC_RUNTIME_TYPE"] = '/' + runtime
            
        cmake.configure(source_folder=self.name)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join(self.name, "include"))
        self.copy("*.hpp", dst="include", src=os.path.join(self.name, "include"))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["jinja2cpp"]

