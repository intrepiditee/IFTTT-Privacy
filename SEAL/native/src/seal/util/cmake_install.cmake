# Install script for directory: /usr/src/app/SEAL/native/src/seal/util

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

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/SEAL-3.4/seal/util" TYPE FILE FILES
    "/usr/src/app/SEAL/native/src/seal/util/baseconverter.h"
    "/usr/src/app/SEAL/native/src/seal/util/blake2.h"
    "/usr/src/app/SEAL/native/src/seal/util/blake2-impl.h"
    "/usr/src/app/SEAL/native/src/seal/util/clang.h"
    "/usr/src/app/SEAL/native/src/seal/util/clipnormal.h"
    "/usr/src/app/SEAL/native/src/seal/util/common.h"
    "/usr/src/app/SEAL/native/src/seal/util/config.h"
    "/usr/src/app/SEAL/native/src/seal/util/croots.h"
    "/usr/src/app/SEAL/native/src/seal/util/defines.h"
    "/usr/src/app/SEAL/native/src/seal/util/gcc.h"
    "/usr/src/app/SEAL/native/src/seal/util/globals.h"
    "/usr/src/app/SEAL/native/src/seal/util/hash.h"
    "/usr/src/app/SEAL/native/src/seal/util/hestdparms.h"
    "/usr/src/app/SEAL/native/src/seal/util/locks.h"
    "/usr/src/app/SEAL/native/src/seal/util/mempool.h"
    "/usr/src/app/SEAL/native/src/seal/util/msvc.h"
    "/usr/src/app/SEAL/native/src/seal/util/numth.h"
    "/usr/src/app/SEAL/native/src/seal/util/pointer.h"
    "/usr/src/app/SEAL/native/src/seal/util/polyarith.h"
    "/usr/src/app/SEAL/native/src/seal/util/polyarithmod.h"
    "/usr/src/app/SEAL/native/src/seal/util/polyarithsmallmod.h"
    "/usr/src/app/SEAL/native/src/seal/util/polycore.h"
    "/usr/src/app/SEAL/native/src/seal/util/rlwe.h"
    "/usr/src/app/SEAL/native/src/seal/util/scalingvariant.h"
    "/usr/src/app/SEAL/native/src/seal/util/smallntt.h"
    "/usr/src/app/SEAL/native/src/seal/util/uintarith.h"
    "/usr/src/app/SEAL/native/src/seal/util/uintarithmod.h"
    "/usr/src/app/SEAL/native/src/seal/util/uintarithsmallmod.h"
    "/usr/src/app/SEAL/native/src/seal/util/uintcore.h"
    "/usr/src/app/SEAL/native/src/seal/util/ztools.h"
    )
endif()

