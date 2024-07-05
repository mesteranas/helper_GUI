import guiTools
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import QUrl
import guiTools.clikboard
from settings import *
language.init_translation()
class openLink (qt.QDialog):
    def __init__(self,p,link):
        super().__init__(p)
        self.setWindowTitle(_("Open link dialog"))
        label=qt.QLabel(_("link"))
        self.link=guiTools.QReadOnlyTextEdit()
        self.link.setText(link)
        self.link.setAccessibleName(_("link"))
        self.open=guiTools.QPushButton(_("open link "))
        self.open.setDefault(True)
        self.open.clicked.connect(self.fopen)
        self.copy=guiTools.QPushButton(_("copy link"))
        self.copy.clicked.connect(self.fcopy)
        layout=qt.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.link)
        layout.addWidget(self.open)
        layout.addWidget(self.copy)
        self.setLayout(layout)
    def fopen(self):
        qt1.QDesktopServices.openUrl(QUrl(self.link.toPlainText()))
        self.close()
    def fcopy(self):
        guiTools.clikboard.copyText(self.link.toPlainText())
        self.close()
def OpenLink (p,Link):
	openLink (p,Link).exec()