cmake_minimum_required(VERSION 2.8)
project( tracking )

LIST(APPEND CMAKE_MODULE_PATH "/usr/local/lib/cmake")

find_package( OpenCV REQUIRED )

set(CMAKE_BUILD_TYPE Debug)

set(TRACK_DIR Raspi-ImageProcessing/desktop/objectTracking)

set(CMAKE_CXX_FLAGS "-std=c++11 ${CMAKE_CXX_FLAGS} -g -ftest-coverage -fprofile-arcs -Wall -Wextra -Wno-unused -pedantic")

set(LIB_SOURCES
    ${TRACK_DIR}/Flooder.h
    ${TRACK_DIR}/Flooder.cpp
    ${TRACK_DIR}/Vec3.cpp
    ${TRACK_DIR}/Vec3.h
    ${TRACK_DIR}/ColorTracker.h
    ${TRACK_DIR}/ColorTracker.cpp
    ${TRACK_DIR}/ImgFunc.h
    ${TRACK_DIR}/ImgFunc.cpp
    ${TRACK_DIR}/BinMap.h
    ${TRACK_DIR}/BinMap.cpp
    ${TRACK_DIR}/Vec2.h
    ${TRACK_DIR}/Vec2.cpp
    )

set(LIB_NAME "TrackingCode")
add_library(${LIB_NAME} ${LIB_SOURCES})

set(TRACKING_SOURCES
    main.cpp
    )
add_executable( tracking ${TRACKING_SOURCES} )
target_link_libraries( tracking ${OpenCV_LIBS} ${LIB_NAME})

if(BUILD_RASPI)

    find_package(raspicam REQUIRED)
    if( raspicam_CV_FOUND )
        target_link_libraries(tracking ${raspicam_CV_LIBS})
    else()
        MESSAGE(FATAL_ERROR "Raspicam not found")
    endif()
endif()
