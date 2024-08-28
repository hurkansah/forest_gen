cmake_minimum_required(VERSION 3.5)
project(sim_gazebo)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -Wall")

set(CATKIN_DEPENDENCIES
  gazebo_plugins
  gazebo_ros
  geometry_msgs
  roscpp
  std_msgs
  tf2
  tf2_msgs
  tf2_ros
  )

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  ${CATKIN_DEPENDENCIES}
  )

# include Gazebo
find_package(gazebo REQUIRED)

# include Qt
find_package(Qt5Widgets REQUIRED)

# include OpenCV
find_package(OpenCV REQUIRED)

# XXX this approach is extremely error prone
# it would be preferable to either depend on the
# compiled headers from Gazebo directly
# or to have something entirely independent.
#
set(PROTOBUF_IMPORT_DIRS "")
foreach(ITR ${GAZEBO_INCLUDE_DIRS})
  if(ITR MATCHES ".*gazebo-[0-9.]+$")
    set(PROTOBUF_IMPORT_DIRS "${ITR}/gazebo/msgs/proto")
  endif()
endforeach()

set(GAZEBO_MSG_INCLUDE_DIRS)
foreach(ITR ${GAZEBO_INCLUDE_DIRS})
  if(ITR MATCHES ".*gazebo-[0-9.]+$")
    set(GAZEBO_MSG_INCLUDE_DIRS "${ITR}/gazebo/msgs")
  endif()
endforeach()


set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

catkin_package(
  CATKIN_DEPENDS ${CATKIN_DEPENDENCIES}
  DEPENDS GAZEBO Qt5Widgets OpenCV
  LIBRARIES ${LIBRARIES}
  )

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  include
  ${GAZEBO_INCLUDE_DIRS}
  ${GAZEBO_MSG_INCLUDE_DIRS}
  ${CMAKE_CURRENT_BINARY_DIR}
  ${catkin_INCLUDE_DIRS}
  ${Qt5Widgets_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
  )

link_directories(${GAZEBO_LIBRARY_DIRS})

## --------------------------------------------------------------
## |                           Install                          |
## --------------------------------------------------------------

install(TARGETS ${LIBRARIES}
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION}
  )

install(DIRECTORY models/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/models
  )

install(DIRECTORY worlds/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/worlds
  )
