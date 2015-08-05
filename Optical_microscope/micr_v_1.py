# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
from SimpleCV import *


class MainWidget(QtGui.QMainWindow):
    webcam = None
    is_start = False
    list_menu = [{'name': u'Файл',
                  'type': 'menu',
                  'multiply': 0,
                  'split_line': 0},
                 {'name': u'Помощь',
                  'type': 'menu',
                  'multiply': 0,
                  'split_line': 0},
                 {'name': u'Информация',
                  'type': 'menu',
                  'multiply': 0,
                  'split_line': 0},
                 {'name': u'Сохранить изображение',
                  'type': 'action',
                  'menu': 0,
                  'multiply': 0,
                  'split_line': 1},
                 {'name': u'Сгенерировать отчет',
                  'type': 'action',
                  'menu': 0,
                  'multiply': 0,
                  'split_line': 0},
                 {'name': u'Краткое руководство по микроскопу',
                  'type': 'action',
                  'menu': 1,
                  'multiply': 0,
                  'split_line': 0},
                 {'name': u'Краткое руководство по программе',
                  'type': 'action',
                  'menu': 1,
                  'multiply': 0,
                  'split_line': 0},
                 {'name': u'Авторы программы',
                  'type': 'action',
                  'menu': 2,
                  'multiply': 0,
                  'split_line': 0}]

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent=None)
        desktop = QtGui.QApplication.desktop()
        x = desktop.width()
        y = desktop.height()
        self.move(x / 2, y / 2)
        self.setWindowTitle("Project GUI micro")
        self.centralwidget = QtGui.QWidget(self)
        self.vl_main = QtGui.QVBoxLayout(self.centralwidget)
        self.cb_camera = QtGui.QComboBox()
        self.cb_camera.addItems(['0', '1', '2', '3'])
        self.vl_main.addWidget(self.cb_camera)
        self.label = QtGui.QLabel()
        self.vl_main.addWidget(self.label)
        self.hl_button = QtGui.QHBoxLayout()
        self.button_start = QtGui.QPushButton('Start video')
        self.button_start.setCheckable(True)
        self.button_save = QtGui.QPushButton('Save picture')
        self.hl_button.addWidget(self.button_start)
        self.hl_button.addWidget(self.button_save)
        self.vl_main.addLayout(self.hl_button)
        self.setCentralWidget(self.centralwidget)
        self.menubar = self.menuBar()
        self.set_menu()  # Вынесем назначения элементов меню в отдельную функцию для лучшей читаемости кода
        self.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusBar().showMessage('Ready for action')
        # Назначим действия для каждой кнопки
        QtCore.QObject.connect(self.button_start, QtCore.SIGNAL('toggled(bool)'), lambda: self.start_video(x))
        QtCore.QObject.connect(self.button_save, QtCore.SIGNAL('clicked()'), self.save_pict)

    def set_menu(self):
        # Назначаем элементы главного меню
        for i in range(len(self.list_menu)):
            if self.list_menu[i]['type'] == 'menu':
                self.menu = QtGui.QMenu(self.list_menu[i]['name'], self.menubar)
                self.list_menu[i]['type'] = self.menu
                self.menubar.addMenu(self.menu)
            elif self.list_menu[i]['type'] == 'action':
                self.action = QtGui.QAction(self.list_menu[i]['name'], self.menubar)
                # Назначаем действие для каждого активного элемента меню
                if i == 3:
                    self.action.triggered.connect(self.save_pict)
                elif i == 4:
                    pass
                elif i == 5:
                    text1 = u'''Микроскоп состоит из веб-камеры с перевернутой оптикой и корпуса с\
подвижной верхней плитой. Путем регулирования расстояния до веб-камеры с помощью 4 винтов находим\
оптимальный фокус до изучаемого объекта. Четкость изображения оцениваем визуально по\
получаемой картинке.'''
                    header1 = self.list_menu[i]['name']
                    self.action.triggered.connect(lambda: self.inform(header1, text1))
                elif i == 6:
                    text2 = u'''Программа предназначена для получения видео с веб камеры и вывода его на экран или
сохранения фотографии изучаемого объекта. Для старта видео-потока используется кнопка 'Start video',
для сохранения изображения используется кнопка 'Save picture'.'''
                    header2 = self.list_menu[i]['name']
                    self.action.triggered.connect(lambda: self.inform(header2, text2))
                elif i == 7:
                    text3 = u'''Авторы определяться позднее=)'''
                    header3 = self.list_menu[i]['name']
                    self.action.triggered.connect(lambda: self.inform(header3, text3))
                else:
                    self.action.triggered.connect(QtGui.QApplication.quit)
                self.list_menu[i]['type'] = self.action
                self.list_menu[self.list_menu[i]['menu']]['type'].addAction(self.action)
                if self.list_menu[i]['split_line']:
                    self.list_menu[self.list_menu[i]['menu']]['type'].addSeparator()

    def save_pict(self):
        # Данная функция используется для сохранения изображения
        # Вызываем диалог в котором пользователю нужно выбрать место и имя файла для сохранения
        filename = QtGui.QFileDialog.getSaveFileName(None, 'Save picture', filter=QtCore.QString('PNG (*.png)'))
        if filename is None:  # Если пользователь не выбрал куда сохранить файл
            return  # То завершаем работу функции
        filename = str(filename.toLocal8Bit()) + '.png'  # Для работы с русской локалью и добавляем нужное разрешение
        if self.is_start:  # Если запущено видео, сохраняем последний кадр
            self.cam_image.save(filename)
        else:
            if not self.webcam:  # Если веб-камера не использовалась ранее, то запускаем ее
                self.webcam = Camera(self.cb_camera.currentIndex(), {"width": 640, "height": 480})
            else:
                pass
            image = self.webcam.getImage()  # Снимаем изображение с камеры
            image.save(filename)  # Сохраняем изображение по выбранному пути

    def start_video(self, is_toggle):
        # Данная функция используется для запуска видеосъемки и отображении ее в виде QLabel
        if self.button_start.isChecked():  # Если кнопка в нажатом состоянии, то запускаем видеопоток в QLabel
            self.is_start = True  # Ставим общий "флаг" что поток видео запущен, данный флаг можно использовать в других частях кода
            if not self.webcam:  # Если веб-камера не определена раньше - определяем
                number_cam = self.cb_camera.currentIndex()
                self.webcam = Camera(number_cam, {"width": 640, "height": 480})
            else:
                pass
            self.timer = QtCore.QTimer()  # Создаем таймер
            # Связываем таймер с обновлением картинки, каждую секунду обновляем изображение на лейбле
            QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.show_frame)
            self.timer.start(1)  # Запускаем таймер
        else:  # Иначе - останавливаем таймер, а значит остановиться и поток обновления лэйбла
            self.is_start = False  # "Отключаем" флаг потока
            self.timer.stop()

    def show_frame(self):
        # Функция для cнятия изображения с камеры и передачи его в лэйбл
        ipl_image = self.webcam.getImage()  # Снимаем изображение с камеры
        # Далее технические вещи, для корректного конвертирования изображения...
        ipl_image.dl().circle((150, 75), 50, Color.RED, filled=True)
        data = ipl_image.getBitmap().tostring()
        image = QtGui.QImage(data, ipl_image.width, ipl_image.height, 3 * ipl_image.width, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()  # Понятный Qt формат изображения
        pixmap.convertFromImage(image.rgbSwapped())
        self.cam_image = pixmap.scaled(1000, 500)  # Можем изменять длину*ширину изображения для отображения
        self.label.setPixmap(pixmap.scaled(1000, 500))  # Ставим изображения в лэйбл
        QtGui.QApplication.processEvents()  # Запускаем оборот основного цикла чтобы приложение "не зависало"

    def inform(self, header, text):
        # Функция для отображения окон информации
        QtGui.QMessageBox.information(None, header, text)


reload(sys)
sys.setdefaultencoding('utf-8')
app = QtGui.QApplication(sys.argv)
mw = MainWidget()
mw.resize(300, 150)
mw.show()
sys.exit(app.exec_())