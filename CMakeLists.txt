cmake_minimum_required(VERSION 2.8.3)
project(cairo_nlp)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

add_service_files(
  FILES
  STT.srv
  TTS.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
    CATKIN_DEPENDS
    rospy
)
