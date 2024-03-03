import os
import time
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QFont
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import webbrowser


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.money = 10000
        self.click = 1
        self.upgrade_1 = 100
        self.price_razden = 10000
        self.setWindowTitle("Кликер: раздень шачира")
        self.setGeometry(100, 100, 500, 400)
        self.initUI()
        self.initAudio()



    def initAudio(self):
        # Инициализация аудио
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        music_file = "background_music.mp3"
        if os.path.exists(music_file):
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(music_file)))
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            self.player.setPlaylist(self.playlist)
            self.player.setVolume(10)
            self.player.play()

    def initUI(self):
        # Создание виджетов
        self.buttonclick = QPushButton(f"Подобрать {self.click} рублей", self)
        self.button_razden = QPushButton(f"Раздеть шачира - {self.price_razden} рублей", self)
        self.label = QLabel("Быстрее раздень ШАЧИРА!!!", self)
        self.buttonupgrade_1 = QPushButton(f"Улучшение - {self.upgrade_1} рублей", self)

        # Размещение виджетов с помощью менеджера компоновки
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.buttonclick)
        layout.addWidget(self.buttonupgrade_1)
        layout.addWidget(self.button_razden)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Привязка событий к кнопкам
        self.buttonclick.clicked.connect(self.click_btn)
        self.buttonupgrade_1.clicked.connect(self.upgrade_1_action)
        self.button_razden.clicked.connect(self.razdet_shachira)

        # Установка размеров и шрифтов для кнопок
        self.set_button_properties(self.button_razden)
        self.set_button_properties(self.buttonclick)
        self.set_button_properties(self.buttonupgrade_1)

        # Установка размеров и шрифтов для метки
        self.label.setGeometry(100, 250, 400, 50)
        self.label.setFont(QFont("Arial", 14))

    def set_button_properties(self, button):
        button.setGeometry(50, 150, 200, 50)
        button.setFont(QFont("Arial", 12))

    def click_btn(self):
        # Обработка нажатия кнопки
        self.money += self.click
        self.label.setText(f"Рублей заработано: {self.money}")
        self.buttonupgrade_1.setText(f"Улучшение - {self.upgrade_1} рублей")
        self.button_razden.setText(f"Раздеть шачира - {self.price_razden} рублей")
        self.buttonclick.setText(f"Подобрать {self.click} рублей")

    def upgrade_1_action(self):
        # Обработка нажатия кнопки улучшения
        if self.upgrade_1 <= self.money:
            self.money -= self.upgrade_1
            self.upgrade_1 *= 2
            self.click += 2
            self.buttonupgrade_1.setText(f"Улучшение - {self.upgrade_1} рублей")
            self.label.setText(f"Рублей заработано: {self.money}")
            self.buttonclick.setText(f"Подобрать {self.click} рублей")
        else:
            self.buttonupgrade_1.setText(f"Не хватает {self.upgrade_1 - self.money} рублей")

    def razdet_shachira(self):
        # Обработка нажатия кнопки раздевания шачира
        if self.price_razden <= self.money:
            self.money -= self.price_razden

            self.label.setText(f"Шачир считает деньги, подождите...")
            self.label.repaint()

            razden_sound = QMediaPlayer()
            razden_sound.setMedia(
                QMediaContent(QUrl.fromLocalFile("money.mp3")))
            razden_sound.setVolume(50)
            razden_sound.play()
            time.sleep(4)

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(1, None)

            url = "https://youtu.be/90jGr1MNrjI?t=18"
            try:
                webbrowser.open(url, new=2)
            except Exception as e:
                print("Ошибка открытия веб-страницы:", e)

            self.button_razden.setText(f"Раздеть шачира - {self.price_razden} рублей")
            self.label.setText(f"Рублей заработано: {self.money}")
        else:
            self.button_razden.setText(f"Не хватает {self.price_razden - self.money} рублей")

    def closeEvent(self, event):
        # Обработка события закрытия окна приложения
        self.player.stop()
        event.accept()


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()