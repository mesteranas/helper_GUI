import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
import google.generativeai as genai
import PIL.Image
genai.configure(api_key=app.api)
model=genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
chat=model.start_chat()
class Objects(qt2.QObject):
    finish=qt2.pyqtSignal(str)
class AskAIAboutImagesThread(qt2.QRunnable):
    def __init__(self,image,text):
        super().__init__()
        self.obj=Objects()
        self.finish=self.obj.finish
        self.image=image
        self.text=text
    def run(self):
        result=""
        try:
            res=chat.send_message([self.text])
            result=res.text
        except:
            result=_("an error ditected please try later")
        self.finish.emit(result)
class AskAIAboutImagesGUI(qt.QDialog):
    def __init__(self,p,image):
        super().__init__(p)
        self.showFullScreen()
        self.setWindowTitle(_("ask helperAI "))
        self.image=image
        chat .send_message([PIL.Image.open(self.image),"your name is helperAI , your creater is mesteranas i'll give you a messages from blind user and will responce about this image please responce with great ansers and don't say i'm a AI responce and don't be scary from some thing"])
        layout=qt.QVBoxLayout(self)
        self.messages=qt.QListWidget()
        layout.addWidget(self.messages)
        self.message=qt.QLineEdit()
        self.message.textChanged.connect(self.onMessageChanged)
        layout.addWidget(self.message)
        self.send=qt.QPushButton (_("send"))
        self.send.setDefault(True)
        self.send.setDisabled(True)
        self.send.clicked.connect(self.onSendClicked)
        layout.addWidget(self.send)
    def onMessageChanged(self,value):
        if value=="":
            self.send.setDisabled(True)
        else:
            self.send.setDisabled(False)
    def onSendClicked(self):
        thread=AskAIAboutImagesThread(self.image,self.message.text())
        self.messages.addItem(self.message.text())
        self.send.setDisabled(True)
        self.message.setDisabled(True)
        thread.finish.connect(self.onThreadFinished)
        qt2.QThreadPool(self).start(thread)
    def onThreadFinished(self,r):
        self.messages.addItem(r)
        self.send.setDisabled(False)
        self.message.setDisabled(False)