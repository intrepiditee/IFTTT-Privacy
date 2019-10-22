# Install script for directory: /Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/SEAL-3.4/seal/util" TYPE FILE FILES
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/baseconverter.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/blake2.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/blake2-impl.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/clang.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/clipnormal.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/common.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/config.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/croots.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/defines.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/gcc.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/globals.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/hash.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/hestdparms.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/locks.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/mempool.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/msvc.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/numth.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/pointer.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/polyarith.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/polyarithmod.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/polyarithsmallmod.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/polycore.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/rlwe.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/scalingvariant.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/smallntt.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/uintarith.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/uintarithmod.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/uintarithsmallmod.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/uintcore.h"
    "/Users/manumaheshwari/Desktop/Fall 2019/COMP 536/project/IFTTT-Privacy/server/SEAL/native/src/seal/util/ztools.h"
    )
endif()

