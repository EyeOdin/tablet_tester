# Tablet Tester is a Krita plugin to test Tablet Inputs.
# Copyright (C) 2022  Ricardo Jeremias.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Import Krita
from krita import *
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, uic
import os.path
# Variables
DOCKER_NAME = "Tablet Tester"

class TabletTester_Docker(DockWidget):
    """
    Tablet Tester
    """

    def __init__(self):
        super(TabletTester_Docker, self).__init__()

        self.setWindowTitle(DOCKER_NAME)
        self.window = QWidget()
        self.layout = uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + '/tablet_tester_docker.ui', self.window)
        self.setWidget(self.window)

        # Widget
        self.widget = Input(self.layout.widget)
        self.widget.Set_Layout(self.layout)

        # Style Sheet
        alpha = str("background-color: rgba(0, 0, 0, 50); ")
        self.layout.widget.setStyleSheet(alpha)
        self.layout.gpos.setStyleSheet(alpha)
        self.layout.gposf.setStyleSheet(alpha)
        self.layout.unique_id.setStyleSheet(alpha)
        self.layout.button.setStyleSheet(alpha)
        self.layout.buttons.setStyleSheet(alpha)
        self.layout.device.setStyleSheet(alpha)
        self.layout.modifiers.setStyleSheet(alpha)
        self.layout.pointer_type.setStyleSheet(alpha)
        self.layout.spontaneous.setStyleSheet(alpha)
        self.layout.time_stamp.setStyleSheet(alpha)
        self.layout.type.setStyleSheet(alpha)

    def canvasChanged(self, canvas):
        pass


class Input(QWidget):

    def __init__(self, parent):
        super(Input, self).__init__(parent)
        self.layout = None
        self.event_x = 0
        self.event_y = 0
        self.pressure = 0

    def sizeHint(self):
        return QtCore.QSize(5000, 5000)

    def Set_Layout(self, layout):
        self.layout = layout

    def tabletEvent(self, event):
        # Display
        self.event_x = event.x()
        self.event_y = event.y()

        # Tablet Event
        if self.layout != None:
            # 1
            self.layout.x.setValue(event.x())
            self.layout.y.setValue(event.y())
            self.layout.gx.setValue(event.globalX())
            self.layout.gy.setValue(event.globalY())
            self.layout.gpos.setText("Global X : " + str(event.globalPos().x()) + " Global Y : " + str(event.globalPos().y()) )
            self.layout.gposf.setText("Global X F : " + str(event.globalPosF().x()) + " Global Y F : " + str(event.globalPosF().y()) )
            # 2
            self.layout.pressure.setValue(event.pressure())
            self.layout.tpressure.setValue(event.tangentialPressure())
            self.layout.rotation.setValue(event.rotation())
            self.layout.x_tilt.setValue(event.xTilt())
            self.layout.y_tilt.setValue(event.yTilt())
            self.layout.z.setValue(event.z())
            # 3
            self.layout.unique_id.setText("unique ID : " + str(event.uniqueId()))
            self.layout.button.setText("button : " + str(event.button()))
            self.layout.buttons.setText("buttons : " + str(event.buttons()))
            self.layout.device.setText("device : " + str(event.device()))
            self.layout.modifiers.setText("modifiers : " + str(event.modifiers()))
            self.layout.pointer_type.setText("pointer type : " + str(event.pointerType()))
            self.layout.spontaneous.setText("spontaneous : " + str(event.spontaneous()))
            self.layout.time_stamp.setText("time stamp : " + str(event.timestamp()))
            self.layout.type.setText("type : " + str(event.type()))
            # Variables
            self.pressure = event.pressure()
            self.Type_Number(event)
        else:
            self.pressure = 0

        # if event.type() == Qt.QEvent.TabletEnterProximity:
        #     self.layout.label.setText("TabletEnterProximity")
        # if event.type() == Qt.QEvent.TabletLeaveProximity:
        #     self.layout.label.setText("TabletLeaveProximity")

        self.update()

    def Type_Number(self, event):
        num = event.type()
        if num == 92:
            self.layout.label.setText("TabletPress")
        if num == 93:
            self.layout.label.setText("TabletRelease")
        if num == 87:
            self.layout.label.setText("TabletMove")
        if num == 171:
            self.layout.label.setText("TabletEnterProximity")
        if num == 172:
            self.layout.label.setText("TabletLeaveProximity")
        if num == 219:
            self.layout.label.setText("TabletTrackingChange")

    # def TabletPress(self, event):
    #     self.layout.label.setText("TabletPress")
    # def TabletRelease(self, event):
    #     self.layout.label.setText("TabletRelease")
    # def TabletMove(self, event):
    #     self.layout.label.setText("TabletMove")
    # def TabletEnterProximity(self, event):
    #     self.layout.label.setText("TabletEnterProximity")
    # def TabletLeaveProximity(self, event):
    #     self.layout.label.setText("TabletLeaveProximity")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QBrush(QColor("#e5e5e5")))

        factor1 = 50 * self.pressure
        factor2 = 2 * factor1
        size_x = self.event_x  - (factor1)
        size_y = self.event_y  - (factor1)
        painter.drawRect(size_x, size_y, factor2, factor2)
