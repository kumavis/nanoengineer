"""The main window of Atom, controls are here
"""

import qt
from qt import QMainWindow, QPixmap, QWidget, QFrame, QPushButton
from qt import QGroupBox, QComboBox, QAction, QMenuBar, QPopupMenu
from qt import SIGNAL, QFileDialog
from GLPane import *
import os
import help
import icons

#Added by huaicai
from MotorPropDialog import *

helpwindow = None
windowList = []

from constants import *
from chem import fullnamePeriodicTable

def fileparse(name):
    """breaks name into directory, main name, and extension in a tuple.
    fileparse('~/foo/bar/gorp.xam') ==> ('~/foo/bar/', 'gorp', '.xam')
    """
    m=re.match("(.*\/)*([^\.]+)(\..*)?",name)
    return ((m.group(1) or "./"), m.group(2), (m.group(3) or ""))


class MainWindow(QMainWindow):
    def __init__(self,parent = None,name = None,fl = 0):
        global windowList
        QMainWindow.__init__(self,parent,name,fl)
        
        # start with empty window
        self.assy = assembly(self)
        windowList += [self]

        # loads of gruesome boilerplate for UI
        # generated by designer/pyuic
        image0 = QPixmap()
        image0.loadFromData(icons.image0_data,"PNG")
        image1 = QPixmap()
        image1.loadFromData(icons.image1_data,"PNG")
        image2 = QPixmap()
        image2.loadFromData(icons.image2_data,"PNG")
        image3 = QPixmap()
        image3.loadFromData(icons.image3_data,"PNG")
        image4 = QPixmap()
        image4.loadFromData(icons.image4_data,"PNG")
        image5 = QPixmap()
        image5.loadFromData(icons.image5_data,"PNG")
        image6 = QPixmap()
        image6.loadFromData(icons.image6_data,"PNG")
        image7 = QPixmap()
        image7.loadFromData(icons.image7_data,"PNG")
        image8 = QPixmap()
        image8.loadFromData(icons.image8_data,"PNG")
        image9 = QPixmap()
        image9.loadFromData(icons.image9_data,"PNG")
        if name == None:
            self.setName("The MERI Atom!")

        self.resize(787,667)
        self.setCaption(self.trUtf8("The MERI Atom!"))

        self.setCentralWidget(QWidget(self,"qt_central_widget"))
        Form1Layout = QVBoxLayout(self.centralWidget(),11,6,"Form1Layout")


        self.frame4 = QFrame(self.centralWidget(),"frame4")
        self.frame4.setSizePolicy(QSizePolicy(3,3,0,0,False))
        self.frame4.setFrameShape(QFrame.NoFrame)
        self.frame4.setFrameShadow(QFrame.Plain)
        frame4Layout = QHBoxLayout(self.frame4,0,0,"frame4Layout")

        self.groupBox1 = QGroupBox(self.frame4,"groupBox1")
        self.groupBox1.setSizePolicy(QSizePolicy(0,7,0,244,False))


        self.AddAtoms = QPushButton(self.groupBox1,"AddAtoms")
        self.AddAtoms.setGeometry(QRect(20,180,80,24))
        self.AddAtoms.setText(self.trUtf8("addAtoms"))

        self.Done = QPushButton(self.groupBox1,"Done")
        self.Done.setGeometry(QRect(20,210,80,24))
        self.Done.setText(self.trUtf8("Done"))

        self.Movie = QPushButton(self.groupBox1,"Movie")
        self.Movie.setGeometry(QRect(20,250,80,24))
        self.Movie.setText(self.trUtf8("Movie"))

        self.Bondedge = QPushButton(self.groupBox1,"Bondedge")
        self.Bondedge.setGeometry(QRect(20,290,80,24))
        self.Bondedge.setText(self.trUtf8("Bond (edge)"))

        self.UBondall = QPushButton(self.groupBox1,"UBondall")
        self.UBondall.setGeometry(QRect(20,340,80,24))
        self.UBondall.setText(self.trUtf8("Axis"))

        self.UBondedge = QPushButton(self.groupBox1,"UBondedge")
        self.UBondedge.setGeometry(QRect(20,380,90,24))
        self.UBondedge.setText(self.trUtf8("UnBond (edge)"))

        self.Unsel = QPushButton(self.groupBox1,"Unsel")
        self.Unsel.setGeometry(QRect(20,440,80,24))
        self.Unsel.setText(self.trUtf8("Unselect"))

        self.Copybut = QPushButton(self.groupBox1,"Copybut")
        self.Copybut.setGeometry(QRect(20,490,80,24))
        self.Copybut.setText(self.trUtf8("Copy"))

        self.CopyBond = QPushButton(self.groupBox1,"CopyBond")
        self.CopyBond.setGeometry(QRect(20,530,86,24))
        self.CopyBond.setText(self.trUtf8("Copy && Bond"))

        self.KillBut = QPushButton(self.groupBox1,"KillBut")
        self.KillBut.setGeometry(QRect(20,590,80,24))
        self.KillBut.setText(self.trUtf8("Kill"))

        self.Cookie = QPushButton(self.groupBox1,"Cookie")
        self.Cookie.setGeometry(QRect(20,20,80,24))
        self.Cookie.setText(self.trUtf8("CookieCutter"))

        self.Layer = QPushButton(self.groupBox1,"Layer")
        self.Layer.setGeometry(QRect(20,50,80,24))
        self.Layer.setText(self.trUtf8("Layer"))

        self.Bake = QPushButton(self.groupBox1,"Bake")
        self.Bake.setGeometry(QRect(20,80,80,24))
        self.Bake.setText(self.trUtf8("Bake"))

        self.comboBox1 = QComboBox(0,self.groupBox1,"comboBox1")
        self.comboBox1.insertItem(self.trUtf8("Hydrogen"))
        self.comboBox1.insertItem(self.trUtf8("Boron"))
        self.comboBox1.insertItem(self.trUtf8("Carbon"))
        self.comboBox1.insertItem(self.trUtf8("Nitrogen"))
        self.comboBox1.insertItem(self.trUtf8("Oxygen"))
        self.comboBox1.insertItem(self.trUtf8("Fluorine"))
        self.comboBox1.insertItem(self.trUtf8("Aluminum"))
        self.comboBox1.insertItem(self.trUtf8("Silicon"))
        self.comboBox1.insertItem(self.trUtf8("Phosphorus"))
        self.comboBox1.insertItem(self.trUtf8("Sulfur"))
        self.comboBox1.insertItem(self.trUtf8("Chlorine"))
        self.comboBox1.setGeometry(QRect(10,150,110,22))


        self.fileNewAction = QAction(self,"fileNewAction")
        self.fileNewAction.setIconSet(QIconSet(image0))
        self.fileNewAction.setText(self.trUtf8("New"))
        self.fileNewAction.setMenuText(self.trUtf8("&New"))
        self.fileNewAction.setAccel(self.trUtf8("Ctrl+N"))
        self.fileOpenAction = QAction(self,"fileOpenAction")
        self.fileOpenAction.setIconSet(QIconSet(image1))
        self.fileOpenAction.setText(self.trUtf8("Open"))
        self.fileOpenAction.setMenuText(self.trUtf8("&Open..."))
        self.fileOpenAction.setAccel(self.trUtf8("Ctrl+O"))
        self.fileSaveAction = QAction(self,"fileSaveAction")
        self.fileSaveAction.setIconSet(QIconSet(image2))
        self.fileSaveAction.setText(self.trUtf8("Save"))
        self.fileSaveAction.setMenuText(self.trUtf8("&Save"))
        self.fileSaveAction.setAccel(self.trUtf8("Ctrl+S"))
        self.fileSaveAsAction = QAction(self,"fileSaveAsAction")
        self.fileSaveAsAction.setText(self.trUtf8("Save As"))
        self.fileSaveAsAction.setMenuText(self.trUtf8("Save &As..."))
        self.fileSaveAsAction.setAccel(self.trUtf8(""))
        self.fileImageAction = QAction(self,"fileImageAction")
        self.fileImageAction.setIconSet(QIconSet(image3))
        self.fileImageAction.setText(self.trUtf8("Image"))
        self.fileImageAction.setMenuText(self.trUtf8("&Image..."))
        self.fileImageAction.setAccel(self.trUtf8("Ctrl+P"))
        self.fileExitAction = QAction(self,"fileExitAction")
        self.fileExitAction.setText(self.trUtf8("Exit"))
        self.fileExitAction.setMenuText(self.trUtf8("E&xit"))
        self.fileExitAction.setAccel(self.trUtf8(""))
        self.editUndoAction = QAction(self,"editUndoAction")
        self.editUndoAction.setIconSet(QIconSet(image4))
        self.editUndoAction.setText(self.trUtf8("Undo"))
        self.editUndoAction.setMenuText(self.trUtf8("&Undo"))
        self.editUndoAction.setAccel(self.trUtf8("Ctrl+Z"))
        self.editRedoAction = QAction(self,"editRedoAction")
        self.editRedoAction.setIconSet(QIconSet(image5))
        self.editRedoAction.setText(self.trUtf8("Redo"))
        self.editRedoAction.setMenuText(self.trUtf8("&Redo"))
        self.editRedoAction.setAccel(self.trUtf8("Ctrl+Y"))
        self.editCutAction = QAction(self,"editCutAction")
        self.editCutAction.setIconSet(QIconSet(image6))
        self.editCutAction.setText(self.trUtf8("Cut"))
        self.editCutAction.setMenuText(self.trUtf8("Cu&t"))
        self.editCutAction.setAccel(self.trUtf8("Ctrl+X"))
        self.editCopyAction = QAction(self,"editCopyAction")
        self.editCopyAction.setIconSet(QIconSet(image7))
        self.editCopyAction.setText(self.trUtf8("Copy"))
        self.editCopyAction.setMenuText(self.trUtf8("&Copy"))
        self.editCopyAction.setAccel(self.trUtf8("Ctrl+C"))
        self.editPasteAction = QAction(self,"editPasteAction")
        self.editPasteAction.setIconSet(QIconSet(image8))
        self.editPasteAction.setText(self.trUtf8("Paste"))
        self.editPasteAction.setMenuText(self.trUtf8("&Paste"))
        self.editPasteAction.setAccel(self.trUtf8("Ctrl+V"))
        self.editFindAction = QAction(self,"editFindAction")
        self.editFindAction.setIconSet(QIconSet(image9))
        self.editFindAction.setText(self.trUtf8("Find"))
        self.editFindAction.setMenuText(self.trUtf8("&Find..."))
        self.editFindAction.setAccel(self.trUtf8("Ctrl+F"))
        self.helpContentsAction = QAction(self,"helpContentsAction")
        self.helpContentsAction.setText(self.trUtf8("Contents"))
        self.helpContentsAction.setMenuText(self.trUtf8("&Contents..."))
        self.helpContentsAction.setAccel(self.trUtf8(""))
        self.helpIndexAction = QAction(self,"helpIndexAction")
        self.helpIndexAction.setText(self.trUtf8("Index"))
        self.helpIndexAction.setMenuText(self.trUtf8("&Index..."))
        self.helpIndexAction.setAccel(self.trUtf8(""))
        self.helpAboutAction = QAction(self,"helpAboutAction")
        self.helpAboutAction.setText(self.trUtf8("About"))
        self.helpAboutAction.setMenuText(self.trUtf8("&About"))
        self.helpAboutAction.setAccel(self.trUtf8(""))

        self.dispNewViewAction = QAction(self,"dispNewViewAction")
        self.dispNewViewAction.setText(self.trUtf8("NewView"))
        self.dispNewViewAction.setMenuText(self.trUtf8("NewView"))

        self.dispOrthoAction = QAction(self,"dispOrthoAction")
        self.dispOrthoAction.setText(self.trUtf8("Ortho"))
        self.dispOrthoAction.setMenuText(self.trUtf8("Ortho"))

        self.dispPerspecAction = QAction(self,"dispPerspecAction")
        self.dispPerspecAction.setText(self.trUtf8("Perspec"))
        self.dispPerspecAction.setMenuText(self.trUtf8("Perspec"))

        self.dispVdWAction = QAction(self,"dispVdWAction")
        self.dispVdWAction.setText(self.trUtf8("VdW"))
        self.dispVdWAction.setMenuText(self.trUtf8("VdW"))
        self.dispTubesAction = QAction(self,"dispTubesAction")
        self.dispTubesAction.setText(self.trUtf8("Tubes"))
        self.dispTubesAction.setMenuText(self.trUtf8("Tubes"))
        self.dispCPKAction = QAction(self,"dispCPKAction")
        self.dispCPKAction.setText(self.trUtf8("CPK"))
        self.dispCPKAction.setMenuText(self.trUtf8("CPK"))
        self.dispLinesAction = QAction(self,"dispLinesAction")
        self.dispLinesAction.setText(self.trUtf8("Lines"))
        self.dispLinesAction.setMenuText(self.trUtf8("Lines"))

        self.dispDefaultAction = QAction(self,"dispDefaultAction")
        self.dispDefaultAction.setText(self.trUtf8("Default"))
        self.dispDefaultAction.setMenuText(self.trUtf8("Default"))

        self.dispInvisAction = QAction(self,"dispInvisAction")
        self.dispInvisAction.setText(self.trUtf8("Invis"))
        self.dispInvisAction.setMenuText(self.trUtf8("Invis"))
        
        self.dispColorAction = QAction(self,"dispColorAction")
        self.dispColorAction.setText(self.trUtf8("Color"))
        self.dispColorAction.setMenuText(self.trUtf8("Color"))

        self.gridNoneAction = QAction(self,"gridNoneAction")
        self.gridNoneAction.setText(self.trUtf8("None"))
        self.gridNoneAction.setMenuText(self.trUtf8("None"))

        self.gridSquareAction = QAction(self,"gridSquareAction")
        self.gridSquareAction.setText(self.trUtf8("Square"))
        self.gridSquareAction.setMenuText(self.trUtf8("Square"))

        self.gridDiamondAction = QAction(self,"gridDiamondAction")
        self.gridDiamondAction.setText(self.trUtf8("Diamond"))
        self.gridDiamondAction.setMenuText(self.trUtf8("Diamond"))

        self.gridGraphiteAction = QAction(self,"gridGraphiteAction")
        self.gridGraphiteAction.setText(self.trUtf8("Graphite"))
        self.gridGraphiteAction.setMenuText(self.trUtf8("Graphite"))

        self.orient100Action = QAction(self,"orient100Action")
        self.orient100Action.setText(self.trUtf8("100"))
        self.orient100Action.setMenuText(self.trUtf8("100 Surface"))

        self.orient110Action = QAction(self,"orient110Action")
        self.orient110Action.setText(self.trUtf8("110"))
        self.orient110Action.setMenuText(self.trUtf8("110 Surface"))

        self.orient111Action = QAction(self,"orient111Action")
        self.orient111Action.setText(self.trUtf8("111"))
        self.orient111Action.setMenuText(self.trUtf8("111 Surface"))


        self.selectAllAction = QAction(self,"selectAllAction")
        self.selectAllAction.setText(self.trUtf8("All"))
        self.selectAllAction.setMenuText(self.trUtf8("All"))

        self.selectNoneAction = QAction(self,"selectNoneAction")
        self.selectNoneAction.setText(self.trUtf8("None"))
        self.selectNoneAction.setMenuText(self.trUtf8("None"))

        self.selectInvertAction = QAction(self,"selectInvertAction")
        self.selectInvertAction.setText(self.trUtf8("Invert"))
        self.selectInvertAction.setMenuText(self.trUtf8("Invert"))

        self.selectConnectedAction = QAction(self,"selectConnectedAction")
        self.selectConnectedAction.setText(self.trUtf8("Connected"))
        self.selectConnectedAction.setMenuText(self.trUtf8("Connected"))

        self.selectDoublyAction = QAction(self,"selectDoublyAction")
        self.selectDoublyAction.setText(self.trUtf8("Doubly"))
        self.selectDoublyAction.setMenuText(self.trUtf8("Doubly"))

        self.makeGroundAction = QAction(self,"makeGroundAction")
        self.makeGroundAction.setText(self.trUtf8("Ground"))
        self.makeGroundAction.setMenuText(self.trUtf8("Ground"))

        self.makeHandleAction = QAction(self,"makeHandleAction")
        self.makeHandleAction.setText(self.trUtf8("Handle"))
        self.makeHandleAction.setMenuText(self.trUtf8("Handle"))

        self.makeMotorAction = QAction(self,"makeMotorAction")
        self.makeMotorAction.setText(self.trUtf8("Motor"))
        self.makeMotorAction.setMenuText(self.trUtf8("Motor"))

        self.makeLinearMotorAction = QAction(self,"makeLinearMotorAction")
        self.makeLinearMotorAction.setText(self.trUtf8("Linear Motor"))
        self.makeLinearMotorAction.setMenuText(self.trUtf8("Linear Motor"))

        self.makeBearingAction = QAction(self,"makeBearingAction")
        self.makeBearingAction.setText(self.trUtf8("Bearing"))
        self.makeBearingAction.setMenuText(self.trUtf8("Bearing"))

        self.makeSpringAction = QAction(self,"makeSpringAction")
        self.makeSpringAction.setText(self.trUtf8("Spring"))
        self.makeSpringAction.setMenuText(self.trUtf8("Spring"))

        self.makeDynoAction = QAction(self,"makeDynoAction")
        self.makeDynoAction.setText(self.trUtf8("Dyno"))
        self.makeDynoAction.setMenuText(self.trUtf8("Dyno"))

        self.makeHeatsinkAction = QAction(self,"makeHeatsinkAction")
        self.makeHeatsinkAction.setText(self.trUtf8("Heatsink"))
        self.makeHeatsinkAction.setMenuText(self.trUtf8("Heatsink"))


        self.modifyPassivateAction = QAction(self,"modifyPassivateAction")
        self.modifyPassivateAction.setText(self.trUtf8("Passivate"))
        self.modifyPassivateAction.setMenuText(self.trUtf8("Passivate"))

        self.modifyHydrogenateAction = QAction(self,"modifyHydrogenateAction")
        self.modifyHydrogenateAction.setText(self.trUtf8("Hydrogenate"))
        self.modifyHydrogenateAction.setMenuText(self.trUtf8("Hydrogenate"))

        self.modifySeparateAction = QAction(self,"modifySeparateAction")
        self.modifySeparateAction.setText(self.trUtf8("Separate"))
        self.modifySeparateAction.setMenuText(self.trUtf8("Separate"))

        self.modifyMotorAction = QAction(self,"modifyMotorAction")
        self.modifyMotorAction.setText(self.trUtf8("Motor Property"))
        self.modifyMotorAction.setMenuText(self.trUtf8("Motor Property"))



        self.MenuBar = QMenuBar(self,"MenuBar")

        self.fileMenu = QPopupMenu(self)
        self.fileNewAction.addTo(self.fileMenu)
        self.fileOpenAction.addTo(self.fileMenu)
        self.fileSaveAction.addTo(self.fileMenu)
        self.fileSaveAsAction.addTo(self.fileMenu)
        self.fileMenu.insertSeparator()
        self.fileImageAction.addTo(self.fileMenu)
        self.fileMenu.insertSeparator()
        self.fileExitAction.addTo(self.fileMenu)
        self.MenuBar.insertItem(self.trUtf8("&File"),self.fileMenu)

        self.editMenu = QPopupMenu(self)
        self.editUndoAction.addTo(self.editMenu)
        self.editRedoAction.addTo(self.editMenu)
        self.editMenu.insertSeparator()
        self.editCutAction.addTo(self.editMenu)
        self.editCopyAction.addTo(self.editMenu)
        self.editPasteAction.addTo(self.editMenu)
        self.editMenu.insertSeparator()
        self.editFindAction.addTo(self.editMenu)
        self.MenuBar.insertItem(self.trUtf8("&Edit"),self.editMenu)

        self.dispMenu = QPopupMenu(self)
        self.dispNewViewAction.addTo(self.dispMenu)
        self.dispMenu.insertSeparator()

        self.dispOrthoAction.addTo(self.dispMenu)
        self.dispPerspecAction.addTo(self.dispMenu)
        self.dispMenu.insertSeparator()

        self.dispDefaultAction.addTo(self.dispMenu)
        self.dispInvisAction.addTo(self.dispMenu)
        self.dispVdWAction.addTo(self.dispMenu)
        self.dispTubesAction.addTo(self.dispMenu)
        self.dispCPKAction.addTo(self.dispMenu)
        self.dispLinesAction.addTo(self.dispMenu)
        self.dispMenu.insertSeparator()
        
        self.dispColorAction.addTo(self.dispMenu)
        self.MenuBar.insertItem(self.trUtf8("Display"),self.dispMenu)

        self.gridMenu = QPopupMenu(self)
        self.gridNoneAction.addTo(self.gridMenu)
        self.gridSquareAction.addTo(self.gridMenu)
        self.gridDiamondAction.addTo(self.gridMenu)
        self.gridGraphiteAction.addTo(self.gridMenu)
        self.MenuBar.insertItem(self.trUtf8("Grid"),self.gridMenu)

        self.orientMenu = QPopupMenu(self)
        self.orient100Action.addTo(self.orientMenu)
        self.orient110Action.addTo(self.orientMenu)
        self.orient111Action.addTo(self.orientMenu)
        self.MenuBar.insertItem(self.trUtf8("Orientation"),self.orientMenu)

        self.selectMenu = QPopupMenu(self)
        self.selectAllAction.addTo(self.selectMenu)
        self.selectNoneAction.addTo(self.selectMenu)
        self.selectInvertAction.addTo(self.selectMenu)
        self.selectConnectedAction.addTo(self.selectMenu)
        self.selectDoublyAction.addTo(self.selectMenu)
        self.MenuBar.insertItem(self.trUtf8("Select"),self.selectMenu)

        self.makeMenu = QPopupMenu(self)
        self.makeGroundAction.addTo(self.makeMenu)
        self.makeHandleAction.addTo(self.makeMenu)
        self.makeMenu.insertSeparator()

        self.makeMotorAction.addTo(self.makeMenu)
        self.makeLinearMotorAction.addTo(self.makeMenu)
        self.makeBearingAction.addTo(self.makeMenu)
        self.makeSpringAction.addTo(self.makeMenu)
        self.makeDynoAction.addTo(self.makeMenu)
        self.makeHeatsinkAction.addTo(self.makeMenu)
        self.MenuBar.insertItem(self.trUtf8("Make"),self.makeMenu)

        self.modifyMenu = QPopupMenu(self)
        self.modifyPassivateAction.addTo(self.modifyMenu)
        self.modifyHydrogenateAction.addTo(self.modifyMenu)
        self.modifySeparateAction.addTo(self.modifyMenu)
	self.modifyMotorAction.addTo(self.modifyMenu)
        self.MenuBar.insertItem(self.trUtf8("Modify"),self.modifyMenu)

        self.helpMenu = QPopupMenu(self)
        self.helpContentsAction.addTo(self.helpMenu)
        self.helpIndexAction.addTo(self.helpMenu)
        self.helpMenu.insertSeparator()
        self.helpAboutAction.addTo(self.helpMenu)
        self.MenuBar.insertItem(self.trUtf8("&Help"),self.helpMenu)
        
        frame4Layout.addWidget(self.groupBox1)

        #self.glpane = GLPane(self.assy, self.frame4, "glpane", self)

        #frame4Layout.addWidget(self.glpane)
        Form1Layout.addWidget(self.frame4)

        self.connect(self.fileNewAction,SIGNAL("activated()"),self.fileNew)
        self.connect(self.fileOpenAction,SIGNAL("activated()"),self.fileOpen)
        self.connect(self.fileSaveAction,SIGNAL("activated()"),self.fileSave)
        self.connect(self.fileSaveAsAction,SIGNAL("activated()"),
                     self.fileSaveAs)
        self.connect(self.fileImageAction,SIGNAL("activated()"),self.fileImage)
        # fileExitAction connected in atom.py (main program)
        self.connect(self.editUndoAction,SIGNAL("activated()"),self.editUndo)
        self.connect(self.editRedoAction,SIGNAL("activated()"),self.editRedo)
        self.connect(self.editCutAction,SIGNAL("activated()"),self.editCut)
        self.connect(self.editCopyAction,SIGNAL("activated()"),self.editCopy)
        self.connect(self.editPasteAction,SIGNAL("activated()"),self.editPaste)
        self.connect(self.editFindAction,SIGNAL("activated()"),self.editFind)

        self.connect(self.dispNewViewAction,SIGNAL("activated()"),
                     self.dispNewView)
        self.connect(self.dispOrthoAction,SIGNAL("activated()"),self.dispOrtho)
        self.connect(self.dispPerspecAction,SIGNAL("activated()"),
                     self.dispPerspec)
        self.connect(self.dispDefaultAction,SIGNAL("activated()"),
                     self.dispDefault)
        self.connect(self.dispInvisAction,SIGNAL("activated()"),self.dispInvis)
        self.connect(self.dispVdWAction,SIGNAL("activated()"),self.dispVdW)
        self.connect(self.dispTubesAction,SIGNAL("activated()"),self.dispTubes)
        self.connect(self.dispCPKAction,SIGNAL("activated()"),self.dispCPK)
        self.connect(self.dispLinesAction,SIGNAL("activated()"),self.dispLines)
        self.connect(self.dispColorAction,SIGNAL("activated()"),self.dispColor)
        self.connect(self.gridNoneAction,SIGNAL("activated()"),self.gridNone)
        self.connect(self.gridSquareAction,SIGNAL("activated()"),
                     self.gridSquare)
        self.connect(self.gridDiamondAction,SIGNAL("activated()"),
                     self.gridDiamond)
        self.connect(self.gridGraphiteAction,SIGNAL("activated()"),
                     self.gridGraphite)
        self.connect(self.orient100Action,SIGNAL("activated()"),self.orient100)
        self.connect(self.orient110Action,SIGNAL("activated()"),self.orient110)
        self.connect(self.orient111Action,SIGNAL("activated()"),self.orient111)
        self.connect(self.selectAllAction,SIGNAL("activated()"),self.selectAll)
        self.connect(self.selectNoneAction,SIGNAL("activated()"),
                     self.selectNone)
        self.connect(self.selectInvertAction,SIGNAL("activated()"),
                     self.selectInvert)
        self.connect(self.selectConnectedAction,SIGNAL("activated()"),
                     self.selectConnected)
        self.connect(self.selectDoublyAction,SIGNAL("activated()"),
                     self.selectDoubly)
        self.connect(self.makeGroundAction,SIGNAL("activated()"),
                     self.makeGround)
        self.connect(self.makeHandleAction,SIGNAL("activated()"),
                     self.makeHandle)
        self.connect(self.makeMotorAction,SIGNAL("activated()"),self.makeMotor)
	self.connect(self.makeLinearMotorAction,SIGNAL("activated()"),self.makeLinearMotor)
        self.connect(self.makeBearingAction,SIGNAL("activated()"),
                     self.makeBearing)
        self.connect(self.makeSpringAction,SIGNAL("activated()"),
                     self.makeSpring)
        self.connect(self.makeDynoAction,SIGNAL("activated()"),self.makeDyno)
        self.connect(self.makeHeatsinkAction,SIGNAL("activated()"),
                     self.makeHeatsink)
        self.connect(self.modifyPassivateAction,SIGNAL("activated()"),
                     self.modifyPassivate)
        self.connect(self.modifyHydrogenateAction,SIGNAL("activated()"),
                     self.modifyHydrogenate)
        self.connect(self.modifySeparateAction,SIGNAL("activated()"),
                     self.modifySeparate)
        self.connect(self.modifyMotorAction,SIGNAL("activated()"),
                     self.modifyMotorProperty)
        self.connect(self.helpContentsAction,SIGNAL("activated()"),
                     self.helpContents)
        self.connect(self.helpIndexAction,SIGNAL("activated()"),self.helpIndex)
        self.connect(self.helpAboutAction,SIGNAL("activated()"),self.helpAbout)

        self.connect(self.Cookie,SIGNAL("clicked()"),self.cookieCut)
        self.connect(self.Layer,SIGNAL("clicked()"),self.cookieLayer)
        self.connect(self.Bake,SIGNAL("clicked()"),self.cookieBake)
        self.connect(self.comboBox1,SIGNAL("activated(const QString&)"),self.elemChange)
        self.connect(self.AddAtoms,SIGNAL("clicked()"),self.addAtomStart)
        self.connect(self.Done,SIGNAL("clicked()"),self.addAtomDone)
        self.connect(self.Movie,SIGNAL("clicked()"),self.movie)
        self.connect(self.Bondedge,SIGNAL("clicked()"),self.bondEdge)
        self.connect(self.UBondall,SIGNAL("clicked()"),self.ubondAll)
        self.connect(self.UBondedge,SIGNAL("clicked()"),self.ubondEdge)
        self.connect(self.Unsel,SIGNAL("clicked()"),self.selectNone)
        self.connect(self.Copybut,SIGNAL("clicked()"),self.copyDo)
        self.connect(self.CopyBond,SIGNAL("clicked()"),self.copyBond)
        self.connect(self.KillBut,SIGNAL("clicked()"),self.killDo)

    # functions from the "File" menu
    def fileNew(self):
        pass
            
    def fileOpen(self):
        pass


    def fileSave(self):
        pass

    def fileSaveAs(self):
        pass

    def fileImage(self):
        pass

    # functions from the "Edit" menu

    def editUndo(self):
        print "Form1.editUndo(): Not implemented yet"

    def editRedo(self):
        print "Form1.editRedo(): Not implemented yet"

    def editCut(self):
        print "Form1.editCut(): Not implemented yet"

    def editCopy(self):
        print "Form1.editCopy(): Not implemented yet"

    def editPaste(self):
        print "Form1.editPaste(): Not implemented yet"

    def editFind(self):
        print "Form1.editFind(): Not implemented yet"

    # functions from the "Display" menu

    # this will pop up a new window onto the same assembly
    def dispNewView(self):
        pass
	

    # GLPane.ortho is checked in GLPane.paintGL
    def dispOrtho(self):
        pass

    def dispPerspec(self):
        pass

    # set display formats in whatever is selected,
    # or the GLPane global default if nothing is
    def dispDefault(self):
        pass

    def dispInvis(self):
        pass

    def dispVdW(self):
        pass

    def dispTubes(self):
        pass

    def dispCPK(self):
        pass

    def dispLines(self):
        pass

    def setdisplay(self, form):
        pass
  

    # set the color of the selected part(s) (molecule)
    # or the background color if no part is selected.
    # atom colors cannot be changed singly
    def dispColor(self):
        pass
      

    # functions from the "Grid" menu
    # this works by setting the griddraw method of the GLPane
    # to the appropriate function

    def gridNone(self):
        pass
     
    def gridSquare(self):
        pass

    def gridDiamond(self):
        pass

    def gridGraphite(self):
        print "Form1.gridGraphite(): Not implemented yet"

    # functions from the "Orientation" menu
    # points of view corresponding to the three crystal
    # surfaces of diamond

    # along one axis
    def orient100(self):
        pass

    # halfway between two axes
    def orient110(self):
        pass

    # equidistant from three axes
    def orient111(self):
        pass

    # functions from the "Select" menu

    def selectAll(self):
        pass

    def selectNone(self):
        pass

    def selectInvert(self):
        pass

    def selectConnected(self):
        pass


    def selectDoubly(self):
        pass


    # Functions from the "Make" menu

    # these functions (do or will) create small structures that
    # describe records to send to the simulator
    # they don't do much in Atom itself
    def makeGround(self):
        pass
      
    def makeHandle(self):
        print "Form1.makeHandle(): Not implemented yet"

    def makeMotor(self):
        pass

    def makeLinearMotor(self):
        pass


    def makeBearing(self):
        print "Form1.makeBearing(): Not implemented yet"

    def makeSpring(self):
        print "Form1.makeSpring(): Not implemented yet"

    def makeDyno(self):
        print "Form1.makeDyno(): Not implemented yet"

    def makeHeatsink(self):
        print "Form1.makeHeatsink(): Not implemented yet"

    # functions from the "Modify" menu

    # change surface atom types to eliminate dangling bonds
    # a kludgey hack
    def modifyPassivate(self):
        pass

    # add hydrogen atoms to each dangling bond
    def modifyHydrogenate(self):
        pass

    # form a new part (molecule) with whatever atoms are selected
    def modifySeparate(self):
        pass

    # Modify motor property
    def modifyMotorProperty(self):
        pass


    # Functions from the "Help" menu

    def helpContents(self):
        pass

    def helpIndex(self):
        print "Form1.helpIndex(): Not implemented yet"

    def helpAbout(self):
        print "Form1.helpAbout(): Not implemented yet"

    # functions from the buttons down the left side of the display

    # set up cookiecutter mode
    def cookieCut(self):
        pass


    # "push down" one nanometer to cut out the next layer
    def cookieLayer(self):
        pass


    # fill the shape created in the cookiecutter with actual
    # carbon atoms in a diamond lattice (including bonds)
    def cookieBake(self):
        pass

    # the elements combobox:
    # change selected atoms to the element selected
    def elemChange(self, string):
        pass

    # some unimplemented buttons:

    # turn on and off an "add atom with a mouse click" mode
    def addAtomStart(self):
        print "Form1.addAtomStart(): Not implemented yet"
    
    def addAtomDone(self):
        print "Form1.addAtomDone(): Not implemented yet"

    # create bonds where reasonable within selection
    def movie(self):

    # create bonds where reasonable between selected and unselected
    def bondEdge(self):
        print "Form1.bondEdge(): Not implemented yet"

    # (stolen button) turn on or off the axis icon
    def ubondAll(self):

    # break bonds between selected and unselected atoms
    def ubondEdge(self):
        print "Form1.ubondEdge(): Not implemented yet"

    # Make a copy of the selected part (molecule)
    # cannot copy individual atoms
    def copyDo(self):
        pass

    # 2BDone: make a copy of the selected part, move it, and bondEdge it,
    # having unselected the original and selected the copy.
    # the motion is to be the same relative motion done to a part
    # between copying and bondEdging it.
    def copyBond(self):
        print "Form1.copyBond(): Not implemented yet"

    # delete selected parts or atoms
    def killDo(self):
        pass

    # utility functions

    def colorchoose(self):
        pass


    def keyPressEvent(self, e):
        pass
