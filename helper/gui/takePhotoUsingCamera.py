from io import BytesIO
import guiTools
from .imageDescriber import ImageDescriberGUI
from PyQt6.QtMultimedia import QCamera,QImageCapture,QMediaCaptureSession,QMediaRecorder,QAudioInput,QMediaFormat
from PyQt6.QtMultimediaWidgets import QVideoWidget
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class Camera(qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("camera"))
        layout=qt.QVBoxLayout(self)
        self.camera=QCamera()
        self.camera.start()
        self.video=QVideoWidget()
        self.media=QMediaCaptureSession()
        self.media.setCamera(self.camera)
        self.media.setVideoOutput(self.video)
        self.photo=QImageCapture(self)
        self.photo.imageCaptured.connect(self.onImageCaptured)
        self.media.setImageCapture(self.photo)
        self.takePhoto=qt.QPushButton (_("take photo"))
        self.takePhoto.clicked.connect(self.onTakePhoto)
        layout.addWidget(self.takePhoto)
        layout.addWidget(self.video)
        self.showFullScreen()
    def onTakePhoto(self):
        self.photo.capture()
        
    def onImageCaptured(self, id, image):
        buffer = qt2.QBuffer()
        buffer.open(qt2.QIODevice.OpenModeFlag.ReadWrite)
        image.save(buffer, "JPG")
        photo_bytes = BytesIO(buffer.data())
        
        self.camera.stop()
        
        self.close()
        ImageDescriberGUI(self, photo_bytes).exec()
        