# Copyright (c) 2004-2005 Nanorex, Inc.  All rights reserved.
"""
LinearMotorProp.py

$Id$
"""

from qt import *
from LinearMotorPropDialog import *
from VQT import V

class LinearMotorProp(LinearMotorPropDialog):
    def __init__(self, linearMotor, glpane):

        LinearMotorPropDialog.__init__(self)
        self.motor = linearMotor
        self.glpane = glpane
        self.setup()

    def setup(self):
        linearMotor = self.motor
            
        self.motor.originalColor = self.motor.normcolor
        
        self.nameLineEdit.setText(linearMotor.name)

        self.colorPixmapLabel.setPaletteBackgroundColor(
            QColor(int(linearMotor.normcolor[0]*255), 
                         int(linearMotor.normcolor[1]*255), 
                         int(linearMotor.normcolor[2]*255)))
                         
        self.stiffnessLineEdit.setText(str(linearMotor.stiffness))
        self.forceLineEdit.setText(str(linearMotor.force))
        
        self.axLineEdit.setText(str(linearMotor.axis[0]))
        self.ayLineEdit.setText(str(linearMotor.axis[1]))
        self.azLineEdit.setText(str(linearMotor.axis[2]))

        self.cxLineEdit.setText(str(linearMotor.center[0]))
        self.cyLineEdit.setText(str(linearMotor.center[1]))
        self.czLineEdit.setText(str(linearMotor.center[2]))
        
        strList = map(lambda i: linearMotor.atoms[i].element.symbol + str(i),
                                                range(0, len(linearMotor.atoms)))
        self.atomsComboBox.insertStrList(strList, 0)
        
        self.lengthLineEdit.setText(str(linearMotor.length)) # motor length
        self.widthLineEdit.setText(str(linearMotor.width)) # motor width
        self.sradiusLineEdit.setText(str(linearMotor.sradius)) # spoke radius

        self.applyPushButton.setEnabled(False)
        

    #########################
    # Change linear motor color
    #########################
    def changeLinearMotorColor(self):

        color = QColorDialog.getColor(
            QColor(int(self.motor.normcolor[0]*255), 
                         int(self.motor.normcolor[1]*255), 
                         int(self.motor.normcolor[2]*255)),
                         self, "ColorDialog")
                        
        if color.isValid():
            self.colorPixmapLabel.setPaletteBackgroundColor(color)
            self.motor.color = self.motor.normcolor = (color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0)
            self.glpane.paintGL()


    #################
    # OK Button
    #################
    def accept(self):
        self.applyButtonPressed()
        self.motor.cancelled = False
        QDialog.accept(self)

    #################
    # Cancel Button
    #################
    def reject(self):
	    QDialog.reject(self)
	    self.motor.normcolor = self.motor.originalColor
        
    #################
    # Apply Button
    #################	
    def applyButtonPressed(self):
        
        self.motor.force = float(str(self.forceLineEdit.text()))
        self.motor.stiffness = float(str(self.stiffnessLineEdit.text()))

        self.motor.axis[0] = float(str(self.axLineEdit.text()))
        self.motor.axis[1] = float(str(self.ayLineEdit.text()))
        self.motor.axis[2] = float(str(self.azLineEdit.text()))

        self.motor.center[0] = float(str(self.cxLineEdit.text()))
        self.motor.center[1] = float(str(self.cyLineEdit.text()))
        self.motor.center[2] = float(str(self.czLineEdit.text()))
      
        self.motor.length = float(str(self.lengthLineEdit.text())) # motor length
        self.motor.width = float(str(self.widthLineEdit.text())) # motor width
        self.motor.sradius = float(str(self.sradiusLineEdit.text())) # spoke radius
        
        text =  QString(self.nameLineEdit.text())        
        text = text.stripWhiteSpace() # make sure name is not just whitespaces
        if text: self.motor.name = str(text)
        self.nameLineEdit.setText(self.motor.name)
        self.motor.assy.w.win_update() # Update model tree
        self.motor.assy.changed()
                        
        self.applyPushButton.setEnabled(False)
	
    def propertyChanged(self):
        self.applyPushButton.setEnabled(True)	
