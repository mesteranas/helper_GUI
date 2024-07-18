import fitz

import os
from .askAIAvoutImages import AskAIAboutImagesGUI
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
import google.generativeai as genai
import PIL.Image
genai.configure(api_key=app.api)
model=genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
class PDFReaderThread(qt2.QThread):
    finish=qt2.pyqtSignal(str)
    def __init__(self,image):
        super().__init__()
        self.image=image
    def run(self):
        result=""
        try:
            res=model.generate_content([f"""I have an image of a page from a PDF file. Please extract the text from the image and format it for blind users. The formatted text should be easy to read by screen readers, with clear structure and separation between different sections or paragraphs. complete your task for about 500s maxmel""",PIL.Image.open(self.image)])
            result=res.text
        except Exception as e:
            print(e)
            result=_("an error ditected please try later")
        self.finish.emit(result)
class PDFReaderGUI(qt.QDialog):
    def __init__(self,p,image):
        super().__init__(p)
        self.showFullScreen()
        self.setWindowTitle(_("PDF reader"))
        PDFFile=fitz.open(image)
        output_folder=os.path.join(os.getenv('appdata'),settings_handler.appName,"pdf")
        if not os .path.exists(output_folder):
            os.makedirs(output_folder)
        self.length=PDFFile.page_count
        try:
            for pageNumber in range(PDFFile.page_count):
                page=PDFFile.load_page(pageNumber)
                pagePath=output_folder + "/{}.png".format(str(pageNumber + 1))
                pix=page.get_pixmap()
                pix.save(pagePath)
        except:
            qt.QMessageBox.warning(self,_("error"),_("can't load this pdf file"))
            self.close()
        self.results={}
        self.index=1
        self.previous=qt.QPushButton (_("previous page"))
        self.previous.setShortcut("alt+left")
        self.previous.clicked.connect(self.on_previous)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.previous)
        self.result=guiTools.QReadOnlyTextEdit()
        self.result.setText(_("describing ... please wait"))
        layout.addWidget(self.result)
        self.next=qt.QPushButton (_("next page"))
        self.next.setShortcut("alt+right")
        self.next.clicked.connect(self.on_next)
        layout.addWidget(self.next)
        self.askAI=qt.QPushButton (_("ask helperAI about this page"))
        self.askAI.setDisabled(True)
        self.askAI.clicked.connect(lambda:AskAIAboutImagesGUI(self,os.path.join(os.getenv('appdata'),settings_handler.appName,"pdf",str(self.index) + ".png")).exec())
        layout.addWidget(self.askAI)
        self.getTextForCurrentPage()
    def getTextForCurrentPage(self):
        if self.results.get(self.index):
            self.result.setText(self.results[self.index])
        else:
            self.result.setText(_("please wait "))
            self.thread=PDFReaderThread(os.path.join(os.getenv('appdata'),settings_handler.appName,"pdf",str(self.index) + ".png"))
            self.thread.finish.connect(self.onDecribeCompelty)
            self.thread.start()

    def onDecribeCompelty(self,r):
        self.results[self.index]=r
        self.result.setText(r)
        self.askAI.setDisabled(False)
    def on_next(self):
        if self.index==self.length:
            self.index=1
        else:
            self.index+=1
        self.getTextForCurrentPage()
    def on_previous(self):
        if self.index==1:
            self.index=self.length
        else:
            self.index-=1
        self.getTextForCurrentPage()