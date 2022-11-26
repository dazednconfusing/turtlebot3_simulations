################################################################################
# CMake
################################################################################
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

################################################################################
# Packages
################################################################################
find_package(gz-math7 REQUIRED)
set(GZ_MATH_VER ${gz-math7_VERSION_MAJOR})

################################################################################
# Build
################################################################################

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#add_library(obstacle1 SHARED obstacle1.cc)
#target_link_libraries(obstacle1 ${GAZEBO_LIBRARIES})

#add_library(obstacle2 SHARED obstacle2.cc)
#target_link_libraries(obstacle2 ${GAZEBO_LIBRARIES})

#add_library(obstacles SHARED obstacles.cc)
#target_link_libraries(obstacles ${GAZEBO_LIBRARIES})
