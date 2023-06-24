import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class VideoWidget(QWidget):
    def __init__(self, video_path, labels, parent=None):
        super(VideoWidget, self).__init__(parent)
        
        self.video_path = video_path
        self.labels = labels
        self.video_capture = cv2.VideoCapture(self.video_path)
        self.frame_rate = int(1000 / self.video_capture.get(cv2.CAP_PROP_FPS))
        
        self.current_frame = 0
        
        self.video_label = QLabel()
        self.info_label = QLabel()
        
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(self.frame_rate)
        
    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.current_frame += 1
            
            # Обработка текущего кадра и определение класса техники
            
            # TODO: Реализовать обработку кадра и определение класса техники
            
            # Вывод текущего кадра с классом техники на виджет
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            img = QPixmap.fromImage(img)
            self.video_label.setPixmap(img.scaled(self.video_label.size(), Qt.KeepAspectRatio))
            
            # Вывод информации о вхождении и выхождении техники
            # TODO: Реализовать вывод информации о вхождении и выхождении техники на info_label
            
    def closeEvent(self, event):
        self.video_capture.release()
        self.timer.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Загрузка видео и меток
    video_path = "path/to/video.mp4"
    labels = {
        1: "грузовой автомобиль",
        2: "трактор",
        3: "экскаватор",
        4: "подъемный кран"
    }
    
    # Создание виджета и запуск приложения
    widget = VideoWidget(video_path, labels)
    widget.show()
    
    sys.exit(app.exec_())
