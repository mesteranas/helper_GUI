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
class ImageDescriberThread(qt2.QThread):
    finish=qt2.pyqtSignal(str)
    def __init__(self,image):
        super().__init__()
        self.image=image
    def run(self):
        result=""
        try:
            res=model.generate_content([f"""The following is a detailed description of an image intended to provide a vivid and comprehensive understanding for blind users. Describe the scene, objects, actions, and any other relevant details with specific locations, distances, and sizes where possible. Clearly and concisely describe each element to help the listener visualize the scene. If objects are unclear, indicate this. If text is present in the image, output the text along with its location.
                                      
[IMAGE DESCRIPTION START]
The image shows a bustling city street during the day. On the left side of the image, approximately 100 meters from the bottom, there is a row of tall buildings with glass windows reflecting the sunlight. The street is lined with trees spaced about 20 meters apart, each around 10 meters tall. There are people walking on the sidewalk, some holding shopping bags; the sidewalk is about 3 meters wide.
A yellow taxi is parked at the curb on the left side of the street, around 50 meters from the bottom of the image, and a red double-decker bus is driving down the street, approximately 150 meters from the bottom of the image. In the background, the sky is clear with a few scattered clouds.
A street vendor is selling hot dogs from a cart near the corner of the street, positioned about 30 meters from the bottom left corner. A group of children is playing near a fountain in the park, visible in the distance on the right side of the image, roughly 200 meters from the bottom right corner. The fountain is large, with water cascading down multiple tiers, and the children are running around it, laughing and playing. Some objects in the background are not clear.
[IMAGE DESCRIPTION END]
Provide a similarly detailed description for the given image.""",PIL.Image.open(self.image)])
            result=res.text
        except:
            result=_("an error ditected please try later")
        self.finish.emit(result)
class ImageDescriberGUI(qt.QDialog):
    def __init__(self,p,image):
        super().__init__(p)
        self.showFullScreen()
        self.setWindowTitle(_("image describer"))
        self.thread=ImageDescriberThread(image)
        self.thread.finish.connect(self.onDecribeCompelty)
        self.thread.start()
        layout=qt.QVBoxLayout(self)
        self.result=guiTools.QReadOnlyTextEdit()
        self.result.setText(_("describing ... please wait"))
        layout.addWidget(self.result)
        self.askAI=qt.QPushButton (_("ask helperAI about this image"))
        self.askAI.setDisabled(True)
        self.askAI.clicked.connect(lambda:AskAIAboutImagesGUI(self,image).exec())
        layout.addWidget(self.askAI)
    def onDecribeCompelty(self,r):
        self.result.setText(r)
        self.askAI.setDisabled(False)