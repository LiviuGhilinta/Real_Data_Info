import pytest
import os
import sys
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication
from main import MainWindow

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app

def test_init_ui(qapp):
    window = MainWindow()
    assert window.width() == 480
    assert window.height() == 320
    assert window.slider.count() == 4
    window.close()

def test_update_status(qapp):
    window = MainWindow()
    window.update_stats()

    assert "CPU Usage: " in window.copy.text()
    assert "%" in window.copy2.text()
    assert "Total:" in window.copy3.text()
    assert 0 <= window.disk_bar.value() <= 100

    window.close()

def test_slider_navigation(qapp):
    window = MainWindow()
    assert window.slider.currentIndex() == 0

    window.slider.slide_in_next()

    assert window.slider.active is True

    window.close()