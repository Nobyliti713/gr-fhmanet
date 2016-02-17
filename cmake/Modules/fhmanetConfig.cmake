INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_FHMANET fhmanet)

FIND_PATH(
    FHMANET_INCLUDE_DIRS
    NAMES fhmanet/api.h
    HINTS $ENV{FHMANET_DIR}/include
        ${PC_FHMANET_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    FHMANET_LIBRARIES
    NAMES gnuradio-fhmanet
    HINTS $ENV{FHMANET_DIR}/lib
        ${PC_FHMANET_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FHMANET DEFAULT_MSG FHMANET_LIBRARIES FHMANET_INCLUDE_DIRS)
MARK_AS_ADVANCED(FHMANET_LIBRARIES FHMANET_INCLUDE_DIRS)

