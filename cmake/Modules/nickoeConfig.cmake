INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_NICKOE nickoe)

FIND_PATH(
    NICKOE_INCLUDE_DIRS
    NAMES nickoe/api.h
    HINTS $ENV{NICKOE_DIR}/include
        ${PC_NICKOE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    NICKOE_LIBRARIES
    NAMES gnuradio-nickoe
    HINTS $ENV{NICKOE_DIR}/lib
        ${PC_NICKOE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(NICKOE DEFAULT_MSG NICKOE_LIBRARIES NICKOE_INCLUDE_DIRS)
MARK_AS_ADVANCED(NICKOE_LIBRARIES NICKOE_INCLUDE_DIRS)

