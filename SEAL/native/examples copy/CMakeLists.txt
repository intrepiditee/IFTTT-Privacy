# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

cmake_minimum_required(VERSION 3.12)

project(SEALBenchmark VERSION 3.4.2 LANGUAGES CXX)

# Executable will be in ../bin
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${SEALExamples_SOURCE_DIR}/../bin)

add_executable(benchmark examples.cpp)
target_sources(benchmark
    PRIVATE
		subs.cpp
)

# Import Microsoft SEAL
find_package(SEAL 3.4.2 EXACT REQUIRED
    # Providing a path so this can be built without installing Microsoft SEAL
    PATHS ${SEALExamples_SOURCE_DIR}/../src/cmake
)

# Link Microsoft SEAL
target_link_libraries(benchmark SEAL::seal)
