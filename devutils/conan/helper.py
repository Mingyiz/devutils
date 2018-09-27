#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_default
import platform
import copy
import os

def webstreamer_build_template_default(name,config={}):

    CONAN_BUILD_TYPES = config.get('CONAN_BUILD_TYPES','Debug')
    CONAN_BUILD_TYPES = os.environ.get('CONAN_BUILD_TYPES',CONAN_BUILD_TYPES)
    os.environ['CONAN_BUILD_TYPES'] = CONAN_BUILD_TYPES

    CONAN_VISUAL_VERSIONS = None

    if platform.system() == "Windows":
        CONAN_VISUAL_VERSIONS = os.environ.get('CONAN_VISUAL_VERSIONS', '15')
        CONAN_VISUAL_VERSIONS = config.get('CONAN_VISUAL_VERSIONS',CONAN_VISUAL_VERSIONS)
        if CONAN_VISUAL_VERSIONS:
            os.environ['CONAN_VISUAL_VERSIONS'] = CONAN_VISUAL_VERSIONS

    builder = build_template_default.get_builder()
    if os.environ.get('EMCC_VERSIONS'):
        
        for build_type in os.environ['CONAN_BUILD_TYPES'].split(','):
            for version in os.environ['EMCC_VERSIONS'].split(','):
                builder.add(settings={"arch": "any", "build_type": build_type, 
                    "compiler": "emcc", "compiler.version": version,"compiler.libcxx":'libcxxabi'},
                    options={'%s:shared'%name :True}, env_vars={}, build_requires={})

        items = []
        for item in builder.items:
            if not os.environ.get('CONAN_GCC_VERSIONS') and item.settings['compiler'] == 'gcc':
                continue # 
            if not os.environ.get('CONAN_CLANG_VERSIONS') and item.settings['compiler'] == 'clang':
                continue # 
            items.append(item)

        builder.items = items


    return builder

