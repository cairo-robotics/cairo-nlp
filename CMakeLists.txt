cmake_minimum_required(VERSION 2.8.3)
project(cairo_nlp)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_python_setup()

catkin_package(
    CATKIN_DEPENDS
    rospy
)
