import sys


from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton,QVBoxLayout,QProgressBar,QStackedWidget,QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QEasingCurve, QPoint, QPropertyAnimation,QParallelAnimationGroup, QTimer
from PyQt5.QtGui import QFont,QFontDatabase,QPixmap,QIcon,QPainter,QColor,QPen
import psutil






class SlidingStackedWidget(QStackedWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.label1 = QLabel(self)
        self.direction = Qt.Horizontal
        self.speed = 350
        self.animation_type = QEasingCurve.OutCubic
        self.now = 0
        self.next = 0
        self.wrap = True
        self.pnow = QPoint(0,0)
        self.active = False

        self.start_pos = None
        self.min_swipe_distance = 50
  

 
    def slide_in_next(self):
        cur = self.currentIndex()
        if cur < self.count() - 1:
             self.slide_in_index(cur + 1)
        elif self.wrap:
             self.slide_in_index(0)

    def slide_in_prev(self):
        cur = self.currentIndex()
        if cur > 0:
              self.slide_in_index(cur - 1)
        elif self.wrap:
             self.slide_in_index(self.count() - 1)

    def slide_in_index(self,index):
        if self.active or index == self.currentIndex():
            return
        self.active = True
        width  = self.frameGeometry().width()
        height = self.frameGeometry().height()
        if index > self.currentIndex():
             offset_x = width
        else:
             offset_x = -width
        next = self.widget(index)
        now = self.currentWidget()
        next.setGeometry(0,0,width,height)
        next.move(offset_x,0)
        next.show()
        next.raise_()

        anim_now = QPropertyAnimation(now, b"pos")
        anim_now.setDuration(self.speed)
        anim_now.setEasingCurve(self.animation_type)
        anim_now.setStartValue(QPoint(0,0))
        anim_now.setEndValue(QPoint(-offset_x,0))

        anim_next = QPropertyAnimation(next, b"pos")
        anim_next.setDuration(self.speed)
        anim_next.setEasingCurve(self.animation_type)
        anim_next.setStartValue(QPoint(offset_x,0))
        anim_next.setEndValue(QPoint(0,0))     

        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(anim_now)
        self.anim_group.addAnimation(anim_next) 

        def animation_finished():
            self.setCurrentIndex(index)
            now.hide()
            now.move(0,0)
            self.active = False

        self.anim_group.finished.connect(animation_finished)
        self.anim_group.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
             self.drag_start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drag_start_pos is not None:
            delta_x = event.pos().x() - self.drag_start_pos.x()

            if abs(delta_x) >= self.min_swipe_distance:
                if delta_x < 0:
                     self.slide_in_next()
                else:
                     self.slide_in_prev()
            self.drag_start_pos = None
        super().mouseReleaseEvent(event)

def createCardboard(title,details):
        widget = QWidget()
        widget.setStyleSheet(f"background-color:black;  color : #13b9c2 ")
        layout  = QVBoxLayout(widget)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"font-size: 20px; font-weight: bold; margin-top: 10px;")
        lbl_title.setAlignment(Qt.AlignCenter)

        lbl_desc = QLabel(details)
        lbl_desc.setStyleSheet("font-size: 15px; margin-bottom: 10px;")
        lbl_desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_desc)
        return widget

def createProgressCardboard(title,details):
        widget = QWidget()
        widget.setStyleSheet(f"background-color:black;  color : #13b9c2 ")
        layout  = QVBoxLayout(widget)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"font-size: 20px; font-weight: bold; margin-top: 10px;")
        lbl_title.setAlignment(Qt.AlignCenter)

        lbl_desc = QLabel(details)
        lbl_desc.setStyleSheet("font-size: 15px; margin-bottom: 2px;")
        lbl_desc.setAlignment(Qt.AlignCenter)
        progressbar = QProgressBar()
        progressbar.setRange(0,100)
        progressbar.setFixedHeight(15)
        progressbar.setFixedWidth(400)
        progressbar.setStyleSheet("""
                    QProgressBar {
                        border: 2px solid #13b9c2;
                        border-radius: 5px;
                        text-align: center;
                        color: white;
                        font-weight: bold;
                    }
                    QProgressBar::chunk {
                        background-color: #13b9c2;
                    }
                """)
        progressbar.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_desc)
        layout.addWidget(progressbar,alignment=Qt.AlignCenter)
        return widget,lbl_desc,progressbar

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(480,320)
        self.setStyleSheet("background-color: #1f2324")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10,10,10,10)
        self.slider = SlidingStackedWidget(self)
        self.first_page = createCardboard("Hello", ":)")
        self.page1 = createCardboard("CPU",f"CPU Usage: {str(psutil.cpu_percent(interval=None))}% , {psutil.cpu_freq(percpu=False).current/1000} GHz ")
        self.page2 = createCardboard("RAM","testul2")
        self.page3, self.disk_label, self.disk_bar = createProgressCardboard("Memory","")
        self.slider.addWidget(self.first_page)
        self.slider.addWidget(self.page1)
        self.slider.addWidget(self.page2)
        self.slider.addWidget(self.page3)
        main_layout.addWidget(self.slider)

        self.copy = self.page1.layout().itemAt(1).widget()
        self.copy2 = self.page2.layout().itemAt(1).widget()
        self.copy3 = self.page3.layout().itemAt(1).widget()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    def update_stats(self):
        self.copy.setText(f"CPU Usage: {str(psutil.cpu_percent(interval=None))}% , {psutil.cpu_freq(percpu=False).current/1000} GHz")
        disk= psutil.disk_usage('/')[3]
        self.disk_bar.setValue(int(disk))
        self.copy2.setText(f"{psutil.virtual_memory()[2]:.2f}% {(psutil.virtual_memory()[3]/1024**3):.2f}/{(psutil.virtual_memory()[0]/1024**3):.2f} GB")
        self.copy3.setText(
    f"Total: {(psutil.disk_usage('/')[0] / (1024**3) if psutil.disk_usage('/')[0] >= 1024**3 else psutil.disk_usage('/')[0] / (1024**2)):.2f} {'GB' if psutil.disk_usage('/')[0] >= 1024**3 else 'MB'}, "
    f"Used: {(psutil.disk_usage('/')[1] / (1024**3) if psutil.disk_usage('/')[1] >= 1024**3 else psutil.disk_usage('/')[1] / (1024**2)):.2f} {'GB' if psutil.disk_usage('/')[1] >= 1024**3 else 'MB'}, "
    f"Free: {(psutil.disk_usage('/')[2] / (1024**3) if psutil.disk_usage('/')[2] >= 1024**3 else psutil.disk_usage('/')[2] / (1024**2)):.2f} {'GB' if psutil.disk_usage('/')[2] >= 1024**3 else 'MB'}"
)
if __name__ =='__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 
