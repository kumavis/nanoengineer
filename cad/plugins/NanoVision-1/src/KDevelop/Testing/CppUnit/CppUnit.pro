SOURCES += ../../../Testing/CppUnit/CppUnit.cpp \
 ../../../Interface/NXEntityManagerTest.cpp \
 ../../../Interface/NXNumbersTest.cpp \
 ../../../Utility/NXCommandResultTest.cpp \
 ../../../Utility/NXLoggerTest.cpp \
 ../../../Utility/NXStringTokenizerTest.cpp \
 ../../../Utility/NXUtilityTest.cpp \
 ../../../Plugins/HDF5_SimResultsImportExport/HDF5_SimResultsImportExportTest.cpp \
 ../../../Plugins/OpenBabelImportExport/OpenBabelImportExportTest.cpp \
 ../../../Utility/NXPointTest.cpp \
 ../../../Interface/NXSceneGraphTest.cpp \
 ../../../Plugins/NanorexMMPImportExport/NanorexMMPImportExportTest.cpp \
 ../../../Plugins/NanorexMMPImportExport/NanorexMMPImportExportRagelTest.cpp

TEMPLATE = app

TARGET = CppUnit


INCLUDEPATH += ../../../../include \
 $(OPENBABEL_INCPATH) \
 $(HDF5_SIMRESULTS_INCPATH) \
 ../../../../src
# The "../../../src" is temporary for NXEntityManager to access an
# HDF5_SimResultsImportExport plugin function directly.

HEADERS += ../../../Utility/NXCommandResultTest.h \
../../../Utility/NXLoggerTest.h \
../../../Utility/NXStringTokenizerTest.h \
../../../Utility/NXUtilityTest.h \
../../../Interface/NXEntityManagerTest.h \
../../../Interface/NXNumbersTest.h \
../../../Plugins/HDF5_SimResultsImportExport/HDF5_SimResultsImportExportTest.h \
 ../../../Plugins/OpenBabelImportExport/OpenBabelImportExportTest.h \
 ../../../Interface/NXSceneGraphTest.h \
 ../../../Plugins/NanorexMMPImportExport/NanorexMMPImportExportTest.h \
 ../../../Plugins/NanorexMMPImportExport/NanorexMMPImportExportRagelTest.h

macx : TARGETDEPS ~= s/.so/.dylib/g
win32 : TARGETDEPS ~= s/.so/.a/g

DESTDIR = ../../../../bin

CONFIG += debug_and_release \
stl

# This tell qmake to not create a Mac bundle for this application.
CONFIG -= app_bundle

QMAKE_CXXFLAGS_DEBUG += -DNX_DEBUG \
 -g \
 -O0 \
 -fno-inline


TARGETDEPS += ../../../../lib/libNanorexInterface.so \
  ../../../../lib/libNanorexUtility.so

QT -= gui


DISTFILES += ../../../Plugins/NanorexMMPImportExport/NanorexMMPImportExportTest.rl \
 ../../../Plugins/NanorexMMPImportExport/molecule.rl \
 ../../../Plugins/NanorexMMPImportExport/atom.rl \
 ../../../Plugins/NanorexMMPImportExport/utilities.rl \
 ../../../Plugins/NanorexMMPImportExport/group.rl \
 ../../../Plugins/NanorexMMPImportExport/NanorexMMPImportExportRagelTest.rl



LIBS += -L../../../../lib \
  -lNanorexMMPImportExport \
  -lNanorexUtility \
  -lNanorexInterface \
  -L$(OPENBABEL_LIBPATH) \
  -L$(HDF5_SIMRESULTS_INCPATH) \
  -lcppunit \
  -lopenbabel

