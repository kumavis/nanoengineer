# Copyright (c) 2004 Nanorex, Inc.  All rights reserved.
from qt import *
from StatPropDialog import *
from VQT import V

class StatProp(StatPropDialog):
    def __init__(self, stat, glpane):

        StatPropDialog.__init__(self)
        self.stat = stat
        self.glpane = glpane
        self.setup()

    def setup(self):
        stat = self.stat
        
        self.stat.originalColor = self.stat.color
        
        self.nameLineEdit.setText(stat.name)
        self.tempSpinBox.setValue(stat.temp)

        self.colorPixmapLabel.setPaletteBackgroundColor(
            QColor(int(stat.color[0]*255), 
                         int(stat.color[1]*255), 
                         int(stat.color[2]*255)))

        strList = map(lambda i: stat.atoms[i].element.symbol + str(i),
                                                range(0, len(stat.atoms)))
        self.atomsComboBox.insertStrList(strList, 0)

        self.applyPushButton.setEnabled(False)
        

    #########################
    # Change linear stat color
    #########################
    def changeStatColor(self):

        color = QColorDialog.getColor(
            QColor(int(self.stat.color[0]*255), 
                         int(self.stat.color[1]*255), 
                         int(self.stat.color[2]*255)),
                         self, "ColorDialog")
                        
        if color.isValid():
            self.colorPixmapLabel.setPaletteBackgroundColor(color)
            self.stat.color = (color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0)
            self.glpane.paintGL()


    #################
    # OK Button
    #################
    def accept(self):
        self.applyButtonPressed()
        QDialog.accept(self)

    #################
    # Cancel Button
    #################
    def reject(self):
	    QDialog.reject(self)
	    self.stat.color = self.stat.originalColor

    #################
    # Apply Button
    #################	
    def applyButtonPressed(self):
        
        self.stat.name = self.nameLineEdit.text()

        self.applyPushButton.setEnabled(False)
	
    def propertyChanged(self):
        self.applyPushButton.setEnabled(True)	