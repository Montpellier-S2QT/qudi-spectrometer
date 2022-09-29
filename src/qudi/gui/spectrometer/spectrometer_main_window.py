# -*- coding: utf-8 -*-

__all__ = ['SpectrometerMainWindow']

from PySide2 import QtGui, QtCore, QtWidgets
from qtpy import uic

import os

class SpectrometerMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        this_dir = os.path.dirname(__file__)
        ui_file = os.path.join(this_dir, 'ui_mainwindow.ui')
        super().__init__()
        uic.loadUi(ui_file, self)
        self.show()

class SettingsTab(QtWidgets.QWidget):

    def __init__(self):
        this_dir = os.path.dirname(__file__)
        ui_file = os.path.join(this_dir, 'ui_settings_tab.ui')
        super().__init__()
        uic.loadUi(ui_file, self)
        self.show()

class ImageTab(QtWidgets.QWidget):

    def __init__(self):
        this_dir = os.path.dirname(__file__)
        ui_file = os.path.join(this_dir, 'ui_image_tab.ui')
        super().__init__()
        uic.loadUi(ui_file, self)
        self.show()

class AlignmentTab(QtWidgets.QWidget):

    def __init__(self):
        this_dir = os.path.dirname(__file__)
        ui_file = os.path.join(this_dir, 'ui_alignment_tab.ui')

        # Load it
        super().__init__()
        uic.loadUi(ui_file, self)
        self.show()

class SpectrumTab(QtWidgets.QWidget):
    def __init__(self):
        this_dir = os.path.dirname(__file__)
        ui_file = os.path.join(this_dir, 'ui_spectrum_tab.ui')
        super().__init__()
        uic.loadUi(ui_file, self)
        self.show()