#!/usr/bin/env python3
import json
import os
from pathlib import Path
import argparse

def create_main_cmakelists(config):
    project_name = config["projectName"]
    c_standard = config["cStandard"]
    cpp_standard = config["cppStandard"]
    
    content = f"""cmake_minimum_required(VERSION 3.10)

project({project_name} C CXX)

cmake_policy(SET CMP0135 NEW)

set(CMAKE_C_STANDARD {c_standard})
set(CMAKE_CXX_STANDARD {cpp_standard})
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set a default build type if none was specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'Release' as none was specified.")
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build, options are: Debug Release RelWithDebInfo MinSizeRel." FORCE)
endif()

# Compiler flags
set(CMAKE_C_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_C_FLAGS_DEBUG "-g")
set(CMAKE_C_FLAGS_RELEASE "-O3")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

# Add library subdirectories
"""
    for lib in config["libraries"]:
        content += f"add_subdirectory(lib/{lib['name']})\n"

    content += "\n# Add executables\n"
    for exe in config["executables"]:
        exe_name = exe["name"]
        sources = " ".join(exe["sources"])
        content += f"add_executable({exe_name} {sources})\n"
        
        if "dependencies" in exe and exe["dependencies"]:
            deps = " ".join(exe["dependencies"])
            content += f"target_link_libraries({exe_name} PRIVATE {deps})\n"
        
        content += f"""
set_target_properties({exe_name} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/bin
)
"""
    if config.get("enableTests", True):
        content += """

# --- Testing ---
enable_testing()
add_subdirectory(tests)
"""
    return content

def create_lib_cmakelists(lib_config):
    lib_name = lib_config["name"]
    sources = " ".join(lib_config["sources"])
    
    return f"""add_library({lib_name} {" ".join(lib_config["sources"])})

target_include_directories({lib_name} PUBLIC include)
"""

def main():
    parser = argparse.ArgumentParser(description="Create a new C/C++ project from a template.")
    parser.add_argument("outputDir", type=Path, nargs="?", default=None, help="The output directory for the new project. Defaults to the project name in the current directory.")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    template_path = script_dir / "project_template.json"

    try:
        with open(template_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{template_path}' not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{template_path}': {e}")
        return

    project_name = config["projectName"]
    
    if "outputDir" in config:
        root = Path(config["outputDir"]) / project_name
    else:
        root = Path(project_name)
    
    if root.exists():
        print(f"Error: Directory '{root}' already exists.")
        return

    print(f"Creating project '{project_name}' in '{root}'...")

    # Create root CMakeLists.txt
    root.mkdir(parents=True)
    (root / "CMakeLists.txt").write_text(create_main_cmakelists(config))

    # Create executables sources
    for exe in config["executables"]:
        for src in exe["sources"]:
            (root / src).write_text(f'#include <stdio.h>\n\nint main(void) {{\n    printf("Hello from {exe["name"]}\\n");\n    return 0;\n}}\n')

    # Create libraries
    lib_dir = root / "lib"
    lib_dir.mkdir()
    for lib in config["libraries"]:
        lib_path = lib_dir / lib["name"]
        lib_path.mkdir()
        (lib_path / "CMakeLists.txt").write_text(create_lib_cmakelists(lib))
        
        # Create source files
        for src in lib["sources"]:
            (lib_path / src).write_text(f'#include "{lib["name"]}.h"\n#include <stdio.h>\n\nvoid {lib["name"]}_hello() {{\n    printf("Hello from {lib["name"]}\\n");\n}}\n')
            
        # Create header files
        include_path = lib_path / "include"
        include_path.mkdir()
        for hdr in lib["headers"]:
            header_guard = f'{lib["name"].upper()}_H'
            (include_path / hdr).write_text(f"#ifndef {header_guard}\n#define {header_guard}\n\nvoid {lib['name']}_hello(void);\n\n#endif\n")

    # Create tests directory
    if config.get("enableTests", False):
        tests_dir = root / "tests"
        tests_dir.mkdir()
        (tests_dir / "CMakeLists.txt").write_text(f"""# Add GTest
                                                  
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# Create the test executable
add_executable(run_tests test_foo.cpp)

# Link against GTest and the library to be tested
target_link_libraries(run_tests PRIVATE GTest::gtest_main foo)

# Discover and add tests to CTest
include(GoogleTest)
gtest_discover_tests(run_tests)
""")
        (tests_dir / "test_foo.cpp").write_text("""#include <gtest/gtest.h>
#include "foo.h"

TEST(FooTest, BasicTest) {
    // A simple test to ensure the function can be called
    foo_hello();
    SUCCEED();
}

TEST(FooTest, AlwaysPasses) {
    EXPECT_TRUE(true);
}
""")

    print(f"Project '{project_name}' created successfully in '{root}'.")
    print("To build:")
    print(f"  cd {root}")
    print("  cmake -B build -G Ninja")
    print("  cmake --build build")

if __name__ == "__main__":
    main()
