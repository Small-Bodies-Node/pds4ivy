# Licensed under a 3-clause BSD style license - see LICENSE.rst

import sys
import os
import logging

from ginga.qtw.QtHelp import QtGui, QtCore
from ginga.qtw.ImageViewCanvasQt import ImageViewCanvas

from .PDS4LabelHandler import PDS4LabelHandler


class PDS4ImageViewer(QtGui.QMainWindow):

    def __init__(self, logger):
        super(PDS4ImageViewer, self).__init__()
        self.logger = logger

        pi = ImageViewCanvas(self.logger, render='widget')
        pi.enable_autocuts('on')
        pi.set_autocut_params('zscale')
        pi.enable_autozoom('on')
        pi.set_callback('drag-drop', self.drop_file)
        pi.set_bg(0.2, 0.2, 0.2)
        pi.ui_setActive(True)
        pi.enable_draw(False)
        self.pds4image = pi

        bd = pi.get_bindings()
        bd.enable_all(True)

        w = pi.get_widget()
        w.resize(512, 512)

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(QtCore.QMargins(2, 2, 2, 2))
        vbox.setSpacing(1)
        vbox.addWidget(w, stretch=1)

        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(QtCore.QMargins(4, 2, 4, 2))

        wopen = QtGui.QPushButton("Open File")
        wopen.clicked.connect(self.open_file)
        wquit = QtGui.QPushButton("Quit")
        wquit.clicked.connect(self.quit)

        hbox.addStretch(1)
        for w in (wopen, wquit):
            hbox.addWidget(w, stretch=0)

        hw = QtGui.QWidget()
        hw.setLayout(hbox)
        vbox.addWidget(hw, stretch=0)

        vw = QtGui.QWidget()
        self.setCentralWidget(vw)
        vw.setLayout(vbox)

    def load_file(self, filepath):
        from ginga.AstroImage import AstroImage
        image = AstroImage(ioclass=PDS4LabelHandler)
        image.load_file(filepath)
        self.pds4image.set_image(image)
        self.setWindowTitle(filepath)

    def open_file(self):
        res = QtGui.QFileDialog.getOpenFileName(self, "Open PDS4 label",
                                                ".", "PDS4 labels (*.xml)")
        if isinstance(res, tuple):
            fileName = res[0]
        else:
            fileName = str(res)
        if len(fileName) != 0:
            self.load_file(fileName)

    def drop_file(self, pds4image, paths):
        fileName = paths[0]
        self.load_file(fileName)

    def quit(self, *args):
        self.logger.info("Attempting to shut down the application...")
        self.deleteLater()
