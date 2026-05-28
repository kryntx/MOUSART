cmake_minimum_required(VERSION 3.16)
project(MOUSART VERSION 2.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt5 REQUIRED COMPONENTS Core Gui Qml Quick Widgets SerialPort)

set(SOURCES
    src/main.cpp
    src/core/thememanager.cpp
    src/core/serialportmanager.cpp
    src/core/virtualserialmanager.cpp
    src/core/configmanager.cpp
    src/core/dataanalyzer.cpp
    src/core/logfilemanager.cpp
)

set(HEADERS
    src/core/thememanager.h
    src/core/serialportmanager.h
    src/core/virtualserialmanager.h
    src/core/configmanager.h
    src/core/dataanalyzer.h
    src/core/logfilemanager.h
)

qt5_add_resources(QRC_RESOURCES qml.qrc)

add_executable(${PROJECT_NAME}
    ${SOURCES}
    ${HEADERS}
    ${QRC_RESOURCES}
)

target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt5::Core
    Qt5::Gui
    Qt5::Qml
    Qt5::Quick
    Qt5::Widgets
    Qt5::SerialPort
)

set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)
