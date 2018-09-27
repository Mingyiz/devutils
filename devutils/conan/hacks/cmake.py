#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import shutil
import platform
from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools

from conans.util.files import mkdir, get_abs_path
from conans.client import defs_to_string, join_arguments
from conans.tools import cpu_count, args_to_string

def _configure(self, args=None, defs=None, source_dir=None, build_dir=None,
            source_folder=None, build_folder=None, cache_build_folder=None,
            pkg_config_paths=None):

    # TODO: Deprecate source_dir and build_dir in favor of xxx_folder
    if not self._conanfile.should_configure:
        return
    args = args or []
    defs = defs or {}
    source_dir, self.build_dir = self._get_dirs(source_folder, build_folder,
                                                source_dir, build_dir,
                                                cache_build_folder)
    mkdir(self.build_dir)
    arg_list = join_arguments([
        self.command_line,
        args_to_string(args),
        defs_to_string(defs),
        args_to_string([source_dir])
    ])

    if pkg_config_paths:
        pkg_env = {"PKG_CONFIG_PATH":
                    os.pathsep.join(get_abs_path(f, self._conanfile.install_folder)
                                    for f in pkg_config_paths)}
    else:
        # If we are using pkg_config generator automate the pcs location, otherwise it could
        # read wrong files
        set_env = "pkg_config" in self._conanfile.generators \
                    and "PKG_CONFIG_PATH" not in os.environ
        pkg_env = {"PKG_CONFIG_PATH": self._conanfile.install_folder} if set_env else {}

    with tools.environment_append(pkg_env):
        compiler = self._settings.get_safe("compiler")
        command = "cd %s && cmake %s" % (args_to_string([self.build_dir]), arg_list)
        if compiler == 'emcc':
            self._conanfile.output.warn( 'Used hacked CMake in emcc build')
            command = "cd %s && emcmake cmake %s" % (args_to_string([self.build_dir]), arg_list)

        if platform.system() == "Windows" and self.generator == "MinGW Makefiles":
            with tools.remove_from_path("sh"):
                self._conanfile.run(command)
        else:
            self._conanfile.run(command)

from conans import CMake

if not hasattr(CMake,'_conan_hacks'):
    CMake._conan_hacks={}

if not CMake._conan_hacks.has_key('configure'):
    CMake._conan_hacks['configure']={
        'origin':CMake.configure,
        'hacked':_configure
    }
    CMake.configure = _configure


